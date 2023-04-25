import pygame, sys
from level import Level
import config
from levels_layout.level_layout import *

class Game:
    

    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        # TODO: Change to settings file
        
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption('Mario')
        
        # choosing which level load
        self.level_map = level_2
        self.level = Level(self.level_map, self.screen)
        

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            dt = self.clock.tick() / 1000
            # self.level.run(dt)
            # TODO: Add better death handling
            self.level.run(0.005)
            if self.level.status == 'finished':
                print('Finished!!!')
                break
            if self.level.status == 'dead':
                print('Dead!!!')
                break

            
            pygame.display.update()
            
            
    