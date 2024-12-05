# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
from pathlib import Path
from typing import Iterable, List

from fm_weck.engine import RESERVED_LOCATIONS


def mountable_absolute_paths_of_command(cwd: Path, command: List[str]) -> Iterable[Path]:
    """
    Iterate over all arguments in command and find those that are paths.
    The paths are returned as absolute paths, that already exist on the host.
    """

    # FIXME: Disallowing home is a temporary solution to get this to work in the BenchCloud.
    # The benchcloud will eventually hide /home, so it can be omitted in this case.
    # But potential users should be aware of this.
    no_mount = {"/", "/dev", "/proc", "/sys", "/home", "/sys/fs/cgroup"}

    command_iter = (arg for arg in command if arg not in no_mount)
    seen = set()
    for arg in command_iter:
        if arg in RESERVED_LOCATIONS:
            logging.warning("Ignoring reserved path %s. This path is internally used and mounted by fm-weck.", arg)

        path = Path(arg)
        if path not in seen and path.is_absolute() and path.exists() and not path.is_relative_to(cwd):
            yield path
            seen.add(path)
