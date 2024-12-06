import typer

from arlas.cli.service import Service
from arlas.cli.variables import variables

user = typer.Typer()


@user.command(help="Create user", name="add", epilog=variables["help_epilog"])
def add(email: str = typer.Argument(help="User's email")):
    config = variables["arlas"]
    print(Service.create_user(config, email).get("id"))


@user.command(help="Delete user", name="delete", epilog=variables["help_epilog"])
def delete(id: str = typer.Argument(help="User's identifier")):
    config = variables["arlas"]
    print(Service.delete_user(config, id).get("message"))


@user.command(help="Activate user account", name="activate", epilog=variables["help_epilog"])
def activate(id: str = typer.Argument(help="User's identifier")):
    config = variables["arlas"]
    print(Service.activate(config, id).get("message"))


@user.command(help="Deactivate user account", name="deactivate", epilog=variables["help_epilog"])
def deactivate(id: str = typer.Argument(help="User's identifier")):
    config = variables["arlas"]
    print(Service.deactivate(config, id).get("message"))
