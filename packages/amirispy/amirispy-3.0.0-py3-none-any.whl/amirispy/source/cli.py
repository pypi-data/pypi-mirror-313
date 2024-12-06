# SPDX-FileCopyrightText: 2024 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import argparse
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Tuple, Optional, List

from amirispy.scripts.subcommands.install import InstallMode
from amirispy.source.logs import LogLevels

AMIRIS_PARSER = "Command-line interface to the electricity market model AMIRIS"
AMIRIS_LOG_FILE_HELP = "Provide logging file (default: None)"
AMIRIS_LOG_LEVEL_HELP = f"Choose logging level (default: {LogLevels.ERROR.name})"
AMIRIS_COMMAND_HELP = "Choose one of the following commands:"
INSTALL_HELP = "Downloads and installs latest open access AMIRIS instance"
INSTALL_URL_MODEL_HELP = "URL to download AMIRIS model from (default: latest AMIRIS artifact)"
INSTALL_TARGET_HELP = "Folder to install 'amiris-core_<version>-jar-with-dependencies.jar' to (default: './')"
INSTALL_FORCE_HELP = "Force install to overwrite existing AMIRIS installation and/or examples (default: False)"
INSTALL_MODE_HELP = "Choose to install model and examples `all` (default), only `model`, or only `examples`"
RUN_HELP = "Compile scenario, execute AMIRIS, and extract results"
RUN_JAR_HELP = "Path to 'amiris-core_<version>-jar-with-dependencies.jar'"
RUN_SCENARIO_HELP = "Path to a scenario yaml-file"
RUN_OUTPUT_HELP = "Directory to write output to"
RUN_OUTPUT_OPTION_HELP = (
    "optional pass through of FAME-Io's output conversion options, see "
    "https://gitlab.com/fame-framework/fame-io/-/blob/main/README.md#read-fame-results"
)
RUN_NO_CHECK_HELP = "Skip checks for Java installation and correct version"
BATCH_HELP = "Batch mode to perform multiple runs each with scenario compilation, execution, and results extraction"
BATCH_SCENARIO_HELP = "Path to single or list of: scenario yaml-files or their enclosing directories"
BATCH_RECURSIVE_HELP = "Option to recursively search in provided Path for scenario (default: False)"
DEFAULT_PATTERN = "*.y*ml"
BATCH_PATTERN_HELP = f"Optional name pattern that scenario files searched for must match (default: '{DEFAULT_PATTERN}')"
COMPARE_HELP = "Compare if results of two AMIRIS runs and equivalent"
COMPARE_EXPECTED_HELP = "Path to folder with expected results"
COMPARE_TEST_HELP = "Path to folder with results to test"
COMPARE_IGNORE_HELP = "Optional list of file names to not be compared"
URL_LATEST_AMIRIS = "https://gitlab.com/dlr-ve/esy/amiris/amiris/-/jobs/artifacts/main/download?job=deploy:jdk11"


class GeneralOptions(Enum):
    """Specifies general options for workflow"""

    LOG = auto()
    LOGFILE = auto()


class Command(Enum):
    """Specifies command to execute"""

    RUN = auto()
    INSTALL = auto()
    COMPARE = auto()
    BATCH = auto()


class CompareOptions(Enum):
    """Options for command `compare`"""

    EXPECTED = auto()
    TEST = auto()
    IGNORE = auto()


class InstallOptions(Enum):
    """Options for command `install`"""

    URL = auto()
    TARGET = auto()
    FORCE = auto()
    MODE = auto()


class RunOptions(Enum):
    """Options for command `run`"""

    JAR = auto()
    SCENARIO = auto()
    OUTPUT = auto()
    OUTPUT_OPTIONS = auto()
    NO_CHECKS = auto()


class BatchOptions(Enum):
    """Options for command `batch`"""

    JAR = auto()
    SCENARIOS = auto()
    OUTPUT = auto()
    RECURSIVE = auto()
    PATTERN = auto()
    NO_CHECKS = auto()


Options = {
    Command.COMPARE: CompareOptions,
    Command.RUN: RunOptions,
    Command.INSTALL: InstallOptions,
    Command.BATCH: BatchOptions,
}


def arg_handling_run(input_args: Optional[List[str]] = None) -> Tuple[Command, Dict[Enum, Any]]:
    """
    Handles command line arguments for `amiris` and returns `command` and its options `args`
    Allows to set args from a string through input_args
    """

    parent_parser = argparse.ArgumentParser(prog="amiris", description=AMIRIS_PARSER)
    parent_parser.add_argument("-lf", "--logfile", type=Path, required=False, help=AMIRIS_LOG_FILE_HELP)
    parent_parser.add_argument(
        "-l",
        "--log",
        default=LogLevels.WARN.name,
        choices=[level.name.lower() for level in LogLevels],
        help=AMIRIS_LOG_LEVEL_HELP,
    )
    subparsers = parent_parser.add_subparsers(dest="command", required=True, help=AMIRIS_COMMAND_HELP)

    install_parser = subparsers.add_parser("install", help=INSTALL_HELP)
    install_parser.add_argument("--url", "-u", default=URL_LATEST_AMIRIS, help=INSTALL_URL_MODEL_HELP)
    install_parser.add_argument("--target", "-t", type=Path, default=Path("./"), help=INSTALL_TARGET_HELP)
    install_parser.add_argument("--force", "-f", default=False, action="store_true", help=INSTALL_FORCE_HELP)
    install_parser.add_argument(
        "--mode",
        "-m",
        type=str.lower,
        choices=[mode.name.lower() for mode in InstallMode],
        default=InstallMode.ALL.name,
        help=INSTALL_MODE_HELP,
    )
    run_parser = subparsers.add_parser("run", help=RUN_HELP)
    run_parser.add_argument("--jar", "-j", type=Path, required=True, help=RUN_JAR_HELP)
    run_parser.add_argument("--scenario", "-s", type=Path, required=True, help=RUN_SCENARIO_HELP)
    run_parser.add_argument("--output", "-o", type=Path, default=Path("./result"), help=RUN_OUTPUT_HELP)
    run_parser.add_argument("--output-options", "-oo", type=str, default="", help=RUN_OUTPUT_OPTION_HELP)
    run_parser.add_argument("--no-checks", "-nc", action="store_true", default=False, help=RUN_NO_CHECK_HELP)

    batch_parser = subparsers.add_parser("batch", help=BATCH_HELP)
    batch_parser.add_argument("--jar", "-j", type=Path, required=True, help=RUN_JAR_HELP)
    batch_parser.add_argument("--scenarios", "-s", nargs="+", type=Path, required=True, help=BATCH_SCENARIO_HELP)
    batch_parser.add_argument("--output", "-o", type=Path, default=Path("./"), help=RUN_OUTPUT_HELP)
    batch_parser.add_argument("--recursive", "-r", default=False, action="store_true", help=BATCH_RECURSIVE_HELP)
    batch_parser.add_argument("--pattern", "-p", type=str, default=DEFAULT_PATTERN, help=BATCH_PATTERN_HELP)
    batch_parser.add_argument("--no-checks", "-nc", action="store_true", default=False, help=RUN_NO_CHECK_HELP)

    compare_parser = subparsers.add_parser("compare", help=COMPARE_HELP)
    compare_parser.add_argument("--expected", "-e", type=Path, required=True, help=COMPARE_EXPECTED_HELP)
    compare_parser.add_argument("--test", "-t", type=Path, required=True, help=COMPARE_TEST_HELP)
    compare_parser.add_argument("--ignore", "-i", required=False, help=COMPARE_IGNORE_HELP)

    args = vars(parent_parser.parse_args(input_args))

    command = Command[args.pop("command").upper()]

    return command, enumify(command, args)


def enumify(command: Command, args: dict) -> Dict[Enum, Any]:
    """Matches `args` for given `command` to their respective Enum"""

    result = {}
    for option in GeneralOptions:
        result[option] = args.pop(option.name.lower())

    for option in Options[command]:
        result[option] = args.pop(option.name.lower())
    return result
