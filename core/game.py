# core/game.py
import pygame
from utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from levels.level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
import sys  # Para permitir encerramento correto do jogo

class Game:
    def __init__(self):
        # Inicializa o Pygame e configura o jogo
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("The Emptiness Machine")
        self.clock = pygame.time.Clock()
        
        # Carrega os mapas
        self.tmx_maps = {
            0: load_pygame(join('assets', 'data', 'levels', 'omni.tmx'))
        }
        # Configura o nível inicial
        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        """Loop principal do jogo."""
        while True:
            delta_time = self.clock.tick(60) / 1000  # Controla o FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Atualiza e renderiza o nível atual
            self.current_stage.run(delta_time)
            pygame.display.update()
