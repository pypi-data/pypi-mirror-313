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

"""opentf-ctl reports generating part"""

from typing import Any, Dict, List, Tuple

import os
import sys
import time

from opentf.tools.ctlcommons import (
    _ensure_options,
    _ensure_uuid,
    _error,
    _fatal,
    _warning,
    _file_not_found,
    _get_arg,
    _is_command,
    _is_filename_pattern,
)
from opentf.tools.ctlconfig import read_configuration, CONFIG
from opentf.tools.ctlworkflows import _get_workflows, _get_workflow_events
from opentf.tools.ctlnetworking import _post, _insightcollector
from opentf.tools.ctlattachments import download_attachment


########################################################################
# Help messages

GENERATE_REPORT_HELP = '''Generate a report from a local Insight Collector definition file

Example:
  # Generate a HTML summary report using a local definition file
  opentf-ctl generate report 2cd3365a-6fbe-4d60-9146-b8bd6f42d1c8 using custom_definition.yaml --name=detailed-execution-report --save-to=/user/home/reports/ --as=detailed_report_007.html

Options:
  --name={...}: report name, i.e `name` property of an insight from definition file (supports Unix file patterns).
  --save-to={...}: destination path, must be a directory.
  --as={...}: file name to save the report as (overrides the report name from the definition file).
  --timeout=x or -t x: sets a timeout for report generation (in seconds, defaults to 60 seconds if not specified).

Usage:
  opentf-ctl generate report WORKFLOW_ID using definition_file [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Generate report

DEFAULT_QUERY_TIMEOUT = 60.0


def _post_insight_definition(workflow_id: str, using: str, name_pattern: str):
    try:
        files = {'insights': open(using, 'rb')}
        return _post(
            _insightcollector(),
            f'/workflows/{workflow_id}/insights?insight={name_pattern}',
            statuses=(200, 422),
            files=files,
        )
    except FileNotFoundError as err:
        _file_not_found(using, err)
    except Exception as err:
        _fatal('Cannot retrieve reports from Insight Collector: %s.', str(err))


def _get_workflow_results(
    expected: int, request_id: str, workflow_id: str, timeout: float
) -> List[Dict[str, Any]]:
    retrieved_results = 0
    workflow_results = []
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            break
        events = list(_get_workflow_events(workflow_id, watch=False))
        workflow_results = [
            event
            for event in events
            if event['kind'] == 'WorkflowResult'
            and event['metadata'].get('request_id') == request_id
        ]
        if (len(workflow_results) == 1) and (
            workflow_results[0]['metadata']['name'] == 'No insights published'
        ):
            break
        retrieved_results = len(workflow_results)
        if retrieved_results == expected:
            break
        time.sleep(CONFIG['orchestrator']['polling-delay'])
    return workflow_results


def _process_insightcollector_result(
    result: Dict[str, Any],
    workflow_id: str,
    using: str,
    name_pattern: str,
    timeout: float,
) -> List[Dict[str, Any]]:
    if result.get('code') != 200:
        _fatal(
            'Insight Collector failed to generate reports.  Error code %s, error message %s',
            result.get('code'),
            result.get('message'),
        )
    if 'details' not in result or 'expected' not in result.get('details', {}):
        _fatal(
            'Unexpected response from insightcollector.  Was expecting a JSON object with a `details.expected` entry, got: %s.',
            str(result),
        )
    details = result['details']
    if not details.get('expected'):
        _warning(
            'No expected reports can be generated for workflow %s using configuration file %s and name pattern %s.',
            workflow_id,
            using,
            name_pattern,
        )
        sys.exit(0)
    request_id = details.get('request_id')
    if not request_id:
        _fatal(
            'Unexpected response from insightcollector, request id parameter missing.'
        )
    return _get_workflow_results(
        len(details['expected']), request_id, workflow_id, timeout
    )


def _get_timeout(timeout: str) -> float:
    polling_delay = CONFIG['orchestrator']['polling-delay']
    try:
        timeout_ = float(timeout) if timeout else DEFAULT_QUERY_TIMEOUT
        if timeout_ < 0:
            raise ValueError
        if timeout_ < polling_delay:
            _warning('Timeout is lesser than polling delay (%s sec).', polling_delay)
        return timeout_
    except (ValueError, TypeError):
        _warning(
            'Timeout must be a positive integer, got %s, resetting to default value.',
            timeout,
        )
        return DEFAULT_QUERY_TIMEOUT


def _query_insightcollector(
    workflow_id: str,
    name_pattern: str,
    using: str,
    save_to: str,
    save_as: str,
    timeout: str,
) -> None:
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    timeout_ = _get_timeout(timeout)
    print(f'Generating reports (`{name_pattern}`) using `{using}` definition...')
    result = _post_insight_definition(workflow_id, using, name_pattern)
    workflow_results = _process_insightcollector_result(
        result, workflow_id, using, name_pattern, timeout_
    )
    if workflow_results:
        if not os.path.exists(save_to):
            os.makedirs(save_to)
        attachment_uuids = [
            attachment['uuid']
            for wr in workflow_results
            for attachment in wr['metadata']['attachments'].values()
        ]
        for uuid in attachment_uuids:
            download_attachment(workflow_id, uuid, save_to, save_as)
    else:
        _error('Timeout while retrieving generated reports.')
        sys.exit(1)


def _get_report_options() -> Tuple:
    return (
        _get_arg('--name=') or '*',
        _get_arg('--save-to=') or '.',
        _get_arg('--as=') or None,
        _get_arg('--timeout=') or _get_arg('-t=') or DEFAULT_QUERY_TIMEOUT,
    )


def generate_report(workflow_id: str, using: str):
    """Generate report or reports based on user-provided configuration file and name pattern."""
    name_pattern, save_to, save_as, timeout = _get_report_options()
    if not using:
        _error('Configuration file path not provided.')
        sys.exit(1)
    if save_as and _is_filename_pattern(name_pattern):
        _error(
            'Cannot download multiple reports using the same file name (`%s`).', save_as
        )
        sys.exit(1)
    if save_as and (os.sep in save_as):
        _error(
            'File name `%s` is a path. Use `--save-to` option to specify the download directory.',
            save_as,
        )
        sys.exit(1)
    if os.path.isfile(save_to):
        _error(
            'File path `%s` is a file, not a directory. Cannot download reports to a file.',
            save_to,
        )
        sys.exit(1)
    if using and not os.path.exists(using):
        _error('Configuration file `%s` not found.', using)
        sys.exit(1)
    try:
        _query_insightcollector(
            workflow_id, name_pattern, using, save_to, save_as, timeout
        )
    except Exception as err:
        _fatal(
            'Failed to generate report %s for workflow %s at %s: %s.',
            name_pattern,
            workflow_id,
            save_to,
            str(err),
        )


########################################################################
# Exposed functions


def print_generate_report_help(args: List[str]):
    """Display help."""
    if _is_command('generate report', args):
        print(GENERATE_REPORT_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def generate_report_cmd():
    """Generate insights-based reports."""
    if _is_command('generate report _', sys.argv):
        workflow_id = _ensure_options(
            'generate report _ using _',
            sys.argv[1:],
            extra=[('--name',), ('--save-to',), ('--timeout', '-t'), ('--as',)],
        )
        read_configuration()
        generate_report(workflow_id, sys.argv[5])  # type: ignore
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
