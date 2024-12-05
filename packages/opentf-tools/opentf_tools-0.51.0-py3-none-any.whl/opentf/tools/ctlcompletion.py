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

"""opentf-ctl bash autocompletion handling"""

from typing import Any, Dict, Iterable, List, Optional

import os
import re
import sys

from opentf.tools.ctlattachments import _get_attachment_uuids
from opentf.tools.ctlcommons import _is_command, _error
from opentf.tools.ctlconfig import _read_opentfconfig, read_configuration
from opentf.tools.ctlnetworking import _get_workflows

########################################################################
## Constants

COMPLETION_SCRIPT_BASH = '''
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
#
# bash completion for opentf-ctl

_opentf_ctl_completions() {
    words=()
    cword=0

    if declare -f __reassemble_comp_words_by_ref > /dev/null; then
        __reassemble_comp_words_by_ref ":=" words cword
    else
        _comp__reassemble_words ":=" words cword
    fi

    local cur="${words[cword]}"
    local user_input="${words[@]:1:cword}"

    local suggestions
    suggestions=$(python3 {ctlcompletion_path} $user_input "$cur")

    if [[ -n "$suggestions" ]]; then
        if [[ $suggestions == "__file__" ]]; then
            compopt -o default
        else
            if [[ "$cur" == *"="* || "$cur" == *":"* ]]; then
                local value

                if [[ "$cur" == *"="* ]]; then
                    value="${cur#*=}"
                if [[ "$value" == *":"* ]]; then
                      value="${value##*:}"
                fi
                else
                    value="${cur##*:}"
                fi

                COMPREPLY=( $(compgen -W "$suggestions" -- "$value") )
            else
                COMPREPLY=( $(compgen -W "$suggestions" -- "$cur") )
            fi

            if [[ "$suggestions" == *":" ]]; then
                compopt -o nospace
            else
                compopt +o nospace
            fi
        fi
    else
        COMPREPLY=( "" )
        compopt +o nospace
    fi
}
complete -F _opentf_ctl_completions opentf-ctl
'''

DYNAMIC_PARAMS = (
    'agent_id',
    'context',
    'orchestrator',
    'subscription_id',
    'user',
    'workflow_id',
    'workflow_id:attachment_id',
)
CONFIG_PARAMS = ('context', 'user', 'orchestrator')

UUID_REGEX = r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$'

COMMANDS = {
    'check': {'token': {'using': {'filepath': {}}}},
    'config': {
        'generate': {},
        'view': {},
        'use-context': {'context': {}},
        'set-context': {'context': {}},
        'delete-context': {'context': {}},
        'set-credentials': {'user': {}},
        'delete-credentials': {'user': {}},
        'set-orchestrator': {'orchestrator': {}},
        'delete-orchestrator': {'orchestrator': {}},
    },
    'cp': {'workflow_id:attachment_id': {'filepath': {}}},
    'delete': {'agent': {'agent_id': {}}, 'subscription': {'subscription_id': {}}},
    'describe': {'qualitygate': {'workflow_id': {}}},
    'generate': {
        'token': {'using': {'filepath': {}}},
        'report': {'workflow_id': {'using': {'filepath': {}}}},
    },
    'get': {
        'agents': {},
        'channels': {},
        'namespaces': {},
        'subscriptions': {},
        'workflows': {},
        'attachments': {'workflow_id': {}},
        'datasource': {'workflow_id': {}},
        'qualitygate': {'workflow_id': {}},
        'workflow': {'workflow_id': {}},
    },
    'kill': {'workflow': {'workflow_id': {}}},
    'run': {'workflow': {'filepath': {}}},
    'version': {},
    'view': {'token': {}},
}

SHARED_OPTIONS = {
    '--output': [
        'get workflows',
        'run workflow',
        'get workflow',
        'get agents',
        'get channels',
        'get qualitygate',
        'get subscriptions',
        'get attachments',
        'get datasource',
    ],
    '--selector': [
        'get workflows',
        'run workflow',
        'get workflow',
        'kill workflow',
        'get agents',
        'delete agent',
        'get channels',
        'get namespaces',
        'get subscriptions',
        'delete subscription',
    ],
    '--field-selector': [
        'get workflows',
        'run workflow',
        'get workflow',
        'kill workflow',
        'get agents',
        'delete agent',
        'get channels',
        'get subscriptions',
        'delete subscription',
        'get datasource',
    ],
    '--namespace': ['run workflow', 'config set-context'],
    '--watch': ['run workflow', 'get workflow'],
    '--mode': ['run workflow', 'get qualitygate', 'describe qualitygate'],
    '--step-depth': ['run workflow', 'get workflow', 'config set-credentials'],
    '--job-depth': ['run workflow', 'get workflow', 'config set-credentials'],
    '--max-command-length': [
        'run workflow',
        'get workflow',
        'config set-credentials',
    ],
    '--show-notifications': ['run workflow', 'get workflow'],
    '--verbose': ['run workflow', 'get workflow', 'get attachments'],
    '--show-attachments': ['run workflow', 'get workflow'],
    '--dry-run': ['run workflow', 'kill workflow'],
    '--all': ['kill workflow', 'delete agent', 'delete subscription'],
    '--using': ['get qualitygate', 'describe qualitygate', 'run workflow'],
    '--plugin': ['get qualitygate', 'run workflow'],
    '--timeout': [
        'get qualitygate',
        'describe qualitygate',
        'generate report',
        'get datasource',
    ],
    '--token': ['config generate', 'config set-credentials'],
    '--insecure-skip-tls-verify': ['config generate', 'config set-orchestrator'],
    '--name': ['config generate', 'generate report'],
}

SERVICE_TMPL = '{SERVICE}'
FILEPATH = '__file__'

SERVICES = (
    'agentchannel',
    'eventbus',
    'insightcollector',
    'killswitch',
    'localstore',
    'observer',
    'qualitygate',
    'receptionist',
)

SPECIFIC_OPTIONS = {
    'get workflows': ['--having'],
    'run workflow': ['-e', '-f', '--tags', '--report', '--wait'],
    'kill workflow': ['--reason', '--source'],
    'generate token': [
        '--algorithm',
        '--issuer',
        '--subject',
        '--expiration',
        '--output-file',
    ],
    'cp': ['--type'],
    'generate report': ['--save-to', '--as'],
    'get datasource': ['--kind'],
    'config generate': ['--orchestrator-server', '--orchestrator-{SERVICE}-port'],
    'config set-context': ['--orchestrator', '--user'],
    'config set-orchestrator': [
        '--warmup-delay',
        '--polling-delay',
        '--max-retry',
        '--server',
        '--{SERVICE}-force-base-url',
        '--{SERVICE}-port',
        '--{SERVICE}-prefix',
    ],
    'version': ['--debug'],
}

OPTIONS_VALUES = {
    '--output': ['wide', 'custom-columns', 'json', 'yaml'],
    '--using': [FILEPATH],
    '--plugin': {
        'gitlab:': [
            'server',
            'project',
            'mr',
            'issue',
            'keep-history',
            'token',
            'label',
        ]
    },
    '--insecure-skip-tls-verify': ['true', 'false'],
    '--save-to': [FILEPATH],
    '--kind': ['testcases', 'tags', 'jobs'],
    '--{SERVICE}-force-base-url': ['true', 'false'],
}

########################################################################


def _get_agent_ids():
    # kludge to avoid circular import issue
    from opentf.tools.ctl import _get_agents

    return [agent['metadata']['agent_id'] for agent in _get_agents()]


def _get_subscription_ids():
    # kludge to avoid circular import issue
    from opentf.tools.ctl import _get_subscriptions

    return list(_get_subscriptions())


def _get_context_param_values(param: str) -> List[str]:
    _, config = _read_opentfconfig()
    key = f'{param}s'
    return [item['name'] for item in config.get(key, [])]


def _filter_items_on_prefix(items: Iterable, prefix: str) -> List[str]:
    return [item for item in items if item.startswith(prefix)]


PARAMS_GETTERS = {
    'agent_id': _get_agent_ids,
    'subscription_id': _get_subscription_ids,
    'workflow_id': _get_workflows,
}


def _handle_double_param(current_input: str):
    # currently handles cp command only
    first, sep, second = current_input.partition(':')
    if not sep:
        items = _filter_items_on_prefix(_get_workflows(), first)
        if len(items) == 1:
            return [items[0] + ':']
        return items
    if not re.match(UUID_REGEX, first):
        if first := _filter_items_on_prefix(_get_workflows(), first):
            first = first[0]
        else:
            return []
    return _filter_items_on_prefix(_get_attachment_uuids(first), second)


def _get_dynamic_params(
    param: str, cur_pos: int, len_args: int, current_input: str
) -> List[str]:
    if ':' in param:
        return _handle_double_param(current_input)
    if param in CONFIG_PARAMS:
        items = _get_context_param_values(param)
    else:
        items = PARAMS_GETTERS[param]()
    if cur_pos == len_args - 2:
        return _filter_items_on_prefix(items, current_input)
    if cur_pos == len_args - 1:
        return items
    return []


def _maybe_expand_services(options: Iterable[str]) -> List[str]:
    expanded = []
    for opt in options:
        if SERVICE_TMPL in opt:
            expanded += [opt.replace(SERVICE_TMPL, service) for service in SERVICES]
            continue
        expanded += [opt]
    return expanded


def _get_cmd_options(context: str, current_input: str) -> List[str]:
    shared = [
        opt
        for opt, cmds in SHARED_OPTIONS.items()
        if context in cmds and opt.startswith(current_input)
    ]
    specific = _maybe_expand_services(SPECIFIC_OPTIONS.get(context, []))
    return shared + _filter_items_on_prefix(specific, current_input)


def _get_options_values():
    options_args = {}
    added = False
    for k in _maybe_expand_services(OPTIONS_VALUES):
        for service in SERVICES:
            if service in k:
                options_args[k] = OPTIONS_VALUES[k.replace(service, SERVICE_TMPL)]
                added = True
                break
        if not added:
            options_args.setdefault(k, OPTIONS_VALUES[k])
    return options_args


def _get_options_or_values(
    context: str, last_arg: str, option_arg: str, current_input: str
) -> List[str]:
    """Get options or options values completion list.

    # Required parameters

    - context: a string, represents an `opentf-ctl`command
    - last_arg: a string, last item of args array, possibly an option
    - option_arg: a string, possibly an option
    - current_input: a string, user current input

    # Returned value

    A list of completion suggestions.
    """
    options_values = _get_options_values()
    option = value = ''
    if '=' in last_arg and '=' in current_input:
        option, _, value = current_input.partition('=')
        items = options_values.get(option, [])
        if ':' in value:
            plugin, _, value = value.partition(':')
            items = items.get(plugin + ':', [])
        return _filter_items_on_prefix(items, value)
    if ':' in last_arg and ':' in current_input:
        option, _, value = current_input.partition(':')
        return _filter_items_on_prefix(
            options_values[option_arg].get(option + ':', []), value
        )
    if current_input and (opts := options_values.get(option_arg)):
        if isinstance(opts, list) and opts[0] == FILEPATH:
            return [FILEPATH]
        return _filter_items_on_prefix(opts, current_input)
    if last_arg in options_values:
        return options_values[last_arg]
    return _get_cmd_options(context, current_input)


def _dynamic_arg(arg: str, cmd: Dict[str, Any]):
    return cmd and (arg not in cmd) and (list(cmd)[0] in (*DYNAMIC_PARAMS, 'filepath'))


def _process_arg(arg: str, cmd: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not cmd:
        return None
    if _dynamic_arg(arg, cmd):
        return cmd.get(list(cmd)[0])
    return cmd.get(arg)


def _go_further(args: List[str], current_input: str):
    if args and (current_input != args[-1] or current_input.startswith('-')):
        return True, None
    if args and current_input == args[-1]:
        cmd = COMMANDS
        for arg in args[:-1]:
            cmd = _process_arg(arg, cmd)
        if cmd:
            return True, list(cmd)[0]
    return False, None


def _get_context(args_count: int, args: List[str]) -> str:
    if args_count >= 1 and args[0] in ('version', 'cp'):
        return args[0]
    if args_count <= 1:
        return ''
    return ' '.join(args[:2])


def get_suggestions(args: List[str], current_input: str) -> List[str]:
    """Get auto-complete suggestions.

    # Required parameters

    - args: a list of strings, sys.argv values without `opentf-ctl`
    - current_input: a string, user current input

    # Returned value

    A list of completion suggestions.
    """
    cmd_dict = COMMANDS
    args_count = len(args)

    if args_count and not current_input and (args[0] not in cmd_dict):
        return []

    context = _get_context(args_count, args)
    if context and any(arg.startswith('--') for arg in args[-2:]):
        return _get_options_or_values(context, args[-1], args[-2], current_input)

    go_further, last = _go_further(args, current_input)
    for n, arg in enumerate(args):
        if arg in cmd_dict:
            cmd_dict = cmd_dict[arg]
            if dynamic_params := [p for p in DYNAMIC_PARAMS if p in cmd_dict]:
                if args_count > n + 1 and go_further and dynamic_params[0] != last:
                    continue
                read_configuration()
                return _get_dynamic_params(
                    dynamic_params[0], n, args_count, current_input
                )
        elif cmd_dict and (dyn_arg := list(cmd_dict)[0]) in DYNAMIC_PARAMS:
            cmd_dict = cmd_dict[dyn_arg]
        elif go_further:
            if current_input == args[-1] and not current_input.startswith('-'):
                continue
            return _get_cmd_options(context, current_input)

    if 'filepath' in cmd_dict:
        return [FILEPATH]

    return _filter_items_on_prefix(cmd_dict, current_input) or _get_cmd_options(
        context, current_input
    )


def output_script():
    """Output bash completion script."""
    ctlcompletion_path = os.path.abspath(__file__)
    print(COMPLETION_SCRIPT_BASH.replace('{ctlcompletion_path}', ctlcompletion_path))


########################################################################
# Exposed functions


def completion_cmd():
    """Output completion script"""
    if _is_command('completion bash', sys.argv):
        output_script()
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def main():
    """Output suggestions list as space-separated string."""
    *args, current_input = sys.argv[1:]
    suggestions = get_suggestions(args, current_input)
    print(' '.join(suggestions))


if __name__ == '__main__':
    main()
