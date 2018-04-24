from itertools import count
from utils import Timeout

class TimedIterativeABAgent:
	def __init__(self, evalFn, initial_depth=8, timeout=960):
		self.depth = 0
		self.evalFn = evalFn
		self.initial_depth = initial_depth
		self.timeout = timeout
		self.seen = {}
	
	def compute_action(self, state):
		with Timeout(self.timeout):
			for d in count(self.initial_depth):
				self.depth = d
				self.seen.clear()
				score, action = self.alphabeta(state)
				
				if score == self.evalFn.min:
					action = ''
					break
				elif score == self.evalFn.max:
					break
				
		return score, action

	def alphabeta(self, state, alpha=float('-inf'), beta=float('inf'), depth=0, prev='', prev_eval=0):
		
		if depth == self.depth:
			return prev_eval, prev

		actions = state.legal_actions
		if not actions:
			return prev_eval, prev
		
		children = [state.successor(action) for action in actions]
		evals = [self.evalFn(child) for child in children]
		children = list(zip(evals, actions, children))
		
		if depth % 2:
			agent = self.beta
			reducer = min
			children.sort()
		else:
			agent = self.alpha
			reducer = max
			children.sort(reverse=1)
			
		return reducer(agent(alpha, beta, depth, children), key=lambda r: r[0])
	
	def beta(self, alpha, beta, depth, children):
		for score, action, state in children:
			if state not in self.seen:
				score, _ = self.alphabeta(
					state,
					alpha, beta, depth + 1,
					action, score
				)
				self.seen[state] = score
			else:
				score = self.seen[state]
			yield score, action
			beta = min(beta, score)
			if beta <= alpha: break

	def alpha(self, alpha, beta, depth, children):
		for score, action, state in children:
			if state not in self.seen:
				score, _ = self.alphabeta(
					state,
					alpha, beta, depth + 1,
					action, score
				)
				self.seen[state] = score
			else:
				score = self.seen[state]
			
			yield score, action
			alpha = max(alpha, score)
			if beta <= alpha: break
