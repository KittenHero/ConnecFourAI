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
        self.hori = [None]*4
        self.vert = [None]*4
        self.diag = []

    @classmethod
    def from_string(cls, turn, state):
        state = np.array(mat.asmatrix(
            state.replace(',', ' ;')
                 .replace('r', ' {},'.format(ConnectFour.player('r')))
                 .replace('y', ' {},'.format(ConnectFour.player('y')))
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

    def consec_hor(self, n):
        if self.hori[n] is None:
            row_summer = np.triu(np.tril(np.ones((self.width, self.width), dtype=int)), 1 - n)
            self.hor[n] = (self.state @ row_summer)[:, :1-n]
        return self.hor[n]
        
    def consec_ver(self, n):
        if self.vert[n] is None:
        col_summer = np.tril(np.triu(np.ones((self.height, self.height), dtype=int)), n - 1)
        return (col_summer @ self.state)[:1-n, :]

    def consec_diag(self, n):
        if not self.diag:
            self.diag = [None]*4
            mdiag, mshift, odiag, oshift = [np.copy(self.state) for _ in range(4)]
            up_shift = np.eye(self.height, k=1, dtype=int)
            left_shift = np.eye(self.width, k=-1, dtype=int)

            for i in range(1, 4):
                mshift = up_shift @ mshift @ left_shift
                oshift = up_shift @ oshift @ left_shift.T
                mdiag += mshift
                odiag += oshift
                self.diag[i] = np.copy(mdiag[:1-i, :1-i]), np.copy(odiag[:1-i, i:])
        return self.diag[n]

    def count_consec(self, n, player):
        if n == 1:
            return np.count_nonzero(self.state == player)

        score = n*player
        hori = np.count_nonzero(self.consec_hor == score)
        vert = np.count_nonzero(self.consec_ver == score)

        mdiag, odiag = self.consec_diag(n)
        mdiag = np.count_nonzero(mdiag == score)
        odiag = np.count_nonzero(odiag == score)

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
