class MinimaxAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth
        self.expanded = 0

    def getAction(self, state):
        self.expanded = 0
        _, action = self.minimax(state)
        return action

    def actions_gen(self, state, actions, depth):
        yield from [
            self.minimax(
                state.successor(action),
                depth + 1,
                sequence + [action]
            )
            for i, action in enumerate(actions)
        ]


    def minimax(self, state, depth = 0, action):

        self.expanded += 1
        actions = state.legal_actions[1:] # discards skips

        if depth == self.depth or not actions:
            return self.evalFn(state), action

        actions = self.actions_gen(state, actions, depth)
        if depth % 2:
            return max(actions)
        else:
            return min(actions)

class AlphaBetaAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth

    def getAction(self, state):
        self.actionID = 0
        _, action = self.abHelper(state)
        return action
        
    def abHelper(self, state, depth = 0, action, alpha=None, beta=None):
        actions = state.legal_actions[1:] # discards skips
        if depth == self.depth or not actions:
            return self.evalFn(state), action
        else if depth % 2:
            return min(self.beta(self, state, depth, actions, alpha, beta))
        else:
            return max(self.alpha(self, state, depth, actions, alpha, beta))

    def alpha(self, state, depth, actions, alpha, beta):
        for action in self.actions_gen:
            score, action = self.abHelper(
                state.successor(action),
                depth + 1, action,
                alpha, beta
            )
            yield score, action
            if alpha == None or score > alpha:
                alpha = score
                if beta != None and alpha >= beta
                    break

    def beta(self, state, depth, actions, alpha, beta):
        for action in actions:
            score, action = self.abHelper(
                state.successor(action),
                depth + 1, action,
                alpha, beta
            )
            yield score, action
            if alpha == None or score > alpha:
                alpha = score
                if beta != None and alpha >= beta
                    break

