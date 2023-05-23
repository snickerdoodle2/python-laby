import pygame, sys
from level import Level
from warp_level import WarpLevel
import config
from levels_layout.level_layout import LEVELS, warp_level


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

        self.start_screen = True
        self.pause = False
        
        pygame.mixer.music.load('assets/theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

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

                elif self.level.status == 'finished' and event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.set_level(0)

                elif self.level.status == 'dead' and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.set_level(0)

                elif self.level.status != 'dead' and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                    if self.pause: pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()

                elif self.start_screen == True and event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.start_screen = False
                    self.set_level(0)

            if self.start_screen:
                self.show_start_screen()
                continue

            if self.level.status == 'warp':
                    self.level = WarpLevel(warp_level, self.screen)

            if self.level.status == 'dead':
                self.show_death_screen()
                continue

            if self.pause:
                self.show_pause_screen()
                continue

            if self.level.status == 'finished':
                self.cur_level += 1
                if not self.update_level():
                    self.show_winner_screen()
                    continue
                
            if self.level.status == '1':
                self.cur_level = 0
                self.update_level()
            if self.level.status == '2':
                self.cur_level = 1
                self.update_level()
            if self.level.status == '3':
                self.cur_level = 2
                self.update_level()

            dt = self.clock.tick(200) / 1000
            # self.level.run(dt)
            self.level.run(0.005)

            pygame.display.update()

    def show_start_screen(self) -> None:
        self.screen.fill('light blue')
        self.show_two_lines_of_text("BROWARIO", 80, "Press S to start", 30, 50)
        pygame.display.flip()

    def show_pause_screen(self) -> None:
        self.show_two_lines_of_text("Paused!", 80, "Press ESC to resume", 30, 50)
        pygame.display.flip()

    def show_death_screen(self) -> None:
        self.show_two_lines_of_text("GAME OVER!", 100, "Press R to restart", 40, 50)
        pygame.display.flip()

    def show_winner_screen(self) -> None:
        self.show_two_lines_of_text("YOU WON!", 110, "Press S to start game again", 40, 60)
        pygame.display.flip()

    def show_two_lines_of_text(self, text_1: str, size_1: int, text_2: str, size_2: int, lines_gap: int) -> None:
        bigger_font = pygame.font.Font('assets/Pixeboy.ttf', size_1)
        smaller_font = pygame.font.Font('assets/Pixeboy.ttf', size_2)

        text_1 = bigger_font.render(text_1, True, (255, 255, 255))
        text_2 = smaller_font.render(text_2, True, (255, 255, 255))

        text_rect_1 = text_1.get_rect(center=(config.DISPLAY_WIDTH // 2, config.DISPLAY_HEIGHT // 2))
        text_rect_2 = text_2.get_rect(center=(config.DISPLAY_WIDTH // 2, config.DISPLAY_HEIGHT // 2 + lines_gap))

        self.screen.blit(text_1, text_rect_1)
        self.screen.blit(text_2, text_rect_2)
