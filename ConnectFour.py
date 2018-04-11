from argparse import ArgumentParser, ArgumentTypeError
import re

def str_to_board(string):
    match = re.compile(r'((?:\.|r|y){7},?){6}').match(string)
    if not match or match.group() != string:
        raise ArgumentTypeError(f'Invalid board: {string}')
    return string

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('state', help='Current board state', type=str_to_board)
    parser.add_argument('player', help='Current player', choices=['red', 'yellow'])
    agent_args = parser.add_argument_group('Agent options')
    agent_args.add_argument('agent', help='Agent to use', choices=['A', 'M'], nargs='?')
    agent_args.add_argument('depth', help='Agent search depth', type=int, nargs='?')

    return parser.parse_args()

if __name__ == '__main__':
    print(parse_args())
