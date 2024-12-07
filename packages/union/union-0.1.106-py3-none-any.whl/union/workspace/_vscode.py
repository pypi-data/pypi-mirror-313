import inspect
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from multiprocessing import Process
from pathlib import Path
from shutil import which
from string import Template
from subprocess import run
from textwrap import dedent
from time import sleep, time
from typing import List, NamedTuple, Optional, Union

import flytekit
import fsspec
from flytekit import ImageSpec, PythonFunctionTask, Resources, current_context
from flytekit.configuration import AuthType, SerializationSettings
from flytekit.core.base_task import Task
from flytekit.core.context_manager import FlyteContextManager
from flytekit.core.utils import ClassDecorator
from flytekit.extend import TaskResolverMixin
from flytekit.types.directory import FlyteDirectory
from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.yaml import DataClassYAMLMixin

VSCODE_TYPE_VALUE = "vscode"
# Config keys to store in task template
TASK_FUNCTION_SOURCE_PATH = "TASK_FUNCTION_SOURCE_PATH"

WORKSPACE_IMAGE_NAME = "workspace"
CODE_SERVER_CLI_NAME = "code-server"
DEFAULT_PORT = 8080
DOWNLOAD_DIR = Path.home() / ".code-server"
WORKSPACE_DIR = Path("/workspace")
HEARTBEAT_PATH = Path.home() / ".local" / "share" / "code-server" / "heartbeat"
CODE_SERVER_SETTINGS_PATH = Path.home() / ".local" / "share" / "code-server" / "User" / "settings.json"
CODE_SERVER_VERSION = "4.23.1"
CODE_SERVER_DOWNLOAD_URL = (
    "https://github.com/coder/code-server/releases/download/v{version}/code-server-{version}-linux-{arch}.tar.gz"
)
CODE_SERVER_CLI_NAME_TEMPLATE = "code-server-{version}-linux-{arch}"
HEARTBEAT_CHECK_SECONDS = 60

ROOT_PATH = Path.home()
BASHRC_PATH = Path.home() / ".bashrc"
UNION_GITHUB_TOKEN_ENV = "UNION_WORKSPACE_GITHUB_TOKEN"
UNION_SERVERLESS_API_KEY_ENV = "UNION_WORKSPACE_SERVERLESS_API_KEY"
GIT_CONFIG_PATH = Path.home() / ".gitconfig"
TERMINATE_WORKSPACE_FILE_NAME = "terminate_workspace.py"


GIT_CONFIG_TEMPLATE = Template(
    """\
$USER_INFO

[credential "https://github.com"]
    helper =
    helper = !/usr/bin/gh auth git-credential
[credential "https://gist.github.com"]
    helper =
    helper = !/usr/bin/gh auth git-credential

[url "https://$GITHUB_TOKEN@github.com/"]
    insteadOf = https://github.com/
"""
)

_DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE = """\
name: my-workspace
# Make sure that the project and domain exists
project: flytesnacks
domain: development
container_image: ghcr.io/unionai/workspace:0.0.10

resources:
    cpu: "2"
    mem: "4Gi"
    gpu: null

workspace_root: ~/workspace
on_startup: null
metadata: null
ttl_seconds: 1200
"""

_DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC = """\
name: my-workspace
project: flytesnacks
domain: development
container_image:
    builder: "union"

resources:
    cpu: "2"
    mem: "4Gi"
    gpu: null

on_startup: null
metadata: null
ttl_seconds: 1200
"""


WorkspaceOutput = NamedTuple("WorkspaceOutput", [("state_dir", FlyteDirectory)])


class ImageSpecConfig(DataClassYAMLMixin, DataClassJSONMixin, ImageSpec):
    def __hash__(self):
        return hash(self.to_dict().__str__())


class ResourceConfig(DataClassYAMLMixin, Resources):
    pass


@dataclass
class WorkspaceConfig(DataClassYAMLMixin, DataClassJSONMixin):
    name: str
    project: str
    domain: str
    container_image: Optional[Union[ImageSpecConfig, str]] = None
    resources: Optional[ResourceConfig] = None
    on_startup: Optional[Union[str, List[str]]] = None
    workspace_root: str = "~/workspace"
    working_dir: Optional[str] = None
    ttl_seconds: int = 1200  # 20 minutes is the default up time

    def __post_init__(self):
        # Quick hack to always build image
        if not isinstance(self.container_image, str):
            from union.ucimage._image_builder import _register_union_image_builder

            _register_union_image_builder()

            if os.getenv("UNION_DEV"):
                from union._testing import imagespec_with_local_union

                image_spec = imagespec_with_local_union(builder="union")
            else:
                image_spec = ImageSpec(builder="union")

            _user_image_spec = self.container_image
            self.container_image = ImageSpecConfig(
                name=f"{WORKSPACE_IMAGE_NAME}-{self.container_image.name}",
                builder=image_spec.builder,
                packages=[
                    *(image_spec.packages or []),
                    *(_user_image_spec.packages or []),
                ],
                source_root=image_spec.source_root,
                apt_packages=[
                    *(_user_image_spec.apt_packages or []),
                    "git",
                    "sudo",
                    "wget",
                    "vim",
                ],
                commands=[
                    "wget https://github.com/cli/cli/releases/download/v2.49.0/gh_2.49.0_linux_amd64.deb "
                    "-O /tmp/gh.deb",
                    "apt install /tmp/gh.deb",
                    "wget https://github.com/coder/code-server/releases/download/v4.23.1/code-server_4.23.1_amd64.deb "
                    "-O /tmp/code-server.deb",
                    "apt install /tmp/code-server.deb",
                    *(_user_image_spec.commands or []),
                ],
            )


def configure_python_path():
    python_bin = os.path.dirname(sys.executable)
    with BASHRC_PATH.open("a") as f:
        f.write(os.linesep)
        f.write(f"export PATH={python_bin}:$PATH")
        f.write(os.linesep)
        f.write(r'export PS1="\[\e[0;34m\]\w\[\e[m\]\$ "')


def configure_union_remote(host: str):
    from union._config import _write_config_to_path

    _write_config_to_path(host, AuthType.DEVICEFLOW.value)


def configure_git(repo: str, workspace_dir: Path, git_name: str, git_email: str) -> str:
    """Configures workspace built with ImageSpec on Union's hosted image builder."""

    ctx = current_context()
    secrets = ctx.secrets

    with BASHRC_PATH.open("a") as f:
        github_token = secrets.get(key=UNION_GITHUB_TOKEN_ENV)
        f.write(f"export GITHUB_TOKEN={github_token}")

    user_info = dedent(
        f"""\
    [user]
        name = {git_name}
        email = {git_email}
    """
    )
    git_config = GIT_CONFIG_TEMPLATE.substitute(
        USER_INFO=user_info,
        GITHUB_TOKEN=github_token,
    )

    GIT_CONFIG_PATH.write_text(git_config)

    root_dir = workspace_dir

    if repo != "":
        workspace_dir.mkdir(exist_ok=True)
        subprocess.run(["/usr/bin/git", "clone", repo], cwd=workspace_dir, text=True)
        for item in workspace_dir.iterdir():
            if item.is_dir():
                root_dir = item
                break
    return root_dir


class vscode(ClassDecorator):
    """Union specific VSCode extension."""

    def __init__(self, task_function: Optional[callable] = None):
        super().__init__(task_function=task_function)

    def execute(self, *args, **kwargs):
        ctx = FlyteContextManager.current_context()
        ctx.user_space_params.builder().add_attr(
            TASK_FUNCTION_SOURCE_PATH, inspect.getsourcefile(self.task_function)
        ).build()

        if ctx.execution_state.is_local_execution():
            return

        return self.task_function(*args, **kwargs)

    def get_extra_config(self):
        return {self.LINK_TYPE_KEY: VSCODE_TYPE_VALUE, self.PORT_KEY: f"{DEFAULT_PORT}"}


@vscode
def workspace(
    config_content: str,
    host: str,
    console_http_domain: str,
    state_dir: Optional[FlyteDirectory] = None,
) -> WorkspaceOutput:
    ROOT_PATH.mkdir(exist_ok=True)
    configure_python_path()
    configure_union_remote(host)

    workspace_config = WorkspaceConfig.from_yaml(config_content)
    workspace_dir = Path(workspace_config.workspace_root).expanduser()
    workspace_dir.mkdir(exist_ok=True)

    on_startup = workspace_config.on_startup
    if on_startup is not None:
        if isinstance(on_startup, str):
            on_startup = [on_startup]

        commands = [
            *on_startup,
            # ensure that contents in the workspace directory is writable by the
            # user. This is needed e.g. when cloned git repos are checked out
            # as part of on_startup, but the state_dir needs to overwrite files
            # in the .git directory
            "chmod 775 -R .",
        ]

        for cmd in commands:
            subprocess.run(cmd.split(), cwd=workspace_dir, text=True)

    if state_dir is not None:
        state_dir.download()
        shutil.copytree(state_dir.path, workspace_dir, dirs_exist_ok=True)

    # overwrite the config with the new config
    config_path = workspace_dir / "config.yaml"
    config_path.write_text(config_content)

    # Configure code-server
    configure_code_server_config()

    start_vscode_service(console_http_domain, workspace_dir, workspace_config.ttl_seconds, workspace_config.working_dir)
    return WorkspaceOutput(state_dir=FlyteDirectory(path=str(workspace_dir)))


class WorkspaceResolver(TaskResolverMixin):
    @property
    def location(self) -> str:
        return "union.workspace._vscode.resolver"

    @property
    def name(self) -> str:
        return "union.workspace.vscode"

    def get_task_for_workspace(
        self,
        config: WorkspaceConfig,
    ) -> PythonFunctionTask:
        return PythonFunctionTask(
            task_config=None,
            task_function=workspace,
            task_type="workspace",
            task_resolver=self,
            requests=config.resources,
            container_image=config.container_image,
        )

    def load_task(self, loader_args: List[str]) -> PythonFunctionTask:
        return PythonFunctionTask(
            task_config=None,
            task_function=workspace,
            task_type="workspace",
            task_resolver=self,
        )

    def loader_args(self, settings: SerializationSettings, task: PythonFunctionTask) -> List[str]:
        return ["workspace"]

    def get_all_tasks(self) -> List[Task]:
        raise NotImplementedError


resolver = WorkspaceResolver()


def download_http(url: str, local_dest_path: Path) -> Path:
    """Download URL to `download_dir`. Returns Path of downloaded file."""
    logger = flytekit.current_context().logging

    fs = fsspec.filesystem("http")
    logger.info(f"Downloading {url} to {local_dest_path}")
    fs.get(url, local_dest_path)
    logger.info("File downloaded successfully!")

    return local_dest_path


def download_and_configure_vscode(version: str) -> str:
    """Download and configure vscode."""
    logger = flytekit.current_context().logging
    code_server_cli = which(CODE_SERVER_CLI_NAME)
    if code_server_cli is not None:
        logger.info(f"Code server binary already exists at {code_server_cli}")
        logger.info("Skipping downloading coe server")
        return code_server_cli

    # Download code-server
    logger.info(f"Code server is not in $PATH, downloading code server to {DOWNLOAD_DIR}...")
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    machine_info = platform.machine()
    logger.info(f"machine type: {machine_info}")

    if machine_info == "aarch64":
        arch = "arm64"
    elif machine_info == "x86_64":
        arch = "amd64"
    else:
        msg = (
            "Automatic download is only supported on AMD64 and ARM64 architectures. "
            "If you are using a different architecture, please visit the code-server official "
            "website to manually download the appropriate version for your image."
        )
        raise ValueError(msg)

    code_server_tar_path_url = CODE_SERVER_DOWNLOAD_URL.format(version=version, arch=arch)
    code_server_local_path = DOWNLOAD_DIR / "code-server.tar.gz"
    download_http(code_server_tar_path_url, code_server_local_path)
    with tarfile.open(code_server_local_path, "r:gz") as tar:
        tar.extractall(path=DOWNLOAD_DIR)

    code_server_cli = (
        DOWNLOAD_DIR / CODE_SERVER_CLI_NAME_TEMPLATE.format(version=version, arch=arch) / "bin" / CODE_SERVER_CLI_NAME
    )
    return os.fspath(code_server_cli)


def monitor_vscode(child_process, ttl_seconds):
    logger = flytekit.current_context().logging
    start_time = time()

    while child_process.is_alive():
        if not HEARTBEAT_PATH.exists():
            delta = time() - start_time
        else:
            delta = time() - HEARTBEAT_PATH.stat().st_mtime

        logger.info(f"The latest activity on code server was {delta} ago.")
        if delta > ttl_seconds:
            logger.info(
                f"code server is idle for more than {ttl_seconds} seconds. Terminating process {child_process.pid}"
            )
            child_process.terminate()
            child_process.join()
            return

        sleep(HEARTBEAT_CHECK_SECONDS)


def configure_code_server_config():
    config = {
        "terminal.integrated.defaultProfile.linux": "bash",
        "remote.autoForwardPortsSource": "hybrid",
        "commands.treeViewStatusBarVisibleSymbol": "",
        "commands.commands": {
            "⏹️ Terminate Workspace": {
                "sequence": [
                    {
                        "command": "commands.runInTerminal",
                        "args": {
                            "text": "python ~/workspace/terminate_workspace.py",
                            "name": "terminate",
                            "waitForExit": False,
                            "reuse": "newest",
                        },
                    },
                    {
                        "command": "commands.focusTerminal",
                        "args": "terminate",
                    },
                ],
                "statusBar": {
                    "alignment": "left",
                    "text": "$(stop) Terminate Workspace",
                    "backgroundColor": "warning",
                    "priority": -9999,
                },
            }
        },
    }
    with CODE_SERVER_SETTINGS_PATH.open("w") as file:
        json.dump(config, file, indent=4)


def prepare_terminate_workspace_python(
    console_http_domain: str,
    workspace_root: Path,
    pid: int,
):
    """
    Generate a Python script for users to resume the task.
    """

    python_script = dedent(f"""\
    import argparse
    import os
    import signal
    import time
    import webbrowser

    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--force", action="store_true", help="Force terminate the workspace.")
        args = parser.parse_args()

        if args.force:
            answer = "Y"
        else:
            print(
                "⛔️ This operation will terminate the workspace. The contents "
                "in the {workspace_root} directory will not be saved."
            )
            answer = input("Do you really want to terminate? [Y/n]: ").strip().upper()

        if answer in ['Y', '']:
            os.kill({pid}, signal.SIGTERM)
            print(f"🛑 The server is terminating. You will be redirected to Union in a few seconds.")
            time.sleep(3)
            webbrowser.open(f"{console_http_domain}/", new=0)
            print("⤴️ Redirecting to Union.")
        else:
            print("Operation canceled.")
    """)

    with (workspace_root / TERMINATE_WORKSPACE_FILE_NAME).open("w") as file:
        file.write(python_script)


def prepare_task_json(workspace_root: Path, working_dir: Path):
    tasks_json = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "terminate",
                "type": "shell",
                "command": f"python {str(workspace_root / TERMINATE_WORKSPACE_FILE_NAME)}",
            }
        ],
    }

    vscode_directory = working_dir / ".vscode"
    if not os.path.exists(vscode_directory):
        os.makedirs(vscode_directory)

    with open(os.path.join(vscode_directory, "tasks.json"), "w") as file:
        json.dump(tasks_json, file, indent=4)


def start_vscode_service(
    console_http_domain: str,
    workspace_root: Path,
    ttl_seconds: int,
    working_dir: Optional[str] = None,
):
    code_server_cli = download_and_configure_vscode(CODE_SERVER_VERSION)

    host = f"0.0.0.0:{DEFAULT_PORT}"

    command = [
        code_server_cli,
        "--bind-addr",
        host,
        "--disable-workspace-trust",
        "--auth",
        "none",
    ]

    workspace_root = workspace_root.absolute()
    if working_dir is not None:
        working_dir = workspace_root / working_dir
    else:
        working_dir = workspace_root

    command.append(os.fspath(working_dir))

    child_process = Process(target=run, args=[command], kwargs={"text": True})
    child_process.start()

    print(f"Preparing terminate workspace python script in {workspace_root}, pid: {child_process.pid}")
    prepare_terminate_workspace_python(console_http_domain, workspace_root, child_process.pid)

    print(f"Preparing launch.json in {workspace_root}")
    prepare_task_json(workspace_root, working_dir)

    monitor_vscode(child_process, ttl_seconds)
