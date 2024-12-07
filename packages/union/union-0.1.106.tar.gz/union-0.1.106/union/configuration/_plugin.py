"""All imports to union in this file should be in the function definition.

This plugin is loaded by flytekit, so any imports to union can lead to circular imports.
"""

from contextlib import suppress
from typing import Optional

import click
from click import Group, Option
from flytekit.remote import FlyteRemote


class UnionAIPlugin:
    @staticmethod
    def get_remote(
        config: Optional[str],
        project: str,
        domain: str,
        data_upload_location: Optional[str] = None,
    ) -> FlyteRemote:
        from union._config import _get_config_obj
        from union.remote import UnionRemote

        config_obj = _get_config_obj(config)

        return UnionRemote(
            config_obj,
            default_project=project,
            default_domain=domain,
            data_upload_location=data_upload_location,
        )

    @staticmethod
    def configure_pyflyte_cli(main: Group) -> Group:
        """Configure pyflyte's CLI."""

        import union._config

        # Import filesystems here so they get copied over properly when union is installed in
        # development mode
        import union.filesystems
        from union._config import _get_config_obj
        from union.cli._app_common import ENABLE_UNION_SERVING
        from union.cli._create import create
        from union.cli._delete import delete
        from union.cli._deploy import deploy
        from union.cli._get import get
        from union.cli._info import info
        from union.cli._stop import stop
        from union.cli._update import update
        from union.ucimage._image_builder import _register_union_image_builder

        def _cli_main_config_callback(ctx, param, value):
            from union._config import ConfigSource, ConfigWithSource
            from union._exceptions import UnionRequireConfigException

            # Set org based on config from `pyflyte --config` for downstream cli
            # commands to use.
            # Only register image builder for serverless
            with suppress(UnionRequireConfigException):
                if isinstance(value, str):
                    config_source = ConfigWithSource(config=value, source=ConfigSource.CLI)
                    config_obj = _get_config_obj(config_source)
                else:
                    config_obj = _get_config_obj(value)

                if union._config._should_enable_image_builder(config_obj.platform.endpoint):
                    _register_union_image_builder()

            return value

        for p in main.params:
            if p.name == "config":
                p.callback = _cli_main_config_callback

        # Configure org at the top level:
        def _set_org(ctx, param, value):
            if value is not None:
                union._config._UNION_CONFIG.org = value

        main.params.append(
            click.Option(
                ["--org"],
                help="Set organization",
                hidden=True,
                callback=_set_org,
                expose_value=False,
            )
        )

        def update_or_create_group(new_group):
            try:
                main_group = main.commands[new_group.name]
                for name, command in new_group.commands.items():
                    main_group.add_command(command, name)
            except KeyError:
                main.add_command(new_group)

        new_groups = [create, delete, update, get]

        if ENABLE_UNION_SERVING:
            new_groups.extend([deploy, stop])

        for group in new_groups:
            update_or_create_group(group)

        new_commands = [info]
        for command in new_commands:
            main.add_command(command)

        def yield_all_options():
            commands = [main]

            while commands:
                command = commands.pop()
                yield from (p for p in command.params if isinstance(p, Option))

                if isinstance(command, Group):
                    commands.extend(list(command.commands.values()))

        for param in yield_all_options():
            if param.name == "image_config" and param.default is not None and not callable(param.default):
                param.default = lambda: [union._config._get_default_image()]

        return main

    @staticmethod
    def secret_requires_group() -> bool:
        """Return True if secrets require group entry."""
        return False

    @staticmethod
    def get_default_image() -> Optional[str]:
        """Return default image."""

        from union._config import _get_default_image

        return _get_default_image()

    @staticmethod
    def get_auth_success_html(endpoint: str) -> Optional[str]:
        """Get default success html. Return None to use flytekit's default success html."""
        from union._config import _get_auth_success_html

        return _get_auth_success_html(endpoint)
