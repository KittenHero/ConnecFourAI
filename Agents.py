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
        _, _, action = self.abHelper(state, alpha=self.evalFn.min, beta=self.evalFn.max)
        return action
        
    def abHelper(self, state, depth=0, action=None, alpha=None, beta=None):
        self.expanded += 1
        actions = state.legal_actions[1:] # discards skips
        if depth == self.depth or not actions:
            return self.evalFn(state), self.expanded, action
        elif depth % 2:
            return min(self.beta(state, depth, actions, alpha, beta))
        else:
            return max(self.alpha(state, depth, actions, alpha, beta))

    def alpha(self, state, depth, actions, alpha, beta):
        for action in actions:
            score, _, action = self.abHelper(
                state.successor(action),
                depth + 1, action,
                alpha, beta
            )
            yield score, self.expanded, action
            if alpha == None or score > alpha:
                alpha = score
                if beta != None and alpha >= beta:
                    break

    def beta(self, state, depth, actions, alpha, beta):
        for action in actions:
            score, _, action = self.abHelper(
                state.successor(action),
                depth + 1, action,
                alpha, beta
            )
            yield score, self.expanded, action
            if beta == None or beta < score:
                beta = score
                if alpha != None and alpha >= beta:
                    break
