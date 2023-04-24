import pygame
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, position, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = position)
        
    def update(self, x_change) -> None:
        self.rect.x += x_change
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, position, size, value):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft = position)
        
        self.value = value
        
    def update(self, x_change) -> None:
        self.rect.x += x_change