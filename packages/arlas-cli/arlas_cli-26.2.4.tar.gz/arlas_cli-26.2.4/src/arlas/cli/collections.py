import json
import typer
import os
import sys
from prettytable import PrettyTable

from arlas.cli.settings import Configuration, Resource
from arlas.cli.service import Service
from arlas.cli.variables import variables

collections = typer.Typer()


@collections.callback()
def configuration(config: str = typer.Option(default=None, help="Name of the ARLAS configuration to use from your configuration file ({}).".format(variables["configuration_file"]))):
    variables["arlas"] = Configuration.solve_config(config)


@collections.command(help="List collections", name="list", epilog=variables["help_epilog"])
def list_collections():
    config = variables["arlas"]
    collections = Service.list_collections(config)
    __print_table(collections[0], collections[1:], sortby="name")


@collections.command(help="Count the number of hits within a collection (or all collection if not provided)",
                     epilog=variables["help_epilog"])
def count(
    collection: str = typer.Argument(default=None, help="Collection's name")
):
    config = variables["arlas"]
    count = Service.count_collection(config, collection)
    __print_table(count[0], count[1:], sortby="collection name")


@collections.command(help="Describe a collection", epilog=variables["help_epilog"])
def describe(
    collection: str = typer.Argument(help="Collection's name")
):
    config = variables["arlas"]
    fields = Service.describe_collection(config, collection)
    __print_table(fields[0], fields[1:], sortby="field name")

    fields = Service.metadata_collection(config, collection)
    __print_table(fields[0], fields[1:], sortby=None)


@collections.command(help="Set collection visibility to public", epilog=variables["help_epilog"])
def public(
    collection: str = typer.Argument(help="Collection's name")
):
    config = variables["arlas"]
    ispublic = Service.set_collection_visibility(config, collection, public=True)
    print("{} is {}".format(collection, "public" if ispublic else "private"))


@collections.command(help="Set collection visibility to private", epilog=variables["help_epilog"])
def private(
    collection: str = typer.Argument(help="Collection's name")
):
    config = variables["arlas"]
    ispublic = Service.set_collection_visibility(config, collection, public=False)
    print("{} is {}".format(collection, "public" if ispublic else "private"))


@collections.command(help="Share the collection with the organisation", epilog=variables["help_epilog"])
def share(
    collection: str = typer.Argument(help="Collection's name"),
    organisation: str = typer.Argument(help="Organisation's name")
):
    config = variables["arlas"]
    shared = Service.share_with(config, collection, organisation)
    print("{} is shared with {}".format(collection, ", ".join(shared)))


@collections.command(help="Unshare the collection with the organisation", epilog=variables["help_epilog"])
def unshare(
    collection: str = typer.Argument(help="Collection's name"),
    organisation: str = typer.Argument(help="Organisation's name")
):
    config = variables["arlas"]
    shared = Service.unshare_with(config, collection, organisation)
    print("{} is shared with {}".format(collection, ", ".join(shared)))


@collections.command(help="Set the collection display name", name="name", epilog=variables["help_epilog"])
def set_display_name(
    collection: str = typer.Argument(help="Collection's name"),
    name: str = typer.Argument(help="The display name")
):
    config = variables["arlas"]
    name = Service.set_collection_display_name(config, collection, name)
    print("{} display name is {}".format(collection, name))


@collections.command(help="Set the field display name", name="set_alias", epilog=variables["help_epilog"])
def set_field_display_name(
    collection: str = typer.Argument(help="Collection's name"),
    field_path: str = typer.Argument(help="The field path"),
    display_name: str = typer.Argument(help="The field's display name. If none provided, then the alias is removed if it existed", default=None)
):
    config = variables["arlas"]
    fields = Service.set_collection_field_display_name(config, collection, field_path, display_name)
    __print_table(fields[0], fields[1:], sortby=None)


@collections.command(help="Display a sample of a collection", epilog=variables["help_epilog"])
def sample(
    collection: str = typer.Argument(help="Collection's name"),
    pretty: bool = typer.Option(default=True),
    size: int = typer.Option(default=10)
):
    config = variables["arlas"]
    sample = Service.sample_collection(config, collection, pretty=pretty, size=size)
    print(json.dumps(sample.get("hits", []), indent=2 if pretty else None))


@collections.command(help="Delete a collection", epilog=variables["help_epilog"])
def delete(
    collection: str = typer.Argument(help="collection's name")
):
    config = variables["arlas"]
    if typer.confirm("You are about to delete the collection '{}' on the '{}' configuration.\n".format(collection, config),
                     prompt_suffix="Do you want to continue (del {} on {})?".format(collection, config),
                     default=False, ):
        Service.delete_collection(
            config,
            collection=collection)
        print("{} has been deleted on {}.".format(collection, config))


@collections.command(help="Create a collection", epilog=variables["help_epilog"])
def create(
    collection: str = typer.Argument(help="Collection's name"),
    model: str = typer.Option(default=None, help="Name of the model within your configuration, or URL or file path"),
    index: str = typer.Option(default=None, help="Name of the index referenced by the collection"),
    display_name: str = typer.Option(default=None, help="Display name of the collection"),
    public: bool = typer.Option(default=False, help="Whether the collection is public or not"),
    owner: str = typer.Option(default=None, help="Organisation's owner"),
    orgs: list[str] = typer.Option(default=[], help="List of organisations accessing the collection"),
    id_path: str = typer.Option(default=None, help="Override the JSON path to the id field."),
    centroid_path: str = typer.Option(default=None, help="Override the JSON path to the centroid field."),
    geometry_path: str = typer.Option(default=None, help="Override the JSON path to the geometry field."),
    date_path: str = typer.Option(default=None, help="Override the JSON path to the date field.")
):
    config = variables["arlas"]
    if not owner and (orgs or public):
        print("Error: an owner must be provided for sharing the collection.", file=sys.stderr)
        exit(1)
    model_resource = None
    if model:
        model_resource = Configuration.settings.models.get(model, None)
        if not model_resource:
            if os.path.exists(model):
                model_resource = Resource(location=model)
            else:
                print("Error: model {} not found".format(model), file=sys.stderr)
                exit(1)
    Service.create_collection(
        config,
        collection,
        model_resource=model_resource,
        index=index,
        display_name=display_name,
        owner=owner,
        orgs=orgs,
        is_public=public,
        id_path=id_path,
        centroid_path=centroid_path,
        geometry_path=geometry_path,
        date_path=date_path)
    print("Collection {} created on {}".format(collection, config))


def __print_table(field_names: list[str], rows, sortby: str = None):
    tab = PrettyTable(field_names, sortby=sortby, align="l")
    tab.add_rows(rows)
    print(tab)

