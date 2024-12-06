# SPDX-FileCopyrightText: 2022 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path

from amirispy.source.fameio_calls import compile_output, call_amiris, compile_input, determine_all_paths

from amirispy.source.cli import RunOptions
from amirispy.source.files import check_if_write_access
from amirispy.source.logs import log_error_and_raise
from amirispy.source.util import check_java

_ERR_NOT_A_FILE = "Specified path '{}' is no file."


def run_amiris(options: dict) -> None:
    """
    Compile scenario to protobuf using fameio.scripts.make_config,
    execute AMIRIS, and extract results using fameio.scripts.convert_results

    Args:
        options: dictionary of command line instructions

    Returns:
        None
    """
    check_java(skip=options[RunOptions.NO_CHECKS])
    origin_wd = Path.cwd()
    check_if_write_access(origin_wd)

    path_to_scenario: Path = options[RunOptions.SCENARIO]
    if not path_to_scenario.is_file():
        log_error_and_raise(ValueError(_ERR_NOT_A_FILE.format(path_to_scenario)))

    paths = determine_all_paths(path_to_scenario, origin_wd, options, batch=False)
    os.chdir(paths["SCENARIO_DIRECTORY"])
    compile_input(options, paths)
    os.chdir(origin_wd)
    call_amiris(paths)
    compile_output(options, paths)
