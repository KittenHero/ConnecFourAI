from ConnectFourState import ConnectFourBit
from argparse import ArgumentParser
from utils import board_validator
from sys import exit

def parse_args():
	parser = ArgumentParser()
	move_group = parser.add_argument_group('making move')
	move_group.add_argument('board', help='current state', type=board_validator, nargs='?')
	move_group.add_argument('player', help='current player', choices=['red', 'yellow'], nargs='?')
	move_group.add_argument('move', help='move played', nargs='?')
	
	parser.add_argument('-n', '--new', help='make a new board', action='store_true')
	return parser.parse_args()

def main(args):
	if args.new:
		return ConnectFourBit(0, (0, 0))
	else:
		state = ConnectFourBit.from_string(args.player, args.board)
		if args.move and args.move in '0123456':
			return state.successor(int(args.move))
		else:
			return state.successor('')

if __name__ == '__main__':
	state = main(parse_args())
	print(state)
	exit(state.game_over)
