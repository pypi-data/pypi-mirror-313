# Copyright 2023 Henix, henix.fr
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

"""opentf-ctl get qualitygate gitlab extension"""

from typing import Any, Dict, Optional, List, Tuple

import requests

from opentf.tools.ctlcommons import _error, _warning


########################################################################
# Gitlab MR note posting

NOTEST = 'NOTEST'
FAILURE = 'FAILURE'
SUCCESS = 'SUCCESS'
INVALIDSCOPE = 'INVALID_SCOPE'

STATUSES_FORMATS = {
    NOTEST: {
        'emoji': ':no_entry_sign:',
        'msg': 'no test',
        'cats': ':no_entry_sign: :joy_cat:',
    },
    FAILURE: {
        'emoji': ':x:',
        'msg': 'failure',
        'cats': ':x: :smile_cat:',
    },
    SUCCESS: {
        'emoji': ':white_check_mark:',
        'msg': 'success',
        'cats': ':white_check_mark: :cat:',
    },
    INVALIDSCOPE: {
        'emoji': ':exclamation:',
        'msg': 'invalid scope',
        'cats': ':exclamation: :smirk_cat:',
    },
}

STATUSES_LABELS = {
    NOTEST: 'No test',
    FAILURE: 'Failed',
    SUCCESS: 'Passed',
}

NOTES_API_TEMPLATE = '/api/v4/projects/{project}/{target}/{target_id}/notes'
NOTE_HEADER_TEMPLATE = '<h2>Quality gate status for mode {mode}</h2>'

TARGET_API_TEMPLATE = '/api/v4/projects/{project}/{target}/{target_id}'

DEFAULT_TIMEOUT = 10  # HTTP requests timeout
DEFAULT_LABEL_PREFIX = 'QualityGate'

MANDATORY_PARAMETERS = ('server', 'project', 'target', 'target_id', 'keep_history')

########################################################################
# GitLab Notes APIs


def _maybe_get_noteid(
    url: str, mode: str, last_note_id: int, token: Optional[Dict[str, str]]
) -> Optional[str]:
    try:
        what = requests.get(url, params=token, timeout=DEFAULT_TIMEOUT)
        if what.status_code == 200:
            note_id = [
                note['id']
                for note in what.json()
                if (NOTE_HEADER_TEMPLATE.format(mode=mode) in note['body'])
                and (note['id'] != last_note_id)
            ]
            return note_id[0] if note_id else None
        _warning(
            'Cannot retrieve notes from Gitlab: status code %s, error %s.',
            what.status_code,
            what.json(),
        )
    except Exception as err:
        _error('Exception while retrieving notes from Gitlab: %s.', str(err))
    return None


def _post_note(
    url: str, data: Dict[str, Any], token: Optional[Dict[str, str]]
) -> Tuple[Dict[str, Any], int]:
    what = requests.post(url, data=data, params=token, timeout=DEFAULT_TIMEOUT)
    status = what.status_code
    try:
        response = what.json()
        if status != 201:
            _warning(
                'Failed to post Quality gate results: response code %d, error message: %s.',
                status,
                response,
            )
        return response, status
    except Exception:
        _error(
            'Failed to post Quality gate results: response code %d, was expecting a JSON object while querying %s, got: %s.',
            status,
            url,
            what.headers.get('Content-Type'),
        )
        return {}, status


def _delete_note(url: str, token: Optional[Dict[str, str]]) -> None:
    what = requests.delete(url, params=token, timeout=DEFAULT_TIMEOUT)
    if what.status_code not in (204, 202):
        _warning(
            'Failed to remove previous quality gate results: response code %d.',
            what.status_code,
        )


########################################################################
# GitLab Labels APIs


def _get_labels_with_prefix(
    url: str, prefix: str, token: Optional[Dict[str, str]]
) -> Optional[List[str]]:
    what = requests.get(url, params=token, timeout=DEFAULT_TIMEOUT)
    if what.status_code != 200:
        _warning(
            'Cannot retrieve labels from GitLab target: status code %d, error %s.',
            what.status_code,
            what.json(),
        )
        return None
    labels = what.json().get('labels')
    if not labels:
        return None
    return [label for label in labels if label.startswith(f'{prefix}::')]


def _add_label(url: str, label: str, token: Optional[Dict[str, str]]) -> None:
    params = {'add_labels': label}
    if token:
        params.update(token)
    what = requests.put(url, params=params, timeout=DEFAULT_TIMEOUT)
    if what.status_code != 200:
        _warning(
            'Failed to label GitLab target with `%s`: status code %d, error %s.',
            label,
            what.status_code,
            what.json(),
        )


def _remove_labels(
    url: str, labels: List[str], token: Optional[Dict[str, str]]
) -> None:
    params = {'remove_labels': ','.join(labels)}
    if token:
        params.update(token)
    what = requests.put(url, params=params, timeout=DEFAULT_TIMEOUT)
    if what.status_code != 200:
        _warning(
            'Cannot remove labels `%s` from GitLab target: status code %d, error %s.',
            ', '.join(labels),
            what.status_code,
            what.json(),
        )


########################################################################
# Formatting


def _format_qualitygate_response(
    mode: str, qualitygate: Dict[str, Any], cats: bool
) -> str:
    emoji = 'cats' if cats else 'emoji'
    status = qualitygate['status']
    formatted = NOTE_HEADER_TEMPLATE.format(mode=mode)

    if status == FAILURE:
        formatted += f'<h2>Quality gate failed {STATUSES_FORMATS[status][emoji]}</h2>'
    elif status == SUCCESS:
        formatted += f'<details><summary><h2>Quality gate passed {STATUSES_FORMATS[status][emoji]}</h2></summary>'
    elif status == NOTEST:
        formatted += f'<details><summary><h2>Quality gate not applied {STATUSES_FORMATS[status][emoji]}</h2>'
        formatted += (
            '<br>Workflow contains no test matching quality gate scopes.</summary>'
        )
    formatted += _get_rules_summary(qualitygate)
    if status in (SUCCESS, NOTEST):
        formatted += '</details>'

    warnings = list(qualitygate.get('warnings', [])) + [
        f'Rule <b>{name}</b>: {data["message"]}'
        for name, data in qualitygate['rules'].items()
        if data['result'] == INVALIDSCOPE
    ]
    if warnings:
        formatted += '<h2>Warnings :warning:</h2>'
        formatted += '<ul>'
        formatted += '\n'.join(f'<li>{msg}</li>' for msg in warnings)
        formatted += '</ul>'
    return formatted


def _get_rules_summary(qualitygate: Dict[str, Any]) -> str:
    rules_summary = '<h3>Rules summary</h3>'
    for name, data in qualitygate['rules'].items():
        status = data['result']
        result_emoji = STATUSES_FORMATS[status]['emoji']
        rules_summary += f'''{result_emoji} <b>{name.upper()}</b>: {STATUSES_FORMATS[status]['msg']}.
Tests: {data.get('tests_in_scope', 0)},
failed: {data.get('tests_failed', 0)},
passed: {data.get('tests_passed', 0)},
success ratio: {data.get('success_ratio', 'N/A')},
threshold: {data['threshold']}<br>'''
    return rules_summary


########################################################################
## Principal methods


def set_label(
    url: str, prefix: str, qg_status: str, token: Optional[Dict[str, str]]
) -> None:
    """Set label on GitLab target (MR or issue).

    Cleans labels with the specified prefix, if appropriate.

    # Required parameters

    - url: a string,
    - prefix: a string,
    - qg_status: a string
    - [token]: a dictionary of strings,
    """
    try:
        new_label = f'{prefix}::{STATUSES_LABELS[qg_status]}'
        existing_labels = _get_labels_with_prefix(url, prefix, token)
        if existing_labels == [new_label]:
            return
        if existing_labels:
            _remove_labels(url, existing_labels, token)
        _add_label(url, new_label, token)
    except Exception as err:
        _error('Error while labeling GitLab target: %s.', str(err))


def dispatch_results_by_target_type(
    gl_params: Dict[str, str], mode: str, response: Dict[str, Any]
) -> None:
    """Dispatch results depending on GitLab target type.

    Two targets are supported: merge requests and issues.

    # Required parameters

    - gl_params: a dictionary of strings,
    - mode: a string,
    - response: a dictionary
    """
    if gl_params.get('mr'):
        gl_params['target'] = 'merge_requests'
        gl_params['target_id'] = gl_params['mr']
        publish_results(gl_params, mode, response)
    if gl_params.get('issue'):
        gl_params['target'] = 'issues'
        gl_params['target_id'] = gl_params['issue']
        publish_results(gl_params, mode, response)
    if not gl_params.get('issue') and not gl_params.get('mr'):
        gl_params.update({'target': '', 'target_id': ''})
        publish_results(gl_params, mode, response)


def publish_results(
    gl_params: Dict[str, str], mode: str, qualitygate: Dict[str, Any]
) -> None:
    """Push a note to GitLab.

    `gl_params` contains:

    - 'server': CI_SERVER_URL,
    - 'project': CI_MERGE_REQUEST_PROJECT_ID,
    - 'target': `issues` or `merge_requests`,
    - 'target_id': issue_iid or merge_request_iid (CI_MERGE_REQUEST_IID)
    - 'keep_history': true or false
    - ['token'],
    - ['cats'],
    - ['label']

    # Required parameters

    - gl_params: a dictionary
    - mode: a string
    - response: a dictionary
    """
    if gl_params.get('server') and not all(
        gl_params.get(key) for key in ['target_id', 'project']
    ):
        print('Aborting publication, no MR to publish to.')
        return

    if missing_params := [
        p for p in MANDATORY_PARAMETERS if gl_params.get(p) in (None, '')
    ]:
        _error(
            'Cannot post results to GitLab, missing mandatory parameters: %s.',
            ', '.join(missing_params).replace('_', '-'),
        )
        return

    keep_history = gl_params['keep_history']
    if isinstance(keep_history, str):
        if keep_history.lower().strip() not in ('true', 'false'):
            _error(
                'Cannot post results to GitLab: `keep-history` parameter must be `true` or `false`, got %s.',
                keep_history,
            )
            return
        keep_history = keep_history.lower().strip() == 'true'

    base_url = gl_params['server']
    token = gl_params.get('token')
    label_prefix = gl_params.get('label')
    cats = gl_params.get('cats') is not None

    notes_path = NOTES_API_TEMPLATE.format(**gl_params)
    token = {'private_token': token} if token else None
    data = {'body': _format_qualitygate_response(mode, qualitygate, cats)}

    try:
        response, status = _post_note(base_url + notes_path, data, token)
        if status != 201:
            return

        if label_prefix:
            target_path = TARGET_API_TEMPLATE.format(**gl_params)
            label_prefix = (
                DEFAULT_LABEL_PREFIX if label_prefix == 'default' else label_prefix
            )
            set_label(
                base_url + target_path, label_prefix, qualitygate['status'], token
            )

        if not keep_history:
            note_id = _maybe_get_noteid(
                base_url + notes_path, mode, response['id'], token
            )
            if note_id is None:
                return
            notes_path += f'/{note_id}'
            _delete_note(base_url + notes_path, token)
    except Exception as err:
        msg = str(err)
        if token:
            msg = msg.replace(token['private_token'], '[MASKED]')
        _error('Error while posting results to Gitlab. %s.', msg)
