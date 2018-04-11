class MinimaxAgent:
    def __init__(self, evalFn, depth):
        self.evalFn = evalFn
        self.depth = depth

    def getAction(self, state):
        self.actionID = 0
        _, action = self.minimax(state)
        return action

    def minimax(self, state, depth = 0, action):

        actions = state.getLegalActions()[1:] # discards skips

        if depth == self.depth or not actions:
            return self.evalFn(state), action

        actions = [
            self.minimax(
                state.successor(action),
                depth + 1,
                self.actionID,
                sequence + [action]
            )
            for i, action in enumerate(actions)
        ]

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
        _, _, (action, *_) = self.abHelper)
        
    def abHelper(self, state, depth = 0, action, alpha=None, beta=None):
        if depth == self.depth:
            return self.evalFn(state), action
        else if depth % 2:
            return self.beta(self, state, depth, alpha, beta)
        else:
            return self.alpha(self, state, depth, alpha, beta)

    def alpha(self, state, depth, alpha, beta):
        for action in state.getLegalActions():
            potential = 

