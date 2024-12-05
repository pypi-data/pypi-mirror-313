# Copyright (c) 2024 Henix, Henix.fr
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

"""opentf-ctl datasources handling part"""

from typing import Any, Dict, List

import sys
import time

from opentf.tools.ctlcommons import (
    _debug,
    _is_command,
    _error,
    _ensure_options,
    _ensure_uuid,
    _fatal,
    generate_output,
    _get_arg,
    _make_params_from_selectors,
    _warning,
)
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import _observer, _get
from opentf.tools.ctlworkflows import _get_workflows

#######################################################################
# Help messages

GET_DATASOURCES_HELP = '''Get workflow data source

Example:
  # Get workflow test cases data source
  opentf-ctl get datasource b0dcc5e2-c905-4608-9177-7ea7e50827e0 --kind=testcases

Options:
  --kind=kind or -k kind: get data source of specified kind (mandatory)
  --output=format or -o format: show information in specified format (json or yaml).
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --output=wide or -o wide: show additional information (environment tags and job name).
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)
  --timeout=x or -t x: set a timeout for data source query (in seconds)

Usage:
  opentf-ctl get datasource WORKFLOW_ID --kind=kind [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

#######################################################################
# Constants

TESTCASES = 'testcases'
JOBS = 'jobs'
TAGS = 'tags'

COLUMN_NAME = 'NAME:.metadata.name'
COLUMN_SUCCESS = 'SUCCESS:.status.testCaseStatusSummary.success'
COLUMN_FAILURE = 'FAILURE:.status.testCaseStatusSummary.failure'
COLUMN_ERROR = 'ERROR:.status.testCaseStatusSummary.error'
COLUMN_SKIPPED = 'SKIPPED:.status.testCaseStatusSummary.skipped'
COLUMN_TOTAL = 'TOTAL:.status.testCaseCount'


DEFAULT_COLUMNS_TESTCASES = (
    COLUMN_NAME,
    'TECHNOLOGY:.test.technology',
    'OUTCOME:.test.outcome',
    'EXECUTION TIME:.execution.duration',
)

WIDE_COLUMNS_TESTCASES = (
    COLUMN_NAME,
    'TECHNOLOGY:.test.technology',
    'OUTCOME:.test.outcome',
    'EXECUTION TIME:.execution.duration',
    'RUNS-ON:.test.runs-on',
    'JOB:.test.job',
)

DEFAULT_COLUMNS_JOBS = (
    COLUMN_NAME,
    COLUMN_SUCCESS,
    COLUMN_FAILURE,
    COLUMN_TOTAL,
)

WIDE_COLUMNS_JOBS = (
    COLUMN_NAME,
    COLUMN_SUCCESS,
    COLUMN_FAILURE,
    COLUMN_ERROR,
    COLUMN_SKIPPED,
    COLUMN_TOTAL,
    'RUNS-ON:.spec.runs-on',
)

DEFAULT_COLUMNS_TAGS = (
    COLUMN_NAME,
    COLUMN_SUCCESS,
    COLUMN_FAILURE,
    COLUMN_TOTAL,
)

WIDE_COLUMNS_TAGS = (
    COLUMN_NAME,
    COLUMN_SUCCESS,
    COLUMN_FAILURE,
    COLUMN_ERROR,
    COLUMN_SKIPPED,
    COLUMN_TOTAL,
)

DATASOURCES_COLUMNS = {
    TESTCASES: (DEFAULT_COLUMNS_TESTCASES, WIDE_COLUMNS_TESTCASES),
    JOBS: (DEFAULT_COLUMNS_JOBS, WIDE_COLUMNS_JOBS),
    TAGS: (DEFAULT_COLUMNS_TAGS, WIDE_COLUMNS_TAGS),
}


#######################################################################
DATASOURCES_TIMEOUT = 8
DATASOURCES_WAIT = 1


def _query_observer_datasources(
    workflow_id: str, datasources_kind: str, timeout: int
) -> List[Dict[str, Any]]:
    url = f'/workflows/{workflow_id}/datasources/{datasources_kind}'
    start_time = time.time()
    while True:
        response = _get(
            _observer(),
            url,
            'Could not get datasources.',
            params=_make_params_from_selectors(),
            statuses=(200, 202, 204, 404, 422),
            raw=True,
        )
        if response.status_code == 202:
            if time.time() - start_time > timeout:
                print(f'Datasource events caching timeout ({timeout} sec), aborting.')
                sys.exit(101)
            time.sleep(DATASOURCES_WAIT)
            continue
        if not response.json()['details'] or not response.json()['details'].get(
            'items'
        ):
            msg = response.json()['message']
            if response.status_code != 200:
                _error(msg)
                sys.exit(1)
            else:
                if msg:
                    print(msg)
                    sys.exit(0)
                return []
        break

    try:
        items = response.json()['details']['items']
        while 'next' in response.links:
            next_url = url + '?' + response.links['next']['url'].partition('?')[2]
            response = _get(
                _observer(),
                next_url,
                'Could not get datasources.',
                statuses=(200, 202, 204, 404, 422),
                raw=True,
            )
            items += response.json()['details']['items']
        return items
    except ValueError as err:
        _error('Could not deserialize observer response: %s.', str(err))
        _debug(response.text)
        sys.exit(2)


def _get_timeout():
    timeout = _get_arg('--timeout=') or _get_arg('-t=')
    try:
        timeout_ = int(timeout) if timeout else DATASOURCES_TIMEOUT
        if timeout_ < 0:
            raise ValueError
        return timeout_
    except (ValueError, TypeError):
        _warning(
            'Timeout must be a positive integer, got %s, resetting to default value.',
            timeout,
        )
        return DATASOURCES_TIMEOUT


def get_datasources(workflow_id: str):
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    datasources_kind = _get_arg('--kind=') or _get_arg('-k=')
    if not datasources_kind:
        _error('No datasources kind provided.')
        sys.exit(1)
    if datasources_kind not in DATASOURCES_COLUMNS:
        _error(
            'Unknown datasource, was expecting %s.',
            ', '.join(DATASOURCES_COLUMNS.keys()),
        )
        sys.exit(1)
    timeout = _get_timeout()
    try:
        datasources = _query_observer_datasources(
            workflow_id, datasources_kind, timeout
        )
        generate_output(datasources, *DATASOURCES_COLUMNS[datasources_kind])
    except Exception as err:
        _fatal(
            'Failed to get %s datasource for workflow %s: %s.',
            datasources_kind,
            workflow_id,
            str(err),
        )


#######################################################################
# Exposed functions


def print_get_datasources_help(args: List[str]):
    """Display help."""
    if _is_command('get datasource', args):
        print(GET_DATASOURCES_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def get_datasources_cmd():
    """Get workflow datasources."""
    if _is_command('get datasource _', sys.argv):
        workflow_id = _ensure_options(
            'get datasource _',
            sys.argv[1:],
            extra=[
                ('--field-selector',),
                ('--output', '-o'),
                ('--kind', '-k'),
                ('--timeout', '-t'),
            ],
        )
        read_configuration()
        get_datasources(workflow_id)  # type: ignore
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
