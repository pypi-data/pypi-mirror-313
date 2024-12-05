# Copyright 2021-2023 Henix, henix.fr
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

"""opentf-ctl quality gate handling part"""

from typing import Any, Dict, List, Optional

import os
import sys

from opentf.tools.ctlcommons import (
    _ensure_options,
    _file_not_found,
    _is_command,
    _get_arg,
    generate_output,
    _ensure_uuid,
    _error,
    _fatal,
    _warning,
)

from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import (
    _qualitygate,
    _get_json,
    _get_workflows,
    _post,
)
from opentf.tools.ctlplugin_gitlab import dispatch_results_by_target_type

PLUGIN_OPTION = '--plugin'

########################################################################
# Help messages

GET_QUALITYGATE_HELP = '''Get quality gate status for a workflow

Examples:
  # Get the quality gate status of a workflow applying the specific quality gate from the definition file
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383 --using=my.qualitygate.yaml --mode=my.quality.gate

  # Get the quality gate status of a workflow applying the default strict quality gate (threshold=100%)
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383

  # Get the quality gate status of a workflow applying a specific quality gate showing scope and ratio only
  opentf-ctl get qualitygate a13f0572-b23b-40bc-a6eb-a12429f0143c --mode custom.quality.gate -o custom-columns=RULE_SCOPE:.rule.scope,RATIO:.rule.success_ratio

Options:
  --mode=my.quality.gate|strict|passing|... or -m=...: use the specific quality gate from the definition file
    or one of the default quality gates (strict with 100% threshold and passing with 0% threshold).
  --using=/path/to/definition.yaml: use the specific quality gate definition file.
  --plugin gitlab:param=value: GitLab plugin parameters. gitlab:server, gitlab:project and gitlab:mr are
    mandatory when using this option.
    (more at: https://opentestfactory.org/tools/running-commands.html#optional-parameters_5)
  --output=wide or -o wide: show additional information (rule threshold and scope).
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --timeout=x or -t x: set a timeout for quality gate query (in seconds)

Usage:
  opentf-ctl get qualitygate WORKFLOW_ID [--mode=mode] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DESCRIBE_QUALITYGATE_HELP = '''Get quality gate status description for a workflow

Examples:
  # Get the quality gate status description of a workflow applying the specific quality gate from the definition file
  opentf-ctl describe qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383 --using=my.qualitygate.yaml --mode=my.quality.gate

  # Get the qualitygate status description of a workflow applying the default strict quality gate (threshold=100%)
  opentf-ctl describe qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383

Options:
  --mode=my.quality.gate|strict|passing|... or -m=...: use the specific quality gate from the definition file
    or one of the default quality gates (strict with 100% threshold and passing with 0% threshold).
  --using=/path/to/definition.yaml: use the specific quality gate definition file.
  --timeout=x or -t x: set a timeout for quality gate query (in seconds)

Usage:
  opentf-ctl describe qualitygate WORKFLOW_ID [--mode=mode] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Quality gate

DEFAULT_COLUMNS = (
    'RULE:.rule.name',
    'RESULT:.rule.result',
    'TESTS_IN_SCOPE:.rule.tests_in_scope',
    'TESTS_FAILED:.rule.tests_failed',
    'TESTS_PASSED:.rule.tests_passed',
    'SUCCESS_RATIO:.rule.success_ratio',
)
WIDE_COLUMNS = (
    'RULE:.rule.name',
    'RESULT:.rule.result',
    'TESTS_IN_SCOPE:.rule.tests_in_scope',
    'TESTS_FAILED:.rule.tests_failed',
    'TESTS_PASSED:.rule.tests_passed',
    'SUCCESS_RATIO:.rule.success_ratio',
    'THRESHOLD:.rule.threshold',
    'SCOPE:.rule.scope',
)

NOTEST = 'NOTEST'
FAILURE = 'FAILURE'
RUNNING = 'RUNNING'
SUCCESS = 'SUCCESS'
INVALIDSCOPE = 'INVALID_SCOPE'


STATUS_TEMPLATES = {
    SUCCESS: 'Workflow {workflow_id} passed the quality gate `{mode}` applying the rule `{rule}`.',
    FAILURE: 'Workflow {workflow_id} failed the quality gate `{mode}` applying the rule `{rule}`.',
    NOTEST: 'Workflow {workflow_id} contains no tests matching the quality gate `{mode}` rule `{rule}`.',
    INVALIDSCOPE: 'The quality gate `{mode}` rule `{rule}` scope `{scope}` is invalid.',
}

DEFAULT_QUERY_TIMEOUT = 8

########################################################################
# Helpers


def _describe_qualitygate(workflow_id: str, mode: str, status: Dict[str, Any]) -> None:
    """Get quality gate results for a workflow in a pretty form."""
    for rule, data in status.items():
        if data['result'] not in (SUCCESS, NOTEST, FAILURE, INVALIDSCOPE):
            _error(
                f'Unexpected quality gate result when applying rule `{rule}`: {data["result"]} (was expecting {", ".join(STATUS_TEMPLATES)}).'
            )
            continue
        print(f'\n--------RESULTS: {mode}, {rule}--------\n')
        print(
            _make_qualitygate_status_message(
                data['result'], workflow_id, mode, rule, data.get('scope')
            )
        )
        if data['result'] in (SUCCESS, FAILURE):
            print('\n    --------STATISTICS--------\n')
            print(f'    Tests in scope: {data["tests_in_scope"]}')
            print(f'    Tests failed:   {data["tests_failed"]}')
            print(f'    Tests passed:   {data["tests_passed"]}')
            print(f'    Success ratio:  {data["success_ratio"]}')
            print(f'    Threshold:      {data["threshold"]}')


def _make_qualitygate_status_message(
    status: str, workflow_id: str, mode: str, rule: str, scope: Optional[str]
) -> str:
    return STATUS_TEMPLATES[status].format(
        workflow_id=workflow_id, mode=mode, rule=rule, scope=scope
    )


def _process_qualitygate_result(
    result: Dict[str, Any], workflow_id: str
) -> Dict[str, Any]:
    code = result.get('code')
    if code == 202:
        print(
            f'Workflow {workflow_id} events caching still in progress. Please retry later.'
        )
        sys.exit(101)
    if code == 404:
        _fatal(
            'Unknown workflow %s.  It is either too new, too old, or the provided '
            + 'workflow ID is incorrect.  You can use "opentf-ctl get workflows" to list '
            + 'the known workflow IDs.',
            workflow_id,
        )
    if code == 422:
        _fatal(result.get('message'))
    if 'details' not in result or 'status' not in result.get('details', {}):
        _fatal(
            'Unexpected response from qualitygate.  Was expecting a JSON object'
            + ' with a .details.status entry, got: %s.',
            str(result),
        )

    return result['details']


def _print_final_status(workflow_id, mode, status):
    if status == FAILURE:
        print(f'Workflow {workflow_id} failed the quality gate using mode {mode}.')
        sys.exit(102)
    if status == SUCCESS:
        print(f'Workflow {workflow_id} passed the quality gate using mode {mode}.')
    if status == NOTEST:
        print(f'Workflow {workflow_id} contains no test matching quality gate scopes.')


def _get_qualitygate_status(
    workflow_id: str, mode: str, timeout: int
) -> Dict[str, Any]:
    return _get_json(
        _qualitygate(),
        f'/workflows/{workflow_id}/qualitygate?mode={mode}',
        statuses=(200, 202, 404, 422),
        params={'timeout': timeout},
    )


def _post_qualitygate_definition(workflow_id: str, using: str, mode: str, timeout: int):
    try:
        files = {'qualitygates': open(using, 'rb')}
        return _post(
            _qualitygate(),
            f'/workflows/{workflow_id}/qualitygate?mode={mode}',
            statuses=(200, 202, 404, 422),
            files=files,
            params={'timeout': timeout},
        )
    except FileNotFoundError as err:
        _file_not_found(using, err)
    except Exception as err:
        _fatal(f'Exception while handling quality gate definition file: {err}')


def _query_qualitygate(
    workflow_id: str, using: Optional[str], mode: str, timeout: int
) -> Dict[str, Any]:
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    if using:
        result = _post_qualitygate_definition(workflow_id, using, mode, timeout)
    else:
        result = _get_qualitygate_status(workflow_id, mode, timeout)
    return _process_qualitygate_result(result, workflow_id)


def _warn_if_empty_gl_params(params: Dict[str, str]) -> None:
    for name, value in params.items():
        if not value:
            _warning('The command-line option `gitlab:%s` value is empty.', name)


def _add_gl_params(args: List[str]) -> Dict:
    params = {}
    process = False
    for option in args:
        if option == PLUGIN_OPTION:
            process = True
            continue
        if option.startswith(f'{PLUGIN_OPTION}='):
            process = True
            option = option[len(PLUGIN_OPTION) + 1 :]
        if process:
            process = False
            if '=' in option:
                name, _, value = option.partition('=')
                if name.startswith('gitlab:'):
                    params[name[7:].replace('-', '_')] = value
    _warn_if_empty_gl_params(params)
    return params


def get_qualitygate(
    workflow_id: str,
    mode: str,
    describe: bool = False,
    using: Optional[str] = None,
    timeout: Optional[str] = None,
) -> None:
    """Get qualitygate status.

    # Required parameter

    - workflow_id: a non-empty string (an UUID)
    - mode: a string

    # Optional parameters

    - describe: a boolean (default: False)
    - using: a string (default: None)

    # Raised exceptions

    Abort with an error code of 2 if the specified `workflow_id` is
    invalid or if an error occurred while contacting the orchestrator.

    Abort with an error code of 101 if the workflow is still running.

    Abort with an error code of 102 if the quality gate failed.
    """
    try:
        timeout_ = int(timeout) if timeout else DEFAULT_QUERY_TIMEOUT
        if timeout_ < 0:
            raise ValueError
    except (ValueError, TypeError):
        _warning(
            'Timeout must be a positive integer, got %s, resetting to default value.',
            timeout,
        )
        timeout_ = DEFAULT_QUERY_TIMEOUT
    response = _query_qualitygate(workflow_id, using, mode, timeout_)
    status = response['status']
    if status not in (NOTEST, FAILURE, RUNNING, SUCCESS, INVALIDSCOPE):
        _fatal(
            f'Unexpected workflow status from qualitygate service: %s (was expecting one of RUNNING, {", ".join(STATUS_TEMPLATES)}).',
            status,
        )
    if status == RUNNING:
        print(
            f'Workflow {workflow_id} is still running.  Please retry after workflow completion.'
        )
        sys.exit(101)

    for msg in response.get('warnings', []):
        _warning(msg)

    data = []
    if (rules := response.get('rules')) is not None:
        for rule_name, rule in rules.items():
            if rule['result'] == INVALIDSCOPE:
                _error(f'Error in rule `{rule_name}`. {rule["message"]}')

        if describe:
            _describe_qualitygate(workflow_id, mode, rules)
        else:
            data = [
                {'rule': {'name': name, **definition}}
                for name, definition in rules.items()
            ]
            generate_output(data, DEFAULT_COLUMNS, WIDE_COLUMNS)

    if gl_params := _add_gl_params(sys.argv[1:]):
        if not gl_params.get('server'):
            gl_params['server'] = os.environ.get('CI_SERVER_URL')
        if not gl_params.get('project'):
            gl_params['project'] = os.environ.get('CI_MERGE_REQUEST_PROJECT_ID')
        if (not gl_params.get('mr')) and (not gl_params.get('issue')):
            gl_params['mr'] = os.environ.get('CI_MERGE_REQUEST_IID')
        print('Publishing results to GitLab...')
        dispatch_results_by_target_type(gl_params, mode, response)

    _print_final_status(workflow_id, mode, status)


########################################################################
# Exposed functions


def print_qualitygate_help(args: List[str]):
    """Display help."""
    if _is_command('get qualitygate', args):
        print(GET_QUALITYGATE_HELP)
    elif _is_command('describe qualitygate', args):
        print(DESCRIBE_QUALITYGATE_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def qualitygate_cmd():
    """Interact with qualitygate."""
    if _is_command('get qualitygate _', sys.argv):
        workflow_id = _ensure_options(
            'get qualitygate _',
            sys.argv[1:],
            extra=[
                ('--mode', '-m'),
                ('--output', '-o'),
                ('--using', '-u'),
                ('--timeout', '-t'),
            ],
            multi=[(PLUGIN_OPTION,)],
        )
        read_configuration()
        get_qualitygate(
            workflow_id,
            _get_arg('--mode=') or _get_arg('-m=') or 'strict',
            False,
            _get_arg('--using=') or _get_arg('-u='),
            _get_arg('--timeout=') or _get_arg('-t='),
        )
    elif _is_command('describe qualitygate _', sys.argv):
        workflow_id = _ensure_options(
            'describe qualitygate _',
            sys.argv[1:],
            extra=[('--mode', '-m'), ('--using', '-u'), ('--timeout', '-t')],
        )
        read_configuration()
        get_qualitygate(
            workflow_id,
            _get_arg('--mode=') or _get_arg('-m=') or 'strict',
            True,
            _get_arg('--using=') or _get_arg('-u='),
            _get_arg('--timeout=') or _get_arg('-t='),
        )
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
