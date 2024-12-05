# Copyright 2022-2023 Henix, henix.fr
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

"""opentf-ctl networking"""

from typing import Any, Dict, List, NoReturn, Optional

import sys

from time import sleep
from urllib.parse import urlparse

import requests

from opentf.tools.ctlcommons import _error, _fatal, _debug
from opentf.tools.ctlconfig import CONFIG, HEADERS


########################################################################


def _make_hostport(service: str) -> str:
    """Adjust server port for service.

    Handles legacy and new orchestrator config format.

    The 'legacy' format was using a 'ports' section, the new format
    is using a 'services' section.  If both sections are present,
    the 'new' format is used.
    """
    if 'orchestrator' not in CONFIG:
        _error(
            'No orchestrator defined in the context.  Please use the '
            + ' "opentf-ctl config view" command to check your configuration.'
        )
        sys.exit(1)
    if 'server' not in CONFIG['orchestrator']:
        _error(
            'No server defined for orchestrator.  Please use the '
            + ' "opentf-ctl config set-orchestrator --help" command to define'
            + ' a server in your configuration.'
        )
        sys.exit(1)
    server = CONFIG['orchestrator']['server']
    if 'ports' in CONFIG['orchestrator'] and 'services' in CONFIG['orchestrator']:
        _error(
            'The orchestrator configuration contains both a ports section and '
            + 'a services section.  It can only contains one of those.  Please '
            + 'use the "opentf-ctl config view" command to check your configuration.'
        )
        sys.exit(1)
    if 'services' in CONFIG['orchestrator']:
        svc = CONFIG['orchestrator']['services'].get(service, {})
        if 'port' in svc:
            url = urlparse(server)
            new = url._replace(netloc=url.netloc.split(':')[0] + ':' + str(svc['port']))
            server = new.geturl()
        if 'prefix' in svc:
            server = server.rstrip('/') + '/' + svc['prefix']
    elif 'ports' in CONFIG['orchestrator']:
        if port := CONFIG['orchestrator']['ports'].get(service):
            url = urlparse(server)
            new = url._replace(netloc=url.netloc.split(':')[0] + ':' + str(port))
            server = new.geturl()
    return server.strip('/')


def _receptionist() -> str:
    return _make_hostport('receptionist')


def _observer() -> str:
    return _make_hostport('observer')


def _killswitch() -> str:
    return _make_hostport('killswitch')


def _eventbus() -> str:
    return _make_hostport('eventbus')


def _agentchannel() -> str:
    return _make_hostport('agentchannel')


def _qualitygate() -> str:
    return _make_hostport('qualitygate')


def _localstore() -> str:
    return _make_hostport('localstore')


def _insightcollector() -> str:
    return _make_hostport('insightcollector')


########################################################################


def _get(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    *,
    params=None,
    statuses=(200,),
    handler=None,
    raw: bool = False,
):
    """Perform a GET request.

    # Required parameters

    - base_url: a string (the service endpoint base)

    # Optional parameters

    - path: a string ('' if not specified)
    - msg: a string or None (None by default)
    - statuses: a tuple of integers (`(200,)` by default)
    - handler: a function or None (None by default)
    - raw: a boolean (False by default)

    # Returned value

    A _Response_ object if `raw` is True, a JSON object otherwise.
    """
    if msg is None:
        msg = f'Could not query {base_url}{path}'
    retry = CONFIG['orchestrator']['max-retry']
    while True:
        try:
            what = requests.get(
                base_url + path,
                params=params,
                headers=HEADERS,
                verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
            )
            if what.status_code in statuses:
                if not raw:
                    what = what.json()
                return what
            if handler is not None:
                handler(what)
                return what
            (_error if retry else _fatal)(
                msg + ', got %d: %s.', what.status_code, what.text
            )
        except requests.exceptions.ConnectionError as err:
            _could_not_connect(base_url, err, fatal=retry == 0)
        except Exception as err:
            _fatal(msg + ': %s.', err)
        _error('Retrying...')
        sleep(CONFIG['orchestrator']['polling-delay'])
        retry -= 1


def _get_json(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    *,
    params=None,
    statuses=(200,),
    handler=None,
) -> Dict[str, Any]:
    """Perform a GET request

    # Required parameters

    - base_url: a string (the service endpoint base)

    # Optional parameters

    - path: a string ('' if not specified)
    - msg: a string or None (None by default)
    - statuses: a tuple of integers (`(200,)` by default)
    - handler: a function or None (None by default)

    # Returned value

    A dictionary.
    """
    result = _get(
        base_url,
        path,
        msg,
        statuses=statuses,
        handler=handler,
        params=params,
        raw=False,
    )
    if not isinstance(result, dict):
        _fatal(
            'Internal error, was expecting a dictionary, got a %s.', result.__class__
        )
    return result


def _get_file(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    *,
    params=None,
    statuses=(200,),
) -> requests.Response:
    """Perform a GET request.

    # Required parameters

    - base_url: a string (the service endpoint base)

    # Optional parameters

    - path: a string ('' if not specified)
    - msg: a string or None (None by default)
    - statuses: a tuple of integers (`(200,)` by default)
    - handler: a function or None (None by default)

    # Returned value

    A _Response_ object.
    """
    if msg is None:
        msg = f'Could not query {base_url}{path}'
    try:
        what = requests.get(
            base_url + path,
            params=params,
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
            stream=True,
        )
        if what.status_code not in statuses:
            _error(msg + ', got %d: %s.', what.status_code, what.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as err:
        _could_not_connect(base_url, err)
    except Exception as err:
        _fatal(msg + ': %s.', err)

    return what


def _head(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    *,
    params=None,
    statuses=(200,),
) -> requests.Response:
    """Perform a HEAD request.

    # Required parameters

    - base_url: a string (the service endpoint base)

    # Optional parameters

    - path: a string ('' if not specified)
    - msg: a string or None (None by default)
    - statuses: a tuple of integers (`(200,)` by default)
    - handler: a function or None (None by default)

    # Returned value

    A _Response_ object.
    """
    if msg is None:
        msg = f'Could not obtain headers from {base_url}{path}'
    try:
        what = requests.head(
            base_url + path,
            params=params,
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
            stream=True,
        )
        if what.status_code not in statuses:
            _error(msg + ', got %d: %s.', what.status_code, what.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as err:
        _could_not_connect(base_url, err)
    except Exception as err:
        _fatal(msg + ': %s.', err)

    return what


def _post(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    statuses=(200,),
    handler=None,
    params=None,
    files: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Post request.

    If the query status is not in `statuses`, does not return.

    If `handler` is specified, it is called with the `Response` object
    when the query status code is not in `statuses`.  It is expected not
    to return.

    # Required parameters

    - base_url: a string

    # Optional parameters

    - path: a string (an empty string by default)
    - msg: a string or None (None by default)
    - statuses: a tuple of integers (`(200,)`  by default)
    - handler: a function of arity one or None (None by default)
    - files: a dictionary or None (None by default)

    # Returned value

    A dictionary, the JSON content of the query.
    """
    if msg is None:
        msg = f'Could not post to {base_url}{path}'
    try:
        what = requests.post(
            base_url + path,
            files=files,
            headers=HEADERS,
            params=params,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if what.status_code in statuses:
            what = what.json()
        elif handler is not None:
            handler(what)
        else:
            _error(msg + ', got %d: %s.', what.status_code, what.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as err:
        _could_not_connect(base_url, err)
    except Exception as err:
        _fatal(msg + ': %s.', err)

    return what  # type: ignore


def _delete(
    base_url: str,
    path: str = '',
    msg: Optional[str] = None,
    *,
    statuses=(200,),
    handler=None,
    params=None,
):
    if msg is None:
        msg = f'Could not delete {base_url}{path}'
    try:
        what = requests.delete(
            base_url + path,
            headers=HEADERS,
            params=params,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
            timeout=30,
        )
        if what.status_code in statuses:
            what = what.json()
        elif handler is not None:
            handler(what)
        elif what.status_code == 404:
            _error(msg + ': not found.')
            sys.exit(1)
        else:
            _error(msg + ', got %d: %s.', what.status_code, what.text)
            sys.exit(1)
    except requests.exceptions.ConnectionError as err:
        _could_not_connect(base_url, err)
    except Exception as err:
        _fatal(base_url + ': %s.', err)

    return what


########################################################################


def _could_not_connect(target: str, err, fatal=True) -> NoReturn:
    if isinstance(err, requests.exceptions.ProxyError):
        _error('A proxy error occurred: %s.', str(err))
        _error(
            '(You can use the HTTP_PROXY or the HTTPS_PROXY environment variables'
            + ' to set a proxy.)'
        )
    elif isinstance(err, requests.exceptions.SSLError):
        _error('A SSL error occurred: %s.', str(err))
        _error(
            '(You can disable SSL verification by using the "--insecure-skip-tls-verify=true"'
            + ' command-line option.  **Please note that this should be for debugging'
            + ' purpose only.**)'
        )
    else:
        _error(
            'Could not reach the orchestrator (%s).  Is the orchestrator running?',
            str(err),
        )
    (_fatal if fatal else _error)('(Attempting to reach %s.)', target)


########################################################################


def _handle_maybe_outdated(response) -> NoReturn:
    if response.status_code in (404, 405):
        _error('Could not get workflows list.  Maybe an outdated orchestrator version.')
        _debug('(Return code was %d.)', response.status_code)
    else:
        _error(
            'Could not get workflows list.  Return code was %d.',
            response.status_code,
        )
    sys.exit(2)


def _get_workflows(params: Optional[Dict[str, Any]] = None) -> List[str]:
    response = _get(
        _observer(),
        '/workflows',
        'Could not get workflows list',
        handler=_handle_maybe_outdated,
        params=params,
        raw=True,
    )
    if params and not response.headers.get('X-Processed-Query'):
        _fatal(
            'The orchestrator does not support selectors, please specify explicit workflow IDs or upgrade your orchestrator.'
        )
    try:
        result = response.json()
    except Exception as err:
        _fatal('Could not get workflows list: %s.', err)
    return result['details']['items']
