from Agents import MinimaxAgent
from ConnectFourState import ConnectFourBit
from Functions import DefaultEval
import cProfile
import pstats

board = ','.join(['.'*7]*6)
player = 'red'
eval_fn = DefaultEval(player)
agent = MinimaxAgent(eval_fn, depth=5)


state = ConnectFourBit.from_string(player, board)


cProfile.run('agent.compute_action(state)', 'minimax_p')
p = pstats.Stats('minimax_p')
p.strip_dirs().sort_stats('cumtime').print_stats('.py:')
