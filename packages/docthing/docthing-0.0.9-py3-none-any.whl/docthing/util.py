# SPDX-License-Identifier: MIT
''' BEGIN FILE DOCUMENTATION (level: 3)
Useful development tools are provided inside the `docthing.util` module.
This module contains function that are used by docthing internally and should
**never** be used by users of docthing.
These functions are not guaranteed to be stable and may change at any time.
What is granted is that if the function signature changes, it will be
documented in the changelog. If the function is deprecated, it will be
marked as such. If the function is removed, it will be marked as deprecated
for at least one major version.
At this time the provided functions are:
- `mkdir_silent(output_dir)`: creates the specified output directory if it
doesn't already exist.
- `sha256sum(string)`: computes the SHA-256 hash of a given string.
- `get_datadir()`: returns a parent directory path where persistent application
data can be stored.
- `get_docthing_datadir()`: returns the path to the docthing data directory.
- `get_docthing_plugin_dir(plugin_type)`: returns the path to the docthing
plugin directory.
END FILE DOCUMENTATION '''

import os
import hashlib
import pathlib
import sys

from .constants import SUPPORTED_PLUGIN_TYPES

# =======================
# COMMON UTILS
# =======================


def mkdir_silent(output_dir):
    '''
    Creates the specified output directory if it doesn't already exist.

    This function checks if the given `output_dir` path exists, and if not, it creates
    the directory and any necessary parent directories using `os.makedirs()`.

    This is a utility function that can be used to ensure that an output directory is
    available before writing files to it.

        Args:
            output_dir (str): The path of the output directory to create.
    '''
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def parse_value(value_str):
    '''
    Parses a string value into a Python data type.

    This function takes a string representation of a value and attempts to convert it
    to the appropriate Python data type. It handles the following cases:

    - 'true' -> True
    - 'false' -> False
    - 'null' or 'none' -> None
    - Comma-separated list of values -> List of parsed values
    - Integer -> int
    - Float -> float
    - Otherwise, returns the original string

    This function is useful for parsing configuration values or other user-provided
    string data into the appropriate Python types.
    '''
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    elif value_str.lower() == 'null' or value_str.lower() == 'none':
        return None
    elif ',' in value_str:
        return [parse_value(item.strip()) for item in value_str.split(',')]
    try:
        return int(value_str)
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            return value_str


def sha256sum(string):
    '''
    Computes the SHA-256 hash of a given string.
    '''
    return hashlib.sha256(str.encode(string)).hexdigest()


def get_datadir() -> pathlib.Path:
    '''
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming

    ref: https://stackoverflow.com/questions/19078969/python-getting-appdata-folder-in-a-cross-platform-way
    '''
    home = pathlib.Path.home()

    if sys.platform == 'win32':
        return home / 'AppData/Roaming'
    elif sys.platform.startswith('linux'):
        return home / '.local/share'
    elif sys.platform == 'darwin':
        return home / 'Library/Application Support'


def get_docthing_datadir():
    '''
    Returns the path to the docthing data directory.
    '''
    return get_datadir() / 'docthing'


def get_docthing_plugin_dir(plugin_type=None):
    '''
    Returns the path to the docthing plugin directory.

    This directory should be used to store plugins for docthing
    inside subdirectories named after the plugin type.

    If `plugin_type` is provided the path to the subdirectory is returned.
    '''
    if plugin_type not in SUPPORTED_PLUGIN_TYPES:
        raise ValueError('Plugin type not supported.')

    res = get_docthing_datadir() / 'plugins'
    if plugin_type:
        res = res / plugin_type
    return res
