class MinimaxAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth
        self.expanded = 0

    def compute_action(self, state):
        self.expanded = 0
        _, action = self.minimax(state)
        return action

    def minimax(self, state, depth=0, action=None):

        self.expanded += 1
        actions = state.legal_actions[1:] # discards skips

        if depth == self.depth or not actions:
            return self.evalFn(state), action

        actions = (
            self.minimax(
                state.successor(action),
                depth + 1,
                action
            ) for action in actions
        )
        if depth % 2:
            return min(actions)
        else:
            return max(actions, key=lambda k: k[0])

class AlphaBetaAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth
        self.expanded = 0

    def compute_action(self, state):
        self.expanded = 0
        _, action = self.alphabeta(state)
        return action

    def alphabeta(self, state, alpha=float('-inf'), beta=float('inf'), depth=0, action=None):
        self.expanded += 1
        actions = state.legal_actions[1:] # discard skip
        if not actions or depth == self.depth:
            return self.evalFn(state), action
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
            if beta <= alpha:
                break

    def alpha(self, state, alpha, beta, depth, actions):
        for action in actions:
            score, _ = self.alphabeta(
                state.successor(action),
                alpha, beta, depth + 1,
                action
            )
            yield score, action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
