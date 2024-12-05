# Copyright 2022 Henix, henix.fr
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

"""opentf-ctl commons"""

from typing import Any, Dict, Iterable, List, NoReturn, Optional, Union

import json
import logging
import re
import sys

import yaml


########################################################################
# debug


def _error(*msg) -> None:
    logging.error(*msg)


def _fatal(*msg) -> NoReturn:
    _error(*msg)
    sys.exit(2)


def _warning(*msg) -> None:
    logging.warning(*msg)


def _debug(*msg) -> None:
    logging.debug(*msg)


def _info(*msg) -> None:
    logging.info(*msg)


########################################################################
# sys.argv processing


COMMON_OPTIONS = [
    ('--token=',),
    ('--user=',),
    ('--orchestrator=',),
    ('--context=',),
    ('--insecure-skip-tls-verify=',),
    ('--warmup-delay=',),
    ('--polling-delay=',),
    ('--max-retry=',),
    ('--opentfconfig=',),
]


def _filter_options(args: List[str], extra=(), multi=(), flags=()) -> List[str]:
    """Check options.

    # Required parameters

    - args: a list of strings

    # Optional parameters

    - extra: a collection of string collections
    - multi: a collection of string collections
    - flags: a collection of string collections

    Items in `extra` are expecting a parameter, in the form `extra=x` or
    `extra x` (for example: `--user=foo` or `--user foo`).

    Items in `multi` are expecting a parameter, in the form `extra=x` or
    `extra x` and can be repeated (for example: `--user=foo --user=bar`
    or `--user foo --user bar`).

    Items in `extra` and `multi` may end with `=`, but this is not
    mandatory, it will be implicitly added if not there.

    # Returned value

    A possibly empty list of strings, the unhandled elements in `args`.
    """

    def _consume(option):
        for item in list(options):
            if option in item:
                options.remove(item)
                for alias in item:
                    allowed.remove(alias)
                break

    def _processed(what, candidates):
        for option in candidates:
            if option[-1] == '=':
                if what.startswith(option):
                    processed[index] = None
                    return option
                if what == option[:-1]:
                    if index < max_index:
                        processed[index] = processed[index + 1] = None
                        return option
                    _error(f'Missing parameter for option {item}.')
                    sys.exit(2)
            if what == option:
                processed[index] = None
                return option
        return False

    max_index = len(args) - 1
    processed: List[Optional[str]] = list(args)
    options = [
        tuple(f'{alias.rstrip("=")}=' for alias in option)
        for option in COMMON_OPTIONS + list(extra)
    ]
    for option in flags:
        options.append(option)
    allowed = [alias for option in options for alias in option]
    multis = [f'{alias.rstrip("=")}=' for option in multi for alias in option]

    for index, item in enumerate(args):
        if processed[index] is None:
            continue
        if found := _processed(item.replace('_', '-'), allowed):
            _consume(found)
            continue
        _processed(item.replace('_', '-'), multis)

    return [arg for arg in processed if arg is not None]


def _ensure_options(
    command: str, args: List[str], extra=(), multi=(), flags=()
) -> Optional[Union[str, List[str]]]:
    """Ensure options are allowed.

    # Required parameters

    - command: a string
    - args: a list of strings

    # Optional parameters

    - extra: a collection of string collections
    - multi: a collection of string collections
    - flags: a collection of string collections

    Items in `extra` are expecting a parameter, in the form `extra=x` or
    `extra x` (for example: `--user=foo` or `--user foo`).

    Items in `multi` are expecting a parameter, in the form `extra=x` or
    `extra x` and can be repeated (for example: `--user=foo --user=bar`
    or `--user foo --user bar`).

    Items in `extra` and `multi` may end with `=`, but this is not
    mandatory, it will be implicitly added if not there.

    # Returned value

    A string, a list of string, or None.  Returns a string if `command`
    contains a `_` placeholder, the corresponding value.  Returns a list
    of strings (possibly empty) if `command` contains a `*` placeholder.
    Returns None otherwise.

    # Raised exceptions

    Raises a `SystemExit` exception if some args are missing or
    unexpected or incomplete.
    """
    unknown = _filter_options(args, extra, multi, flags)
    pattern = command.split()
    if '*' not in pattern and len(unknown) < len(pattern):
        _error(f'Missing parameter: was expecting "{command}", got "{unknown}".')
        sys.exit(2)
    if '*' not in pattern and len(unknown) > len(pattern):
        unexpected = ' '.join(unknown)
        _error(
            f'Unexpected or duplicate parameters: was expecting "{command}", got "{unexpected}".'
        )
        sys.exit(2)
    if '_' in pattern:
        return unknown[pattern.index('_')]
    if '*' in pattern:
        return unknown[pattern.index('*') :]
    return None


def _is_command(command: str, args: List[str]) -> bool:
    """Check if args matches command.

    `_` are placeholders for one item, `*` for zero to n items.

    # Examples

    ```text
    _is_command('get job _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('get   job  _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('GET JOB _', ['', 'get', 'job', 'foo'])  -> False
    _is_command('del job *', ['', 'del', 'job', 'foo'])  -> True
    _is_command('del job *', ['', 'del', 'job'])  -> True
    _is_command('del job *', ['', 'del', 'job', 'foo', 'bar'])  -> True
    ```

    # Required parameters

    - command: a string
    - args: a list of strings

    # Returned value

    A boolean.
    """
    args = _filter_options(args[1:])
    pattern = command.split()
    if pattern and pattern[-1] == '*':
        pattern = pattern[:-1]
    pattern_length = len(pattern)
    maybe_missing = pattern_length == len(args) + 1 and pattern[-1] == '_'
    if pattern_length >= 1 + len(args) and not maybe_missing:
        return False
    for pos, item in enumerate(pattern, start=0):
        if maybe_missing and pos == pattern_length - 1:
            _error(
                f'Missing required parameter.  Use "{" ".join(pattern[:-1])} --help" for details.'
            )
            sys.exit(1)
        if item not in ('_', args[pos]):
            return False
    return True


def _get_arg(prefix: str) -> Optional[str]:
    """Get value from sys.argv.

    `prefix` is a command line option prefix, such as `--foo=`.  It
    should not contain '_' symbols.

    The first found corresponding command line option is returned.

    The comparaison replaces '_' with '-' in the command line options.

    # Examples

    ```text
    _get_arg('--foo_bar=') -> baz if sys.argv contains `--foo-bar=baz`
                                or `--foo_bar=baz` or `--foo-bar baz`
    _get_arg('--foo=')     -> yada if sys.argv contains `--foo yada`
                                None otherwise
    _get_arg('-o=')        -> yada if sys.argv contains `-o yada` or
                                `-o=yada`, None otherwise
    ```

    # Required parameters

    - prefix: a string

    # Returned value

    None if `prefix` is not found in `sys.argv`, the corresponding entry
    with the prefix stripped if found.
    """
    max_index = len(sys.argv) - 1
    for index, item in enumerate(sys.argv[1:], start=1):
        if prefix[-1] == '=':
            if item.replace('_', '-').startswith(prefix):
                return item[len(prefix) :]
            if item == prefix[:-1] and index < max_index:
                return sys.argv[index + 1]
    return None


def _get_args(prefix: str) -> Optional[List[str]]:
    """Get all values with prefix from sys.argv."""
    args = []
    max_index = len(sys.argv) - 1
    for index, item in enumerate(sys.argv[1:], start=1):
        if prefix[-1] == '=':
            if item.replace('_', '-').startswith(prefix):
                args.append(item[len(prefix) :])
            if item == prefix[:-1] and index < max_index:
                args.append(sys.argv[index + 1])
    return args


# csv processing


def _get_columns(wide: Iterable[str], default: Iterable[str]) -> Iterable[str]:
    """Return requested columns.

    Returns custom-columns if specified on command line.
    If not, if wide is specified on command line, returns `wide`.
    Else `default` is returned.

    Raises ValueError if command line parameters are invalid.
    """
    output = _get_arg('--output=')
    if output is None:
        output = _get_arg('-o=')
    if output == 'wide':
        return wide

    if output and output.startswith('custom-columns='):
        ccs = output[15:].split(',')
        if not all(':' in cc for cc in ccs):
            raise ValueError(
                'Invalid custom-columns specification.  Expecting a comma-separated'
                ' list of entries of form TITLE:path'
            )
        return ccs
    if _get_arg('custom-columns='):
        raise ValueError('Missing "-o" parameter (found lone "custom-columns=")')
    return default


def _get_jsonpath(data: Any, path: List[str]) -> Any:
    """Return data at path in data."""
    if not path:
        return data
    field, path = path[0], path[1:]
    if field == '*' and isinstance(data, dict):
        result = list(filter(None, (_get_jsonpath(val, path) for val in data.values())))
        if '*' in path or '*~' in path:
            return [y for x in result for y in x]
        return result
    if field == '*~' and isinstance(data, dict):
        return list(filter(None, data))
    if isinstance(data, dict):
        return _get_jsonpath(data.get(field), path)
    if field == '*' and isinstance(data, list):
        result = list(filter(None, (_get_jsonpath(val, path) for val in data)))
        if '*' in path or '*~' in path:
            return [y for x in result for y in x]
        return result
    return None


def _generate_row(manifest: Dict[str, Any], columns: Iterable[str]) -> List[str]:
    row = []
    for item in columns:
        fields = item.split(':')[1].lstrip('.').split('.')
        if '*~' in fields and fields.index('*~') != len(fields) - 1:
            _error(
                'Invalid column specification: "*~", if used, must be last in path in "%s".',
                item,
            )
            sys.exit(2)
        value = _get_jsonpath(manifest, fields)
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        elif value is None:
            value = '<none>'
        row.append(str(value))
    return row


def _emit_table(
    data: Iterable[Iterable[str]], columns: Iterable[str], file=sys.stdout
) -> None:
    """Generate table.

    `data` is an iterable.  `columns` is a columns specification
    ('title:path').

    `file` is optional, and is `sys.stdout` by default.
    """

    def _make_row(items):
        return ''.join(item.ljust(widths[idx]) for idx, item in enumerate(items))

    data = list(data)
    headers = [column.split(':')[0] for column in columns]
    widths = [len(name) + 2 for name in headers]
    for row in data:
        for idx, item in enumerate(row):
            widths[idx] = max(widths[idx], len(item) + 2)
    print(_make_row(headers).rstrip(), file=file)
    for row in data:
        print(_make_row(row).rstrip(), file=file)


def generate_output(
    data: Iterable[Dict[str, Any]],
    default: Iterable[str],
    wide: Iterable[str],
    file=sys.stdout,
):
    """Generate output.

    Uses `sys.argv` to determine output format and columns.

    # Required parameters

    - data: an iterable of dictionaries
    - default: a list of strings
    - wide: a list of strings

    # Optional parameters

    - file: a file-like object (`sys.stdout` by default)
    """
    try:
        columns = _get_columns(wide, default)
    except ValueError as err:
        _error('Invalid parameters: %s', err)
        sys.exit(2)

    output = _get_arg('--output=')
    if output is None:
        output = _get_arg('-o=')
    if output == 'yaml':
        yaml.safe_dump(data, file)
    elif output == 'json':
        json.dump(data, file, indent=2)
    else:
        _emit_table(
            (_generate_row(manifest, columns) for manifest in data), columns, file=file
        )


# misc. helpers

UUID_REGEX = r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$'
UUID_TEMPLATE = '00000000-0000-0000-0000-000000000000'
WILDCARDS = ('*', '?', '[', ']', '!')


def _ensure_uuid(parameter: str, complete: Optional[Any] = None) -> str:
    """Ensure parameter is a valid UUID.

    # Required parameters

    - parameter: a string (an UUID or the begining of one)

    # Optional parameters

    - complete: a function of no parameter or None (None by default)

    # Raised exceptions

    Abort with error code 2 if `parameter` is not a valid UUID.
    """
    if len(parameter) < len(UUID_TEMPLATE):
        if not re.match(UUID_REGEX, parameter + UUID_TEMPLATE[len(parameter) :]):
            _error(
                'Parameter %s is not a valid UUID.  UUIDs should only contains '
                'digits, dashes ("-"), and lower case letters ranging from "a" to "f".',
                parameter,
            )
            sys.exit(2)
        if complete is not None:
            ids = [item for item in complete() if item.startswith(parameter)]
            if len(ids) == 1:
                parameter = ids[0]
            elif len(ids) > 1:
                _error(
                    'Ambiguous ID prefix "%s", matches:\n- %s',
                    parameter,
                    '\n- '.join(ids),
                )
                sys.exit(2)
            else:
                _error('ID prefix "%s" matches no known ID.', parameter)
                sys.exit(2)
    if not re.match(UUID_REGEX, parameter):
        _error(
            'Parameter %s is not a valid UUID.  UUIDs should only contains '
            'digits, dashes ("-"), and lower case letters ranging from "a" to "f", '
            'and are 36 characters long.',
            parameter,
        )
        sys.exit(2)
    return parameter


def _make_params_from_selectors() -> dict:
    """
    Get selectors from command line and return parameters dictionary
    which could then be passed in a request.
    Currently supports two types of parameters:
    labelSelector and fieldSelector.
    """
    params = {}
    if label_selector := _get_arg('--selector=') or _get_arg('-l='):
        params['labelSelector'] = label_selector
    if field_selector := _get_arg('--field-selector='):
        params['fieldSelector'] = field_selector
    return params


def _ensure_either_uuids_or_selectors(
    ids: List[str], collector, default: Optional[Dict[str, Any]] = None
) -> List[str]:
    """Check query parameters.

    # Required parameters

    - ids: a list of strings, possibly empty
    - collector: a function of one parameter (an optional dictionary),
                 returning a possibly empty list of strings

    # Optional parameters

    - default: a dictionary or None (None by default)

    # Returned value

    A non-empty list of strings.
    """
    selectors = any(_get_arg(x) for x in ('--selector=', '-l=', '--field-selector='))
    if '--all' in sys.argv and selectors:
        _error('Cannot combine selectors with --all.')
        sys.exit(2)
    if ids and ('--all' in sys.argv or selectors):
        _error('Cannot combine UUIDs with selectors or --all.')
        sys.exit(2)
    if not ids and not ('--all' in sys.argv or selectors):
        _error('Missing parameters, needing either UUIDs or selectors.')
        sys.exit(2)
    if '--all' in sys.argv:
        ids = collector(default)
    elif selectors:
        ids = collector(_make_params_from_selectors())
    if not ids:
        print('Nothing to delete.')
        sys.exit(0)
    return ids


def _file_not_found(name: str, err: Any) -> NoReturn:
    _error('File not found: %s.', name)
    _debug('Error is: %s.', err)
    sys.exit(2)


def _is_filename_pattern(name: str) -> bool:
    """Check if the file name is pattern."""
    return any(wildcard in name for wildcard in WILDCARDS)
