import pygame
from config import BLOCK_SIZE


class Block(pygame.sprite.Sprite):
    def __init__(self, position, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(position[0] + BLOCK_SIZE // 2, position[1] + BLOCK_SIZE // 2))

    def update(self, x_change) -> None:
        self.rect.x += x_change


class Coin(pygame.sprite.Sprite):
    def __init__(self, position, value):
        super().__init__()
        self.image = pygame.image.load('assets/coin.png')
        self.rect = self.image.get_rect(center=(position[0] + BLOCK_SIZE // 2, position[1] + BLOCK_SIZE // 2))

        self.value = value

    def update(self, x_change) -> None:
        self.rect.x += x_change


class Powerup(pygame.sprite.Sprite):
    def __init__(self, position, size, value):
        super().__init__()
        self.image = pygame.image.load('assets/beer.png')
        self.rect = self.image.get_rect(center=(position[0] + BLOCK_SIZE // 2, position[1] + BLOCK_SIZE // 2))
        self.value = value

    def update(self, x_change) -> None:
        self.rect.x += x_change
