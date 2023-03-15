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
		floor.image = pygame.Surface((1200, 50))
		floor.image.fill('gray')
		floor.rect = floor.image.get_rect(topleft=(0, 650))
		self.blocks.add(floor)

		obst = pygame.sprite.Sprite()
		obst.image = pygame.Surface((100, 100))
		obst.rect = obst.image.get_rect(topleft=(400, 100))
		obst.image.fill('gray')
		self.blocks.add(obst)
# TO REMOVE ^^^^

	def run(self, dt) -> None:
		self.display_surface.fill('black')

		self.blocks.draw(self.display_surface)

		self.player.update(dt)
		self.handle_horizontal_collision(dt)
		self.handle_vertical_collision(dt)
		self.player.draw(self.display_surface)

	def handle_horizontal_collision(self, dt):
		player = self.player.sprite
		player.rect.x += player.direction.x	* player.movement_speed * dt
		for block in self.blocks.sprites():
			if block.rect.colliderect(player):
				if player.direction.x > 0:
					player.rect.right = block.rect.left
				elif player.direction.x < 0:
					player.rect.left = block.rect.right

	def handle_vertical_collision(self, dt):
		player = self.player.sprite
		player.rect.y += player.direction.y * player.falling_speed * dt
		for block in self.blocks.sprites():
			if block.rect.colliderect(player):
				if player.direction.y > 0:
					player.rect.bottom = block.rect.top
					player.direction.y = 0
				elif player.direction.y < 0:
					player.rect.top = block.rect.bottom
					player.direction.y = 0
