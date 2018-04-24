class DefaultEval:
	def __init__(self, player):
		self.player = player
		if self.player.startswith('r'):
			self.opponent = 'yellow'
		else:
			self.opponent = 'red'
		self.max = 10000
		self.min = - self.max

	def __call__(self, state):
		if state.game_over:
			return (1 - (state.winner != self.player) * 2) * self.max
		return self.default_score(state, state.player(self.player)) - self.default_score(state, state.player(self.opponent))
	
	@staticmethod
	def default_score(state, player):
		consec = [state.count_consec(i, player) for i in range(1, 4)]
		return consec[0] + 10 * consec[1] + 80 * consec[2]

class EnhancedEval:
	max = 0xffff
	min = -0xffff
	def __init__(self, player):
		self.player = player
		if self.player.startswith('r'):
			self.opponent = 'yellow'
		else:
			self.opponent = 'red'

	def __call__(self, state):
		if state.game_over:
			if not state.winner:
				return 0
			elif state.winner == self.opponent:
				return self.min
			else:
				return self.max
		else:
			return self.remain_winning(state, self.player) - self.remain_winning(state, self.opponent)
		
	@staticmethod
	def remain_winning(state, player):
		player = state.player(player)
		board = state.state[player]
		potential = state.state[player ^ 1] ^ 0x7f7f_7f7f_7f7f
		
		hp = potential & (potential >> 1)
		mp = potential & (potential >> 7)
		vp = potential & (potential >> 8)
		op = potential & (potential >> 9)
		
		hp = hp & (hp >> 2)
		mp = mp & (mp >> 14)
		vp = vp & (vp >> 16)
		op = op & (op >> 18)
		
		h2 = board & (board >> 1)
		m2 = board & (board >> 7)
		v2 = board & (board >> 8)
		o2 = board & (board >> 9)
		
		h3 = (board & (h2 >> 1)) & (hp | (hp << 1))
		m3 = (board & (m2 >> 7)) & (hp | (hp << 7))
		v3 = (board & (v2 >> 8)) & (hp | (hp << 8))
		o3 = (board & (o2 >> 9)) & (hp | (hp << 9))
		
		h2 = h2 & (hp | (hp << 2))
		m2 = m2 & (mp | (mp << 14))
		v2 = v2 & (vp | (vp << 16))
		o2 = o2 & (op | (op << 18))
		
		counts = [
			sum(map(state.bit_count_48, boards))
			for boards in (
				(hp, mp, vp, op),
				(h2, m2, v2, o2),
				(h3, m3, v3, o3)
			)
		]
		
		return counts[0] + counts[1] + 4*counts[2]
