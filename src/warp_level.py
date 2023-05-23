from level import Level
import pygame
from block import Block, Portal
from config import BLOCK_SIZE
from player import Player
class WarpLevel(Level):
    def __init__(self, level_interface_data, surface) -> None:
        self.display_surface = surface
        self.world_x_shift = 0
        self.level_layout = level_interface_data
        self.active_powerup = 0
        self.setup(self.level_layout)
        self.status = 'running'

    def setup(self, level_layout_data) -> None:
        self.player = pygame.sprite.GroupSingle()

        # Add blocks to self.blocks from level_data
        self.blocks = pygame.sprite.Group()
        self.portal_one = pygame.sprite.Group()
        self.portal_two = pygame.sprite.Group()
        self.portal_three = pygame.sprite.Group()



        for row_index, row in enumerate(level_layout_data):
            for col_index, cell in enumerate(row):

                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE
                # add obstacle on map
                if cell == 'H':
                    new_block = Block((x, y), "assets/brick.png")
                    self.blocks.add(new_block)

                # add grass on map
                elif cell == 'X':
                    new_block = Block((x, y), "assets/grass.png")
                    self.blocks.add(new_block)

                elif cell == 'P':
                    self.player.add(Player((x, y)))

                elif cell == '1':
                    self.portal_one.add(Portal((x,y), 'chartreuse'))

                elif cell == '2':
                    self.portal_two.add(Portal((x,y), 'coral'))

                elif cell == '3':
                    self.portal_three.add(Portal((x,y), 'chartreuse'))

    def run(self, dt) -> None:
        # reset the screen
        self.display_surface.fill('light blue')

        # calculate where the player want to go
        self.player.update()

        # changing enemy direction while hitting an object
        self.set_screen_movement()

        # move blocks, coins and flag on screen
        self.blocks.update(self.world_x_shift * dt)
        self.portal_one.update(self.world_x_shift * dt)
        self.portal_two.update(self.world_x_shift * dt)
        self.portal_three.update(self.world_x_shift * dt)

        self.status = self.handle_portal_collision()

        # check colisions and set player's position
        self.handle_horizontal_collision(dt)
        self.handle_vertical_collision(dt)

        # draw blocks, coins, flag and enemies
        self.blocks.draw(self.display_surface)
        self.portal_one.draw(self.display_surface)
        self.portal_two.draw(self.display_surface)
        self.portal_three.draw(self.display_surface)

        # draw the player
        self.player.draw(self.display_surface)

    def handle_portal_collision(self):
        if self.handle_single_portal_collision(self.portal_one): return '1'
        if self.handle_single_portal_collision(self.portal_two): return '2'
        if self.handle_single_portal_collision(self.portal_three): return '3'
        return 'running'

    def handle_single_portal_collision(self, portals):
        player  = self.player.sprite
        for portal in portals.sprites():
            if portal.rect.colliderect(player): return True
        return False
            
