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

"""Helpers for the OpenTestFactory authn/authz config."""

from typing import Any, Dict, Iterable, List, Optional, Set

import csv
import json
import logging
import os
import re

from .config import ConfigError
from .schemas import validate_schema


########################################################################

POLICY = 'abac.opentestfactory.org/v1alpha1/Policy'

READONLY_VERBS = ('get', 'watch', 'list')
READWRITE_VERBS = ('create', 'delete', 'update', 'patch')

NAMESPACE = r'\s*(\*|([a-zA-Z0-9][a-zA-Z0-9-]*))\s*'
NAMESPACES_PATTERN = re.compile(rf'^{NAMESPACE}(,{NAMESPACE})*$')


########################################################################
# Config files helpers


def _read_key_files(items: Iterable[str], context: Dict[str, Any]) -> None:
    """Read a series of key files.

    Keys are loaded and stored in the context's `trusted_keys` entry as
    a list of `(key value, list of namespaces)` tuples.

    Uses `context['authorization_trustedkeys']` to map keys to
    namespaces (assuming `default` for keys not present in the
    aforementioned entry).

    # Required parameters

    - items: an iterable of strings
    - context: a dictionary

    Items are either fully-qualified file names or fully-qualified
    directory name ending with '/*'.

    For example:

    - `/etc/opentf/a_public_key`
    - `/etc/opentf/dept_a/*`
    - `/etc/opentf/another_public_key`
    - `/etc/opentf/dept_b/*`

    # Raised exceptions

    Raises _ConfigError_ if no key is found.
    """
    files = []
    for item in items:
        if item.endswith('/*'):
            files += [
                f'{item[:-1]}{file}'
                for file in os.listdir(item[:-2])
                if not file.startswith('.')
            ]
        else:
            files.append(item)
    auths = {}
    for auth in context.get('authorization_trustedkeys', []):
        if len(auth) >= 4:
            auths[auth[0]] = list(map(str.strip, auth[3].split(',')))
    keys = []
    summary_keys = []
    found_files = []
    for i, keyfile in enumerate(files):
        try:
            with open(keyfile, 'r', encoding='utf-8') as key:
                description = f'trusted key #{i} ({keyfile})'
                namespaces = auths.get(keyfile, ['default'])
                logging.debug('Reading %s', description)
                keys.append((key.read(), namespaces))
                summary_keys.append((description, namespaces))
                found_files.append(keyfile)
        except Exception as err:
            logging.error(
                'Error while reading trusted key #%d (%s), skipping:', i, keyfile
            )
            logging.error(err)

    if not keys:
        raise ConfigError(
            f'Could not find at least one valid trusted key among {files}, aborting.'
        )

    for auth in context.get('authorization_trustedkeys', []):
        if auth[0] not in found_files:
            logging.error(
                'Could not find key "%s" specified in trusted keys authorization file among trusted keys %s, skipping.',
                auth[0],
                str(files),
            )

    logging.debug('Trusted keys/namespaces mapping: %s', summary_keys)
    context['trusted_keys'] = keys


def _read_authorization_policy_file(file: str, context: Dict[str, Any]) -> None:
    """Read ABAC authorization policy file.

    Policy file is a JSONL file, of form:

    ```json
    {"apiVersion": "abac.opentestfactory.org/v1alpha1", "kind": "Policy", "spec": {"user": "alice", "namespace": "*", "resource": "*", "apiGroup": "*"}}
    ...
    ```

    # Required parameters

    - file: a string
    - context: a dictionary

    # Returned value

    None.  Fills the `context['authorization_policies']` entry with JSON
    policies (dictionaries).

    # Raised exceptions

    Raises _ConfigError_ if the specified file is not a JSONL file.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Authorization policy file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            authorization_policies = []
            for l in f.read().splitlines():
                if l.strip() and not l.strip().startswith('#'):
                    try:
                        policy = json.loads(l)
                        valid, extra = validate_schema(POLICY, policy)
                        if not valid:
                            raise ConfigError(
                                f'Invalid policy {policy} in file "{file}": {extra}.'
                            )
                        authorization_policies.append(policy)
                    except json.decoder.JSONDecodeError as err:
                        raise ConfigError(
                            f'Invalid JSON entry "{l}" in policy file "{file}": {err}.'
                        )
        context['authorization_policies'] = authorization_policies
    except ConfigError:
        raise
    except Exception as err:
        raise ConfigError(f'Could not read policy file "{file}": {err}.')


def _read_trustedkeys_auth_file(file: str, context: Dict[str, Any]) -> None:
    """Read trustedkeys file.

    Trusted keys auth file is of form:

    ```text
    key,name,"group1,group2,group3","namespace_1,namespace_2"
    ```

    The first 2 columns are required, the remaining columns are
    optional.

    # Required parameters

    - file: a string, the file name
    - context: a dictionary

    # Returned value

    None.  Fills the `context['authorization_trustedkeys'] entry with
    tuples, one per non-empty line in file.

    # Raised exceptions

    Raises _ConfigError_ if the specified token file is invalid.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Trusted keys authorization file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            authorization_trustedkeys = list(
                filter(
                    lambda entry: entry and not entry[0].startswith('#'),
                    csv.reader(f, delimiter=',', skipinitialspace=True),
                )
            )
        authorization_trustedkeys = [
            entry
            for entry in authorization_trustedkeys
            if not (len(entry) == 1 and entry[0] == '')
        ]

        if not authorization_trustedkeys:
            raise ConfigError(
                f'No entry found in trusted keys authorization file "{file}".'
            )
        for entry in authorization_trustedkeys:
            if len(entry) < 2:
                raise ConfigError(
                    f'Entries in trusted keys authorization file "{file}" must have at least 2 elements: {entry}.'
                )
            if len(entry) >= 4 and entry[3]:
                if not NAMESPACES_PATTERN.match(entry[3]):
                    raise ConfigError(
                        f'Invalid namespaces specification "{entry[3]}" in trusted keys authorization file "{file}".  Namespaces names are either "*" or formed from letters, digits, and hyphens.'
                    )
        if len(authorization_trustedkeys) != len(
            set(x[0] for x in authorization_trustedkeys)
        ):
            raise ConfigError(
                f'Duplicated entries in trusted keys authorization file "{file}".'
            )
        context['authorization_trustedkeys'] = authorization_trustedkeys
    except ConfigError:
        raise
    except Exception as err:
        raise ConfigError(
            f'Could not read trusted keys authorization file "{file}": {err}.'
        )


def _read_token_auth_file(file: str, context: Dict[str, Any]) -> None:
    """Read token file.

    Static token file is of form:

    ```text
    token,user,uid,"group1,group2,group3"
    ```

    The first 3 columns are required, the remaining columns are
    optional.

    # Required parameters

    - file: a string, the file name
    - context: a dictionary

    # Returned value

    Fills the `context['authorization_tokens']` entry with one list per
    line in file.

    The list contains the token, the user name, the user ID and, if
    present, the groups.

    # Raised exceptions

    Raises _ConfigError_ if the specified token file is invalid.
    """
    if not os.path.exists(file):
        raise ConfigError(f'Token authorization file "{file}" does not exist.')
    try:
        with open(file, 'r', encoding='utf-8') as f:
            authorization_tokens = list(
                filter(
                    lambda entry: entry and not entry[0].startswith('#'),
                    csv.reader(f, delimiter=',', skipinitialspace=True),
                )
            )
        authorization_tokens = [
            entry
            for entry in authorization_tokens
            if not (len(entry) == 1 and entry[0] == '')
        ]
        if not authorization_tokens:
            raise ConfigError(f'No entry found in token authorization file "{file}".')
        for entry in authorization_tokens:
            if len(entry) < 3:
                raise ConfigError(
                    f'Entries in token authorization file "{file}" must have at least 3 elements: {entry}.'
                )
            if len(entry) > 3:
                entry[3] = set(map(str.strip, entry[3].split(',')))  # type: ignore
        context['authorization_tokens'] = authorization_tokens
    except ConfigError:
        raise
    except Exception as err:
        raise ConfigError(f'Could not read token authorization file "{file}": {err}.')


########################################################################
# request authorizers helpers

USERIDS_RULES_CACHE: Dict[str, List[Any]] = {}
USERIDS_NAMESPACES_CACHE: Dict[str, Set[str]] = {}


def _in_group(user_id: str, group: Optional[str], context: Dict[str, Any]) -> bool:
    """Check if user is in group.

    Group membership is defined in token authorization file.

    # Required parameters

    - user_id: a string
    - group: a string or None
    - context: a dictionary

    # Returned value

    A boolean.  True if the user ID is in the group, False otherwise.
    If `group` is None, returns False.
    """
    tokens = context.get('authorization_tokens')
    if group is not None and tokens is not None:
        for entry in tokens:
            if entry[2] == user_id and len(entry) > 3:
                return group in entry[3]
    return False


def _cache_userid_rules(user_id: str, context: Dict[str, Any]) -> None:
    USERIDS_RULES_CACHE[user_id] = [
        policy['spec']
        for policy in context['authorization_policies']
        if policy['spec'].get('user') == user_id
        or _in_group(user_id, policy['spec'].get('group'), context)
    ]


def _cache_userid_namespaces(user_id: str) -> None:
    USERIDS_NAMESPACES_CACHE[user_id] = {
        rule['namespace']
        for rule in USERIDS_RULES_CACHE[user_id]
        if 'namespace' in rule
    }


def _rule_gives_permission(
    rule: Dict[str, Any],
    namespace: str,
    resource: Optional[str] = None,
    verb: Optional[str] = None,
) -> bool:
    """Check access in namespace."""
    if rule['namespace'] in ('*', namespace) and rule['resource'] in (
        resource,
        '*',
    ):
        if verb in READONLY_VERBS and rule.get('readonly'):
            return True
        if not rule.get('readonly'):
            return True
    return False


########################################################################


def is_user_authorized(
    user_id: str, resource: str, verb: str, context: Dict[str, Any]
) -> bool:
    """Check if resource access is authorized, disregarding namespace.

    # Required parameters

    - user_id: a string
    - resources: a string
    - verb: a string
    - context: a dictionary

    # Returned value

    True if `user` is allowed to access resource, False otherwise.
    """
    if user_id not in USERIDS_RULES_CACHE:
        _cache_userid_rules(user_id, context)

    return any(
        verb in READONLY_VERBS if rule.get('readonly') else True
        for rule in USERIDS_RULES_CACHE[user_id]
        if rule['resource'] in (resource, '*')
    )


def get_user_accessible_namespaces(
    user_id: str,
    context: Dict[str, Any],
    resource: Optional[str] = None,
    verb: Optional[str] = None,
) -> List[str]:
    """Check access granted by rules.

    # Required parameters

    - user_id: a string
    - context: a dictionary

    # Optional parameters

    - resource: a string or None (None by default)
    - verb: a string or None (None by default)

    # Returned value

    A list of namespaces or `['*']`.

    If `resource` and `verb` are not specified, returns the list of
    namespaces for which the user has access to at least one resource
    type.
    """
    if user_id not in USERIDS_RULES_CACHE:
        _cache_userid_rules(user_id, context)
    if user_id not in USERIDS_NAMESPACES_CACHE:
        _cache_userid_namespaces(user_id)

    if resource and verb:
        namespaces = {
            namespace
            for namespace in USERIDS_NAMESPACES_CACHE[user_id]
            for rule in USERIDS_RULES_CACHE[user_id]
            if _rule_gives_permission(rule, namespace, resource, verb)
        }
    else:
        namespaces = USERIDS_NAMESPACES_CACHE[user_id]

    return ['*'] if '*' in namespaces else list(namespaces)


def initialize_authn_authz(args, context: Dict[str, Any]) -> None:
    """Initialize authn & authz

    Handles the following service parameters:

    - `--trusted-authorities`
    - `--enable-insecure-login`
    - `--insecure-bind-address`
    - `--authorization-mode` (ABAC, RBAC, JWT)

    The `context` is updated accordingly.

    # Required parameters

    - args: an argparse result
    - context: a dictionary
    """
    abac = rbac = False
    if args.trusted_authorities:
        context['trusted_authorities'] = [
            ta.strip() for ta in args.trusted_authorities.split(',')
        ]
    if args.authorization_mode:
        context['authorization_mode'] = [
            am.strip() for am in args.authorization_mode.split(',')
        ]
        abac = 'ABAC' in context['authorization_mode']
        rbac = 'RBAC' in context['authorization_mode']
        if abac and rbac:
            raise ConfigError(
                'Cannot specify both ABAC and RBAC as authorization mode.'
            )
        if abac:
            if not args.authorization_policy_file:
                raise ConfigError('ABAC requires an authorization policy file.')
            if not args.token_auth_file:
                raise ConfigError('ABAC requires a token authentication file.')
            _read_authorization_policy_file(args.authorization_policy_file, context)
            _read_token_auth_file(args.token_auth_file, context)

        if rbac:
            raise ConfigError('RBAC not supported yet.')

    if args.enable_insecure_login:
        context['enable_insecure_login'] = True
    if 'enable_insecure_login' not in context:
        context['enable_insecure_login'] = False
    if 'insecure_bind_address' not in context:
        context['insecure_bind_address'] = args.insecure_bind_address
    if args.trustedkeys_auth_file:
        _read_trustedkeys_auth_file(args.trustedkeys_auth_file, context)
    _read_key_files(context.get('trusted_authorities', []), context)
