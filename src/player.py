import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, pos) -> None:
		super().__init__()
		self.image = pygame.Surface((64, 64))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)