import re
import sys
import typer
import yaml
from prettytable import PrettyTable
from arlas.cli.settings import ARLAS, AuthorizationService, Configuration, Resource
from arlas.cli.variables import variables
import arlas.cli.arlas_cloud as arlas_cloud

configurations = typer.Typer()


@configurations.command(help="List configurations", name="list", epilog=variables["help_epilog"])
def list_configurations():
    confs = []
    for (name, conf) in Configuration.settings.arlas.items():
        confs.append([name, conf.server.location])
    tab = PrettyTable(["name", "url"], sortby="name", align="l")
    tab.add_rows(confs)
    print(tab)


@configurations.command(help="Add a configuration", name="create", epilog=variables["help_epilog"])
def create_configuration(
    name: str = typer.Argument(help="Name of the configuration"),
    server: str = typer.Option(help="ARLAS Server url"),
    headers: list[str] = typer.Option([], help="header (name:value)"),

    persistence: str = typer.Option(default=None, help="ARLAS Persistence url"),
    persistence_headers: list[str] = typer.Option([], help="header (name:value)"),

    elastic: str = typer.Option(default=None, help="elasticsearch url"),
    elastic_login: str = typer.Option(default=None, help="elasticsearch login"),
    elastic_password: str = typer.Option(default=None, help="elasticsearch password"),
    elastic_headers: list[str] = typer.Option([], help="header (name:value)"),
    allow_delete: bool = typer.Option(default=False, help="Is delete command allowed for this configuration?"),

    auth_token_url: str = typer.Option(default=None, help="Token URL of the authentication service"),
    auth_headers: list[str] = typer.Option([], help="header (name:value)"),
    auth_org: str = typer.Option(default=None, help="ARLAS IAM Organization"),
    auth_login: str = typer.Option(default=None, help="login"),
    auth_password: str = typer.Option(default=None, help="password"),
    auth_client_id: str = typer.Option(default=None, help="Client ID"),
    auth_client_secret: str = typer.Option(default=None, help="Client secret"),
    auth_grant_type: str = typer.Option(default=None, help="Grant type (e.g. password)"),
    auth_arlas_iam: bool = typer.Option(default=True, help="Is it an ARLAS IAM service?")
):
    if Configuration.settings.arlas.get(name):
        print("Error: a configuration with that name already exists, please remove it first.", file=sys.stderr)
        exit(1)

    if auth_org:
        headers.append("arlas-org-filter:" + auth_org)
        auth_headers.append("arlas-org-filter:" + auth_org)
        persistence_headers.append("arlas-org-filter:" + auth_org)

    conf = ARLAS(
        server=Resource(location=server, headers=dict(map(lambda h: (h.split(":")[0], h.split(":")[1]), headers))),
        allow_delete=allow_delete)
    if persistence:
        conf.persistence = Resource(location=persistence, headers=dict(map(lambda h: (h.split(":")[0], h.split(":")[1]), persistence_headers)))

    if auth_token_url:
        conf.authorization = AuthorizationService(
            token_url=Resource(login=auth_login, password=auth_password, location=auth_token_url, headers=dict(map(lambda h: (h.split(":")[0], h.split(":")[1]), auth_headers))),
            client_id=auth_client_id,
            client_secret=auth_client_secret,
            grant_type=auth_grant_type,
            arlas_iam=auth_arlas_iam
        )
    if elastic:
        conf.elastic = Resource(location=elastic, headers=dict(map(lambda h: (h.split(":")[0], h.split(":")[1]), elastic_headers)), login=elastic_login, password=elastic_password)
    Configuration.settings.arlas[name] = conf
    Configuration.save(variables["configuration_file"])
    Configuration.init(variables["configuration_file"])
    print("Configuration {} created.".format(name))


@configurations.command(help="Add a configuration for ARLAS Cloud", name="login", epilog=variables["help_epilog"])
def login(
    auth_login: str = typer.Argument(help="ARLAS login"),
    elastic_login: str = typer.Argument(help="Elasticsearch login"),
    elastic: str = typer.Argument(help="Elasticsearch url"),
    auth_org: str = typer.Option(default=None, help="ARLAS IAM Organization, default is your email domain name"),
    allow_delete: bool = typer.Option(default=True, help="Is delete command allowed for this configuration?"),
    auth_password: str = typer.Option(default=None, help="ARLAS password"),
    elastic_password: str = typer.Option(default=None, help="elasticsearch password")
):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', auth_login):
        print("Error: login {} is not a valid email".format(auth_login), file=sys.stderr)
        exit(1)

    name = "cloud.arlas.io." + auth_login.split("@")[0]
    if Configuration.settings.arlas.get(name):
        print("Error: a configuration with that name already exists, please remove it first.", file=sys.stderr)
        exit(1)
    print("Creating configuration for {} ...".format(name))
    if not auth_org:
        auth_org = auth_login.split("@")[1]
        print("Using {} as your organisation name.".format(auth_org))
    if not auth_password:
        auth_password = typer.prompt("Please enter your password for ARLAS Cloud (account {})\n".format(auth_login), hide_input=True, prompt_suffix="Password:")
    if not elastic_password:
        elastic_password = typer.prompt("Thank you, now, please enter your password for elasticsearch (account {})\n".format(elastic_login), hide_input=True, prompt_suffix="Password:")

    create_configuration(
        name=name,
        server=arlas_cloud.ARLAS_SERVER,
        headers=[arlas_cloud.CONTENT_TYPE],
        persistence=arlas_cloud.ARLAS_PERSISTENCE,
        persistence_headers=[arlas_cloud.CONTENT_TYPE],
        elastic=elastic,
        elastic_login=elastic_login,
        elastic_password=elastic_password,
        elastic_headers=[arlas_cloud.CONTENT_TYPE],
        allow_delete=allow_delete,
        auth_token_url=arlas_cloud.AUTH_TOKEN_URL,
        auth_headers=[arlas_cloud.CONTENT_TYPE],
        auth_org=auth_org,
        auth_login=auth_login,
        auth_password=auth_password,
        auth_arlas_iam=True,
        auth_client_id=None,
        auth_client_secret=None,
        auth_grant_type=None,
    )
    Configuration.settings.default = name
    Configuration.save(variables["configuration_file"])
    Configuration.init(variables["configuration_file"])
    print("{} is now your default configuration.".format(name))


@configurations.command(help="Delete a configuration", name="delete", epilog=variables["help_epilog"])
def delete_configuration(
    config: str = typer.Argument(help="Name of the configuration"),
):
    if Configuration.settings.arlas.get(config, None) is None:
        print("Error: arlas configuration {} not found among [{}]".format(config, ", ".join(Configuration.settings.arlas.keys())), file=sys.stderr)
        exit(1)
    Configuration.settings.arlas.pop(config)
    Configuration.save(variables["configuration_file"])
    Configuration.init(variables["configuration_file"])
    print("Configuration {} deleted.".format(config))


@configurations.command(help="Describe a configuration", name="describe", epilog=variables["help_epilog"])
def describe_configuration(
    config: str = typer.Argument(help="Name of the configuration"),
):
    if Configuration.settings.arlas.get(config, None) is None:
        print("Error: arlas configuration {} not found among [{}]".format(config, ", ".join(Configuration.settings.arlas.keys())), file=sys.stderr)
        exit(1)
    print(yaml.dump(Configuration.settings.arlas[config].model_dump()))