from enum import Enum
from settings import GAME_SIZE, REC_SIZE


class Directions(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4


class SnakeNode:
	position_x: int
	position_y: int

	def __init__(self, pos_x, pos_y):
		self.position_x = pos_x
		self.position_y = pos_y


class Snake:
	body: []
	direction: Directions
	
	def __init__(self):
		self.body = [SnakeNode(0, 0)]
		self.direction = Directions.RIGHT

	def change_direction(self, new_direction: Directions):
		self.direction = new_direction

	def move(self):
		for i in range(len(self.body) - 1, 0, -1):
			self.body[i] = SnakeNode(self.body[i - 1].position_x, self.body[i - 1].position_y)

		if self.direction == Directions.UP:
			self.body[0].position_y -= (REC_SIZE + 1)
			if self.body[0].position_y < 0 or self.snake_overlaps():
				return False
		elif self.direction == Directions.DOWN:
			self.body[0].position_y += (REC_SIZE + 1)
			if self.body[0].position_y > GAME_SIZE or self.snake_overlaps():
				return False
		elif self.direction == Directions.LEFT:
			self.body[0].position_x -= (REC_SIZE + 1)
			if self.body[0].position_x < 0 or self.snake_overlaps():
				return False
		elif self.direction == Directions.RIGHT:
			self.body[0].position_x += (REC_SIZE + 1)
			if self.body[0].position_x > GAME_SIZE or self.snake_overlaps():
				return False
		return True

	def eat(self):
		self.body.append(SnakeNode(-100, -100))

	def snake_overlaps(self):
		for body_part in self.body[1:]:
			if self.body[0].position_x == body_part.position_x and self.body[0].position_y == body_part.position_y:
				return True
		return False
