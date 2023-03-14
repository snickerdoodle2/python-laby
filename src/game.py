import pygame, sys
from level import Level

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Mario')
        self.level = Level(self.screen)
        self.level.setup()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.level.run()

            
            pygame.display.update()