class ConnectFourBit:
	width  = 7
	height = 6
	
	def __init__(self, turn, state=None):
		if state is not None:
			self.state = state
		else:
			self.state = (0, 0)
		self.occupied = self.state[0] | self.state[1]
		self.turn = turn
		self.winner = None
		self.consecs = ([None]*4, [None]*4)

	@classmethod
	def player(cls, player):
		if player.startswith('r'):
			return 0
		elif player.startswith('y'):
			return 1
		else:
			assert 0, 'Invalid player'

	@classmethod
	def from_string(cls, turn, state):
		interleaved = int(
			state[::-1]
				.replace('r', '01')
				.replace('y', '10')
				.replace('.', '00')
				.replace(',', '00'),
			base=2
		)
		red    = cls.deinterleave_96(interleaved)
		yellow = cls.deinterleave_96(interleaved >> 1)
		return cls(cls.player(turn), (red, yellow))
	
	@staticmethod
	def deinterleave_96(x): # Sean Eron Anderson : bit twiddling hacks
		x = x & 0x5555_5555_5555_5555_5555_5555
		x = (x | (x >> 1)) & 0x3333_3333_3333_3333_3333_3333
		x = (x | (x >> 2)) & 0x0f0f_0f0f_0f0f_0f0f_0f0f_0f0f
		x = (x | (x >> 4)) & 0x00ff_00ff_00ff_00ff_00ff_00ff
		x = (x | (x >> 8)) & 0xffff_0000_ffff_0000_ffff
		x = (x | (x >> 16)) & 0xffff_0000_0000_ffff_ffff
		return (x | (x >> 32)) & 0xffff_ffff_ffff
	
	@property
	def legal_actions(self):
		if self.game_over:
			return ()
		else:
			return [
				i for i in range(self.width)
				if not 1 & (self.occupied >> 40 + i)
			]
	
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
			return self.width == self.bit_count_8(self.occupied >> 40)
	
	
	def successor(self, action):
		red, yellow = self.state
		turn = self.turn ^ 1
		if action != '':
			rmask = 1 << action
			row = next(
				y for y in range(self.height)
				if not (self.occupied >> y*8) & rmask
			)
			if self.turn & 1:
				yellow |= rmask << row*8
			else:
				red |= rmask << row*8
		return self.__class__(turn, (red, yellow))
	
	def count_consec(self, n, player):
		consec = self.consecs[player]
		if consec[n-1] is None:
			consec[n-1] = self.b_count_consec(n, self.state[player])
		return consec[n-1]
	
	@classmethod
	def b_count_consec(cls, n, board):
		if n == 1: return cls.bit_count_48(board)
		hz_shift = board & (board >> 1)
		vt_shift = board & (board >> 8)
		md_shift = board & (board >> 9)
		od_shift = board & (board >> 7)
		if n > 2:
			if n == 3:
				hz_shift = board & (hz_shift >> 1)
				vt_shift = board & (vt_shift >> 8)
				md_shift = board & (md_shift >> 9)
				od_shift = board & (od_shift >> 7)
			else:
				hz_shift = hz_shift & (hz_shift >> 2)
				vt_shift = vt_shift & (vt_shift >> 16)
				md_shift = md_shift & (md_shift >> 18)
				od_shift = od_shift & (od_shift >> 14)
				return hz_shift or vt_shift or md_shift or vt_shift
		
		return sum(map(
			cls.bit_count_48,
			(hz_shift, vt_shift, md_shift, od_shift)
		))
	
	@staticmethod
	def bit_count_48(x):
		if not x: return 0
		# wikipedia : Hamming weight
		x -= (x >> 1) & 0x5555_5555_5555
		x = (x & 0x3333_3333_3333) + ((x >> 2) & 0x3333_3333_3333)
		x = (x + (x >> 4)) & 0x0f0f_0f0f_0f0f
		return (x * 0x0101_0101_0101_0101 >> 56) & 0x3f
	
	@staticmethod
	def bit_count_8(x):
		if not x: return 0
		
		x -= (x >> 1) & 0x55
		x = (x & 0x33) + ((x >> 2) & 0x33)
		return (x + (x >> 4)) & 0x0f
	
	def __hash__(self):
		return hash(self.state)
	
	def __eq__(self, other):
		return isinstance(other, self.__class__) and other.state == self.state
	
	def __repr__(self):
		return 'ConnectFourBit({}, {})'.format(self.turn, self.state)
	
	def __str__(self):
		red, yellow = self.state
		rows = [0]*self.height
		for y in range(self.height):
			r = [0]*self.width
			for x in range(self.width):
				r[x] = 'r' if red & 1 else 'y' if yellow & 1 else '.'
				red >>= 1
				yellow >>= 1
			rows[y] = ''.join(r)
			red >>= 1
			yellow >>= 1
		rows = ','.join(rows)
			
		return '%s %s' % (rows, 'yellow' if self.turn else 'red')
