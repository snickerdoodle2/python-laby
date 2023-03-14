import pygame
from player import Player

class Level:
	def __init__(self, surface) -> None:
		self.display_surface = surface

	def setup(self) -> None:
		self.player = pygame.sprite.GroupSingle()
		self.blocks = pygame.sprite.Group()
# TO REMOVE vvvv
		self.player.add(Player((300, 300)))
		floor = pygame.sprite.Sprite()
		floor.image = pygame.Surface((1200, 300))
		floor.image.fill('gray')
		floor.rect = floor.image.get_rect(topleft=(0, 400))
		self.blocks.add(floor)
# TO REMOVE ^^^^

	def run(self, dt) -> None:
		self.display_surface.fill('black')

		self.blocks.draw(self.display_surface)

		self.player.update(dt)
		self.player.draw(self.display_surface)