# SPDX-FileCopyrightText: 2023 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log
import re
import shutil
import subprocess

from amirispy.source.logs import log_and_raise_critical

_ERR_NO_JAVA = "No Java installation found. See {} for further instructions."
_ERR_JAVA_VERSION = "Local Java version '{}' does not match requirements '>{}'."
_URL_INSTALLATION_INSTRUCTIONS = "https://gitlab.com/dlr-ve/esy/amiris/amiris-py#further-requirements"

JAVA_VERSION_PATTERN = '"(\d+\.\d+).*"'
JAVA_VERSION_MINIMUM = 11


def check_java_installation(raise_exception: bool = False) -> None:
    """If Java installation is not found, logs `Warning` (default) or raises Exception if `raise_exception`"""
    if not shutil.which("java"):
        if raise_exception:
            log_and_raise_critical(_ERR_NO_JAVA.format(_URL_INSTALLATION_INSTRUCTIONS))
        else:
            log.warning(_ERR_NO_JAVA.format(_URL_INSTALLATION_INSTRUCTIONS))


def check_java_version(raise_exception: bool = False) -> None:
    """If Java version is not compatible, logs `Warning` (default) or raises Exception if `raise_exception`"""
    version_raw = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
    version_number = re.search(JAVA_VERSION_PATTERN, str(version_raw)).groups()[0]

    if float(version_number) < JAVA_VERSION_MINIMUM:
        if raise_exception:
            log_and_raise_critical(_ERR_JAVA_VERSION.format(version_number, JAVA_VERSION_MINIMUM))
        else:
            log.warning(_ERR_JAVA_VERSION.format(version_number, JAVA_VERSION_MINIMUM))


def check_java(skip: bool) -> None:
    """Checks java installation and version if not `skip`"""
    if not skip:
        check_java_installation(raise_exception=True)
        check_java_version(raise_exception=True)
