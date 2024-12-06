import json
import os
from commandsniffer.commands.base import BaseCommand
from commandsniffer.commands.compilers import CCompilerCommand
from commandsniffer.commands.linkers import CLinkerCommand
from commandsniffer.utils import Result
from typing import Any, Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from commandsniffer.commands.base import BaseCommand
from multiprocessing import Pool
import subprocess


@dataclass
class CommandLog:
    stdout_log: str = field(default='')
    stderr_log: str = field(default='')


class Replayer:
    """ In the future we will add more hooks in the plugin """

    def before_exec_command(self, command: BaseCommand) -> Optional[BaseCommand]:
        """ Returns a new command if it want to replace the command that
        will be executed. """
        print(f"Replaying {command.command} {' '.join(command.arguments)}")
        return None

    def after_exec_command(self, command: BaseCommand) -> None:
        pass


@dataclass
class CommandRunner:
    replayer: Optional[Replayer] = field(default=None)

    def run_each(self, command: BaseCommand) -> Result[None, CommandLog]:
        if self.replayer is not None:
            new_command = self.replayer.before_exec_command(command)
            if new_command is not None:
                command = new_command
        proc = subprocess.run([command.command] + command.arguments,
                              cwd=command.working_directory,
                              env=command.environ,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if self.replayer is not None:
            self.replayer.after_exec_command(command)
        if proc.returncode != 0:
            log = CommandLog(stdout_log=proc.stdout.decode('utf-8'), stderr_log=proc.stderr.decode('utf-8'))
            return Result.err(log)
        return Result.ok(None)

    def run_para(self, commands: Set[BaseCommand], nworkers: int = 2) -> Result[None, CommandLog]:
        with Pool(nworkers) as pool:
            results = pool.map(self.run_each, commands)
        for result in results:
            if result.is_err():
                return result
        return Result.ok(None)


@dataclass
class CommandGraph:
    commands: List[BaseCommand]
    dependencies: Dict[BaseCommand, Set[BaseCommand]]

    @classmethod
    def from_command_db(cls, command_db_path: str) -> 'CommandGraph':
        graph = CommandGraph([], {})
        with open(command_db_path, 'r') as f:
            command_db = json.load(f)

        def identify_by_ext(args: List[str], ext: Tuple[str, ...]) -> List[str]:
            return list(filter(lambda x: x.endswith(ext), args))

        def identify_by_arg(args: List[str], pre_arg: List[str]) -> Optional[str]:
            for i, arg in enumerate(args):
                if arg in pre_arg:
                    return args[i + 1]
            return None

        def identify_input(cmd: BaseCommand) -> List[str]:
            if isinstance(cmd, CCompilerCommand):
                return identify_by_ext(cmd.arguments, ('.c', '.cpp', '.cc'))
            elif isinstance(cmd, CLinkerCommand):
                return identify_by_ext(cmd.arguments, ('.o', '.a', '.so'))
            return []

        def identify_output(cmd: BaseCommand) -> Optional[str]:
            return identify_by_arg(cmd.arguments, ['-o'])

        def norm_path(work_dir: str, path: str) -> str:
            if os.path.isabs(path):
                return os.path.normpath(path)
            return os.path.normpath(os.path.join(work_dir, path))

        def to_command(id: int, cmd_desc: Dict[str, Any]) -> BaseCommand:
            cmd_cls = BaseCommand
            if cmd_desc['type'] == 'compile':
                cmd_cls = CCompilerCommand
            elif cmd_desc['type'] == 'link':
                cmd_cls = CLinkerCommand
            cmd = cmd_cls(id=id, command=cmd_desc['command'], arguments=cmd_desc['arguments'],
                          working_directory=cmd_desc['working_directory'], environ=cmd_desc['environ'])
            input_files = identify_input(cmd)
            cmd.input_files = [norm_path(cmd.working_directory, path) for path in input_files]
            if (output_file := identify_output(cmd)) is not None:
                cmd.output_file = norm_path(cmd.working_directory, output_file)
            return cmd

        input_commands: Dict[str, Set[BaseCommand]] = {}
        output_commands: Dict[str, Set[BaseCommand]] = {}
        for i, cmd_desc in enumerate(command_db):
            cmd = to_command(i, cmd_desc)
            for input_file in cmd.input_files:
                input_commands.setdefault(input_file, set()).add(cmd)
                dep_commands = output_commands.get(input_file, set())
                graph.dependencies[cmd] = dep_commands

            if cmd.output_file is not None:
                output_commands.setdefault(cmd.output_file, set()).add(cmd)
            graph.commands.append(cmd)
        return graph

    def replay(self, replayer: Optional[Replayer], nworkers: int = 1) -> None:
        runner = CommandRunner(replayer)
        pending_commands: Set[BaseCommand] = set(self.commands)
        done_commands: Set[BaseCommand] = set()
        while pending_commands:
            ready_commands: Set[BaseCommand] = set()
            for command in pending_commands:
                if all(dep in done_commands for dep in self.dependencies.get(command, set())):
                    ready_commands.add(command)
            res = runner.run_para(ready_commands, nworkers)
            if res.is_err():
                raise Exception(f"Error running commands: {res.err}")
            pending_commands -= ready_commands
            done_commands |= ready_commands
        print("Replayed successfully!")
