# SPDX-FileCopyrightText: 2024 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log
import subprocess
from pathlib import Path
from typing import Dict

from _ctypes import ArgumentError
from fameio.scripts.convert_results import run as convert_results
from fameio.scripts.make_config import run as make_config
from fameio.cli.convert_results import handle_args as handle_output_args
from fameio.cli.options import Options, ResolveOptions, TimeOptions

from amirispy.source.cli import BatchOptions, GeneralOptions, RunOptions
from amirispy.source.files import ensure_folder_exists, check_if_write_access, warn_if_not_empty
from amirispy.source.logs import log_error_and_raise

ERR_FAMEIO_OUTPUT_ARGS = "Invalid fameio output conversion options: '{}'"


def determine_all_paths(
    scenario_yaml: Path, working_directory: Path, options: Dict, batch: bool = False
) -> Dict[str, Path]:
    """
    Determines all Paths for the given scenario file and working directory

    Args:
        scenario_yaml: path to the scenario file
        working_directory: the base working directory
        options: amiris-py command line options
        batch: bool which is True when to determine paths for batch runs (default: False)

    Returns:
        Dictionary containing all Paths to final results and temporary files
    """
    paths = {
        "SCENARIO_FILE": scenario_yaml if scenario_yaml.is_absolute() else working_directory.joinpath(scenario_yaml),
        "SCENARIO_DIRECTORY": scenario_yaml.parent,
        "BASE_NAME": scenario_yaml.stem,
        "INPUT_PB": working_directory.joinpath("input.pb"),
        "OUTPUT_PB": working_directory.joinpath("output.pb"),
    }

    jar_option = BatchOptions.JAR if batch else RunOptions.JAR
    output_option = BatchOptions.OUTPUT if batch else RunOptions.OUTPUT
    paths.update(
        {
            "JAR_FILE": options[jar_option],
            "SETUP_FILE": Path(options[jar_option].parents[0], "fameSetup.yaml"),
            "RESULT_FOLDER": Path(options[output_option]),
        }
    )

    return paths


def compile_input(options: dict, paths: Dict[str, Path]) -> None:
    """
    Creates protobuf file using given `options` and `paths`

    Args:
        options: for logging
        paths: to given input and output files
    """
    fameio_input_config = {
        Options.FILE: paths["SCENARIO_FILE"].resolve(),
        Options.LOG_LEVEL: options[GeneralOptions.LOG],
        Options.LOG_FILE: options[GeneralOptions.LOGFILE],
        Options.OUTPUT: paths["INPUT_PB"],
    }
    log.info("Creating binary protobuf input file: `{protobuf_file_path}` from scenario `{scenario_file}`")
    make_config(fameio_input_config)


def call_amiris(paths: Dict[str, Path]) -> None:
    """
    Run AMIRIS using given paths

    Args:
        paths: to all required files
    """
    call = 'java -jar "{}" -f "{}" -o "output.pb"'.format(paths["JAR_FILE"], paths["INPUT_PB"])
    log.info(f"Calling AMIRIS with {paths['SCENARIO_FILE']}")
    subprocess.run(call, shell=True, check=True)


def compile_output(options: Dict, paths: Dict[str, Path]) -> None:
    """
    Conducts to conversion of AMIRIS output to CSV files based on given options and paths

    Args:
        options: for logging
        paths: to given input and output files
    """
    default_fameio_output_config = {
        Options.FILE: paths["OUTPUT_PB"].resolve(),
        Options.LOG_LEVEL: options[GeneralOptions.LOG],
        Options.LOG_FILE: options[GeneralOptions.LOGFILE],
        Options.AGENT_LIST: None,
        Options.OUTPUT: paths["RESULT_FOLDER"],
        Options.SINGLE_AGENT_EXPORT: False,
        Options.MEMORY_SAVING: False,
        Options.RESOLVE_COMPLEX_FIELD: ResolveOptions.SPLIT.name,
        Options.TIME: TimeOptions.UTC.name,
        Options.TIME_MERGING: [0, 1800, 1799],
    }

    ensure_folder_exists(paths["RESULT_FOLDER"])
    check_if_write_access(paths["RESULT_FOLDER"])
    log.info("Converting protobuf to csv files")
    warn_if_not_empty(paths["RESULT_FOLDER"])
    fameio_output_config = override_eligible_defaults(default_fameio_output_config, options[RunOptions.OUTPUT_OPTIONS])
    convert_results(fameio_output_config)


def override_eligible_defaults(defaults: Dict, overrides: str) -> Dict:
    """
    Replaces default fameio arguments with given overrides - ensures that the output folder and file are not modified

    Args:
        defaults: standard fameio output options
        overrides: (possibly empty) list of fameio output arguments to be used instead

    Returns:
        dict of (modified) fameio arguments
    """
    fixed_output_folder = defaults[Options.OUTPUT]
    fixed_file_to_convert = defaults[Options.FILE]
    try:
        argument_list = overrides.split()
        fameio_output_config = handle_output_args(argument_list, defaults)
    except SystemExit:
        log_error_and_raise(ArgumentError(ERR_FAMEIO_OUTPUT_ARGS.format(overrides)))
    fameio_output_config[Options.OUTPUT] = fixed_output_folder
    fameio_output_config[Options.FILE] = fixed_file_to_convert
    return fameio_output_config
