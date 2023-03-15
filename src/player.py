import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, pos) -> None:
		super().__init__()
		# TO UPDATE vvvv
		self.image = pygame.Surface((64, 64))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)
		self.can_jump = True
		# TO UPDATE ^^^^
		self.movement_speed = 600
		self.direction = pygame.Vector2()

	def get_input(self) -> None:
		keys_state = pygame.key.get_pressed()
		if keys_state[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys_state[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if keys_state[pygame.K_SPACE] and self.can_jump:
			self.direction.y = -1600
			self.can_jump = False
		else:
			self.direction.y += 25

	def update(self) -> None:
		self.get_input()
