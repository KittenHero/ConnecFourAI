import numpy as np
import numpy.matrixlib as mat

class ConnectFour:
	width = 7
	height = 6

	def __init__(self, turn, state=None):
		if state is not None:
			self.state = state
		else:
			self.state = np.zeros((self.width, self.height), dtype=np.int8)
		self.turn = turn
		self.winner = None
		self.rconsec = [None]*4
		self.yconsec = [None]*4
		self.diag = [None]*4

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
		row_summer = np.triu(np.tril(np.ones((self.width, self.width), dtype=np.int8)), 1 - n)
		return (self.state @ row_summer)[:, :1 - n]


	def consec_ver(self, n):
		col_summer = np.tril(np.triu(np.ones((self.height, self.height), dtype=np.int8)), n - 1)
		return (col_summer @ self.state)[:1 - n, :]

	def consec_diag(self, n):
		n -= 1
		if not self.diag[n]:
			mdiag, mshift, odiag, oshift = [np.copy(self.state) for _ in range(4)]
			ushift = np.eye(self.height, k=1, dtype=np.int16)
			lshift = np.eye(self.width, k=-1, dtype=np.int16)

			for i in range(1, 4):
				mshift = ushift @ mshift @ lshift
				oshift = ushift @ oshift @ lshift.T
				mdiag += mshift
				odiag += oshift
				self.diag[i] = np.copy(mdiag[:-i, :-i]), np.copy(odiag[:-i, i-1:])
		return self.diag[n]

	def count_consec(self, n, player):
		if n == 1:
			return np.count_nonzero(self.state == player)

		if self.rconsec[n-1] is None:
			hori = self.consec_hor(n)
			vert = self.consec_ver(n)
			mdiag, odiag = self.consec_diag(n)
			consecs = [hori, vert, mdiag, odiag]
			
			count_consec = lambda player: lambda matrix: np.count_nonzero(matrix == n*player)
			self.rconsec[n-1] = sum(map(count_consec(self.player('r')), consecs))
			self.yconsec[n-1] = sum(map(count_consec(self.player('y')), consecs))

		if player == self.player('r'):
			return self.rconsec[n-1]
		else:
			return self.yconsec[n-1]

	def successor(self, action):
		if action is not None:
			col = action
			row = min(np.nonzero(self.state[:, col] == 0)[0])
			state = np.copy(self.state)
			state[row, col] = self.turn
		else:
			state = self.state

		return ConnectFour(-self.turn, state)
