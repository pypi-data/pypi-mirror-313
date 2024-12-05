# Copyright (c) 2023-2024 Henix, Henix.fr
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

"""opentf-ctl workflow attachments handling part"""

from typing import Any, Dict, List, Optional, Tuple, Set

import fnmatch
import os
import sys

from time import sleep, time

from opentf.tools.ctlcommons import (
    _error,
    _fatal,
    _warning,
    _is_command,
    _is_filename_pattern,
    _ensure_options,
    _ensure_uuid,
    generate_output,
    _get_arg,
)
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import _observer, _localstore, _get, _get_file, _head
from opentf.tools.ctlworkflows import _get_workflows, _get_workflow_attachments_events


########################################################################
# Constants

UUID_LENGTH = 36
ATTACHMENT_PREFIX_LENGTH = len('/tmp/')
ALLURE_PREFIX_LENGTH = len('allureReporting/')


WORKERS_BUSY_WAIT_SECONDS = 5
WORKERS_MAX_WAIT_SECONDS = 60
WORKERS_IDLE_GRACE_SECONDS = 10

########################################################################
# Help messages

CP_HELP = '''Get a local copy of a workflow attachment or workflow attachments

Examples:
  # Get a local copy of a workflow attachment
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:39e68299-8995-4915-9367-1df1ff642159 /target/dir/output_file.ext

  # Get a local copy of all workflow attachments in .tar format
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:*.tar /target/dir/

  # Get a local copy of all surefire-xml typed workflow attachments
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:* /target/dir --type *surefire-xml

Options:
  --type={...} or -t {...}: get only attachments of specified type (supports Unix file patterns).

Usage:
  opentf-ctl cp WORKFLOW_ID:(ATTACHMENT_ID | file_pattern) DESTINATION [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_ATTACHMENTS_HELP = '''List workflow attachments

Examples:
  # List workflow attachments
  opentf-ctl get attachments 9ea3be45-ee90-4135-b47f-e66e4f793383

  # List workflow attachments and their source files
  opentf-ctl get attachments 9ea3be45-ee90-4135-b47f-e66e4f793383 --verbose

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information (channel OS, attachment type and creation time).
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --verbose or -v: show attachments source files (i.e., workflow Allure report source files)

Usage:
  opent-ctl get attachments WORKFLOW_ID [--output=wide] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

########################################################################
# Helpers


def _get_attachment_uuids(workflow_id: str) -> List[str]:
    attachments = _get_attachments_dict(workflow_id, True)
    return [attachment['uuid'] for attachment in attachments.values()]


def _get_options(options: List[str]) -> Tuple[str, str, str]:
    """Parse command line.

    Returns workflow_id, attachment_id or spec, destination filepath.
    """
    workflow_id, _, attachment_id = options[0].partition(':')
    if not workflow_id or not attachment_id or len(options) != 2:
        _fatal(
            'Invalid parameters. Was expecting WORKFLOW_ID:ATTACHMENT_ID DESTINATION_FILEPATH, got: %s.',
            ' '.join(options),
        )
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    if _is_filename_pattern(attachment_id):
        return (workflow_id, attachment_id, options[1])
    attachment_id = _ensure_uuid(
        attachment_id, lambda: _get_attachment_uuids(workflow_id)
    )
    return (workflow_id, attachment_id, options[1])


def _get_download_name(headers: Dict[str, Any], attachment_id: str) -> str:
    """Try to get name based on Content-Disposition header."""
    _, _, name_with_uuid = headers.get('Content-Disposition', '').partition('name=')
    if name_with_uuid.startswith(attachment_id):
        return name_with_uuid[UUID_LENGTH + 1 :]
    return 'untitled'


########################################################################
# Handle single attachment


def _get_attachment_stream(workflow_id: str, attachment_id: str):
    msg = f'Failed to get attachment {attachment_id} from localstore'
    response = _get_file(
        _localstore(),
        f'/workflows/{workflow_id}/files/{attachment_id}',
        msg=msg,
        statuses=(200, 404, 403, 500),
    )

    if response.status_code != 200:
        _fatal(
            '%s. Error code: %d, message: "%s"',
            msg,
            response.status_code,
            response.json().get('message'),
        )

    return response


def _save_attachment_stream(
    response, attachment_id: str, filepath: str, filename: Optional[str] = None
) -> None:
    """Save attachment to file or directory.

    #  Required parameters

    - response: a Response object
    - attachment_id: a string
    - filepath: a string, the file or directory path
    - filename: a string, the file name
    """
    download_name = _get_download_name(response.headers, attachment_id)
    if os.path.isdir(filepath):
        filepath += f'/{filename or download_name}'
    with open(os.path.normpath(filepath), 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(f'Attachment {download_name} ({attachment_id}) is downloaded at {filepath}.')


def download_attachment(
    workflow_id: str, attachment_id: str, filepath: str, filename: Optional[str] = None
) -> None:
    """Download attachment to filepath."""
    try:
        response = _get_attachment_stream(workflow_id, attachment_id)
        _save_attachment_stream(response, attachment_id, filepath, filename)
    except Exception as err:
        _fatal(
            'Failed to download attachment %s as %s: %s.',
            attachment_id,
            filepath,
            str(err),
        )


########################################################################
# Handle multiple attachments


def _matches_type(filetype: Optional[str], pattern: Optional[str]) -> bool:
    """Check if filetype matches pattern.

    If no pattern specified, returns True.  Otherwise, return False if
    no filetype specified.  Compare filetype with pattern.
    """
    if not pattern:
        return True
    if not filetype:
        return False
    return fnmatch.fnmatch(filetype, pattern)


def _make_target_path(data: Dict[str, Any]) -> Dict[str, str]:
    parent_step = data.get('parent_step')
    if not parent_step:
        return {'path': '', 'filename': data['filename']}
    if parent_step.get('sequence_id') in ('setup', 'teardown'):
        return {
            'path': f"./{data['job']['name']}/{parent_step['sequence_id']}",
            'filename': f"{data['metadata']['step_sequence_id']}_{data['filename']}",
        }
    return {
        'path': f"./{data['job']['name']}/{parent_step['sequence_id']}_{parent_step['testcase']}",
        'filename': data['filename'],
    }


def _get_attachments_paths(
    attachments: Dict[str, Any], name_pattern: str, type_pattern: Optional[str]
) -> Dict[str, Any]:
    result = {
        uuid: _make_target_path(data)
        for uuid, data in attachments.items()
        if fnmatch.fnmatch(data['filename'], name_pattern)
        and _matches_type(data.get('type'), type_pattern)
    }
    if not result:
        _error('No attachment matching pattern found.')
        sys.exit(1)
    return result


def download_attachments(workflow_id: str, pattern: str, filepath: str) -> None:
    """Download multiple attachments to filepath."""
    if os.path.isfile(filepath):
        _error(
            'File path `%s` is a file, not directory. Can not download multiple attachments to a file, aborting.',
            filepath,
        )
        sys.exit(1)
    attachments = _get_attachments_dict(workflow_id, False)
    attachments_paths = _get_attachments_paths(
        attachments, pattern, _get_arg('--type=') or _get_arg('-t=')
    )
    for uuid, data in attachments_paths.items():
        dir_path = os.path.normpath(f"{filepath}/{data['path']}")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        download_attachment(workflow_id, uuid, dir_path, data['filename'])


########################################################################
# Handle workflow reports download


def _handle_paths(
    filename: str, paths: Set[str], workflow_id: str, attachment_uuid: str
):
    for path in paths:
        dir_path, _, user_file = path.rpartition('/')
        dir_path = os.path.normpath(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        user_file = user_file if user_file != '.' else ''
        download_attachment(
            workflow_id, attachment_uuid, dir_path, user_file or filename
        )


def _do_download_reports(workflow_id: str, reports: Dict[str, Any]):
    sleep(WORKERS_IDLE_GRACE_SECONDS)
    msg = 'Failed to get WorkflowResult events from observer.'
    response = _get(
        _observer(),
        f'/workflows/{workflow_id}/status?fieldSelector=kind==WorkflowResult',
        msg,
    )
    if not (results := response.get('details', {}).get('items')):
        _error(msg)
        sys.exit(1)

    names_uuids = {
        name: data['uuid']
        for result in results
        for attachment, data in result['metadata']['attachments'].items()
        if (name := attachment.rsplit('_')[-1])
    }

    for report in reports:
        if report in names_uuids:
            _handle_paths(report, reports[report], workflow_id, names_uuids[report])
        else:
            _warning(
                'Report %s not found in workflow results, cannot download.', report
            )


def _get_workers_status(workflow_id: str):
    msg = 'Failed to get workers status from observer'
    response = _get(_observer(), f'/workflows/{workflow_id}/workers', msg)
    return response['details']['status']


def download_workflow_reports(workflow_id: str, reports: Dict[str, Set[str]]) -> None:
    """Download workflow reports after workers completion.

    # Required arguments
      - workflow_id: a string,
      - reports: a dictionary, report types are keys and destination paths values
    """
    if not reports:
        _error('No report to download, aborting.')
        sys.exit(1)
    print('Waiting for workflow workers teardown...')
    timeout = time() + WORKERS_MAX_WAIT_SECONDS
    while True:
        try:
            sleep(WORKERS_BUSY_WAIT_SECONDS)
            workers_status = _get_workers_status(workflow_id)
            if workers_status == 'IDLE':
                _do_download_reports(workflow_id, reports)
                break
            if time() <= timeout:
                continue
            if workers_status == 'BUSY':
                _warning(
                    'Timeout while waiting for worker completion for workflow, some reports may be missing.'
                )
                _do_download_reports(workflow_id, reports)
                break
        except Exception as err:
            _error('Internal error while downloading reports: %s.', str(err))
            break


########################################################################
# Get attachments

DEFAULT_COLUMNS = (
    'JOB_NAME:.attachment.job.name',
    'STEP:.attachment.parent_step.sequence_id',
    'UUID:.attachment.uuid',
    'FILENAME:.attachment.filename',
    'TESTCASE:.attachment.parent_step.testcase',
)

WIDE_COLUMNS = (
    'JOB_NAME:.attachment.job.name',
    'STEP:.attachment.parent_step.sequence_id',
    'UUID:.attachment.uuid',
    'FILENAME:.attachment.filename',
    'TESTCASE:.attachment.parent_step.testcase',
    'CHANNEL_OS:.attachment.job.channel_os',
    'TYPE:.attachment.type',
    'CREATED_AT:.attachment.metadata.creationTimestamp',
)

METADATA_KEYS = (
    'annotations',
    'step_id',
    'creationTimestamp',
    'name',
    'step_origin',
    'step_sequence_id',
)
JOB_KEYS = ('namespace', 'channel_os', 'channel_id', 'job_id', 'job_origin')

EventsList = List[Dict[str, Any]]


def _get_file_name(attachment: str) -> str:
    file = attachment[ATTACHMENT_PREFIX_LENGTH:]
    if 'allure' in attachment:
        return file[ALLURE_PREFIX_LENGTH + UUID_LENGTH + 1 :]
    return file.split('_', maxsplit=2)[2]


def _complete_job_and_parent_step(
    attachment: Dict[str, Any],
    parents: EventsList,
    commands: EventsList,
) -> Dict[str, Optional[str]]:
    job_id = attachment['job'].get('job_id')
    for command in commands:
        if command['metadata']['job_id'] == job_id:
            attachment['job']['name'] = command['metadata']['name']

    metadata = attachment['metadata']
    origin = metadata.get('step_origin') or [metadata['step_id']]
    parent_job = [
        job
        for parent in parents
        for name, job in parent.get('jobs', {}).items()
        for step in job.get('steps', [])
        if step.get('id') == origin[0]
        and attachment['job'].get('name') in (name, job.get('name'))
    ] or [{'steps': []}]
    for count, step in enumerate(parent_job[0]['steps'], start=1):
        if step.get('id') != origin[0]:
            continue
        parent_step = {
            'step_id': step['id'],
            'technology': step.get('uses', '').partition('/')[0],
            'testcase': step.get('with', {}).get('test', '').split('/')[-1],
            'sequence_id': count,
        }
        break
    else:
        parent_step = {
            'sequence_id': metadata.get('annotations', {})
            .get('opentestfactory.org/hooks', {})
            .get('channel')
        }
    attachment['parent_step'] = parent_step
    return attachment


def _get_uuid_and_filetype(attachment, metadata):
    if not 'allure' in attachment:
        properties = metadata.get('attachments', {}).get(attachment, {})
        return properties['uuid'], properties.get('type')
    return metadata['workflow_id'], None


def _get_attachment_data_steps(
    workflow_id: str, verbose: bool
) -> Tuple[EventsList, EventsList, EventsList]:
    events = _get_workflow_attachments_events(workflow_id, verbose)
    results = [
        event
        for event in events
        if event['kind'] in ('ExecutionResult', 'WorkflowResult')
    ]
    parents = [
        event for event in events if event['kind'] in ('Workflow', 'GeneratorResult')
    ]
    commands = [
        event
        for event in events
        if event['kind'] == 'ExecutionCommand'
        and event.get('metadata', {}).get('step_sequence_id') == -1
    ]
    return results, parents, commands


def _file_exists(attachment_id: str, workflow_id: str) -> bool:
    msg = f'Failed to fetch attachment {attachment_id} headers from localstore'
    response = _head(
        _localstore(),
        f'/workflows/{workflow_id}/files/{attachment_id}',
        msg=msg,
        statuses=(200, 404),
    )

    return response.status_code == 200


def _add_attachment_metadata(
    event: Dict[str, Any], data: Dict[str, Any]
) -> Dict[str, Any]:
    metadata = event['metadata']
    for key, value in metadata.items():
        if key in METADATA_KEYS:
            data['metadata'][key] = value
        elif key in JOB_KEYS:
            data['job'][key] = value
    data['status'] = event.get('status', 0)
    if data['status'] != 0:
        data['message'] = '\n'.join(event.get('logs', []))
    return data


def _get_attachments_dict(workflow_id: str, verbose: bool) -> Dict[str, Any]:
    results, parents, commands = _get_attachment_data_steps(workflow_id, verbose)
    attachments = {}
    for event in results:
        for attachment in event['attachments']:
            metadata = event['metadata']
            uuid, filetype = _get_uuid_and_filetype(attachment, metadata)

            data = {
                'uuid': uuid,
                'filename': _get_file_name(attachment),
                'type': filetype,
                'metadata': {},
                'job': {},
                'parent_step': {},
            }

            _add_attachment_metadata(event, data)

            if event['kind'] == 'ExecutionResult':
                _complete_job_and_parent_step(data, parents, commands)
            if data['status'] != 0 and _file_exists(uuid, workflow_id):
                data['status'] = 0
                del data['message']
            attachments[uuid] = data
    return attachments


def list_attachments(workflow_id: str, verbose: bool) -> None:
    """Get workflow attachments list."""
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    attachments = _get_attachments_dict(workflow_id, verbose)
    if verbose:
        print(
            '\n'.join(
                [
                    f"{attachment['message']}\n"
                    for attachment in attachments.values()
                    if attachment.get('message')
                ]
            )
        )
    output_data = [
        {'attachment': {'uuid': uuid, **definition}}
        for uuid, definition in attachments.items()
        if not definition.get('message')
    ]
    generate_output(output_data, DEFAULT_COLUMNS, WIDE_COLUMNS)


########################################################################
# Exposed functions


def print_attachments_help(args: List[str]):
    """Display help."""
    if _is_command('cp', args):
        print(CP_HELP)
    elif _is_command('get attachments', args):
        print(GET_ATTACHMENTS_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def attachments_cmd():
    """Interact with attachments."""
    if _is_command('cp _', sys.argv):
        options = _ensure_options('cp *', sys.argv[1:], extra=[('--type', '-t')])
        read_configuration()
        if options and _is_filename_pattern(options[0]):
            download_attachments(*_get_options(options))
        else:
            download_attachment(*_get_options(options))
    elif _is_command('get attachments _', sys.argv):
        workflow_id = _ensure_options(
            'get attachments _',
            sys.argv[1:],
            extra=[('--output', '-o')],
            flags=[('--verbose', '-v')],
        )
        read_configuration()
        list_attachments(workflow_id, '--verbose' in sys.argv or '-v' in sys.argv)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
