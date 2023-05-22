import pygame


class GroundEnemy(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.image.load('assets/goomba.png')
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.Vector2(-1, 0)

    def update(self, x_change):
        self.rect.x += x_change


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.image.load('assets/bird.png')
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.Vector2(-1, 0)

    def update(self, x_change):
        self.rect.x += x_change
