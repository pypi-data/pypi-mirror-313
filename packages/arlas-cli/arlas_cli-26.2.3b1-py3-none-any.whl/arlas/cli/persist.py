import sys

import typer
from prettytable import PrettyTable

from arlas.cli.service import Service
from arlas.cli.settings import Configuration, Resource
from arlas.cli.variables import variables

persist = typer.Typer()


@persist.callback()
def configuration(config: str = typer.Option(default=None, help="Name of the ARLAS configuration to use from your configuration file ({}).".format(variables["configuration_file"]))):
    variables["arlas"] = Configuration.solve_config(config)


@persist.command(help="Add an entry, returns its ID", name="add", epilog=variables["help_epilog"])
def add(
    file: str = typer.Argument(help="File path"),
    zone: str = typer.Argument(help="zone"),
    name: str = typer.Option(help="name", default="none"),
    reader: list[str] = typer.Option(help="Readers", default=[]),
    writer: list[str] = typer.Option(help="writers", default=[]),
    encode: bool = typer.Option(help="Encode in BASE64", default=False)
):
    config = variables["arlas"]
    id = Service.persistence_add_file(config, Resource(location=file), zone=zone, name=name, readers=reader, writers=writer, encode=encode)
    print(id)


@persist.command(help="Delete an entry", name="delete", epilog=variables["help_epilog"])
def delete(
    id: str = typer.Argument(help="entry identifier")
):
    config = variables["arlas"]
    if not Configuration.settings.arlas.get(config).allow_delete:
        print("Error: delete on \"{}\" is not allowed. To allow delete, change your configuration file ({}).".format(config, variables["configuration_file"]), file=sys.stderr)
        exit(1)

    if typer.confirm("You are about to delete the entry '{}' on '{}' configuration.\n".format(id, config),
                     prompt_suffix="Do you want to continue (del {} on {})?".format(id, config),
                     default=False, ):
        if config != "local" and config.find("test") < 0:
            if typer.prompt("WARNING: You are not on a test environment. To delete {} on {}, type the name of the configuration ({})".format(id, config, config)) != config:
                print("Error: delete on \"{}\" cancelled.".format(config), file=sys.stderr)
                exit(1)

    Service.persistence_delete(config, id=id)
    print("Resource {} deleted.".format(id))


@persist.command(help="Retrieve an entry", name="get", epilog=variables["help_epilog"])
def get(
    id: str = typer.Argument(help="entry identifier")
):
    config = variables["arlas"]
    print(Service.persistence_get(config, id=id).get("doc_value"), end="")


@persist.command(help="List entries within a zone", name="zone", epilog=variables["help_epilog"])
def zone(
    zone: str = typer.Argument(help="Zone name")
):
    config = variables["arlas"]
    table = Service.persistence_zone(config, zone=zone)
    tab = PrettyTable(table[0], sortby="name", align="l")
    tab.add_rows(table[1:])
    print(tab)


@persist.command(help="List groups allowed to access a zone", name="groups", epilog=variables["help_epilog"])
def groups(
    zone: str = typer.Argument(help="Zone name")
):
    config = variables["arlas"]
    table = Service.persistence_groups(config, zone=zone)
    tab = PrettyTable(table[0], sortby="group", align="l")
    tab.add_rows(table[1:])
    print(tab)


@persist.command(help="Describe an entry", name="describe", epilog=variables["help_epilog"])
def describe(
    id: str = typer.Argument(help="entry identifier")
):
    config = variables["arlas"]
    table = Service.persistence_describe(config, id=id)
    tab = PrettyTable(table[0], align="l")
    tab.add_rows(table[1:])
    print(tab)
