import pygame
from player import Player

class Level:
	def __init__(self, surface) -> None:
		self.display_surface = surface

	def setup(self, levelData) -> None:
		self.player = pygame.sprite.GroupSingle()
		# Prepare lists for blocks 
		self.blocks = pygame.sprite.Group()
		self.player.add(Player((300, 300)))


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
		# self.handle_horizontal_collision(dt)
		# self.handle_vertical_collision(dt)
		# draw the player
		self.player.draw(self.display_surface)