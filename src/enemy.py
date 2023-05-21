import pygame


class GroundEnemy(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.Vector2(-1, 0)

    def update(self, x_change):
        self.rect.x += x_change


class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface((size, size // 2))
        self.image.fill('brown')
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.Vector2(-1, 0)

    def update(self, x_change):
        self.rect.x += x_change
