import requests
import typer
import os
import sys

from .service import Service
from arlas.cli.user import user
from arlas.cli.iam import iam
from arlas.cli.org import org
from arlas.cli.collections import collections
from arlas.cli.configurations import configurations
from arlas.cli.persist import persist
from arlas.cli.index import indices
from arlas.cli.variables import variables
from arlas.cli.settings import ARLAS, Configuration, Resource, Settings

app = typer.Typer(add_completion=False, no_args_is_help=True)
arlas_cli_version = "26.2.3"


@app.callback(invoke_without_command=True)
def init(
    config_file: str = typer.Option(None, help="Path to the configuration file if you do not want to use the default one: .arlas/cli/configuration.yaml."),
    print_curl: bool = typer.Option(False, help="Print curl command"),
    version: bool = typer.Option(False, "--version", help="Print command line version")
):
    Service.curl = print_curl
    if config_file:
        variables["configuration_file"] = config_file
    if version:
        print(arlas_cli_version)
    if os.path.exists(variables["configuration_file"]):
        Configuration.init(configuration_file=variables["configuration_file"])
        if "arlas" in dict(Configuration.settings):
            if len(Configuration.settings.arlas) > 0:
                # Configuration is ok.
                ...
            else:
                print("Warning : no configuration available")
        else:
            print("Error : no arlas endpoint found in {}.".format(variables["configuration_file"]), file=sys.stderr)
            sys.exit(1)
    else:
        # we create a template to facilitate the creation of the configuration file
        os.makedirs(os.path.dirname(variables["configuration_file"]), exist_ok=True)
        Configuration.settings = Settings(
            arlas={
                "local": ARLAS(
                    server=Resource(location="http://localhost/arlas", headers={"Content-Type": "application/json"}),
                    persistence=Resource(location="http://localhost/persist", headers={"Content-Type": "application/json"}),
                    elastic=Resource(location="http://localhost:9200", headers={"Content-Type": "application/json"}),
                    allow_delete=True
                )
            },
            mappings={
            },
            models={
            }
        )
        Configuration.save(variables["configuration_file"])
        print("Warning : no configuration file found, we created a default one with a 'local' confs accessing local ARLAS exploration stack ({}).".format(variables["configuration_file"]), file=sys.stderr)
        sys.exit(0)


def main():
    try:
        json = requests.get('https://pypi.org/pypi/arlas.cli/json').json()
        if json:
            latest_version = json.get("info", {}).get("version", None)
            if latest_version:
                if arlas_cli_version == "_".join(["arlas", "cli", "versions"]):
                    # Local dev 'python3.10 -m arlas.cli.cli' usage
                    ...
                elif arlas_cli_version != latest_version:
                    print("WARNING: You are not using the latest version of arlas_cli! Please update with:", file=sys.stderr)
                    print("pip3.10 install arlas_cli==" + latest_version, file=sys.stderr)
            else:
                print("WARNING: Can not identify arlas.cli latest version.", file=sys.stderr)
    except Exception:
        print("WARNING: Can not contact pypi.org to identify if this arlas_cli is the latest version.", file=sys.stderr)
    app.add_typer(collections, name="collections")
    app.add_typer(indices, name="indices")
    app.add_typer(persist, name="persist")
    app.add_typer(configurations, name="confs")
    iam.add_typer(org, name="orgs")
    iam.add_typer(user, name="users")
    app.add_typer(iam, name="iam")
    app()


if __name__ == "__main__":
    main()
