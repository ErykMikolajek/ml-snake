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

		# self.score = 0
		self.model = Model()
		self.player = Snake()
		self.clock = pygame.time.Clock()
		self.display_apple()

	def draw_snake(self, player_: Snake):
		for body_part in player_.body:
			pygame.draw.rect(self.surface, SNAKE_COLOR,
			                 pygame.Rect(body_part.position_x, body_part.position_y, REC_SIZE, REC_SIZE))
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
		while self.surface.get_at((random_x, random_y)) != (0, 0, 0):
			random_x = random.randint(0, GAME_SIZE/(REC_SIZE + 1) - 1) * (REC_SIZE + 1)
			random_y = random.randint(0, GAME_SIZE/(REC_SIZE + 1) - 1) * (REC_SIZE + 1)
		self.apple.position_x = random_x
		self.apple.position_y = random_y
		pygame.draw.rect(self.surface, (217, 2, 2), pygame.Rect(random_x, random_y, REC_SIZE, REC_SIZE))
		# pygame.display.flip()

	def distance_to_walls(self):
		top_dist = self.player.body[0].position_y/(REC_SIZE + 1)
		bot_dist = (GAME_SIZE - self.player.body[0].position_y)/(REC_SIZE + 1)
		left_dist = self.player.body[0].position_x/(REC_SIZE + 1)
		right_dist = (GAME_SIZE - self.player.body[0].position_x) / (REC_SIZE + 1)
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
				self.model.score_func += 1.0
				self.model.moves_left = 10
				self.player.eat()
				self.display_apple()
			self.draw_snake(self.player)
			pygame.display.flip()
			self.clock.tick(5)
			distances = self.distance_to_walls()
			print("Distances: ", distances)

		self.model.evaluate_function()
		print(self.model.score_func)
