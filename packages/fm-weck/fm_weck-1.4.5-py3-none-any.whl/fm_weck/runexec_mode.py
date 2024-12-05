# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import shutil
from pathlib import Path
from typing import Optional

from fm_weck.resources import BENCHEXEC_WHL
from fm_weck.runexec_util import mountable_absolute_paths_of_command

from .config import Config
from .engine import CACHE_MOUNT_LOCATION, Engine

logger = logging.getLogger(__name__)


def run_runexec(
    benchexec_package: Optional[Path],
    use_image: Optional[str],
    configuration: Config,
    extra_container_args: list[list[str]],
    command: list[str],
):
    if use_image is not None:
        configuration.set_default_image(use_image)

    engine = Engine.from_config(configuration)
    engine.add_benchexec_capabilities = True
    engine.add_mounting_capabilities = False

    if benchexec_package is not None:
        engine.mount(benchexec_package.parent.absolute(), "/home/__fm_weck_benchexec")
        engine.env["PYTHONPATH"] = f"/home/__fm_weck_benchexec/{benchexec_package.name}"
    else:
        # Default to the bundled benchexec package
        benchexec_package = configuration.get_shelve_path_for_benchexec()
        shutil.copyfile(BENCHEXEC_WHL, benchexec_package)
        engine.env["PYTHONPATH"] = f"{CACHE_MOUNT_LOCATION}/.lib/benchexec.whl"

    for path in mountable_absolute_paths_of_command(Path.cwd().absolute(), command):
        engine.mount(path, str(path) + ":ro")

    for arg in extra_container_args:
        engine.add_container_long_opt(arg)

    configuration.make_runexec_script_available()

    return engine.run(f"{CACHE_MOUNT_LOCATION}/.scripts/runexec", *command)
