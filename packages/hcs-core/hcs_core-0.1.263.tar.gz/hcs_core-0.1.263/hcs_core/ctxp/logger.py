"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import re
import logging
import coloredlogs
from logging.handlers import RotatingFileHandler

LOG_FORMAT_SIMPLE = "%(levelname).4s %(asctime)s %(name)-16s %(message)s"
LOG_FORMAT_LONG = "%(color_on)s%(asctime)s.%(msecs)03d [%(process)-5d:%(threadName)-12s] %(levelname)-7s [%(name)-16s] %(message)s%(color_off)s"
DATE_FORMAT_SIMPLE = "%H:%M:%S"


def mask_password(msg: str) -> str:
    msg = re.sub(r"(\"password\"\s*:\s*\"?)(.*?)(\"?[\s*,? | \s*\}])", r"\1******\3", msg)
    return msg


class LogFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",
        logging.ERROR: "\033[1;31m",
        logging.WARNING: "\033[1;33m",
        logging.INFO: "\033[0;37m",
        logging.DEBUG: "\033[1;30m",
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, mask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = color
        self.mask = mask

    def format(self, record, *args, **kwargs):
        if self.color is True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""

        record.name = _shorten_package_name(record.name, 16)

        msg = super(LogFormatter, self).format(record, *args, **kwargs)
        return mask_password(msg) if self.mask else msg


class LogFormatterFixedNameWidth(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record, *args, **kwargs):
        record.name = _shorten_package_name(record.name, 16)
        return super(LogFormatterFixedNameWidth, self).format(record, *args, **kwargs)


def _shorten_package_name(package_name, max_length):
    if len(package_name) <= max_length:
        return package_name

    parts = package_name.split(".")
    shortened_parts = []

    for i, part in enumerate(parts):
        shortened_parts.append(part[0])

        if i == len(parts) - 1:
            # Last package name
            remaining_length = max_length - len(".".join(shortened_parts))
            if len(part) > remaining_length:
                shortened_parts[-1] = "..." + part[-remaining_length + 3 :]
            else:
                shortened_parts[-1] = part
        else:
            new_package_name = ".".join(shortened_parts)

            if len(new_package_name) + len(parts) - i - 1 > max_length:
                break

    return ".".join(shortened_parts)


def setup(
    console_log_output="stdout",
    console_log_level="INFO",
    console_log_color=True,
    console_log_mask=True,
    logfile_file=None,
    logfile_log_level="INFO",
    logfile_log_color=False,
    logfile_log_mask=True,
    log_line_template=LOG_FORMAT_SIMPLE,
    date_fmt=DATE_FORMAT_SIMPLE,
):
    # Alternative: 'global logger; logger = logging.getLogger("<name>")'
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if console_log_output is not None:
        setup_console_output(
            logger,
            console_log_output,
            console_log_level,
            console_log_color,
            console_log_mask,
            log_line_template,
            date_fmt,
        )

    if logfile_file:
        setup_file_output(
            logger,
            logfile_file,
            logfile_log_level,
            logfile_log_color,
            logfile_log_mask,
            log_line_template,
        )


def setup_console_output(
    logger, console_log_output, console_log_level, console_log_color, console_log_mask, log_line_template, date_fmt
):
    if not date_fmt:
        date_fmt = coloredlogs.DEFAULT_DATE_FORMAT
    coloredlogs.install(
        level=console_log_level,
        fmt=log_line_template,
        datefmt=date_fmt,
        formatter=LogFormatter(fmt=log_line_template, color=console_log_color, mask=console_log_mask),
    )

    # console_log_output = console_log_output.lower()
    # if console_log_output == "stdout":
    #     console_log_output = sys.stdout
    # elif console_log_output == "stderr":
    #     console_log_output = sys.stderr
    # else:
    #     raise Exception("Failed to set console output: invalid output: '%s'" % console_log_output)
    # console_handler = logging.StreamHandler(console_log_output)

    # try:
    #     console_handler.setLevel(console_log_level.upper())
    # except:
    #     print("Failed to set console log level: invalid level: '%s'" % console_log_level)
    #     raise

    # console_formatter = LogFormatter(fmt=log_line_template, color=console_log_color, mask=console_log_mask)
    # console_handler.setFormatter(console_formatter)
    # logger.addHandler(console_handler)


def setup_file_output(
    logger,
    logfile_file,
    logfile_log_level,
    logfile_log_color,
    logfile_log_mask,
    log_line_template,
):
    logfile_max_bytes = 50 * 1024 * 1024
    logfile_max_count = 20
    try:
        logfile_handler = RotatingFileHandler(logfile_file, maxBytes=logfile_max_bytes, backupCount=logfile_max_count)
    except Exception as exception:
        print("Failed to set up log file: %s" % str(exception))
        raise

    try:
        logfile_handler.setLevel(logfile_log_level.upper())
    except Exception:
        print("Failed to set log file log level: invalid level: '%s'" % logfile_log_level)
        raise

    logfile_formatter = LogFormatter(fmt=log_line_template, color=logfile_log_color, mask=logfile_log_mask)
    logfile_handler.setFormatter(logfile_formatter)
    logger.addHandler(logfile_handler)


def get(file_name):
    return logging.getLogger(os.path.basename(os.path.splitext(file_name)[0]))
