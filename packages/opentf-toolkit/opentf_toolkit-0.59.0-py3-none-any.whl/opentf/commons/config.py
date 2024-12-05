# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for the OpenTestFactory config."""

from typing import Any, Dict, List, Optional, Tuple

import argparse
import inspect
import os

from logging.config import dictConfig

import yaml

from .schemas import validate_schema, SERVICECONFIG


########################################################################

NOTIFICATION_LOGGER_EXCLUSIONS = 'eventbus'

DEFAULT_CONTEXT = {
    'host': '127.0.0.1',
    'port': 443,
    'ssl_context': 'adhoc',
    'eventbus': {'endpoint': 'https://127.0.0.1:38368', 'token': 'invalid-token'},
}

DEBUG_LEVELS = {'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'}


########################################################################


class ConfigError(Exception):
    """Invalid configuration file."""


def make_argparser(description: str, configfile: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--descriptor', help='alternate descriptor file')
    parser.add_argument(
        '--config', help=f'alternate config file (default to {configfile})'
    )
    parser.add_argument('--context', help='alternative context')
    parser.add_argument('--host', help='alternative host')
    parser.add_argument('--port', help='alternative port')
    parser.add_argument(
        '--ssl_context', '--ssl-context', help='alternative ssl context'
    )
    parser.add_argument(
        '--trusted_authorities',
        '--trusted-authorities',
        help='alternative trusted authorities',
    )
    parser.add_argument(
        '--enable_insecure_login',
        '--enable-insecure-login',
        action='store_true',
        help='enable insecure login (disabled by default)',
    )
    parser.add_argument(
        '--insecure_bind_address',
        '--insecure-bind-address',
        help='insecure bind address (127.0.0.1 by default)',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--authorization_mode',
        '--authorization-mode',
        help='authorization mode, JWT without RBAC if unspecified',
    )
    parser.add_argument(
        '--authorization_policy_file',
        '--authorization-policy-file',
        help='authorization policies for ABAC',
    )
    parser.add_argument(
        '--token_auth_file',
        '--token-auth-file',
        help='authenticated users for ABAC and RBAC',
    )
    parser.add_argument(
        '--trustedkeys_auth_file',
        '--trustedkeys-auth-file',
        help='authenticated trusted keys for ABAC and RBAC',
    )
    return parser


def configure_logging(name: str, debug_level: str) -> None:
    logging_conf = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in {name}: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': f'ext://{os.environ.get("OPENTF_LOGGING_REDIRECT", "flask.logging.wsgi_errors_stream")}',
                'formatter': 'default',
            },
        },
        'root': {
            'level': debug_level,
            'handlers': ['wsgi'],
        },
    }
    if name not in NOTIFICATION_LOGGER_EXCLUSIONS:
        logging_conf['handlers']['eventbus'] = {
            'class': 'opentf.commons.EventbusLogger',
            'formatter': 'default',
        }
        logging_conf['root']['handlers'] += ['eventbus']
    dictConfig(logging_conf)


def _read_configfile(
    argsconfig: Optional[str], configfile: str
) -> Tuple[str, Dict[str, Any]]:
    try:
        filename = argsconfig or configfile
        with open(filename, 'r', encoding='utf-8') as cnf:
            config = yaml.safe_load(cnf)
        if not isinstance(config, dict):
            raise ValueError('Config file is not an object.')
        return filename, config
    except Exception as err:
        raise ConfigError(f'Could not get configfile "{filename}", aborting: {err}.')


def read_config(
    argsconfig: Optional[str],
    argscontext: Optional[str],
    configfile: str,
    defaultcontext,
    schema,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    if argsconfig is None and not os.path.isfile(configfile):
        if argscontext:
            raise ConfigError(
                'Cannot specify a context when using default configuration.'
            )
        context = defaultcontext or DEFAULT_CONTEXT
        config = {}
    else:
        configfile, config = _read_configfile(argsconfig, configfile)
        valid, extra = validate_schema(schema or SERVICECONFIG, config)
        if not valid:
            raise ConfigError(f'Config file "{configfile}" is invalid: {extra}.')

        context_name = argscontext or config['current-context']
        try:
            context = get_named(context_name, config['contexts'])['context']
        except ValueError as err:
            raise ConfigError(f'Could not find context "{context_name}": {err}.')
    return context, config


def read_descriptor(
    argsdescriptor: Optional[str], descriptor: Any
) -> Tuple[str, List[Dict[str, Any]]]:
    try:
        if argsdescriptor:
            filename = argsdescriptor
        else:
            for frame in inspect.stack():
                if frame.frame.f_code.co_name == '<module>':
                    break
            else:
                raise ConfigError('Could not get module location, aborting.')
            filename = os.path.join(
                os.path.dirname(frame.filename),
                descriptor or 'service.yaml',
            )
        with open(filename, 'r', encoding='utf-8') as definition:
            manifests = list(yaml.safe_load_all(definition))
        return filename, manifests
    except Exception as err:
        raise ConfigError(f'Could not get descriptor "{filename}", aborting: {err}.')


def get_named(name: str, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get an entry from a list of entries.

    # Required parameters

    - name: a string, the entry 'name'
    - entries: a list of dictionaries

    # Returned value

    A dictionary, the entry with the 'name' `name`.

    # Raised exceptions

    A _ValueError_ exception is raised if no entry is found or if more
    than one entry is found.
    """
    items = [entry for entry in entries if entry.get('name') == name]
    if not items:
        raise ValueError(f'Found no entry with name "{name}"')
    if len(items) > 1:
        raise ValueError(f'Found more than one entry with name "{name}"')
    return items.pop()


def get_debug_level(name: str) -> str:
    """Get service log level.

    Driven by environment variables.  If `{service name}_DEBUG_LEVEL` is
    defined, this value is used.  If not, if `DEBUG_LEVEL` is set, then
    it is used.  Otherwise, returns `INFO`.

    Value must be one of `CRITICAL`, `ERROR`, `WARNING`, `INFO`,
    `DEBUG`, `TRACE`, or `NOTSET`.

    # Required parameter

    - name: a string, the service name

    # Returned value

    The requested log level if in the allowed values, `INFO` otherwise.
    """
    level = os.environ.get(
        f'{name.upper()}_DEBUG_LEVEL', os.environ.get('DEBUG_LEVEL', 'INFO')
    )
    if level == 'TRACE':
        level = 'NOTSET'
    return level if level in DEBUG_LEVELS else 'INFO'
