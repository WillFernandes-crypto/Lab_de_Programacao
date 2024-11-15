# main.py
import pygame
from core.game import *
from core.input import get_user_input
from utils.settings import *
from levels.level import *
from pytmx.util_pygame import load_pygame
from os.path import join

class Main:
    def __init__(self):
        # Inicializa o Pygame
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("The Emptiness Machine")
        self.clock = pygame.time.Clock()
        self.tmx_maps = {0: load_pygame(join('assets', 'data', 'levels', 'omni.tmx'))}
        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        # Inicia o loop do jogo
        while True:
            delta_time = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(delta_time)
            pygame.display.update()

if __name__ == '__main__':
    game = Main()
    game.run()