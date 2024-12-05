# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import importlib.resources as pkg_resources
import logging
import os
import shutil
import stat
import sys
from functools import cache
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Tuple, TypeVar

try:
    from fm_tools.fmdata import FmData
except ImportError:

    class FmData:
        def __init__(self, data, version):
            raise ImportError("fm_tools is not imported.")

        def get_actor_name(self):
            raise ImportError("fm_tools is not imported.")

        def get_version(self):
            raise ImportError("fm_tools is not imported.")


from fm_weck.resources import RUN_WITH_OVERLAY, RUNEXEC_SCRIPT

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

_SEARCH_ORDER: tuple[Path, ...] = (
    Path.cwd() / ".fm-weck",
    Path.home() / ".fm-weck",
    Path.home() / ".config" / "fm-weck",
    Path.home() / ".config" / "fm-weck" / "config.toml",
)
BASE_CONFIG = """
[logging]
level = "INFO"

[defaults]
engine = "podman"
"""

_T = TypeVar("_T")


class Config(object):
    """
    The config singleton holds the configuration for the weck tool.
    """

    _instance = None
    _config_source = None
    _source_path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = None
            cls._instance._dry_run = False
        return cls._instance

    def load(self, config: Optional[Path] = None) -> dict[str, Any]:
        if self._config:
            return self._config

        if config:
            if not config.exists() or not config.is_file():
                raise FileNotFoundError(f"config file {config} does not exist")

            with config.open("rb") as f:
                self._config = toml.load(f)
                self._config_source = config.resolve()
                return self._config

        for path in _SEARCH_ORDER:
            if not path.exists():
                continue

            # Configuration is in TOML format
            with path.open("rb") as f:
                self._config = toml.load(f)
                self._config_source = path
                return self._config

        self._config = toml.loads(BASE_CONFIG)
        return self._config

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def get(self, key: str, default: _T = None) -> _T:
        if self._config is not None:
            return self._config.get(key, default)

        return default

    def set_dry_run(self, dry_run: bool) -> None:
        self._dry_run = dry_run

    def is_dry_run(self) -> bool:
        return self._dry_run

    def set_default_image(self, image: str) -> None:
        self._config["defaults"]["image"] = image

    def defaults(self) -> dict[str, Any]:
        return self.get("defaults", {})

    def from_defaults_or_none(self, key: str) -> Any:
        return self.defaults().get(key, None)

    @staticmethod
    def _handle_relative_paths(fn: Callable[[Any], Path]) -> Callable[[Any], Path]:
        def wrapper(self, *args, **kwargs) -> Path:
            """Makes sure relative Paths in the config are relative to the config file."""

            path = fn(self, *args, **kwargs)

            if not self._config_source:
                return path

            if path.is_absolute():
                return path

            return (self._config_source.parent / path).resolve()

        return wrapper

    @property
    @_handle_relative_paths
    def cache_location(self) -> Path:
        cache = Path.home() / ".cache" / "fm-weck_cache"
        xdg_cache_home = os.environ.get("XDG_CACHE_HOME")

        if xdg_cache_home:
            cache = Path(xdg_cache_home) / "fm-weck_cache"

        return Path(self.defaults().get("cache_location", cache.resolve()))

    @_handle_relative_paths
    def as_absolute_path(self, path: Path) -> Path:
        return path

    def mounts(self) -> Iterable[Tuple[Path, Path]]:
        for local, container in self.get("mount", {}).items():
            yield self.as_absolute_path(Path(local)), Path(container)

    def get_checksum_db(self) -> Path:
        return self.cache_location / ".checksums.dbm"

    def get_shelve_space_for(self, fm_data: FmData) -> Path:
        shelve = self.cache_location
        tool_name = fm_data.get_actor_name()  # safe to use in filesystem
        return shelve / tool_name

    def get_shelve_path_for_property(self, path: Path) -> Path:
        shelve = self.cache_location / ".properties"
        shelve.mkdir(parents=True, exist_ok=True)
        property_name = path.name
        return shelve / property_name

    def get_shelve_path_for_benchexec(self) -> Path:
        shelve = self.cache_location / ".lib" / "benchexec.whl"
        shelve.parent.mkdir(parents=True, exist_ok=True)
        return shelve

    @staticmethod
    def _system_is_not_posix():
        return not (sys.platform.startswith("linux") or sys.platform == "darwin")

    def make_runexec_script_available(self) -> Path:
        return self.make_script_available(RUNEXEC_SCRIPT)

    def make_script_available(self, target_name: str = RUN_WITH_OVERLAY) -> Path:
        script_dir = self.cache_location / ".scripts"
        target = script_dir / target_name

        if not (target.exists() and target.is_file()):
            script_dir.mkdir(parents=True, exist_ok=True)

            # Try to copy from package resources
            try:
                with pkg_resources.path("fm_weck.resources", target_name) as source_path:
                    shutil.copy(source_path, target)
            except FileNotFoundError:
                logging.error(f"Resource {target_name} not found in package.")
                return None
        else:
            # Compare modification time if the file exists
            with pkg_resources.path("fm_weck.resources", target_name) as source_path:
                if source_path.stat().st_mtime > target.stat().st_mtime:
                    shutil.copy(source_path, target)
                else:
                    logging.debug(f"Using existing {target_name} script")
                    return target

        if Config._system_is_not_posix():
            return target

        try:
            # Get the current file permissions
            current_permissions = os.stat(target).st_mode

            # Add the executable bit for the owner, group, and others
            os.chmod(target, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except OSError as e:
            logging.error(
                f"Failed to set executable bit: {e}. "
                "This may lead to permission errors when running the script in the container."
            )

        return target


@cache
def parse_fm_data(fm_data: Path, version: Optional[str]) -> FmData:
    import yaml

    if not fm_data.exists() or not fm_data.is_file():
        raise FileNotFoundError(f"fm data file {fm_data} does not exist")

    with fm_data.open("rb") as f:
        data = yaml.safe_load(f)

    return FmData(data, version)
