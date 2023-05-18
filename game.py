import pygame
from pygame.locals import *
from pygame.surface import Surface
from settings import *
from snake import Snake, SnakeNode, Directions
from model import Model
import random


class Game:
	surface: Surface
	apple: SnakeNode

	def __init__(self):
		pygame.init()

		self.surface = pygame.display.set_mode((GAME_SIZE, GAME_SIZE))
		self.apple = SnakeNode(-100, -100)

		self.model = Model()

		random_x = random.randint(0, GAME_SIZE / (REC_SIZE + 1) - 1) * (REC_SIZE + 1)
		random_y = random.randint(0, GAME_SIZE / (REC_SIZE + 1) - 1) * (REC_SIZE + 1)

		random_direction = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]

		if random_x < GAME_SIZE / 2:
			random_direction.remove(Directions.LEFT)
		if random_x > GAME_SIZE / 2:
			random_direction.remove(Directions.RIGHT)
		if random_y < GAME_SIZE / 2:
			random_direction.remove(Directions.UP)
		if random_y > GAME_SIZE / 2:
			random_direction.remove(Directions.DOWN)

		self.player = Snake(random_x, random_y, random_direction[random.randint(0, len(random_direction) - 1)])
		self.clock = pygame.time.Clock()
		self.display_apple()
		self.points_threshold = 3

	def draw_snake(self, player_: Snake):
		for body_part in player_.body:
			pygame.draw.rect(self.surface, SNAKE_COLOR,
			                 pygame.Rect(body_part.position_x, body_part.position_y, REC_SIZE, REC_SIZE), border_radius=7)
		# pygame.display.flip()

	def clean_snake(self, player_: Snake):
		pygame.draw.rect(self.surface, (0, 0, 0),
		                 pygame.Rect(player_.body[-1].position_x, player_.body[-1].position_y, REC_SIZE, REC_SIZE))
		# pygame.display.flip()

	def display_apple(self):
		pygame.draw.rect(self.surface, (0, 0, 0),
		                 pygame.Rect(self.apple.position_x, self.apple.position_y, REC_SIZE, REC_SIZE))
		random_x = random.randint(0, GAME_SIZE/(REC_SIZE + 1) - 1) * (REC_SIZE + 1)
		random_y = random.randint(0, GAME_SIZE/(REC_SIZE + 1) - 1) * (REC_SIZE + 1)
		body_xs, body_ys = self.player.get_cords_arrays()
		while random_x in body_xs and random_y in body_ys:
			random_x = random.randint(0, GAME_SIZE / (REC_SIZE + 1) - 1) * (REC_SIZE + 1)
			random_y = random.randint(0, GAME_SIZE / (REC_SIZE + 1) - 1) * (REC_SIZE + 1)
		self.apple.position_x = random_x
		self.apple.position_y = random_y
		pygame.draw.rect(self.surface, (217, 2, 2), pygame.Rect(random_x, random_y, REC_SIZE, REC_SIZE), border_radius=7)

	def distance_to_walls(self):
		head_x = self.player.body[0].position_x/(REC_SIZE + 1) + 1
		head_y = self.player.body[0].position_y/(REC_SIZE + 1) + 1
		board_bounds = GAME_SIZE/(REC_SIZE + 1) + 1

		return [head_y, board_bounds - head_x, board_bounds - head_y, head_x]

	def distance_to_apple(self):
		# TODO implement
		pass

	def distance_to_nearest_body_part(self):
		head_x = self.player.body[0].position_x / (REC_SIZE + 1) + 1
		head_y = self.player.body[0].position_y / (REC_SIZE + 1) + 1
		top_dist = bot_dist = left_dist = right_dist = GAME_SIZE/(REC_SIZE + 1)
		for body_part in self.player.body[1:]:
			body_x = body_part.position_x / (REC_SIZE + 1) + 1
			body_y = body_part.position_y / (REC_SIZE + 1) + 1
			if body_x >= head_x and body_y == head_y and body_x - head_x < right_dist:
				right_dist = body_x - head_x
			if body_x <= head_x and body_y == head_y and head_x - body_x < left_dist:
				left_dist = head_x - body_x
			if body_y >= head_y and body_x == head_x and body_y - head_y < bot_dist:
				bot_dist = body_y - head_y
			if body_y <= head_y and body_x == head_x and head_y - body_y < top_dist:
				top_dist = head_y - body_y

		return [top_dist, right_dist, bot_dist, left_dist]


	def run(self):

		running = True

		while running:
			for event in pygame.event.get():
				if event.type == WINDOWCLOSE or event.type == QUIT:
					running = False
				elif event.type == KEYDOWN:
					if event.key == K_UP:
						self.player.change_direction(Directions.UP)
						self.model.moves_left -= 1
					elif event.key == K_DOWN:
						self.player.change_direction(Directions.DOWN)
						self.model.moves_left -= 1
					elif event.key == K_RIGHT:
						self.player.change_direction(Directions.RIGHT)
						self.model.moves_left -= 1
					elif event.key == K_LEFT:
						self.player.change_direction(Directions.LEFT)
						self.model.moves_left -= 1
			self.clean_snake(self.player)
			if not self.player.move():
				running = False
			if self.player.body[0].position_x == self.apple.position_x and \
				self.player.body[0].position_y == self.apple.position_y:
				self.model.score_func = self.model.score_func * 1.3 + 1.0
				if self.points_threshold == 1:
					self.model.start_timer()
				elif self.points_threshold <= 0:
					self.model.evaluate_function()
				self.model.moves_left = 10
				self.player.eat()
				self.display_apple()
				self.points_threshold -= 1
			self.draw_snake(self.player)
			pygame.display.flip()
			self.clock.tick(5)
			distances = self.distance_to_nearest_body_part()
			# distances = self.distance_to_walls()
			print(distances)


		print("Final score: ", self.model.score_func)
