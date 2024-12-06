import json
from shapely import wkt
import dateutil.parser as date_parser

MAX_KEYWORD_LENGTH = 100

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Recursive parsing of the json object and dynamic building or consolidation of the tree.
# The tree contains the same structure as the json object except that leaf nodes contains array of values (in __items__).
def __build_tree__(tree: dict, o: any):
    if o is not None:
        if type(o) is dict:
            o: dict = o
            for (k, v) in o.items():
                tree[k] = tree.get(k, {})
                __build_tree__(tree[k], v)
        else:
            if type(o) is list:
                o: list = o
                for c in o:
                    if type(c) is dict or type(c) is list:
                        ...  # We can not manage arrays of objects :-(
                    else:
                        # An array of values should become a simple type field. 
                        # For instance, list[int] becomes int since ES manages int as int or list[int]
                        __build_tree__(tree, c)
            else:
                values: list = tree.get("__items__", [])
                tree["__items__"] = values
                values.append(o)
    else:
        ...


# Takes the tree of values and guess the types recursively by relying on __type_node__
def __type_tree__(path, tree, types):
    if type(tree) is dict:
        for (k, v) in tree.items():
            if path:
                subpath = ".".join([path, k])
            else:
                subpath = k
            if subpath in types:
                tree[k]["__type__"] = types.get(subpath)
            else:
                if k == "__type__":
                    ...
                else:
                    if type(v) is dict:
                        if v.get("__items__"):
                            # it is a leaf, we need to get the type
                            tree[k]["__type__"] = __type_node__(v.get("__items__"), k)
                        else:
                            # it is either an intermediate node or a complex type such as geojson
                            t = __type_node__(v, k)
                            tree[k]["__type__"] = t
                            if t == "object":
                                # it is an intermediate node, we dive in the node
                                __type_tree__(subpath, v, types)
                    else:
                        raise Exception("Unexpected state")
    else:
        raise Exception("Unexpected state")

# Type a node. Here is the "guessing"
def __type_node__(n, name: str = None) -> str:
    if n is None:
        return "UNDEFINED"
    if type(n) is str:
        n: str = n
        # Geo objects ...
        if n.startswith("POINT "):
            try:
                wkt.loads(n)
                return "geo_point"
            except Exception:
                ...
        if n.startswith("LINESTRING ") or n.startswith("POLYGON ") or n.startswith("MULTIPOINT ") or n.startswith("MULTILINESTRING ") or n.startswith("MULTIPOLYGON "):
            try:
                wkt.loads(n)
                return "geo_shape"
            except Exception:
                ...
        if name and name.find("geohash") >= 0:
            return "geo_point"
        lat_lon: list[str] = n.split(",")
        if len(lat_lon) == 2 and is_float(lat_lon[0].strip()) and is_float(lat_lon[1].strip()):
            return "geo_point"
        # Date objects ...
        if name and (name.find("timestamp") >= 0 or name.find("date") >= 0 or name.find("start") >= 0 or name.find("end") >= 0):
            try:
                date_parser.parse(n)
                return "date"
            except Exception:
                ...
        return "text"
    if type(n) is list and len(n) > 0:
        if all(isinstance(x, (bool)) for x in n):
            return "boolean"
        if all(isinstance(x, (int)) for x in n):
            if name and (name.find("timestamp") >= 0 or name.find("_date") >= 0 or name.find("date_") >= 0 or name.find("start_") >= 0 or name.find("_start") >= 0 or name.find("_end") >= 0 or name.find("end_") >= 0):
                # all between year 1950 and 2100, in second or milli second
                if all((x > 631152000 and x < 4102444800) for x in n):
                    return "date-epoch_second"
                if all((x > 631152000000 and x < 4102444800000) for x in n):
                    return "date-epoch_millis"
                else:
                    return "long"
            else:
                return "long"
        if all(isinstance(x, (float)) for x in n):
            return "double"
        if all(isinstance(x, (str)) for x in n):
            t = __type_node__(n[0], name)
            if t == "text":
                if all(len(x) < MAX_KEYWORD_LENGTH for x in n):
                    return "keyword"
                else:
                    return "text"
            else:
                return t
        return "UNDEFINED"
    if type(n) is dict:
        if "type" in n and "coordinates" in n and "__items__" in n.get("type"):
            # looks like geojson ...
            types = n.get("type").get("__items__")
            if all([t.lower() == "point" for t in types]):
                return "geo_point"
            if all([t.lower() in ["point", "multipoint", "linestring", "multistring", "polygon", "multipolygon"] for t in types]):
                return "geo_shape"
            else:
                return "object"
        else:
            return "object"
    return "UNDEFINED"

# from the typed tree, generate the mapping.
def __generate_mapping__(tree, mapping, no_fulltext: list[str], no_index: list[str]):
    if type(tree) is dict:
        for (field_name, v) in tree.items():
            if field_name not in ["__type__", "__values__"]:
                field_type: str = v.get("__type__")
                if field_type == "object":
                    mapping[field_name] = {"properties": {}}
                    __generate_mapping__(tree=v, mapping=mapping[field_name]["properties"], no_fulltext=no_fulltext,
                                         no_index=no_index)
                else:
                    if field_type.startswith("date-"):
                        # Dates can have format patterns containing '-'
                        mapping[field_name] = {"type": "date", "format": field_type.split("-", 1)[1]}
                    else:
                        mapping[field_name] = {"type": field_type}
                        if field_type in ["keyword", "text"]:
                            if field_name not in no_fulltext:
                                mapping[field_name]["copy_to"] = ["internal.fulltext", "internal.autocomplete"]
                    # Avoid indexing field if field in --no-index
                    if field_name in no_index:
                        mapping[field_name]["index"] = "false"
                    print(f"-->{field_name}: {mapping[field_name]['type']}")
    else:
        raise Exception("Unexpected state")


def make_mapping(file: str, nb_lines: int = 2, types: dict[str, str] = {}, no_fulltext: list[str] = [],
                 no_index: list[str] = []):
    tree = {}
    mapping = {}
    with open(file, mode="r", encoding="utf-8") as f:
        i = 0
        for line in f:
            if i > nb_lines:
                break
            else:
                i = i + 1
                hit = json.loads(line)
                __build_tree__(tree, hit)
        __type_tree__("", tree, types)
        __generate_mapping__(tree, mapping, no_fulltext, no_index)
    mapping["internal"] = {
        "properties": {
            "autocomplete": {
                "type": "keyword"
            },
            "fulltext": {
                "type": "text",
                "fielddata": True
            }
        }
    }
    return {
        "mappings": {
            "properties": mapping
        }
    }
