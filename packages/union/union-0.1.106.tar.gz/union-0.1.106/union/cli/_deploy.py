import rich_click as click

from union.app import App
from union.cli._app_common import ApplicationGroupForFiles
from union.remote._app_remote import AppRemote


@click.group(name="deploy")
def deploy():
    """Deploy a resource."""


def deploy_application(app: App, project: str, domain: str):
    app_remote = AppRemote(project=project, domain=domain)
    app_remote.create_or_update(app)


app_help = """Deploy application on Union."""
app_group = ApplicationGroupForFiles(
    name="apps",
    help=app_help,
    func=deploy_application,
    command_name="deploy",
)
deploy.add_command(app_group)
