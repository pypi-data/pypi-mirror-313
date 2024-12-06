# SPDX-License-Identifier: MIT
''' BEGIN FILE DOCUMENTATION (level: 3)
# Constants

In the `docthing.constants` module, you will find the constants used in the
docthing project.

Here will be defined all the _default configuration values_ that can be
overridden by the user, as well as the default configuration file containing
the default values for the `parser` for the most common languages. For obvious
reasons, this can't be an exhaustive list, but it will be updated as new
languages are added to the project.

If a language is not supported, this does not mean that `docthing` will not
work with it. It simply means that the default configuration file for that
language is not available and the user will have to provide their own.

## Prederined Variables

In this file a list of `PREDEFINED_VARIABLES` is defined. These variables
are used to define the default values for the configuration file. Since these
variables changes their value based on the user usage of the tool, they are
actually function implementations that are called when the configuration
file is parsed.
END FILE DOCUMENTATION '''

import os

# C like commented languages extensions
_c_like_languages_parser_config = {
    'begin_ml_comment': '/*',
    'end_ml_comment': '*/',
    'allow_sl_comments': False,
    'sl_comment': '//',
}

# Constants for defaults
DEFAULT_CONFIG_FILE = 'docthing.conf'
DEFAULT_OUTPUT_DIR = 'documentation'
DEFAULT_CONFIG = {
    'main': {
        'meta': 'plantuml'
    },
    'output': {
        'dir': os.path.join('{index-file-dir}', 'documentation'),
        'type': 'markdown'
    },
    'parser': {
        'begin_doc': 'BEGIN FILE DOCUMENTATION',
        'end_doc': 'END FILE DOCUMENTATION',
        'doc_level': '1',
        'allow_sl_comments': False,
        'peek_lines': 1,
        'py': {                                    # Python
            'begin_ml_comment': "'''",
            'end_ml_comment': "'''",
            'allow_sl_comments': False,
            'sl_comment': '#',
        },
        'c': _c_like_languages_parser_config,      # C/C++ source
        'cc': _c_like_languages_parser_config,     # C/C++ source,
        'cpp': _c_like_languages_parser_config,    # C/C++ source
        'h': _c_like_languages_parser_config,      # C/C++ header
        'hh': _c_like_languages_parser_config,     # C/C++ source,
        'hpp': _c_like_languages_parser_config,    # C/C++ header
        'cpp': _c_like_languages_parser_config,    # C/C++ source,
        'cxx': _c_like_languages_parser_config,    # C/C++ source,
        'hxx': _c_like_languages_parser_config,    # C/C++ source,
        'cppm': _c_like_languages_parser_config,   # C/C++ source,
        'ixx': _c_like_languages_parser_config,    # C/C++ source
        'java': _c_like_languages_parser_config,   # Java
        'cs': _c_like_languages_parser_config,     # C#
        'js': _c_like_languages_parser_config,     # JavaScript
        'cjs': _c_like_languages_parser_config,    # JavaScript (commonjs)
        'mjs': _c_like_languages_parser_config,    # JavaScript (module)
        'ts': _c_like_languages_parser_config,     # TypeScript
        'cts': _c_like_languages_parser_config,    # TypeScript (commonjs)
        'mts': _c_like_languages_parser_config,    # TypeScript (module)
        'jsx': _c_like_languages_parser_config,    # React and React Native JavaScript
        'tsx': _c_like_languages_parser_config,    # React and React Native TypeScript
        'jl': {                                    # Julia
            'begin_ml_comment': '#=',
            'end_ml_comment': '=#',
            'allow_sl_comments': False,
            'sl_comment': '#',
        },
        'rs': _c_like_languages_parser_config,     # Rust
        'rlib': _c_like_languages_parser_config,   # Rust library
        'sh': {                                    # Julia
            'begin_ml_comment': '#',
            'end_ml_comment': '#',
            'allow_sl_comments': True,
            'sl_comment': '#',
        },

        # TODO: add more default configuration options for most common
        # languages here
    },
}

SUPPORTED_PLUGIN_TYPES = ['exporter', 'meta-interpreter']


def index_file_dir(config):
    '''
    Determine the directory containing the index file based on the configuration.

    If the `main` section or `index_file` option is not defined in the configuration,
    a default value of `{index-file-dir}` is returned.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            str: The absolute path to the directory containing the index file.
    '''
    if 'main' not in config:
        print('Warning: using variable index-file-dir before defining `main` section in config file')
        return '{index-file-dir}'
    if 'index_file' not in config['main']:
        print('Warning: using variable index-file-dir before defining `index_file` in `main` section in config file')
        return '{index-file-dir}'
    res = os.path.abspath(os.path.dirname(config['main']['index_file']))
    return res if res else os.path.join('.', '')


PREDEFINED_VARIABLES = {
    'index-file-dir': index_file_dir
}
