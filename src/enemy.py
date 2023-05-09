import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.Vector2(-1,0)
        
    def update(self, x_change):
        self.rect.x += x_change
        