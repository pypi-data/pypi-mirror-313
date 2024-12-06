from __future__ import annotations

import typing as t
import logging

import requests
import os
import shutil
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
from urllib.parse import urlencode, urljoin

from tcloud.config import TCloudProject
from tcloud import constants as c, pip_helper as pip

logger = logging.getLogger(__name__)

PACKAGE_NAME = "sqlmesh-enterprise"
EXECUTORS_PEX_NAME = "executors_bin.pex"


def install_sqlmesh_enterprise(project: TCloudProject, previous_extras: t.List[str]) -> bool:
    """Downloads and installs / upgrades the SQLMesh Enterprise package if needed.

    Args:
        project: The target project.
        previous_extras: The extras that were previously installed.

    Returns:
        True if the package was installed or upgraded, False otherwise.
    """
    _configure_state_connection(project)

    # Use the package metadata to avoid importing the package.
    try:
        current_version = version(PACKAGE_NAME)
    except PackageNotFoundError:
        current_version = None

    upgrade_info = _get_enterprise_version_upgrade(project, current_version)
    target_version = upgrade_info["target_version"]
    # Check `upgrade_info` for extras in case the API supports this in the future
    extras = set((project.extras or []) + upgrade_info.get("extras", []))  # type: ignore

    if current_version == target_version and extras.issubset(previous_extras):
        return False

    pip.install(
        PACKAGE_NAME,
        pip_executable=project.pip_executable,
        version=target_version,  # type: ignore
        extra_index_url=upgrade_info.get("extra_index_url"),  # type: ignore
        upgrade=True,
        extras=list(extras),
    )

    return True


def install_executors(project: TCloudProject, tcloud_path: Path = c.TCLOUD_PATH) -> Path:
    artifacts_path = tcloud_path / "artifacts"
    artifacts_path.mkdir(parents=True, exist_ok=True)

    current_version = None
    current_executors_bin_path = None

    version_folders = sorted(artifacts_path.iterdir(), reverse=True)
    if version_folders:
        current_version = version_folders[0].name
        current_executors_bin_path = version_folders[0] / EXECUTORS_PEX_NAME
        if not current_executors_bin_path.exists():
            current_version = None

    logger.info("The current executor version: '%s'", current_version)

    upgrade_info = _get_enterprise_version_upgrade(project, current_version)
    target_version = t.cast(str, upgrade_info["target_version"])

    logger.info("The target executor version: '%s'", target_version)

    if current_version == target_version and current_executors_bin_path:
        return current_executors_bin_path

    for old_version in version_folders:
        if old_version.name != target_version and old_version.is_dir():
            shutil.rmtree(old_version)

    if "executors_pex_url" not in upgrade_info:
        raise ValueError("The upgrade info does not contain the download URL.")

    token = t.cast(t.Optional[str], upgrade_info.get("token"))
    executors_pex_url = t.cast(str, upgrade_info["executors_pex_url"])

    target_version_path = artifacts_path / target_version
    target_version_path.mkdir(exist_ok=True)

    target_executors_bin_path = target_version_path / EXECUTORS_PEX_NAME
    logger.info(
        "Downloading the executors PEX binary from %s to %s",
        executors_pex_url,
        target_executors_bin_path,
    )
    with requests.get(
        executors_pex_url,
        headers={"Authorization": f"Bearer {token}"} if token else None,
        stream=True,
    ) as response:
        response.raise_for_status()
        with open(target_executors_bin_path, "wb") as fd:
            shutil.copyfileobj(response.raw, fd)

    logger.info("Finished downloading the executors PEX binary")

    os.chmod(target_executors_bin_path, 0o744)

    return target_executors_bin_path


def _get_enterprise_version_upgrade(
    project: TCloudProject, current_version: t.Optional[str]
) -> t.Dict[str, t.Union[str, t.List[str]]]:
    url = project.url
    if not url.endswith("/"):
        url += "/"

    upgrade_url = urljoin(url, "state_sync/enterprise_version/upgrade")
    if current_version:
        url_params = urlencode({"current_version": current_version})
        upgrade_url += f"?{url_params}"

    response = requests.get(upgrade_url, headers={"Authorization": f"Bearer {project.token}"})
    response.raise_for_status()
    return response.json()


def _configure_state_connection(project: TCloudProject) -> None:
    if not project.gateway:
        raise ValueError("The gateway must be set.")

    state_connection_env_prefix = f"SQLMESH__GATEWAYS__{project.gateway.upper()}__STATE_CONNECTION"
    os.environ[f"{state_connection_env_prefix}__TYPE"] = "cloud"
    os.environ[f"{state_connection_env_prefix}__URL"] = project.url
    os.environ[f"{state_connection_env_prefix}__TOKEN"] = project.token
    os.environ["SQLMESH__DEFAULT_GATEWAY"] = project.gateway
