import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, pos) -> None:
		super().__init__()
		# TO UPDATE vvvv
		self.image = pygame.Surface((64, 64))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)
		# TO UPDATE ^^^^

		self.gravity = 8
		self.movement_speed = 600
		self.falling_speed = 100
		self.direction = pygame.Vector2()

	def get_input(self) -> None:
		keys_state = pygame.key.get_pressed()
		if keys_state[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys_state[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

	def handle_gravity(self) -> None:
		if pygame.key.get_pressed()[pygame.K_SPACE]:
			self.direction.y = -10
		else:
			self.direction.y += .2

	def update(self, dt) -> None:
		self.get_input()
		self.handle_gravity()
		self.rect.x += self.direction.x	* self.movement_speed * dt
		self.rect.y += self.direction.y * self.falling_speed * dt