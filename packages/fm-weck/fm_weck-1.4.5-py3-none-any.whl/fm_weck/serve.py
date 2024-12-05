# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import dbm
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, Tuple, Union

from fm_tools import FmData
from fm_tools.benchexec_helper import DataModel

from .config import Config, parse_fm_data
from .engine import CACHE_MOUNT_LOCATION, Engine

logger = logging.getLogger(__name__)


def check_cache_entry(shelve_space: Path, checksum: str, config: Config) -> bool:
    checksum_file = config.get_checksum_db()

    if sys.version_info < (3, 11):
        # Python 3.10 and below only support strings as path to dbm.open
        checksum_file = str(checksum_file.resolve())

    try:
        with dbm.open(checksum_file, "r") as db:
            # dbm returns bytes, so we need to encode the checksum
            # we use utf-8 encoding to ensure consistency
            return db[shelve_space.name] == checksum.encode("utf-8")
    except dbm.error:
        logger.debug("Checksum file does not exist")
        return False
    except KeyError:
        logger.debug("Checksum does not exist")
        return False


def update_checksum(shelve_space: Path, checksum: str, config: Config):
    checksum_file = config.get_checksum_db()

    if sys.version_info < (3, 11):
        # Python 3.10 and below only support strings as path to dbm.open
        checksum_file = str(checksum_file.resolve())

    with dbm.open(checksum_file, "c") as db:
        logger.debug("Updating checksum for %s", shelve_space.name)
        logger.debug("Checksum: %s", checksum)
        # dbm only stores bytes, so we need to encode the checksum
        # we use utf-8 encoding to ensure consistency
        db[shelve_space.name] = checksum.encode("utf-8")


def setup_fm_tool(
    fm_tool: Union[Path, FmData], version: Optional[str], configuration: Config, skip_download: bool = False
) -> Tuple[FmData, Path]:
    # Don't explicitly disallow non-FmData here; Pythonic Users might want to exchange the FmData object
    # by a class with the same interface
    fm_data = parse_fm_data(fm_tool, version) if isinstance(fm_tool, (Path, str)) else fm_tool

    shelve_space = configuration.get_shelve_space_for(fm_data)
    logger.debug("Using shelve space %s", shelve_space)

    if (not skip_download) and shelve_space.exists() and shelve_space.is_dir():
        logger.debug("Shelve space already exists, testing checksum")
        checksum = fm_data.archive_location.checksum()
        skip_download = check_cache_entry(shelve_space, checksum, configuration)

    if not skip_download:
        fm_data.download_and_install_into(shelve_space)
        checksum = fm_data.archive_location.checksum()
        update_checksum(shelve_space, checksum, configuration)

    fm_data.get_toolinfo_module().make_available()

    return fm_data, shelve_space


def run_guided(
    fm_tool: Union[Path, FmData],
    version: Optional[str],
    configuration: Config,
    prop: Optional[Path],
    program_files: list[Path],
    additional_args: list[str],
    data_model: Optional[DataModel] = None,
    skip_download: bool = False,
    log_output_to: Optional[Path] = None,
    output_files_to: Optional[Path] = None,
) -> int:
    property_path = None
    if prop is not None:
        try:
            # the source path might not be mounted in the contianer, so we
            # copy the property to the weck_cache which should be mounted
            source_property_path = prop
            property_path = configuration.get_shelve_path_for_property(source_property_path)
            shutil.copyfile(source_property_path, property_path)
        except KeyError:
            logger.error("Unknown property %s", prop)
            return 1

    configuration.make_script_available()

    fm_data, shelve_space = setup_fm_tool(fm_tool, version, configuration, skip_download)
    engine = Engine.from_config(fm_data, configuration)

    if log_output_to is not None:
        engine.set_output_log(log_output_to)

    if output_files_to is not None:
        engine.set_output_files_dir(output_files_to)

    current_dir = Path.cwd().resolve()
    os.chdir(shelve_space)
    command = fm_data.command_line(
        Path("."),
        input_files=program_files,
        working_dir=engine.get_workdir(),
        property=property_path,
        data_model=data_model,
        options=additional_args,
        add_options_from_fm_data=True,
    )
    os.chdir(current_dir)

    logger.debug("Assembled command from fm-tools: %s", command)

    return engine.run(f"{CACHE_MOUNT_LOCATION}/.scripts/run_with_overlay.sh", shelve_space.name, *command)


def run_manual(
    fm_tool: Union[Path, FmData],
    version: Optional[str],
    configuration: Config,
    command: list[str],
    skip_download: bool = False,
) -> int:
    fm_data, shelve_space = setup_fm_tool(fm_tool, version, configuration, skip_download)
    engine = Engine.from_config(fm_data, configuration)

    executable = fm_data.get_executable_path(shelve_space)
    logger.debug("Using executable %s", executable)
    logger.debug("Assembled command %s", [executable, *command])
    return engine.run(executable, *command)
