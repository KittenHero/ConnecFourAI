from signal import setitimer, signal, ITIMER_REAL, SIGALRM
from argparse import ArgumentTypeError
from re import compile

class Timeout:
	def __init__(self, ms):
		self.ms = ms
	
	def handle_timeout(self, signum, frame):
		raise TimeoutError()
	
	def __enter__(self):
		signal(SIGALRM, self.handle_timeout)
		setitimer(ITIMER_REAL, self.ms * 0.001)
		
	def __exit__(self, exc_type, exc_value, exc_traceback):
		if exc_type is TimeoutError:
			return True
		else:
			setitimer(ITIMER_REAL, 0)

def board_validator(string):
	match = compile(r'((?:\.|r|y){7},?){6}').match(string)
	if not match or match.group() != string:
		raise ArgumentTypeError('Invalid board: {}'.format(string))
	return string

