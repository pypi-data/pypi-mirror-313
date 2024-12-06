"""Module to manage applications on Union."""

import logging
import os
import tarfile
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional

import grpc
from flyteidl.core.tasks_pb2 import Resources
from flytekit.clients.auth_helper import get_authenticated_channel
from flytekit.configuration import Config
from flytekit.core.artifact import ArtifactQuery
from flytekit.models.core.types import BlobType
from rich.console import Console

from union._config import (
    ConfigSource,
    ConfigWithSource,
    _get_config_obj,
)
from union.app import App
from union.app._models import AppSerializationSettings, Input, MaterializedInput, URLQuery
from union.internal.app.app_definition_pb2 import App as AppIDL
from union.internal.app.app_definition_pb2 import Identifier, Spec, Status
from union.internal.app.app_payload_pb2 import (
    CreateRequest,
    CreateResponse,
    GetRequest,
    GetResponse,
    ListResponse,
    UpdateRequest,
    UpdateResponse,
    WatchRequest,
    WatchResponse,
)
from union.internal.app.app_payload_pb2 import (
    ListRequest as ListAppsRequest,
)
from union.internal.app.app_service_pb2_grpc import AppServiceStub
from union.internal.common.identifier_pb2 import ProjectIdentifier
from union.internal.common.list_pb2 import ListRequest
from union.remote._remote import UnionRemote

logger = logging.getLogger(__name__)

FILES_TAR_FILE_NAME = "include-files.tar.gz"


class AppRemote:
    def __init__(
        self,
        project: str,
        domain: str,
        config: Optional[Config] = None,
    ):
        if config is None:
            config = _get_config_obj(config, default_to_union_semantics=True)
        else:
            config_with_source = ConfigWithSource(config=config, source=ConfigSource.REMOTE)
            config = _get_config_obj(config_with_source, default_to_union_semantics=True)

        self.config = config
        self.project = project
        self.domain = domain
        self._union_remote = UnionRemote(config=config, default_domain=domain, default_project=project)

    def list(self) -> List[AppIDL]:
        def create_list_request(token: str):
            return ListAppsRequest(
                request=ListRequest(token=token),
                org=self.org,
                project=ProjectIdentifier(name=self.project, domain=self.domain, organization=self.org),
            )

        results = []
        response: ListResponse
        token, has_next = "", True

        while has_next:
            list_request = create_list_request(token=token)

            response = self.sync_client.List(list_request)
            token = response.token
            has_next = token != ""

            results.extend(response.apps)

        return results

    def create_or_update(self, app: App):
        try:
            self.get(name=app.name)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                self.create(app)
                return
            raise

        try:
            self.update(app)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ABORTED and "Either the change has already" in e.details():
                console = Console()
                console.print(f"{app.name} app was already deployed with the current spec")
                return
            raise

    def get(self, name: str) -> AppIDL:
        app_id = Identifier(org=self.org, project=self.project, domain=self.domain, name=name)
        get_app_request = GetRequest(app_id=app_id)

        get_response: GetResponse = self.sync_client.Get(get_app_request)
        app = get_response.app

        return app

    def update(self, app: App):
        additional_distribution = self.upload_files(app)
        materialized_input_values = self.materialize_values(app)

        settings = AppSerializationSettings(
            org=self.org,
            project=self.project,
            domain=self.domain,
            additional_distribution=additional_distribution,
            desired_state=Spec.DesiredState.DESIRED_STATE_STARTED,
            materialized_inputs=materialized_input_values,
        )
        new_app_idl = app._to_union_idl(settings=settings)

        get_app_request = GetRequest(app_id=new_app_idl.metadata.id)
        get_response: GetResponse = self.sync_client.Get(get_app_request)

        old_app_idl = get_response.app

        updated_app_idl = AppIDL(
            metadata=old_app_idl.metadata,
            spec=new_app_idl.spec,
            status=old_app_idl.status,
        )

        console = Console()
        update_request = UpdateRequest(app=updated_app_idl)

        _url = old_app_idl.status.ingress.public_url
        url = f"[link={_url}]{_url}[/link]"
        console.print(f"✨ Updating Application: {app.name} with endpoint: {url}")
        update_response: UpdateResponse = self.sync_client.Update(update_request)

        updated_app = update_response.app

        watch_request = WatchRequest(app_id=updated_app.metadata.id)

        def watch():
            response: WatchResponse
            with console.status("✨ Updating Application") as status:
                for response in self.sync_client.Watch(watch_request):
                    status = response.create_event.app.status.conditions[-1].deployment_status
                    if status in (
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNSPECIFIED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_STOPPED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_FAILED,
                    ):
                        raise RuntimeError("Application failed to update")
                    elif status in (
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_ASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_PENDING,
                    ):
                        status.update("✨ Updating Application...")
                    elif status == Status.DeploymentStatus.DEPLOYMENT_STATUS_STARTED:
                        status.update("🚀 Application updated!")
                        return response.app_id

        # TODO: Fix when watch works
        # watch()
        # console.print(f"Updated endpoint at: {url}")

    def create(self, app: App):
        additional_distribution = self.upload_files(app)
        materialized_input_values = self.materialize_values(app)

        settings = AppSerializationSettings(
            org=self.org,
            project=self.project,
            domain=self.domain,
            additional_distribution=additional_distribution,
            desired_state=Spec.DesiredState.DESIRED_STATE_STARTED,
            materialized_inputs=materialized_input_values,
        )
        app_idl = app._to_union_idl(settings=settings)

        console = Console()
        console.print(f"✨ Creating Application: {app.name}")

        create_request = CreateRequest(app=app_idl)
        create_response: CreateResponse = self.sync_client.Create(create_request)
        new_app = create_response.app

        _url = new_app.status.ingress.public_url
        url = f"[link={_url}]{_url}[/link]"

        logger.debug(f"Create Response {create_response} with endpoint: {url}")
        watch_request = WatchRequest(app_id=new_app.metadata.id)

        def watch() -> Identifier:
            with console.status("✨ Starting Application") as status:
                response: WatchResponse
                for response in self.sync_client.Watch(watch_request):
                    status = response.create_event.app.status
                    if status in (
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNSPECIFIED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_STOPPED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_FAILED,
                    ):
                        raise RuntimeError("Application failed to launch")
                    elif status in (
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_ASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_PENDING,
                    ):
                        status.update("✨ Starting Application...")
                    elif status == Status.DeploymentStatus.DEPLOYMENT_STATUS_STARTED:
                        status.update("🚀 Application deployed!")
                        return response.app_id

        # TODO: Fix when watch works
        # watch()
        console.print(f"Created Endpoint at: {url}")

    def stop(self, name: str):
        app_idl = self.get(name)
        app_idl.spec.desired_state = Spec.DesiredState.DESIRED_STATE_STOPPED

        console = Console()
        console.print(f"⏳ Stopping Application: {name}")

        update_request = UpdateRequest(app=app_idl)
        self.sync_client.Update(update_request)

        watch_request = WatchRequest(app_id=app_idl.metadata.id)

        def watch():
            response: WatchResponse
            with console.status("⏳ Stopping Application...") as status:
                for response in self.sync_client.Watch(watch_request):
                    status = response.delete_event.app.status
                    if status in (
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNSPECIFIED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_UNASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_ASSIGNED,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_PENDING,
                        Status.DeploymentStatus.DEPLOYMENT_STATUS_STARTED,
                    ):
                        status.update("⏳ Stopping Application...")
                    elif status == Status.DeploymentStatus.DEPLOYMENT_STATUS_FAILED:
                        status.update("💥 Application stopped because it failed to launch")
                        break
                    elif status == Status.DeploymentStatus.DEPLOYMENT_STATUS_STOPPED:
                        status.update("💥 Application stopped")
                        break

        # TODO: Uncomment when update actually delete apps
        # watch()

    def _watch(self, name: App):
        """This is for debugging."""
        app_idl = self.get(name)
        watch_request = WatchRequest(app_id=app_idl.metadata.id)

        console = Console()

        def watch():
            response: WatchResponse
            with console.status("⏳ Watching Application..."):
                for response in self.sync_client.Watch(watch_request):
                    console.print(response)

        # TODO: Uncomment when update actually delete apps
        watch()

    def _watch_async(self, name: App):
        app_idl = self.get(name)
        watch_request = WatchRequest(app_id=app_idl.metadata.id)

        console = Console()

        async def watch():
            response: WatchResponse
            with console.status("⏳ Watching Application..."):
                async for response in self.async_client.Watch(watch_request):
                    console.print(response)

        # TODO: Uncomment when update actually delete apps
        import asyncio

        asyncio.run(watch())

    def upload_files(self, app: App) -> Optional[str]:
        """Upload files required by app."""
        if not app.include:
            return None

        with TemporaryDirectory() as temp_dir:
            tar_path = os.path.join(temp_dir, FILES_TAR_FILE_NAME)
            with tarfile.open(tar_path, "w:gz") as tar:
                for resolve_include in app._include_resolved:
                    tar.add(resolve_include.src, arcname=resolve_include.dest)

            _, upload_native_url = self._union_remote.upload_file(Path(tar_path))

            return upload_native_url

    def materialize_values(self, app: App) -> dict:
        output = {}
        for user_input in app.inputs:
            if isinstance(user_input.value, ArtifactQuery):
                query = deepcopy(user_input.value)
                query.project = self.project
                query.domain = self.domain

                result = self._union_remote.get_artifact(query=query.to_flyte_idl())

                blob = result.literal.scalar.blob

                input_type = None
                if blob.metadata.type.dimensionality == BlobType.BlobDimensionality.SINGLE:
                    input_type = Input.Type.File
                elif blob.metadata.type.dimensionality == BlobType.BlobDimensionality.MULTIPART:
                    input_type = Input.Type.Directory

                output[user_input.name] = MaterializedInput(
                    value=result.literal.scalar.blob.uri,
                    type=input_type,
                )

            elif isinstance(user_input.value, URLQuery):
                query = user_input.value
                # Assume application has the same project and domain
                app_idl = self.get(name=query.name)
                if user_input.value.public:
                    output[user_input.name] = MaterializedInput(
                        value=app_idl.status.ingress.public_url,
                        input_type=Input.Type.String,
                    )
                else:
                    # TODO: User app_irl
                    app_id = app_idl.metadata.id
                    # TODO: Update by doing this dynamically on the endpoint?
                    output[user_input.name] = MaterializedInput(
                        value=f"http://{app_id.name}.development.svc.cluster.local",
                        type=Input.Type.String,
                    )

        return output

    @property
    def sync_channel(self) -> grpc.Channel:
        try:
            return self._sync_channel
        except AttributeError:
            self._sync_channel = get_authenticated_channel(self.config.platform)
            return self._sync_channel

    @property
    def org(self) -> Optional[str]:
        try:
            return self._org
        except AttributeError:
            # TODO: Actually make _get_organization call
            self._org = self.config.platform.endpoint.split(".")[0]
            return self._org

    @property
    def sync_client(self) -> AppServiceStub:
        try:
            return self._sync_client
        except AttributeError:
            self._sync_client = AppServiceStub(self.sync_channel)
            return self._sync_client

    @property
    def async_client(self) -> AppServiceStub:
        try:
            return self._async_client
        except AttributeError:
            self._async_client = AppServiceStub(self.async_channel)
            return self._async_client

    @property
    def async_channel(self) -> grpc.aio.Channel:
        from union.filesystems._endpoint import _create_secure_channel_from_config

        try:
            return self._async_channel
        except AttributeError:
            self._async_channel = _create_secure_channel_from_config(self.config.platform, self.sync_channel)
            return self._async_channel

    @staticmethod
    def deployment_status(app_idl: AppIDL) -> str:
        try:
            current_status = app_idl.status.conditions[-1].deployment_status
            return Status.DeploymentStatus.Name(current_status).split("_")[-1].title()
        except Exception:
            return "Unknown"

    @staticmethod
    def desired_state(app_idl: AppIDL) -> str:
        return Spec.DesiredState.Name(app_idl.spec.desired_state).split("_")[-1].title()

    @staticmethod
    def get_limits(app_idl: AppIDL) -> dict:
        output = {}
        for limit in app_idl.spec.container.resources.limits:
            if limit.name == Resources.ResourceName.CPU:
                output["cpu"] = limit.value
            if limit.name == Resources.ResourceName.MEMORY:
                output["memory"] = limit.value
        return output
