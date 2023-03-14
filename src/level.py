import pygame
from player import Player

class Level:
	def __init__(self, surface) -> None:
		self.display_surface = surface

	def setup(self) -> None:
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player((300, 300)))

# TO REMOVE vvvv
		floor = pygame.sprite.Sprite()
		floor.image = pygame.Surface((1200, 300))
		floor.image.fill('gray')
		floor.rect = floor.image.get_rect(topleft=(0, 400))

		self.floor_group = pygame.sprite.GroupSingle()
		self.floor_group.add(floor)
# TO REMOVE ^^^^

	def run(self) -> None:
		self.floor_group.draw(self.display_surface)
		self.player.draw(self.display_surface)