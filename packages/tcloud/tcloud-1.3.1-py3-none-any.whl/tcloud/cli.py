from __future__ import annotations

import os
import requests
import typing as t
import time
import subprocess

import click
import logging

from tcloud.config import load_project_config, load_previous_extras, save_previous_extras
from tcloud.installer import install_sqlmesh_enterprise, install_executors


def _tcloud_version() -> str:
    try:
        from tcloud import __version__

        return __version__
    except ImportError:
        return "0.0.0"


EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC = 5.0


class DynamicGroup(click.Group):
    COMMANDS = ["sqlmesh", "sqlmesh_cicd"]

    def list_commands(self, ctx: click.Context) -> t.List[str]:
        return super().list_commands(ctx) + self.COMMANDS

    def get_command(self, ctx: click.Context, cmd_name: str) -> t.Optional[click.Command]:
        if cmd_name in self.COMMANDS:
            return self._load_sqlmesh_enterprise(cmd_name, ctx.params.get("project"))
        return super().get_command(ctx, cmd_name)

    def _load_sqlmesh_enterprise(self, cmd_name: str, project: t.Optional[str]) -> click.Command:
        try:
            project_config = load_project_config(project)
            installed = install_sqlmesh_enterprise(
                project_config, load_previous_extras(project_config.url)
            )
            if installed:
                save_previous_extras(project_config.url, project_config.extras or [])
        except (ValueError, requests.exceptions.RequestException) as ex:
            raise click.ClickException(str(ex)) from ex

        if cmd_name == "sqlmesh_cicd":
            from sqlmesh_enterprise.cli.bot import bot

            return bot

        from sqlmesh_enterprise.cli.main import cli

        return cli


@click.group(cls=DynamicGroup, no_args_is_help=True)
@click.version_option(version=_tcloud_version(), message="%(version)s")
@click.option(
    "--project",
    type=str,
    help="The name of the project.",
)
@click.pass_context
def cli(ctx: click.Context, project: t.Optional[str]) -> None:
    ctx.ensure_object(dict)
    ctx.obj["project"] = project


@cli.command()
@click.argument("executor_type", required=True, type=click.Choice(["run", "apply"]))
@click.option(
    "--once",
    is_flag=True,
    help="Runs the executor once and exit.",
)
@click.pass_context
def executor(ctx: click.Context, executor_type: str, once: bool) -> None:
    logging.basicConfig(
        format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)",
        level=logging.INFO,
    )

    project = ctx.obj["project"]
    project_config = load_project_config(project)

    def install_and_run() -> None:
        try:
            executors_bin_path = install_executors(project_config)
        except Exception as ex:
            raise click.ClickException(f"Failed to install the executor bin package: {ex}")
        subprocess.run(
            [executors_bin_path, executor_type],
            stdout=None,
            stderr=None,
            env={
                **os.environ,
                "TCLOUD_URL": project_config.url,
                "TCLOUD_TOKEN": project_config.token,
            },
        )

    if once:
        install_and_run()
    else:
        while True:
            run_start_ts = time.monotonic()
            install_and_run()
            elapsed_sec = time.monotonic() - run_start_ts
            if elapsed_sec < EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC:
                time.sleep(EXECUTOR_MIN_INTERVAL_BETWEEN_RUNS_SEC - elapsed_sec)
