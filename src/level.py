import pygame
from player import Player
from config import *
from block import *

from block import Block
class Level:
    def __init__(self, level_interface_data, surface) -> None:
        self.display_surface = surface
        self.world_x_shift = 0
        self.level_layout = level_interface_data
        self.setup(self.level_layout)
        
        
    def setup(self, level_layout_data) -> None:
        # Set up the player
        self.player = pygame.sprite.GroupSingle()
        
        # Add blocks to self.blocks from level_data
        self.blocks = pygame.sprite.Group()
        
        for row_index, row in enumerate(level_layout_data):
            for col_index, cell in enumerate(row):
                
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                # add obstacle on map
                if cell == 'H':
                    new_block = Block((x,y), BLOCK_SIZE, "black")
                    self.blocks.add(new_block)
                # add grass on map
                elif cell == 'X':
                    new_block = Block((x,y), BLOCK_SIZE, "green")
                    self.blocks.add(new_block) 
                
                # add coins on map
                elif cell == 'C':
                    new_block = Block((x,y), BLOCK_SIZE, "yellow")
                    self.blocks.add(new_block) 
                
                # add player on map
                elif cell == 'P':
                    self.player.add(Player((x, y)))        

    
    def set_screen_movement(self) -> None:
        player = self.player.sprite
        # if player want to go to the right size, move screen
        if player.rect.centerx >= DISPLAY_WIDTH//2 and player.direction.x == 1:
            self.world_x_shift = -PLAYER_MOVEMENT_SPEED
            player.movement_speed = 0
        # if player want to go to the left size, move screen
        elif player.rect.centerx <= BLOCK_SIZE*2 and player.direction.x == -1:
            self.world_x_shift = PLAYER_MOVEMENT_SPEED
            player.movement_speed = 0
        # else don't move screen horizontally
        else:
            self.world_x_shift = 0
            player.movement_speed = PLAYER_MOVEMENT_SPEED

    
    def run(self, dt) -> None:
        # reset the screen
        self.display_surface.fill('light blue')

        # calculate where the player want to go
        self.player.update()
              
        self.set_screen_movement()
        # update blocks on screen
        self.blocks.update(self.world_x_shift * dt)
        
        # check colisions and set player's position
        self.handle_horizontal_collision(dt)
        self.handle_vertical_collision(dt)
        
        # draw all the blocks
        self.blocks.draw(self.display_surface)
        
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