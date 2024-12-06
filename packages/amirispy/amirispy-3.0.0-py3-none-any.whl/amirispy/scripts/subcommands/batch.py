# SPDX-FileCopyrightText: 2024 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log
import os
from pathlib import Path
from typing import List

from fameio.input import SchemaError, ScenarioError
from fameio.input.loader import load_yaml
from fameio.input.scenario import Scenario
from fameio.input.validator import SchemaValidator, ValidationError

from amirispy.source.cli import BatchOptions
from amirispy.source.fameio_calls import determine_all_paths, compile_input, call_amiris, compile_output
from amirispy.source.files import check_if_write_access
from amirispy.source.logs import log_error_and_raise, log_and_print
from amirispy.source.util import check_java

_ERR_ALL_PATHS_INVALID = "Provided scenario path(s) '{}' contain no valid scenario YAML files."
_ERR_PATH_NOT_EXISTING = "Provided path '{}' is ignored as it is neither a file nor a directory."
_ERR_NO_VALID_FAME_SCENARIO = "'{}' is not a valid scenario file. You may improve the file name pattern using `-p`"


def batch_run_amiris(options: dict) -> None:
    """
    Compile multiple scenarios to protobuf using fameio.scripts.make_config, execute AMIRIS,
    and extract results using fameio.scripts.convert_results

    Args:
        options: dictionary of command line instructions
    """
    check_java(skip=options[BatchOptions.NO_CHECKS])
    origin_wd = Path.cwd()
    check_if_write_access(origin_wd)

    input_yaml_files = find_valid_scenarios(
        options[BatchOptions.SCENARIOS], options[BatchOptions.RECURSIVE], options[BatchOptions.PATTERN]
    )

    for i, input_yaml_file in enumerate(input_yaml_files):
        if len(input_yaml_files) >= 1:
            log_and_print(f"AMIRIS run {i+1}/{len(input_yaml_files)}")

        paths = determine_all_paths(input_yaml_file, origin_wd, options, batch=True)
        os.chdir(paths["SCENARIO_DIRECTORY"])
        compile_input(options, paths)
        os.chdir(origin_wd)
        call_amiris(paths)
        compile_output(options, paths)


def find_valid_scenarios(search_paths: List[Path], recursive: bool, pattern: str) -> List[Path]:
    """
    Searches for valid scenario YAML files in given `input_yaml_paths`

    Args:
        search_paths: path(s) which are to be searched for valid scenario files
        recursive: if true, subdirectories of each search path are searched as well
        pattern: that file names must match to be returned

    Returns:
        List of Paths to valid scenario files
    """
    files_to_test = get_inner_yaml_files(search_paths, recursive, pattern)
    scenario_files = [file for file in files_to_test if is_valid_fame_input_yaml(file)]
    if not scenario_files:
        log_error_and_raise(ValueError(_ERR_ALL_PATHS_INVALID.format(search_paths)))
    log.info(f"Found these scenario file(s) '{scenario_files}'.")
    return scenario_files


def get_inner_yaml_files(paths: List[Path], recursive: bool, pattern: str) -> List[Path]:
    """
    Returns a list of all YAML files in `paths` (and all subdirectories when `recursive` is set to True)

    Args:
        paths: to search for YAML files
        recursive: if True, subdirectories are also searched
        pattern: that file names must match to be returned

    Returns:
        List of Paths to YAML files contained in `paths` (and its subdirectories)
    """
    yaml_files = []
    for path in paths:
        if path.is_file():
            yaml_files.append(path)
        elif path.is_dir():
            yaml_files.extend([f for f in path.glob(pattern) if f.is_file()])
            if recursive:
                yaml_files.extend(get_inner_yaml_files([f for f in path.glob("*") if f.is_dir()], recursive, pattern))
        else:
            log.error(_ERR_PATH_NOT_EXISTING.format(path))
    return yaml_files


def is_valid_fame_input_yaml(file_to_test: Path) -> bool:
    """
    Checks if the given path points to a valid FAME input YAML file. If not, an error is logged.

    Args:
        file_to_test: Path to a file

    Returns:
        True if the given path points to valid FAME input YAML file, otherwise False
    """
    try:
        scenario = Scenario.from_dict(load_yaml(file_to_test))
        SchemaValidator.validate_scenario_and_timeseries(scenario)
        return True
    except (ScenarioError, SchemaError, FileNotFoundError, ValidationError) as e:
        log.warning(_ERR_NO_VALID_FAME_SCENARIO.format(file_to_test))
        log.info(f"Error: {e}")
    return False
