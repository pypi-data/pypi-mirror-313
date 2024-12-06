
import typer

from arlas.cli.settings import Configuration
from arlas.cli.variables import variables

iam = typer.Typer()


@iam.callback()
def configuration(config: str = typer.Option(default=None, help="Name of the ARLAS configuration to use from your configuration file ({}).".format(variables["configuration_file"]))):
    variables["arlas"] = Configuration.solve_config(config)
