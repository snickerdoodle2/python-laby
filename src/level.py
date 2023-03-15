import pygame
from player import Player

class Level:
	def __init__(self, surface) -> None:
		self.display_surface = surface

	def setup(self) -> None:
		self.player = pygame.sprite.GroupSingle()
		# Prepare lists for blocks 
		self.blocks = pygame.sprite.Group()
# TO REMOVE vvvv -- Only to debug
		self.player.add(Player((300, 300)))
		floor = pygame.sprite.Sprite()
		floor.image = pygame.Surface((1200, 50))
		floor.image.fill('gray')
		floor.rect = floor.image.get_rect(topleft=(0, 650))
		self.blocks.add(floor)

		obst = pygame.sprite.Sprite()
		obst.image = pygame.Surface((100, 100))
		obst.rect = obst.image.get_rect(topleft=(400, 400))
		obst.image.fill('gray')
		self.blocks.add(obst)
# TO REMOVE ^^^^


	def handle_horizontal_collision(self, dt):
		player = self.player.sprite
		# update player's position
		player.rect.x += player.direction.x	* player.movement_speed * dt		
		for block in self.blocks.sprites():
			# check if player collides with a block
			if block.rect.colliderect(player):
				# if player is to the left of the block
				if player.direction.x > 0:
					player.rect.right = block.rect.left
				# if player is to the right of the block
				elif player.direction.x < 0:
					player.rect.left = block.rect.right

	# TODO: REMOVE MID-AIR JUMP!!
	def handle_vertical_collision(self, dt):
		player = self.player.sprite
		# update player's position
		player.rect.y += player.direction.y * dt
		for block in self.blocks.sprites():
			# check if player collides with a block
			if block.rect.colliderect(player):
				# if player is above the block
				if player.direction.y > 0:
					player.can_jump = True
					player.rect.bottom = block.rect.top
					player.direction.y = 0
				# if player is under the block
				elif player.direction.y < 0:
					player.rect.top = block.rect.bottom
					player.direction.y = 0
					


	def run(self, dt) -> None:
		# reset the screen
		self.display_surface.fill('black')

		# draw all the blocks
		self.blocks.draw(self.display_surface)

		# calculate where the player want to go
		self.player.update()
		# check colisions and set player's position
		self.handle_horizontal_collision(dt)
		self.handle_vertical_collision(dt)
		# draw the player
		self.player.draw(self.display_surface)