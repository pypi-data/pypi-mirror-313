# Copyright 2021-2024 Henix, henix.fr
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

"""opentf-ctl"""

from typing import Any, Dict, List, Optional

import json
import sys

from opentf.tools.ctlcommons import (
    generate_output,
    _make_params_from_selectors,
    _ensure_either_uuids_or_selectors,
    _ensure_options,
    _is_command,
    _error,
    _fatal,
    _get_arg,
    _ensure_uuid,
)
from opentf.tools.ctlconfig import (
    read_configuration,
    config_cmd,
    print_config_help,
    CONFIG,
)
from opentf.tools.ctlnetworking import (
    _eventbus,
    _agentchannel,
    _observer,
    _get,
    _delete,
)
from opentf.tools.ctlworkflows import print_workflow_help, workflow_cmd
from opentf.tools.ctlqualitygate import print_qualitygate_help, qualitygate_cmd
from opentf.tools.ctlattachments import print_attachments_help, attachments_cmd
from opentf.tools.ctlcompletion import completion_cmd
from opentf.tools.ctldatasources import print_get_datasources_help, get_datasources_cmd
from opentf.tools.ctlgenerate import print_generate_report_help, generate_report_cmd
from opentf.tools.ctltokens import print_tokens_help, tokens_cmd

########################################################################

# pylint: disable=broad-except

DEFAULT_NAMESPACE = 'default'


########################################################################
# Help messages

GETNAMESPACES_COMMAND = 'get namespaces'
GETSUBSCRIPTIONS_COMMAND = 'get subscriptions'
DELETESUBSCRIPTION_COMMAND = 'delete subscription *'
GETAGENTS_COMMAND = 'get agents'
DELETEAGENT_COMMAND = 'delete agent *'
GETCHANNELS_COMMAND = 'get channels'

GENERAL_HELP = '''opentf-ctl controls the OpenTestFactory orchestrators.

Find more information at: https://opentestfactory.org/tools/running-commands

Basic Commands:
  get workflows                    List active and recent workflows
  run workflow {filename}          Start a workflow
  get workflow {workflow_id}       Get a workflow status
  kill workflow {workflow_id}      Cancel a running workflow

Agent Commands:
  get agents                       List registered agents
  delete agent {agent_id}          De-register an agent

Channel Commands:
  get channels                     List known channels

Qualitygate Commands:
  get qualitygate {workflow_id}    Get quality gate status for a workflow
  describe qualitygate {workflow_id}
                                   Get quality gate status description for a workflow

Attachments Commands:
  get attachments {workflow_id}    List workflow attachments
  cp {workflow_id}:{...} {destination}
                                   Get a local copy of a workflow attachment
  generate report {workflow_id} using {file}
                                   Generate a report based on an insight from definition file

Datasources Commands:
  get datasource {workflow_id}     Get workflow datasource

Token Commands:
  generate token using {key}       Interactively generate a signed token
  check token {token} using {key}  Check if token signature matches public key
  view token {token}               Show token payload

Advanced Commands:
  get namespaces                   List accessible namespaces
  get subscriptions                List active subscriptions
  delete subscription {sub_id}     Cancel an active subscription

Other Commands:
  config                           Modify current opentf-tools configuration
  version                          List the tools version

Usage:
  opentf-ctl <command> [options]

Use "opentf-ctl <command> --help" for more information about a given command.
Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

OPTIONS_HELP = '''
The following environment variables override the defaults, if not overridden by options:

  OPENTF_CONFIG: Path to the opentfconfig file to use for CLI requests
  OPENTF_TOKEN: Bearer token for authentication to the orchestrator

The following options can be passed to any command:

  --token='': Bearer token for authentication to the orchestrator.
  --user='': The name of the opentfconfig user to use.
  --orchestrator='': The name of the opentfconfig orchestrator to use.
  --context='': The name of the opentfconfig context to use.
  --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity.  This will make your HTTPS connections insecure.
  --warmup-delay='': Delay in seconds to wait before sending reading requests after starting a workflow (default 1).
  --polling-delay='': Delay in seconds to wait between polling requests (default 5).
  --max-retry='': Max number of retries before giving up reading information (default 3).
  --opentfconfig='': Path to the opentfconfig file to use for CLI requests.

Those global options can be specified anywhere on the command line, before or after the command.

Example:
  # The following two commands are equivalent
  opentf-ctl --context=allinone get workflows
  opentf-ctl get workflows --context=allinone
'''

VERSION_HELP = '''
List the tools version

Example:
  # Display the version of the tools
  opentf-ctl version

Usage:
  opentf-ctl version [options]

Options:
  --debug: show additional information.

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_SUBSCRIPTIONS_HELP = '''List active subscriptions on the eventbus

Example:
  # List the subscriptions
  opentf-ctl get subscriptions

  # List the subscriptions with more details
  opentf-ctl get subscriptions --output=wide

  # Get just the subscription names and IDs
  opentf-ctl get subscriptions --output=custom-columns=NAME:.metadata.name,ID:.metadata.subscription_id

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --selector=s or -l=s: selector (label query) to filter on, supports '=', '==', and '!='.  (e.g. -l key1=value1,key2=value2)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)

Usage:
  opentf-ctl get subscriptions [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_SUBSCRIPTION_HELP = '''Remove an active subscription from the eventbus

Example:
  # Delete a subscription
  opentf-ctl delete subscription 8947945a-a8ac-4c94-803a-6a226d74ce4a

Options:
  --all: delete all subscriptions.
  --selector=s or -l=s: selector (label query) to filter on, supports '=', '==', and '!='.  (e.g. -l key1=value1,key2=value2)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)

Usage:
  opentf-ctl delete subscription (SUBSCRIPTION_ID... | --selector label | --all) [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_CHANNELS_HELP = '''List known channels

Example:
  # List the channels
  opentf-ctl get channels

  # List the channels with more details
  opentf-ctl get channels --output=wide

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --selector=s or -l=s: selector (label query) to filter on, supports '=', '==', and '!='.  (e.g. -l key1=value1,key2=value2)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)

Usage:
  opentf-ctl get channels [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_NAMESPACES_HELP = '''List accessible namespaces

Example:
  # List the namespaces the current user can access
  opentf-ctl get namespaces

  # List the namespaces the current user can run workflows on
  opentf-ctl get namespaces --selector=resource==workflows,verb==create

Options:
  --selector= or -l=: selector (query) to filter on, supports 'resource==' and 'verb==', both required when specifying a selector.

Usage:
  opentf-ctl get namespaces [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_AGENTS_HELP = '''List registered agents

Example:
  # List the agents
  opentf-ctl get agents

  # List the agents with more details
  opentf-ctl get agents --output=wide

  # Get just the agent IDs
  opentf-ctl get agents --output=custom-columns=ID:.metadata.agent_id

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information.
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --selector=s or -l=s: selector (label query) to filter on, supports '=', '==', and '!='.  (e.g. -l key1=value1,key2=value2)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)

Usage:
  opentf-ctl get agents [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_AGENT_HELP = '''De-register an active agent

Example:
  # De-register the specified agent
  opentf-ctl delete agent 9ea3be45-ee90-4135-b47f-e66e4f793383

Options:
  --all: de-register all agents.
  --selector=s or -l=s: selector (label query) to filter on, supports '=', '==', and '!='.  (e.g. -l key1=value1,key2=value2)
  --field-selector=s: selector (field query) to filter on, supports '=', '==', and '!='. (e.g. --field-selector key1=value1,key2=value2)
    (more at: https://opentestfactory.org/tools/running-commands#label-and-field-selectors)

Usage:
  opentf-ctl delete agent (AGENT_ID... | --selector label | --all) [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Subscriptions


SUBSCRIPTION_COLUMNS = (
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations.*',
)

WIDE_SUBSCRIPTION_COLUMNS = (
    'ID:.metadata.subscription_id',
    'NAME:.metadata.name',
    'ENDPOINT:.spec.subscriber.endpoint',
    'CREATION:.metadata.creationTimestamp',
    'COUNT:.status.publicationCount',
    'SUBSCRIPTIONS:.metadata.annotations.*',
)


def _get_subscriptions(params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = _get(
        _eventbus(),
        '/subscriptions',
        'Could not get subscriptions list',
        params=params,
        raw=True,
    )
    if params:
        header = response.headers.get('X-Processed-Query')
        if not header or not ('fieldSelector' in header or 'labelSelector' in header):
            _fatal(
                'The orchestrator does not support selectors, please specify explicit subscription IDs or upgrade your orchestrator.'
            )
    try:
        result = response.json()
    except Exception as err:
        _fatal('Could not get subscriptions list: %s.', err)
    return result['items']


def list_subscriptions() -> None:
    """List all active subscriptions.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    generate_output(
        list(_get_subscriptions(_make_params_from_selectors()).values()),
        SUBSCRIPTION_COLUMNS,
        WIDE_SUBSCRIPTION_COLUMNS,
    )


def delete_subscription(subscription_ids: List[str]) -> None:
    """Cancel a subscription."""
    subscription_ids = _ensure_either_uuids_or_selectors(
        subscription_ids, _get_subscriptions
    )
    for subscription_id in subscription_ids:
        subscription_id = _ensure_uuid(subscription_id, _get_subscriptions)
        what = _delete(
            _eventbus(),
            f'/subscriptions/{subscription_id}',
            f'Could not delete subscription {subscription_id}',
        )
        print(what['message'])


# Channels

CHANNEL_COLUMNS = (
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)

WIDE_CHANNEL_COLUMNS = (
    'HANDLER_ID:.metadata.channelhandler_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'LAST_REFRESH_TIMESTAMP:.status.lastCommunicationTimestamp',
    'STATUS:.status.phase',
)


def list_channels() -> None:
    """List all active agents.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    what = _get(
        _observer(),
        '/channels',
        'Could not get channels list',
        params=_make_params_from_selectors(),
    )

    generate_output(what['details']['items'], CHANNEL_COLUMNS, WIDE_CHANNEL_COLUMNS)


# Namepaces


def list_namespaces() -> None:
    """List namespaces.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    resource = verb = None
    selector = _get_arg('--selector=') or _get_arg('-l=')
    if selector:
        if len(selector.split(',')) != 2:
            _fatal(
                'Invalid selector, must be of form: "resource==resource,verb==verb", got: %s.',
                selector,
            )
        for item in selector.split(','):
            what, _, value = item.partition('=')
            if what == 'resource':
                resource = value.lstrip('=').strip()
            elif what == 'verb':
                verb = value.lstrip('=').strip()
            else:
                _fatal(
                    'Invalid selector, expecting "resource" or "verb", got: %s.', what
                )
    if (resource and not verb) or (verb and not resource):
        _fatal('Incomplete selector, expecting both "resource" and "verb".')

    url = '/namespaces'
    if resource and verb:
        url += f'?resource={resource}&verb={verb}'
    what = _get(_observer(), url, 'Could not get namespaces list')
    if 'details' not in what or 'items' not in what['details']:
        _fatal('Unexpected response: %s', what)
    namespaces = what['details']['items']
    print('NAMESPACE')
    if '*' in namespaces:
        print('*')
    else:
        for ns in namespaces:
            print(ns)


# Agents

AGENT_COLUMNS = (
    'AGENT_ID:.metadata.agent_id',
    'NAME:.metadata.name',
    'NAMESPACES:.metadata.namespaces',
    'TAGS:.spec.tags',
    'REGISTRATION_TIMESTAMP:.metadata.creationTimestamp',
    'LAST_SEEN_TIMESTAMP:.status.lastCommunicationTimestamp',
    'RUNNING_JOB:.status.currentJobID',
)


def _get_agents(params: Optional[Dict[str, Any]] = None):
    response = _get(
        _agentchannel(),
        '/agents',
        'Could not get agents list',
        params=params,
        raw=True,
    )
    if params and ('fieldSelector' in params or 'labelSelector' in params):
        header = response.headers.get('X-Processed-Query')
        if not header or not ('fieldSelector' in header or 'labelSelector' in header):
            _fatal(
                'The orchestrator does not support selectors, please specify explicit agent IDs or upgrade your orchestrator.'
            )
    try:
        result = response.json()
    except Exception as err:
        _fatal('Could not get agents list: %s.', err)

    data = result['items']

    # pre-2022-05 orchestrators where returning a dictionary, not a list
    # of manifests.
    if isinstance(data, dict):
        data = []
        for agent_id, manifest in result['items'].items():
            manifest['metadata']['agent_id'] = agent_id
            data.append(manifest)
    return data


def list_agents() -> None:
    """List all active agents.

    Outputs information in requested format.

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    generate_output(
        _get_agents(_make_params_from_selectors()), AGENT_COLUMNS, AGENT_COLUMNS
    )


def delete_agent(agent_ids: List[str]) -> None:
    """Deregister agent."""
    agent_ids = _ensure_either_uuids_or_selectors(
        agent_ids,
        lambda filter: [agent['metadata']['agent_id'] for agent in _get_agents(filter)],
    )
    for agent_id in agent_ids:
        agent_id = _ensure_uuid(
            agent_id, lambda: [agent['metadata']['agent_id'] for agent in _get_agents()]
        )
        what = _delete(
            _agentchannel(), f'/agents/{agent_id}', f'Could not delete agent {agent_id}'
        )
        print(what['message'])


# version


def get_tools_version() -> None:
    """
    Prints in the console the current version details.
    """

    from importlib.metadata import version

    fullversion = version('opentf-tools')
    major = fullversion.split('.')[0]
    minor = fullversion.split('.')[1]
    print(
        f'Tools Version: version.Info{{Major:"{major}", Minor: "{minor}", FullVersion: "{fullversion}"}}'
    )


def get_orchestrator_version(debug: bool) -> None:
    """
    Parses and prints in console the content of orchestrator's image BOM
    (Bill of materials) file, namely components names and versions.
    """
    print('Orchestrator:')
    print(f'    Orchestrator server: {CONFIG["orchestrator"]["server"]}')
    bom = _get(_observer(), '/version', 'Could not get BOM details.')
    bom_items = bom['details']['items']
    if 'error' in bom_items.keys():
        _error(bom_items['error'])
        return
    print(f'Components of {bom_items["name"]} image:')
    if debug:
        print(json.dumps(bom_items, indent=2))
        return
    for version in [
        f"{item['name']}: {item['version']}"
        for key, value in bom_items.items()
        for item in value
        if key != 'name'
    ]:
        print('   ', version)


########################################################################
# Helpers


def print_help(args: List[str]) -> None:
    """Display help."""
    if _is_command('options', args):
        print(OPTIONS_HELP)
    if _is_command('version', args):
        print(VERSION_HELP)
    elif _is_command(GETSUBSCRIPTIONS_COMMAND, args):
        print(GET_SUBSCRIPTIONS_HELP)
    elif _is_command('delete subscription', args):
        print(DELETE_SUBSCRIPTION_HELP)
    elif _is_command(GETAGENTS_COMMAND, args):
        print(GET_AGENTS_HELP)
    elif _is_command(GETCHANNELS_COMMAND, args):
        print(GET_CHANNELS_HELP)
    elif _is_command('delete agent', args):
        print(DELETE_AGENT_HELP)
    elif _is_command('_ token', args):
        print_tokens_help(args)
    elif _is_command('config', args):
        print_config_help(args)
    elif _is_command('_ workflow', args) or _is_command('_ workflows', args):
        print_workflow_help(args)
    elif _is_command('get qualitygate', args) or _is_command(
        'describe qualitygate', args
    ):
        print_qualitygate_help(args)
    elif _is_command('cp', args):
        print_attachments_help(args)
    elif _is_command('get attachments', args):
        print_attachments_help(args)
    elif _is_command('generate report', args):
        print_generate_report_help(args)
    elif _is_command('get datasource', args):
        print_get_datasources_help(args)
    elif _is_command(GETNAMESPACES_COMMAND, args):
        print(GET_NAMESPACES_HELP)
    elif len(args) == 2:
        print(GENERAL_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


########################################################################
# Main


def main():
    """Process command."""
    if len(sys.argv) == 1:
        print(GENERAL_HELP)
        sys.exit(1)
    if sys.argv[-1] == '--help':
        print_help(sys.argv)
        sys.exit(0)

    if _is_command('options', sys.argv):
        print(OPTIONS_HELP)
        sys.exit(0)

    if _is_command('version', sys.argv):
        _ensure_options('version', sys.argv[1:], flags=[('--debug',)])
        get_tools_version()
        read_configuration()
        get_orchestrator_version('--debug' in sys.argv)
        sys.exit(0)

    if _is_command('_ token', sys.argv):
        tokens_cmd()
    elif _is_command(GETNAMESPACES_COMMAND, sys.argv):
        _ensure_options(
            GETNAMESPACES_COMMAND, sys.argv[1:], extra=[('--selector', '-l')]
        )
        read_configuration()
        list_namespaces()
    elif _is_command(GETSUBSCRIPTIONS_COMMAND, sys.argv):
        _ensure_options(
            GETSUBSCRIPTIONS_COMMAND,
            sys.argv[1:],
            extra=[('--output', '-o'), ('--field-selector',), ('--selector', '-l')],
        )
        read_configuration()
        list_subscriptions()
    elif _is_command(DELETESUBSCRIPTION_COMMAND, sys.argv):
        subscription_ids = _ensure_options(
            DELETESUBSCRIPTION_COMMAND,
            sys.argv[1:],
            extra=[('--selector', '-l'), ('--field-selector',)],
            flags=[('--all',)],
        )
        read_configuration()
        delete_subscription(subscription_ids)
    elif _is_command(GETAGENTS_COMMAND, sys.argv):
        _ensure_options(
            GETAGENTS_COMMAND,
            sys.argv[1:],
            extra=[('--output', '-o'), ('--field-selector',), ('--selector', '-l')],
        )
        read_configuration()
        list_agents()
    elif _is_command(GETCHANNELS_COMMAND, sys.argv):
        _ensure_options(
            GETCHANNELS_COMMAND,
            sys.argv[1:],
            extra=[('--output', '-o'), ('--field-selector',), ('--selector', '-l')],
        )
        read_configuration()
        list_channels()
    elif _is_command(DELETEAGENT_COMMAND, sys.argv):
        agent_ids = _ensure_options(
            DELETEAGENT_COMMAND,
            sys.argv[1:],
            extra=[('--selector', '-l'), ('--field-selector',)],
            flags=[('--all',)],
        )
        read_configuration()
        delete_agent(agent_ids)
    elif _is_command('_ workflow', sys.argv) or _is_command('_ workflows', sys.argv):
        workflow_cmd()
    elif _is_command('get qualitygate', sys.argv) or _is_command(
        'describe qualitygate', sys.argv
    ):
        qualitygate_cmd()
    elif _is_command('cp', sys.argv):
        attachments_cmd()
    elif _is_command('get attachments', sys.argv):
        attachments_cmd()
    elif _is_command('generate report', sys.argv):
        generate_report_cmd()
    elif _is_command('get datasource _', sys.argv):
        get_datasources_cmd()
    elif _is_command('config', sys.argv):
        config_cmd()
    elif _is_command('completion bash', sys.argv):
        completion_cmd()
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


if __name__ == '__main__':
    main()
