import pygame
from player import Player
from config import *
from block import *

from block import Block
class Level:
    def __init__(self, level_interface_data, surface) -> None:
        self.display_surface = surface
        self.setup(level_interface_data)
        
    def setup(self, level_data) -> None:
        # Upload blocks to self.blocks from level_data
        self.blocks = pygame.sprite.Group()
        
        for row_index, row in enumerate(level_data):
            for col_index, cell in enumerate(row):
                
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                
                if cell == 'X':
                    new_block = Block((x,y), BLOCK_SIZE)
                    self.blocks.add(new_block)
        
        # Set up the player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player((0, 64*8)))

                    


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