import json
import typer
import os
import sys
from prettytable import PrettyTable

from arlas.cli.settings import Configuration, Resource
from arlas.cli.service import Service
from arlas.cli.model_infering import make_mapping
from arlas.cli.variables import variables

indices = typer.Typer()


@indices.callback()
def configuration(config: str = typer.Option(default=None, help="Name of the ARLAS configuration to use from your configuration file ({}).".format(variables["configuration_file"]))):
    variables["arlas"] = Configuration.solve_config(config)


@indices.command(help="List indices", name="list", epilog=variables["help_epilog"])
def list_indices():
    config = variables["arlas"]
    indices = Service.list_indices(config)
    tab = PrettyTable(indices[0], sortby="name", align="l")
    tab.add_rows(indices[1:])
    print(tab)
    print(f"Total count: {sum([int(index_info[2]) for index_info in indices[1:]])}")


@indices.command(help="Describe an index", epilog=variables["help_epilog"])
def describe(
    index: str = typer.Argument(help="index's name")
):
    config = variables["arlas"]
    indices = Service.describe_index(config, index)
    tab = PrettyTable(indices[0], sortby="field name", align="l")
    tab.add_rows(indices[1:])
    print(tab)


@indices.command(help="Clone an index and set its name", epilog=variables["help_epilog"])
def clone(
    source: str = typer.Argument(help="Source index name"),
    target: str = typer.Argument(help="Target cloned index name")
):
    config = variables["arlas"]
    indices = Service.clone_index(config, source, target)
    tab = PrettyTable(indices[0], sortby="name", align="l")
    tab.add_rows(indices[1:])
    print(tab)


@indices.command(help="Migrate an index on another arlas configuration, and set the target index name",
                 epilog=variables["help_epilog"])
def migrate(
    source: str = typer.Argument(help="Source index name"),
    arlas_target: str = typer.Argument(help="Target ARLAS Configuration name"),
    target: str = typer.Argument(help="Target migrated index name")
):
    config = variables["arlas"]
    indices = Service.migrate_index(config, source, arlas_target, target)
    tab = PrettyTable(indices[0], sortby="name", align="l")
    tab.add_rows(indices[1:])
    print(tab)


@indices.command(help="Display a sample of an index", epilog=variables["help_epilog"])
def sample(
    index: str = typer.Argument(help="index's name"),
    pretty: bool = typer.Option(default=True),
    size: int = typer.Option(default=10)
):
    config = variables["arlas"]
    sample = Service.sample_index(config, index, pretty=pretty, size=size)
    print(json.dumps(sample["hits"].get("hits", []), indent=2 if pretty else None))


@indices.command(help="Create an index", epilog=variables["help_epilog"])
def create(
    index: str = typer.Argument(help="index's name"),
    mapping: str = typer.Option(help="Name of the mapping within your configuration, or URL or file path"),
    shards: int = typer.Option(default=1, help="Number of shards for the index")
):
    config = variables["arlas"]
    mapping_resource = Configuration.settings.mappings.get(mapping, None)
    if not mapping_resource:
        if os.path.exists(mapping):
            mapping_resource = Resource(location=mapping)
        else:
            print("Error: model {} not found".format(mapping), file=sys.stderr)
            exit(1)
    Service.create_index_from_resource(
        config,
        index=index,
        mapping_resource=mapping_resource,
        number_of_shards=shards)
    print("Index {} created on {}".format(index, config))


@indices.command(help="Index data", epilog=variables["help_epilog"])
def data(
    index: str = typer.Argument(help="index's name"),
    files: list[str] = typer.Argument(help="List of paths to the file(s) containing the data. Format: NDJSON"),
    bulk: int = typer.Option(default=5000, help="Bulk size for indexing data")
):
    config = variables["arlas"]
    i = 1
    for file in files:
        if not os.path.exists(file):
            print("Error: file \"{}\" not found.".format(file), file=sys.stderr)
            exit(1)
        print("Processing file {}/{} ...".format(i, len(files)))
        count = Service.count_hits(file_path=file)
        Service.index_hits(config, index=index, file_path=file, bulk_size=bulk, count=count)
        i = i + 1


@indices.command(help="Generate the mapping based on the data", epilog=variables["help_epilog"])
def mapping(
    file: str = typer.Argument(help="Path to the file containing the data. Format: NDJSON"),
    nb_lines: int = typer.Option(default=2, help="Number of line to consider for generating the mapping. Avoid going over 10."),
    field_mapping: list[str] = typer.Option(default=[], help="Override the mapping with the provided field path/type. Example: fragment.location:geo_point. Important: the full field path must be provided."),
    no_fulltext: list[str] = typer.Option(default=[], help="List of keyword or text fields that should not be in the fulltext search. Important: the field name only must be provided."),
    no_index: list[str] = typer.Option(default=[], help="List of fields that should not be indexed."),
    push_on: str = typer.Option(default=None, help="Push the generated mapping for the provided index name"),
):
    config = variables["arlas"]
    if not os.path.exists(file):
        print("Error: file \"{}\" not found.".format(file), file=sys.stderr)
        exit(1)
    types = {}
    for fm in field_mapping:
        tmp = fm.split(":")
        if len(tmp) == 2:
            types[tmp[0]] = tmp[1]
        else:
            if tmp[1].startswith("date-"):
                # Dates can have format patterns containing ':'
                tmp = fm.split(":", 1)
                types[tmp[0]] = tmp[1]
            else:
                print(f"Error: invalid field_mapping \"{fm}\". The format is \"field:type\" like \"fragment.location:geo_point\"", file=sys.stderr)
                exit(1)
    mapping = make_mapping(file=file, nb_lines=nb_lines, types=types, no_fulltext=no_fulltext, no_index=no_index)
    if push_on and config:
        Service.create_index(
            config,
            index=push_on,
            mapping=mapping)
        print("Index {} created on {}".format(push_on, config))
    else:
        print(json.dumps(mapping, indent=2))


@indices.command(help="Delete an index", epilog=variables["help_epilog"])
def delete(
    index: str = typer.Argument(help="index's name")
):
    config = variables["arlas"]
    if not Configuration.settings.arlas.get(config).allow_delete:
        print("Error: delete on \"{}\" is not allowed. To allow delete, change your configuration file ({}).".format(config, variables["configuration_file"]), file=sys.stderr)
        exit(1)

    if typer.confirm("You are about to delete the index '{}' on  '{}' configuration.\n".format(index, config),
                     prompt_suffix="Do you want to continue (del {} on {})?".format(index, config),
                     default=False, ):
        if config != "local" and config.find("test") < 0:
            if typer.prompt("WARNING: You are not on a test environment. To delete {} on {}, type the name of the configuration ({})".format(index, config, config)) != config:
                print("Error: delete on \"{}\" cancelled.".format(config), file=sys.stderr)
                exit(1)

        Service.delete_index(
            config,
            index=index)
        print("{} has been deleted on {}.".format(index, config))
