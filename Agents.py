class MinimaxAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth
        self.expanded = 0

    def compute_action(self, state):
        self.expanded = 0
        _, _, action = self.minimax(state)
        return action

    def actions_gen(self, state, actions, depth):
        yield from [
            self.minimax(
                state.successor(action),
                depth + 1,
                action
            )
            for action in actions
        ]

    def minimax(self, state, depth=0, action=None):

        self.expanded += 1
        actions = state.legal_actions[1:] # discards skips

        if depth == self.depth or not actions:
            return self.evalFn(state), self.expanded, action

        actions = self.actions_gen(state, actions, depth)
        if depth % 2:
            return max(actions)
        else:
            return min(actions)

class AlphaBetaAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth
        self.expanded = 0

    def compute_action(self, state):
        self.expanded = 0
        score, tiebreak, action = self.alphabeta(state)
        return action

    def alphabeta(self, state, alpha=float('-inf'), beta=float('inf'), depth=0, action=None):
        self.expanded += 1
        actions = state.legal_actions[1:] # discard skip
        if not actions or depth == self.depth:
            return self.evalFn(state), self.expanded, action
        elif depth % 2:
            return min(self.beta(state, alpha, beta, depth, actions))
        else:
            return max(self.alpha(state, alpha, beta, depth, actions))

    def beta(self, state, alpha, beta, depth, actions):
        for action in actions:
            score, _, _ = self.alphabeta(
                state.successor(action),
                alpha, beta, depth + 1,
                action
            )
            yield score, action, action
            beta = min(beta, score)
            if beta <= alpha:
                break

    def alpha(self, state, alpha, beta, depth, actions):
        for action in actions:
            score, _, _ = self.alphabeta(
                state.successor(action),
                alpha, beta, depth + 1,
                action
            )
            yield score, state.width - action, action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
