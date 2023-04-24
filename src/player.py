import pygame
import config

class Player(pygame.sprite.Sprite):
	def __init__(self, pos) -> None:
		super().__init__()
		# TO UPDATE vvvv
		self.image = pygame.Surface((64, 64))
		self.image.fill('red')
		self.rect = self.image.get_rect(topleft = pos)
		self.can_jump = True
		# TO UPDATE ^^^^
		# TODO: Settings file
		self.movement_speed = config.PLAYER_MOVEMENT_SPEED
		self.gravity = config.GRAVITY
		self.jump_speed = config.PLAYER_JUMP_SPEED
		# vector storing where and how fast player wants to go
		self.direction = pygame.Vector2()

# NIE WIEM CZEMU LOSOWO SKACZE WYZEJ STRZELAM ZE PRZEZ PROBLEMY Z FLOATEM :D
	def get_direction(self) -> None:
		keys_state = pygame.key.get_pressed()
		if keys_state[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys_state[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if keys_state[pygame.K_SPACE] and self.can_jump:
			self.direction.y = self.jump_speed
			self.can_jump = False
		else:
			self.direction.y += self.gravity

	def update(self) -> None:
		self.get_direction()
		self.rect.x += self.direction.x
