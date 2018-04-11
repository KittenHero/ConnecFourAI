import numpy as np

class ConnectFour:
    width = 7
    height = 6

    def __init__(self, turn, state=None):
        if state = None:
            self.state = np.zeros((self.width, self.height), dtype=int)

        else:
            self.state = state
        self.turn = turn

    @staticmethod
    def player(player):
        if player == 'r':
            return 1
        else if player == 'y':
            return -1
        else:
            assert 0, 'Invalid player'
    
    @property
    def legal_actions(self):
        if self.game_over:
            return []
        else:
            return [0] + [i for i, cell in enumerate(self.state[-1], 1) if not cell]
    
    @property
    def game_over(self):
        return self.count_consec(4, 'r') or self.count_consec(4, 'y')

    def count_consec(self, n, player):
        if n == 1:
            return np.count_nonzero(self.state == player)

        row_summer = np.triu(np.tril(np.ones((self.width, self.width), dtype=int), n - 1))
        col_summer = np.tril(np.triu(np.ones((self.height, self.height), dtype=int), n - 1))

        hori = np.count_nonzero((self.state @ row_summer)[:, n-1:] == n*player)
        vert = np.count_nonzero((col_summer @ self.state)[n-1:, :] == n*player)
        
        
        

    def successor(self, action):
        if action:
            col = action - 1
            state = np.copy(self.state)
            state[row, col] = self.turn
        else:
            state = self.state

        return ConnectFour(-self.player, state)
