from argparse import ArgumentParser
from ConnectFourState import ConnectFourBit
from Agents import TimedIterativeABAgent
from Functions import EnhancedEval
from utils import board_validator

class EvalAdaptorAgent:
	def __init__(self, eval_fn):
		self.eval = eval_fn
		self.expanded = 0
	
	def compute_action(self, state):
		return self.eval(state), 0

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('state', help='Current board state', type=board_validator)
	parser.add_argument('player', help='Current player', choices=['red', 'yellow'])
	agent_args = parser.add_argument_group('Agent options')
	agent_args.add_argument('-E', '--evaluation', help='Run only the evaluation', action='store_true')
	agent_args.add_argument('--score', help='Shows the max score value', action='store_true')
	
	return parser.parse_args()

def main():
	args = parse_args()
	state = ConnectFourBit.from_string(args.player, args.state)
	eval_fn = EnhancedEval(args.player)
	agent = EvalAdaptorAgent(eval_fn) if args.evaluation else TimedIterativeABAgent(eval_fn)
	score, action = agent.compute_action(state)
	
	print(action)
	if args.score: print('score:', score)

if __name__ == '__main__':
	main()
