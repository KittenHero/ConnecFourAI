import numpy as np
import numpy.matrixlib as mat

class ConnectFour:
    width = 7
    height = 6

    def __init__(self, turn, state=None):
        if state is not None:
            self.state = state
        else:
            self.state = np.zeros((self.width, self.height), dtype=int)
        self.turn = turn
        self.winner = None

    @classmethod
    def from_string(cls, turn, state):
        state = np.array(mat.asmatrix(
            state.replace(',', ' ;')
                 .replace('r', f" {ConnectFour.player('r')},")
                 .replace('y', f" {ConnectFour.player('y')},")
                 .replace('.', ' 0,'),
            dtype=int
        ))
        return cls(cls.player(turn), state)

    @staticmethod
    def player(player):
        if player.startswith('r'):
            return 1
        elif player.startswith('y'):
            return -1
        else:
            assert 0, 'Invalid player'
    
    @property
    def legal_actions(self):
        if self.game_over:
            return [None]
        else:
            return [None] + [i for i, cell in enumerate(self.state[-1]) if not cell]
    
    @property
    def game_over(self):
        if self.count_consec(4, self.player('r')):
            self.winner = 'red'
            return True
        elif self.count_consec(4, self.player('y')):
            self.winner = 'yellow'
            return True
        else:
            return False

    def count_consec(self, n, player):
        score = n*player
        if n == 1:
            return np.count_nonzero(self.state == player)

        row_summer = np.triu(np.tril(np.ones((self.width, self.width), dtype=int)), 1 - n)
        col_summer = np.tril(np.triu(np.ones((self.height, self.height), dtype=int)), n - 1)

        hori = np.count_nonzero((self.state @ row_summer)[:1-n, :] == score)
        vert = np.count_nonzero((col_summer @ self.state)[:, :1-n] == score)

        mdiag, mshift, odiag, oshift = [np.copy(self.state) for _ in range(4)]
        up_shift = np.eye(self.height, k=1, dtype=int)
        left_shift = np.eye(self.width, k=-1, dtype=int)

        for i in range(1, n):
            mshift = up_shift @ mshift @ left_shift
            oshift = up_shift @ oshift @ left_shift.T
            mdiag += mshift
            odiag += oshift


        mdiag = np.count_nonzero(mdiag[:1-n, :1-n] == score)
        odiag = np.count_nonzero(odiag[:1-n, n:] == score)

        return hori + vert + mdiag + odiag
        
    def successor(self, action):
        if action is not None:
            col = action
            row = min(np.nonzero(self.state[:, col] == 0)[0])
            state = np.copy(self.state)
            state[row, col] = self.turn
        else:
            state = self.state

        return ConnectFour(-self.turn, state)
