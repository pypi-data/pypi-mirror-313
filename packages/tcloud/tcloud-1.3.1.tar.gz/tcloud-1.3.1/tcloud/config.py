from __future__ import annotations

import typing as t
import os
from pathlib import Path
from dataclasses import dataclass

from ruamel.yaml import YAML

from tcloud import constants as c


@dataclass
class TCloudProject:
    url: str
    token: str
    gateway: t.Optional[str]
    extras: t.Optional[t.List[str]]
    pip_executable: t.Optional[str] = None


def _load_yaml(path: Path) -> t.Optional[t.Dict[str, t.Any]]:
    if not path.exists():
        return None
    yaml = YAML(typ="safe")
    with open(path, "r", encoding="utf-8") as fd:
        config_str = fd.read()
        if not config_str:
            return None
    return yaml.load(config_str)


def load_project_config(
    project: t.Optional[str], paths: t.Optional[t.List[Path]] = None
) -> TCloudProject:
    if all(v in os.environ for v in ("TCLOUD_URL", "TCLOUD_TOKEN")) and project is None:
        extras = None
        extras_raw = os.environ.get("TCLOUD_EXTRAS")
        if extras_raw is not None:
            extras = extras_raw.split(",")
        return TCloudProject(
            url=os.environ["TCLOUD_URL"],
            token=os.environ["TCLOUD_TOKEN"],
            gateway=os.environ.get("TCLOUD_GATEWAY"),
            extras=extras,
            pip_executable=os.environ.get("TCLOUD_PIP_EXECUTABLE"),
        )

    if paths is None:
        paths = [
            c.TCLOUD_PATH / "tcloud.yaml",
            c.TCLOUD_PATH / "tcloud.yml",
            Path(".") / "tcloud.yaml",
            Path(".") / "tcloud.yml",
        ]

    merged_config: t.Dict[str, t.Any] = {}

    for path in paths:
        config = _load_yaml(path)

        if config is None:
            continue

        projects = config.get("projects", {})
        projects.update(merged_config.get("projects", {}))
        merged_config["projects"] = projects

        if "default_project" in config:
            merged_config["default_project"] = config["default_project"]

    if not merged_config:
        raise ValueError("Could not find tcloud configuration.")

    default_project = merged_config.get("default_project")
    projects = merged_config.get("projects", {})

    if not projects:
        raise ValueError("No projects found in configuration.")

    if project is None:
        project = default_project

    if project is not None:
        if project not in projects:
            raise ValueError(f"Project '{project}' not found in configuration.")
        return _to_tcloud_project(project, projects[project])

    first_project = next(iter(projects))
    return _to_tcloud_project(first_project, projects[first_project])


def _to_tcloud_project(project: str, raw: t.Dict[str, str]) -> TCloudProject:
    missing_fields = []
    token = os.environ.get("TCLOUD_TOKEN", raw.get("token"))
    if token is None:
        missing_fields.append("token")
    for field in ("url", "gateway"):
        if field not in raw:
            missing_fields.append(field)
    if missing_fields:
        raise ValueError(
            f"""{", ".join([f"'{x}'" for x in missing_fields])} is missing in configuration for project '{project}'."""
        )
    extras = raw.get("extras")
    if isinstance(extras, str):
        extras = extras.split(",")  # type: ignore
    if extras is not None and not isinstance(extras, list):
        raise ValueError(f"'extras' is expected to be a list but got: {extras}.")
    return TCloudProject(
        url=raw["url"],
        token=token,  # type: ignore
        gateway=raw["gateway"],
        extras=extras,  # type: ignore
        pip_executable=raw.get("pip_executable"),
    )


def _load_previous_extras_contents(path: t.Optional[Path] = None) -> t.Dict[str, t.List[str]]:
    return _load_yaml(path or c.EXTRAS_PATH) or {}


def load_previous_extras(project_url: str, path: t.Optional[Path] = None) -> t.List[str]:
    contents = _load_previous_extras_contents(path)
    return contents.get(project_url, [])


def save_previous_extras(
    project_url: str, extras: t.List[str], path: t.Optional[Path] = None
) -> None:
    contents = _load_previous_extras_contents(path)
    contents[project_url] = extras
    yaml = YAML(typ="safe")
    path = path or c.EXTRAS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fd:
        yaml.dump(contents, fd)
