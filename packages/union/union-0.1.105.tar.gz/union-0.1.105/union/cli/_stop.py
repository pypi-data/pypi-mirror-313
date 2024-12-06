import rich_click as click

from union.remote._app_remote import AppRemote


@click.group()
def stop():
    """Stop a resource."""


@stop.command()
@click.argument("name", type=str)
@click.option("--project", default="flytesnacks", help="Project name")
@click.option("--domain", default="development", help="Domain name")
def apps(name: str, project: str, domain: str):
    app_remote = AppRemote(project=project, domain=domain)
    app_remote.stop(name=name)
