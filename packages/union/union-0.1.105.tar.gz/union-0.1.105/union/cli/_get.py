from datetime import datetime, timezone
from typing import Optional

import click
from click import secho, style
from flytekit.clis.sdk_in_container.constants import CTX_VERBOSE
from flytekit.models.task import Resources
from grpc import RpcError
from rich.console import Console
from rich.table import Table

from union._config import _get_config_obj
from union._utils import _timedelta_format
from union.cli._app_common import ENABLE_UNION_SERVING
from union.cli._common import _get_channel_with_org
from union.internal.common.list_pb2 import ListRequest
from union.internal.identity.app_payload_pb2 import ListAppsRequest
from union.internal.identity.app_service_pb2_grpc import AppsServiceStub
from union.internal.secret.payload_pb2 import ListSecretsRequest
from union.internal.secret.secret_pb2_grpc import SecretServiceStub
from union.remote import UnionRemote
from union.remote._app_remote import AppRemote
from union.workspace._vscode_remote import _get_vscode_link, _get_workspace_executions


@click.group()
def get():
    """Get a resource."""


@get.command()
@click.pass_context
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    ctx: click.Context,
    project: Optional[str],
    domain: Optional[str],
):
    """Get secrets."""
    platform_obj = _get_config_obj().platform
    channel, org = _get_channel_with_org(platform_obj)

    stub = SecretServiceStub(channel)
    secrets = []

    next_token, has_next = "", True

    try:
        while has_next:
            request = ListSecretsRequest(domain=domain, project=project, limit=20, token=next_token, organization=org)
            response = stub.ListSecrets(request)
            next_token = response.token
            has_next = next_token != ""

            secrets.extend(response.secrets)
    except RpcError as e:
        raise click.ClickException(f"Unable to get secrets.\n{e}") from e

    if secrets:
        table = Table()
        for name in ["name", "project", "domain"]:
            table.add_column(name, justify="right")

        for secret in secrets:
            project = secret.id.project or "-"
            domain = secret.id.domain or "-"
            table.add_row(secret.id.name, project, domain)

        console = Console()
        console.print(table)
    else:
        click.echo("No secrets found")


@get.group("api-key")
def api_key():
    """Manage API keys."""


@api_key.command("admin")
def admin():
    """Show existing API keys for admin."""
    platform_obj = _get_config_obj().platform
    channel, org = _get_channel_with_org(platform_obj)

    stub = AppsServiceStub(channel)

    apps = []
    next_token, has_next = "", True
    try:
        while has_next:
            request = ListAppsRequest(organization=org, request=ListRequest(limit=20, token=next_token))
            response = stub.List(request)
            next_token = response.token
            has_next = next_token != ""

            apps.extend(response.apps)
    except RpcError as e:
        raise click.ClickException(f"Unable to get apps.\n{e}") from e

    if apps:
        table = Table()
        table.add_column("name", overflow="fold")

        for app in apps:
            table.add_row(app.client_id)

        console = Console()
        console.print(table)
    else:
        click.echo("No apps found.")


@click.command()
@click.pass_context
@click.option("--name", default=None)
@click.option("--project", default="flytesnacks", help="Project name")
@click.option("--domain", default="development", help="Domain name")
def apps(ctx: click.Context, name: Optional[str], project: str, domain: str):
    """Get apps."""

    verbose_on = ctx.obj[CTX_VERBOSE] > 0
    app_remote = AppRemote(project=project, domain=domain)

    if name is None:
        # TODO: Add filter
        app_list = app_remote.list()
        if verbose_on:
            secho(app_list)
            return

        if not app_list:
            secho("No applications running")
            return

        table = Table()
        table.add_column("Name", overflow="fold")
        table.add_column("Link", overflow="fold")
        table.add_column("Status", overflow="fold")
        table.add_column("Desired State", overflow="fold")
        table.add_column("CPU", overflow="fold")
        table.add_column("Memory", overflow="fold")

        table_items = []

        for app in app_list:
            url = f"[link={app.status.ingress.public_url}]Click Here[/link]"
            limits = app_remote.get_limits(app)

            status = app_remote.deployment_status(app)
            desired_state = app_remote.desired_state(app)

            table_items.append(
                {
                    "name": app.metadata.id.name,
                    "url": url,
                    "status": status,
                    "desired_state": desired_state,
                    "cpu": limits.get("cpu", "-"),
                    "memory": limits.get("memory", "-"),
                }
            )

        sorted_table_items = sorted(table_items, key=lambda item: item["status"])

        for item in sorted_table_items:
            table.add_row(
                item["name"],
                item["url"],
                item["status"],
                item["desired_state"],
                item["cpu"],
                item["memory"],
            )

        console = Console()
        console.print(table)
    else:
        app_idl = app_remote.get(name=name)
        if verbose_on:
            secho(app_idl)
        else:
            limits = app_remote.get_limits(app_idl)
            details = {
                "name": app_idl.metadata.id.name,
                "status": app_remote.deployment_status(app_idl),
                "link": app_idl.status.ingress.public_url,
                "desired_state": app_remote.desired_state(app_idl),
                "cpu": limits.get("cpu", "-"),
                "memory": limits.get("memory", "-"),
            }
            items = ["name", "link", "status", "cpu", "memory", "desired_state"]
            max_item_len = max(len(i) for i in items)

            for item in items:
                styled_name = style(f"{item:<{max_item_len}}", bold=True)
                value = details[item]
                secho(f"{styled_name} : {value}")


if ENABLE_UNION_SERVING:
    get.add_command(apps)


@get.command()
@click.pass_context
@click.option("--name", default=None)
@click.option("--project", default="flytesnacks", help="Project name")
@click.option("--domain", default="development", help="Domain name")
@click.option("--show-details", default=False, is_flag=True, help="Show additional details")
def workspace(ctx: click.Context, name: Optional[str], project: str, domain: str, show_details: bool):
    """Get workspaces."""
    remote = UnionRemote(default_domain=domain, default_project=project)

    if name is None:
        _list_workspaces(remote, project, domain)
    else:
        _show_single_workspace(remote, name, project, domain, show_details)


def _show_single_workspace(remote: UnionRemote, name: str, project: str, domain: str, show_details: bool):
    executions = _get_workspace_executions(remote, project, domain)

    named_execution = None
    for execution, ex_name in executions:
        if ex_name == name:
            named_execution = execution
            break
    else:  # no break
        raise click.ClickException(f"Unable to find workspace with name: {name}")

    details = _get_details(remote, name, named_execution)
    items = ["name", "cpu", "memory", "duration"]

    if show_details:
        items.append("execution_url")

    items.append("workspace_url")

    max_item_len = max(len(i) for i in items)

    for item in items:
        styled_name = style(f"{item:<{max_item_len}}", bold=True)
        value = details[item]
        secho(f"{styled_name} : {value}")


def _get_details(remote: UnionRemote, name: str, execution) -> dict:
    output = {"name": name, "cpu": "default", "memory": "default", "gpu": "none"}

    launch_plan = execution.spec.launch_plan
    task = remote.fetch_task(
        project=launch_plan.project,
        domain=launch_plan.domain,
        name=launch_plan.name,
        version=launch_plan.version,
    )

    # get resources information
    requests = task.template.container.resources.requests
    for request in requests:
        if request.name == Resources.ResourceName.CPU:
            output["cpu"] = request.value
        elif request.name == Resources.ResourceName.MEMORY:
            output["memory"] = request.value
        elif request.name == Resources.ResourceName.GPU:
            # TODO: Fix with correct metadata
            output["gpu"] = "1"

    output["version"] = launch_plan.version
    output["workspace_url"] = _get_vscode_link(remote, execution)

    workflow_execution = remote.fetch_execution(
        project=execution.id.project,
        domain=execution.id.domain,
        name=execution.id.name,
    )
    output["execution_url"] = remote.generate_console_url(workflow_execution)

    now = datetime.now(tz=timezone.utc)
    duration = now - execution.closure.started_at
    output["duration"] = _timedelta_format(duration)

    return output


def _list_workspaces(remote: UnionRemote, project: str, domain: str):
    executions = _get_workspace_executions(remote, project, domain)

    if not executions:
        click.echo("No workspaces found.")
        return

    table = Table()
    table.add_column("Name", overflow="fold")
    table.add_column("CPU", overflow="fold")
    table.add_column("Memory", overflow="fold")
    table.add_column("GPU", overflow="fold")
    table.add_column("Duration", overflow="fold")
    table.add_column("Link", overflow="fold")

    for execution, name in executions:
        details = _get_details(remote, name, execution)
        if details["workspace_url"] == "Unavailable":
            url = "Unavailable"
        else:
            url = f"[link={details['workspace_url']}]Click Here[/link]"

        table.add_row(
            name,
            details["cpu"],
            details["memory"],
            details["gpu"],
            details["duration"],
            url,
        )

    console = Console()
    console.print(table)
