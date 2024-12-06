from commandsniffer.graph import CommandGraph, Replayer
from argparse import ArgumentParser
from commandsniffer.interceptor import do_intercept

import sys


def main() -> None:
    parser = ArgumentParser(usage='%(prog)s [options] -- <your-command>')
    parser.add_argument(
        '-o', '--output', type=str, default='commands.json',
        help='output json file containing commands'
    )
    parser.add_argument(
        '-c', '--commands', type=str, required=False,
        help='commands to sniff'
    )
    parser.add_argument(
        '-r', '--replay', action='store_true', default=False,
        help='replay the logged commands'
    )

    try:
        index = sys.argv.index('--')
        interceptor_argv = sys.argv[1:index]
        origin_command_argv = sys.argv[index + 1:]
        args = parser.parse_args(interceptor_argv)
        do_intercept(args.output, args.commands, origin_command_argv)
        if args.replay:
            graph = CommandGraph.from_command_db(args.output)
            graph.replay(replayer=Replayer(), nworkers=2)
    except ValueError:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
