import time


class Model:
	score_func: float
	moves_left: int

	def __init__(self):
		self.score_func = 0
		self.start = time.time()
		self.moves_left = 10

	def evaluate_function(self):
		self.score_func -= (time.time() - self.start)/10

