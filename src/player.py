import pygame
import config


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()

        self.image = pygame.image.load('assets/bawario.png')
        self.rect = self.image.get_rect(topleft=pos)

        self.movement_speed = config.PLAYER_MOVEMENT_SPEED
        self.gravity = config.GRAVITY
        self.jump_speed = config.PLAYER_JUMP_SPEED

        self.direction = pygame.Vector2()
        self.can_jump = True
        self.dead = False
        self.score = 0000
        
        self.jump_sound = pygame.mixer.Sound('assets/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def coin_obtained(self):
        self.score += 100

    def get_direction(self) -> None:
        keys_state = pygame.key.get_pressed()
		
        if keys_state[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys_state[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys_state[pygame.K_SPACE] and self.can_jump:
            pygame.mixer.Sound.play(self.jump_sound)
            self.direction.y = self.jump_speed
            self.can_jump = False

        self.direction.y += self.gravity

    def update(self) -> None:
        self.get_direction()
        if self.rect.top > config.DISPLAY_HEIGHT:
            self.dead = True
