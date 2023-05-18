import time


class Model:
	score_func: float
	moves_left: int

	def __init__(self):
		self.start = None
		self.score_func = 0
		self.moves_left = 10

	def start_timer(self):
		self.start = time.time()
	
	def evaluate_function(self):
		self.score_func = max(0.0, self.score_func - ((time.time() - self.start) * self.score_func * 0.03))
		self.start = time.time()

