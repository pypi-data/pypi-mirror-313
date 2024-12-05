# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

resource_dir = Path(__file__).parent

CONTAINERFILE = resource_dir / "Containerfile"

# During the build of the wheel file, the fm-tools/data directory is copied
# to the wheel file under fm_weck/resources/fm_tools
FM_DATA_LOCATION = resource_dir / "fm_tools"
PROPERTY_LOCATION = resource_dir / "properties"
RUN_WITH_OVERLAY = "run_with_overlay.sh"
BENCHEXEC_WHL = resource_dir / "BenchExec-3.25-py3-none-any.whl"
RUNEXEC_SCRIPT = "runexec"


def iter_fm_data():
    for fm_data in FM_DATA_LOCATION.iterdir():
        if fm_data.is_file() and (fm_data.name.endswith(".yml") or fm_data.name.endswith(".yaml")):
            yield fm_data


def iter_properties():
    for prop in PROPERTY_LOCATION.iterdir():
        if prop.is_file():
            yield prop
