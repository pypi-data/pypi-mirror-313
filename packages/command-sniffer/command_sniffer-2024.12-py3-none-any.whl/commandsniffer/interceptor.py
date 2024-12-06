from commandsniffer import library
from subprocess import run, PIPE
from typing import Any, List, Dict

import os
import re
import sys
import json
import tempfile

interceptor_dir = library.__path__[0]


def do_intercept(output_json_path: str, intercept_commands: str, origin_commands: List[str]) -> None:
    interceptor_clib_build_dir = os.path.join(interceptor_dir, 'build/libinterceptor.so')
    build_script_path = os.path.join(interceptor_dir, 'build.sh')
    proc = run(['bash', build_script_path], capture_output=False, stderr=PIPE)
    if proc.returncode != 0:
        print(f'Error building interceptor library: {proc.stderr.decode()}')
        sys.exit(1)
    else:
        print(f"build c lib succeeded")
    _, temp_log_path = tempfile.mkstemp(dir=os.getcwd())
    env = os.environ.copy()
    if 'LD_PRELOAD' in env:
        env['LD_PRELOAD'] = f'{interceptor_clib_build_dir} {env["LD_PRELOAD"]}'
    else:
        env['LD_PRELOAD'] = interceptor_clib_build_dir
    env['interceptor_log_path'] = temp_log_path
    if intercept_commands:
        env['interceptor_commands'] = intercept_commands

    proc = run(origin_commands, stderr=PIPE, env=env)
    if proc.returncode != 0:
        print(f'Error running original commands: {proc.stderr.decode()}')
        os.remove(temp_log_path)
        sys.exit(1)
    with open(temp_log_path, 'r') as f:
        intercept_lines = f.readlines()

    os.remove(temp_log_path)
    command_db: List[Dict[str, Any]] = []
    current_cmd_desc: Dict[str, Any] = {}
    for line in intercept_lines:
        line = line.strip()
        if (obj := re.match(r'working_directory: (.*)', line)) is not None:
            if current_cmd_desc:
                command_db.append(current_cmd_desc)
                current_cmd_desc = {}
            current_cmd_desc['working_directory'] = obj.group(1).strip()
        elif (obj := re.match(r'type: (.*)', line)) is not None:
            current_cmd_desc['type'] = obj.group(1).strip()
        elif (obj := re.match(r'command: (.*)', line)) is not None:
            raw_command = obj.group(1).strip().split(' ')
            current_cmd_desc['command'] = raw_command[0]
            current_cmd_desc['arguments'] = raw_command[1:]
        elif (obj := re.match(r'environ:', line)) is not None:
            continue
        elif '=' in line:
            key, value = line.split('=', 1)
            current_cmd_desc.setdefault('environ', {})[key.strip()] = value.strip()
        elif line != '':
            print(f"Warning: Unexpected line in interceptor log: {line}")
    if current_cmd_desc:
        command_db.append(current_cmd_desc)
    if not command_db:
        print('No intercepted commands found')
        sys.exit(1)
    with open(output_json_path, 'w') as f:
        json.dump(command_db, f, indent=2)
    print(f'Intercepted commands saved to {os.path.abspath(output_json_path)}')
