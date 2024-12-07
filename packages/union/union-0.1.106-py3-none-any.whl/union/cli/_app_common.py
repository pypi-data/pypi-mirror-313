import importlib.util
import os
import sys
from copy import deepcopy
from pathlib import Path
from textwrap import dedent
from typing import Dict

import rich_click as click

from union.app import App, Input

ENABLE_UNION_SERVING_ENV_VAR = "ENABLE_UNION_SERVING"
ENABLE_UNION_SERVING = os.getenv(ENABLE_UNION_SERVING_ENV_VAR, "0") == "1"


class ApplicationCommand(click.RichCommand):
    def __init__(
        self,
        app: App,
        project: str,
        domain: str,
        func: callable,
        *args,
        **kwargs,
    ):
        self.app = app
        self.project = project
        self.domain = domain
        self.func = func

        kwargs["params"] = [
            click.Option(
                param_decls=[f"--{app_input.name}"],
                required=False,
                type=str,
                help=f"Set {app_input.name}",
            )
            for app_input in app.inputs
        ]

        super().__init__(*args, **kwargs)

    def invoke(self, ctx):
        app = self.app

        # Check if there are any dynamic inputs
        has_new_inputs = False
        new_inputs = []

        for user_input in app.inputs:
            key = user_input.name.lower()
            if key in ctx.params and ctx.params[key]:
                new_inputs.append(
                    Input(
                        name=user_input.name,
                        value=ctx.params[key],
                        auto_download=user_input.auto_download,
                    )
                )
                has_new_inputs = True
            else:
                new_inputs.append(user_input)

        if has_new_inputs:
            app = deepcopy(app)
            app.inputs = new_inputs

        self.func(app=app, project=self.project, domain=self.domain)


class ApplicationForFileGroup(click.RichGroup):
    def __init__(
        self,
        filename: Path,
        func: callable,
        project: str,
        domain: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not filename.exists():
            raise click.ClickException(f"{filename} does not exists")
        self.filename = filename
        self.func = func
        self.project = project
        self.domain = domain

    @property
    def apps(self) -> Dict[str, App]:
        try:
            return self._apps
        except AttributeError:
            module_name = os.path.splitext(os.path.basename(self.filename))[0]
            module_path = os.path.dirname(os.path.abspath(self.filename))

            spec = importlib.util.spec_from_file_location(module_name, self.filename)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module

            sys.path.append(module_path)
            spec.loader.exec_module(module)

            from union.app._models import APP_REGISTRY

            app_directory = os.path.dirname(os.path.abspath(self.filename))
            cwd = os.getcwd()
            self._apps = {k: v._resolve_include(app_directory, cwd) for k, v in APP_REGISTRY.apps.items()}
            return self._apps

    def list_commands(self, ctx):
        return list(self.apps.keys())

    def get_command(self, ctx, app_name):
        try:
            return ApplicationCommand(
                app=self.apps[app_name],
                name=app_name,
                project=self.project,
                domain=self.domain,
                func=self.func,
            )
        except KeyError:
            valid_names = list(self.apps.keys())
            err_msg = dedent(f"""\
                '{app_name}' is not a valid app name in {self.filename}

                Valid names are: {valid_names}""")
            raise click.ClickException(err_msg)


class ApplicationGroupForFiles(click.RichGroup):
    def __init__(self, func: callable, command_name: str, *args, **kwargs):
        kwargs["params"] = [
            click.Option(
                param_decls=["-p", "--project"],
                required=False,
                type=str,
                default="flytesnacks",
                help=f"Project to {command_name} to",
            ),
            click.Option(
                param_decls=["-d", "--domain"],
                required=False,
                type=str,
                default="development",
                help=f"domain to {command_name} to",
            ),
        ]
        super().__init__(*args, **kwargs)
        self.func = func
        self.command_name = command_name

    @property
    def files(self):
        try:
            return self._files
        except AttributeError:
            self._files = [os.fspath(p) for p in Path(".").glob("*.py") if p.name != "__init__.py"]
            return self._files

    def list_commands(self, ctx):
        return self.files

    def get_command(self, ctx, filename):
        return ApplicationForFileGroup(
            filename=Path(filename),
            name=filename,
            project=ctx.params["project"],
            domain=ctx.params["domain"],
            func=self.func,
            help=f"{self.command_name} application in {filename}",
        )
