from functools import reduce, partial
from itertools import chain

class ConnectFourBit:
	width = 7
	height = 6
	rmask = 0b01010101010101
	ymask = 0b10101010101010
	
	def __init__(self, turn, state=None):
		if state is not None:
			self.state = state
		else:
			self.state = [0]*6
		
		self.turn = turn
		self.consecs = [None]*4
		self.winner = None

	@classmethod
	def player(cls, player):
		if player.startswith('r'):
			return cls.rmask
		elif player.startswith('y'):
			return cls.ymask
		else:
			assert 0b00, 'Invalid player'

	@classmethod
	def from_string(cls, turn, state):
		state = list(map(
			partial(int, base=2),
			state
				.replace('r', '01')
				.replace('y', '10')
				.replace('.', '00')
				.split(',')
		))
		return cls(cls.player(turn), state)
	
	@property
	def legal_actions(self):
		if self.game_over:
			return [None]
		else:
			return [None] + [i for i in range(self.width) if not self.state[-1] & (0b11 << 2*(self.width - 1 - i))]
	
	@property
	def game_over(self):
		if self.winner is not None:
			return True
		elif self.count_consec(4, self.player('r')):
			self.winner = 'red'
			return True
		elif self.count_consec(4, self.player('y')):
			self.winner = 'yellow'
			return True
		else:
			return False
	
	def successor(self, action):
		state = self.state[:]
		turn = (self.turn << 1) | (self.turn >> self.width * 2 - 1)
		if action is not None:
			mask = (0b11 << 2*(self.width - 1 - action))
			row = next(y for y in range(self.height) if not self.state[y] & mask)
			state[row] = state[row] | (mask & self.turn)
		return self.__class__(turn, state)
	
	def count_consec(self, n, player):
		if n == 1:
			self.consecs[0] = self.state
		elif self.consecs[n-1] is None: 
			h = [
				reduce(lambda acc, k: acc & (row >> k), range(0, 2*n, 2), self.rmask | self.ymask)
				for row in self.state
			]
			v, md, od = ([0]*(self.height + 1 - n) for _ in range(3))
			for i, rows in enumerate(zip(*(self.state[j:] for j in range(n)))):
				v[i] = reduce(lambda acc, row: acc & row, rows)
				od[i] = reduce(lambda acc, row: row & (acc >> 2), rows)
				md[i] = reduce(lambda acc, k: acc & (rows[k] >> 2*k), range(n), self.rmask | self.ymask)
			
			self.consecs[n-1] = list(chain(h, v, md, od))

		return sum(map(
			lambda row: self.bit_count_16(row & player),
			self.consecs[n-1]
		))
		
	@staticmethod
	def bit_count_16(x):
		if not x: return 0
		
		x = x - ((x >> 1) & 0x5555)
		x = (x & 0x3333) + ((x >> 2) & 0x3333)
		x = (x + (x >> 4)) & 0x0f0f
		return (x + (x >> 8)) & 0xff
