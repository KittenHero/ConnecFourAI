class MinimaxAgent:
	def __init__(self, evalFn, depth):
		self.evalFn = evalFn
		self.depth = depth
		self.expanded = 0

	def compute_action(self, state):
		self.expanded = 0
		return self.minimax(state)

	def minimax(self, state, depth=0, prev=None):
		self.expanded += 1
		actions = state.legal_actions[1:] # discards skips

		if depth == self.depth or not actions:
			return self.evalFn(state), prev

		actions = self.action_taker(state, depth, actions)
		if depth % 2:
			return min(actions)
		else:
			return max(actions, key=lambda k: k[0])
	
	def action_taker(self, state, depth, actions):
		for action in actions:
			score, _ = self.minimax(
				state.successor(action),
				depth + 1,
				action
			)
			yield score, action

class AlphaBetaAgent:
	def __init__(self, evalFn, depth):
		self.evalFn = evalFn
		self.depth = depth
		self.expanded = 0

	def compute_action(self, state):
		self.expanded = 0
		return self.alphabeta(state)

	def alphabeta(self, state, alpha=float('-inf'), beta=float('inf'), depth=0, prev=None):
		self.expanded += 1
		actions = state.legal_actions[1:] # discard skip
		if not actions or depth == self.depth:
			return self.evalFn(state), prev
		elif depth % 2:
			return min(self.beta(state, alpha, beta, depth, actions))
		else:
			return max(self.alpha(state, alpha, beta, depth, actions), key=lambda k: k[0])

	def beta(self, state, alpha, beta, depth, actions):
		for action in actions:
			score, _ = self.alphabeta(
				state.successor(action),
				alpha, beta, depth + 1,
				action
			)
			yield score, action
			beta = min(beta, score)
			if beta <= alpha: break

	def alpha(self, state, alpha, beta, depth, actions):
		for action in actions:
			score, _ = self.alphabeta(
				state.successor(action),
				alpha, beta, depth + 1,
				action
			)
			yield score, action
			alpha = max(alpha, score)
			if beta <= alpha: break
