<!-- SPDX-FileCopyrightText: 2024 German Aerospace Center <amiris@dlr.de>

SPDX-License-Identifier: Apache-2.0 -->

[![PyPI version](https://badge.fury.io/py/amirispy.svg)](https://badge.fury.io/py/amirispy)
[![PyPI license](https://img.shields.io/pypi/l/amirispy.svg)](https://badge.fury.io/py/amirispy)
[![pipeline status](https://gitlab.com/dlr-ve/esy/amiris/amiris-py/badges/main/pipeline.svg)](https://gitlab.com/dlr-ve/esy/amiris/amiris-py/commits/main)


# AMIRIS-Py
Python tools for the electricity market model [AMIRIS](https://dlr-ve.gitlab.io/esy/amiris/home/).

## Installation

    pip install amirispy

You may also use `pipx`. For detailed information please refer to the
official `pipx` [documentation](https://github.com/pypa/pipx).

    pipx install amirispy


### Further Requirements

In order to execute all commands provided by `amirispy`, you also require a Java Development Kit (JDK).
JDK must be installed and accessible via your console in which you run `amirispy`.

To test, run `java --version` which should show your JDK version (required: 11 or above).
If `java` command is not found or relates to a Java Runtime Environment (JRE), please download and install JDK (e.g.
from [Adoptium](https://adoptium.net/de/temurin/releases/?version=17))

## Usage
Currently, there are three distinct commands available:

- `amiris install`: installation of the [latest AMIRIS version](https://gitlab.com/dlr-ve/esy/amiris/amiris)
  and [examples](https://gitlab.com/dlr-ve/esy/amiris/examples) to your computer
- `amiris run`: perform a full workflow by compiling the `.pb` file from your `scenario.yaml`, executing AMIRIS, and
  converting results
- `amiris batch`: perform multiple runs each with scenario compilation, AMIRIS execution, and results extraction
- `amiris comparison`: compare the results of two different AMIRIS runs to check them for their equivalence

You may also use the arguments as a list of strings in your script directly, e.g.

```python
from amirispy.scripts import amiris_cli

amiris_cli(["install", "-m", "model"])
```

### `amiris install`
Downloads and installs the latest open access AMIRIS instance and accompanying examples.

| Option             | Action                                                                                                                                                       |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-u` or `--url`    | URL to download AMIRIS from (default: latest AMIRIS artifact from [https://gitlab.com/dlr-ve/esy/amiris/amiris](https://gitlab.com/dlr-ve/esy/amiris/amiris) |
| `-t` or `--target` | Folder to install `amiris-core_<version>-jar-with-dependencies.jar` to (default: `./`)                                                                       |
| `-f` or `--force`  | Force install which may overwrites existing AMIRIS installation of same version and existing examples (default: False)                                       |
| `-m` or `--mode`   | Option to install model and examples `all` (default), only `model`, or only `examples`                                                                       |

### `amiris run`
Compile scenario, execute AMIRIS, and extract results.

| Option                      | Action                                                                                                                                                            |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-j` or `--jar`             | Path to `amiris-core_<version>-jar-with-dependencies.jar`                                                                                                         |
| `-s` or `--scenario`        | Path to a scenario yaml-file                                                                                                                                      |
| `-o` or `--output`          | Directory to write output to, defaults to "./results"                                                                                                             |
| `-oo` or `--output-options` | Optional arguments to override default output [conversion arguments of fameio](https://gitlab.com/fame-framework/fame-io/-/blob/main/README.md#read-fame-results) |
| `-nc` or `--no-checks`      | Skip checks for Java installation and correct version to increase speed                                                                                           |

### `amiris batch`
Perform multiple runs - each with scenario compilation, AMIRIS execution, and results extraction

| Option                 | Action                                                                        |
|------------------------|-------------------------------------------------------------------------------|
| `-j` or `--jar`        | Path to `amiris-core_<version>-jar-with-dependencies.jar`                     |
| `-s` or `--scenarios`  | Path to single or list of: scenario yaml-files or their enclosing directories |
| `-o` or `--output`     | Directory to write output to                                                  |
| `-r` or `--recursive`  | Option to recursively search in provided Path for scenario (default: False)   |
| `-p` or `--pattern`    | Optional name pattern that scenario files searched for must match             |
| `-nc` or `--no-checks` | Skip checks for Java installation and correct version to increase speed       |

### `amiris compare`
Compare if results of two AMIRIS runs and equivalent.

| Option               | Action                                                            |
|----------------------|-------------------------------------------------------------------|
| `-e` or `--expected` | Path to folder with expected result .csv files                    |
| `-t` or `--test`     | Path to folder with results files (.csv) to test  for equivalence |
| `-i` or `--ignore`   | Optional list of file names not to be compared                    |


### Help
You reach the help menu at any point using `-h` or `--help` which gives you a list of all available options, e.g.:

`amiris --help`


### Logging
You may define a logging level or optional log file as **first** arguments in your workflow using any of the following
arguments:

| Option               | Action                                                                                                           |
|----------------------|------------------------------------------------------------------------------------------------------------------|
| `-l` or `--log`      | Sets the logging level. Default is `error`. Options are `debug`, `info`, `warning`, `warn`, `error`, `critical`. |
| `-lf` or `--logfile` | Sets the logging file. Default is `None`. If `None` is provided, all logs get only printed to the console.       |

Example: `amiris --log debug --logfile my/log/file.txt install`

## Cite AMIRIS-Py
If you use AMIRIS-Py for academic work, please cite:

Christoph Schimeczek, Kristina Nienhaus, Ulrich Frey, Evelyn Sperber, Seyedfarzad Sarfarazi, Felix Nitsch, Johannes
Kochems & A. Achraf El Ghazi (2023). AMIRIS: Agent-based Market model for the Investigation of Renewable and Integrated
energy Systems. Journal of Open Source Software. doi: [10.21105/joss.05041](https://doi.org/10.21105/joss.05041)

## Contributing
Please see [CONTRIBUTING](CONTRIBUTING.md).

## Available Support
This is a purely scientific project by (at the moment) one research group.
Thus, there is no paid technical support available.

If you experience any trouble with AMIRIS, you may contact the developers at
the [openMod-Forum](https://forum.openmod.org/tag/amiris) or via [amiris@dlr.de](mailto:amiris@dlr.de).
Please report bugs and make feature requests by filing issues following the provided templates (see
also [CONTRIBUTING](CONTRIBUTING.md)).
For substantial enhancements, we recommend that you contact us via [amiris@dlr.de](mailto:amiris@dlr.de) for working
together on the code in common projects or towards common publications and thus further develop AMIRIS.

## Acknowledgement
Work on AMIRIS-Py was financed by the Helmholtz Association's Energy System Design research programme.