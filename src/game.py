import pygame, sys
from level import Level
import config

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        # TODO: Change to settings file
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption('Mario')
        
        self.level = Level(self.screen)
        self.level.setup()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick() / 1000
            self.level.run(dt)

            pygame.display.update()