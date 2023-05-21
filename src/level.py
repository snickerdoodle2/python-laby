import pygame
from config import BLOCK_SIZE, DISPLAY_WIDTH, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_SPEED
from enemy import GroundEnemy, FlyingEnemy
from player import Player


from block import Block, Coin, Powerup
class Level:
    def __init__(self, level_interface_data, surface) -> None:
        self.display_surface = surface
        self.world_x_shift = 0
        self.level_layout = level_interface_data
        self.setup(self.level_layout)
        self.status = 'running'
        self.active_powerup = 0
        self.powerup_duration = 1000
        
        self.start_time = pygame.time.get_ticks()
        
        self.font = pygame.font.Font('assets/Pixeboy.ttf', 32)
        
    def setup(self, level_layout_data) -> None:
        # Set up the player
        self.player = pygame.sprite.GroupSingle()
        
        # Add blocks to self.blocks from level_data
        self.blocks = pygame.sprite.Group()

        # Add flag
        self.flag = pygame.sprite.Group()
        
        # Add coins on map
        self.coins = pygame.sprite.Group()
        
        # Add enemies on map
        self.ground_enemies = pygame.sprite.Group()
        self.flying_enemies = pygame.sprite.Group()
        
        self.powerups = pygame.sprite.Group()
        
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
                    new_coin = Coin((x,y), BLOCK_SIZE//1.5, 50)
                    self.coins.add(new_coin)
                
                # add player on map
                elif cell == 'P':
                    self.player.add(Player((x, y)))
                
                # add enemies on ground 
                elif cell == 'E':
                    new_enemy = GroundEnemy((x,y), BLOCK_SIZE)
                    self.ground_enemies.add(new_enemy)
                    
                # add flying enemies
                elif cell == 'B':
                    new_enemy = FlyingEnemy((x,y), BLOCK_SIZE)
                    self.flying_enemies.add(new_enemy)
                
                # add flag on map
                elif cell == 'F':
                    new_block = Block((x,y), BLOCK_SIZE, "pink")
                    self.flag.add(new_block)
                    
                # add power up on map
                elif cell == 'U':
                    new_powerup = Powerup((x,y), BLOCK_SIZE, 600)
                    self.powerups.add(new_powerup)

    
    def set_screen_movement(self) -> None:
        player = self.player.sprite
        # if player want to go to the right size, move screen
        if player.rect.centerx >= DISPLAY_WIDTH//2 and player.direction.x == 1:
            self.world_x_shift = -(PLAYER_MOVEMENT_SPEED + self.active_powerup)
            player.movement_speed = 0
        # if player want to go to the left size, move screen
        elif player.rect.centerx <= BLOCK_SIZE*2 and player.direction.x == -1:
            self.world_x_shift = PLAYER_MOVEMENT_SPEED + self.active_powerup
            player.movement_speed = 0
        # else don't move screen horizontally
        else:
            self.world_x_shift = 0
            player.movement_speed = PLAYER_MOVEMENT_SPEED + self.active_powerup

    
    def run(self, dt) -> None:
        # reset the screen
        self.display_surface.fill('light blue')

        # calculate where the player want to go
        self.player.update()
              
        # changing enemy direction while hitting an object
        self.handle_ground_enemy_collision_with_objects(dt)
        self.set_screen_movement()
        
        # move blocks, coins and flag on screen
        self.blocks.update(self.world_x_shift * dt)
        self.coins.update(self.world_x_shift * dt)
        self.flag.update(self.world_x_shift * dt)
        self.ground_enemies.update(self.world_x_shift * dt)
        self.flying_enemies.update(self.world_x_shift * dt)
        self.powerups.update(self.world_x_shift * dt)

        
        # check colisions and set player's position
        self.handle_horizontal_collision(dt)
        self.handle_vertical_collision(dt)
        
        # coin collecting
        self.handle_coin_collision()
        
        # getting powerups
        self.handle_powerup_collision()
        self.handle_powerup_duration()
        
        # handlin collisions with enemies
        self.handle_collision_with_ground_enemy()
        self.handle_collision_with_flying_enemy(dt)
        
        # draw blocks, coins, flag and enemies
        self.blocks.draw(self.display_surface)
        self.coins.draw(self.display_surface)
        self.flag.draw(self.display_surface)
        self.ground_enemies.draw(self.display_surface)
        self.flying_enemies.draw(self.display_surface)
        self.powerups.draw(self.display_surface)
        
        
        # draw the player
        self.player.draw(self.display_surface)

        self.handle_flag_collision()
        
        # render score text  
        score_text = self.font.render(str(self.player.sprite.score).zfill(8), True, (255, 255, 255))        
        score_rect = score_text.get_rect()
        score_rect.center = (DISPLAY_WIDTH - 80, 30)
        self.display_surface.blit(score_text, score_rect)

        # render timer text
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time)/1000
        timer_text = self.font.render("Time: " + str(elapsed_time), True, (255, 255, 255))
        self.display_surface.blit(timer_text, (30, 30))
        
        if self.player.sprite.dead:
            self.status = 'dead'
            

    # collision handler for enemies on ground
    def handle_ground_enemy_collision_with_objects(self, dt) -> None:
        for enemy in self.ground_enemies.sprites():
            enemy.rect.x += round(enemy.direction.x * (PLAYER_MOVEMENT_SPEED//3) * dt)                        
            for block in self.blocks.sprites():
                if enemy.rect.colliderect(block):
                    if enemy.direction.x == 1:
                        enemy.rect.right = block.rect.left
                    else:
                        enemy.rect.left = block.rect.right

                    enemy.direction.x *= -1
                    
    # collision handler for enemies on ground
    def handle_collision_with_ground_enemy(self) -> None:
        player = self.player.sprite

        for enemy in self.ground_enemies.sprites():
            # check if player collides with a enemy
            if enemy.rect.colliderect(player):
                # if player ran into enemy 💀
                if player.rect.bottom <= enemy.rect.top+10:
                    player.coin_obtained()
                    player.rect.bottom = enemy.rect.top
                    player.direction.y = PLAYER_JUMP_SPEED//2
                    self.ground_enemies.remove(enemy)
                # else if player is above the enemy
                else:
                    self.player.sprite.dead = True

    def handle_collision_with_flying_enemy(self, dt) -> None:
        player = self.player.sprite
        
        for enemy in self.flying_enemies.sprites():
            enemy.rect.x += round(enemy.direction.x * (PLAYER_MOVEMENT_SPEED//3) * dt)
            
        for enemy in self.flying_enemies.sprites():
            # check if player collides with a enemy
            if enemy.rect.colliderect(player):
                # if player is above enemy
                if player.rect.bottom <= enemy.rect.top+10:
                    player.coin_obtained()
                    player.rect.bottom = enemy.rect.top
                    player.direction.y = PLAYER_JUMP_SPEED//2
                    self.flying_enemies.remove(enemy)
                # if player is under enemy
                elif player.rect.top >= enemy.rect.bottom-10:
                    player.coin_obtained()
                    player.rect.top = enemy.rect.bottom
                    player.direction.y = 0
                    self.flying_enemies.remove(enemy)
                # if player ran into enemy 💀
                else:
                    self.player.sprite.dead = True
  
    def handle_coin_collision(self) -> None:
        player = self.player.sprite

        for coin in self.coins.sprites():
            if coin.rect.colliderect(player):
                player.coin_obtained()
                self.coins.remove(coin)
    
                
    def handle_powerup_collision(self) -> None:
        player = self.player.sprite
        
        for powerup in self.powerups.sprites():
            if powerup.rect.colliderect(player):
                self.active_powerup = powerup.value
                self.powerup_duration = 1000
                self.powerups.remove(powerup)

    def handle_powerup_duration(self) -> None:
        if self.powerup_duration > 0 :
            self.powerup_duration -=1
            if self.powerup_duration == 0:
                self.active_powerup = 0
                
            

    def handle_horizontal_collision(self, dt) -> None:
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

    def handle_flag_collision(self) -> None:
        player = self.player.sprite

        for flag in self.flag.sprites():
            if flag.rect.colliderect(player):
                self.status = 'finished'
                break

    # TODO: REMOVE MID-AIR JUMP!!
    def handle_vertical_collision(self, dt) -> None:
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