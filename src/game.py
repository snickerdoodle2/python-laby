import pygame, sys
from level import Level
import config
from levels_layout.level_layout import LEVELS

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        # TODO: Change to settings file
        
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        pygame.display.set_caption('Mario')
        
        # choosing which level load
        self.cur_level = 0
        self.level = None
        self.update_level()
        
        self.pause = False

    def update_level(self) -> bool:
        if self.cur_level >= len(LEVELS): return False
        self.level = Level(LEVELS[self.cur_level], self.screen)    
        return True
    
    def set_level(self, index) -> None:
        self.cur_level = index
        self.update_level()


    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause

            if self.pause:
                self.show_pause_screen()
                continue
            
                                
            dt = self.clock.tick() / 1000
            # self.level.run(dt)
            # TODO: Add better death handling
            self.level.run(0.005)
            if self.level.status == 'finished':
                self.cur_level += 1
                if not self.update_level():
                    print("GZ")
                    break
                
            if self.level.status == 'dead':
                print('Dead!!!')
                break

            
            pygame.display.update()
            
            
    def show_pause_screen(self):
        self.font = pygame.font.Font('assets/Pixeboy.ttf', 50)
        text = self.font.render("Paused", True, (255, 255, 255))
        text_rect = text.get_rect(center=( config.DISPLAY_WIDTH// 2, config.DISPLAY_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()