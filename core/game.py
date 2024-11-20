# core/game.py
import pygame
from utils.settings import *
from utils.support import *
from levels.level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
import sys  # Para permitir encerramento correto do jogo

class Game:
    def __init__(self):
        # Inicializa o Pygame e configura o jogo
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("The Empytiness Machine")
        self.clock = pygame.time.Clock()
        self.import_assets()
        
        # Carrega os mapas
        self.tmx_maps = {
            0: load_pygame(join('assets', 'data', 'levels', 'omni.tmx'))
        }
        # Configura o nível inicial
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)


    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('assets', 'graphics', 'level', 'flag'),
            'saw': import_folder('assets', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('assets', 'graphics','enemies', 'floor_spikes'),
			'palms': import_sub_folders('assets', 'graphics', 'level', 'palms'),
			'candle': import_folder('assets', 'graphics','level', 'candle'),
			'window': import_folder('assets', 'graphics','level', 'window'),
			'big_chain': import_folder('assets', 'graphics','level', 'big_chains'),
			'small_chain': import_folder('assets', 'graphics','level', 'small_chains'),
			'candle_light': import_folder('assets', 'graphics','level', 'candle light'),
			'player': import_sub_folders('assets', 'images','player'),
			'saw': import_folder('assets', 'graphics', 'enemies', 'saw', 'animation'),
			'saw_chain': import_image('assets',  'graphics', 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder('assets', 'graphics', 'level', 'helicopter'),
			'boat': import_folder('assets',  'graphics', 'objects', 'boat'),
			'spike': import_image('assets',  'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('assets',  'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
			'tooth': import_folder('assets', 'graphics','enemies', 'tooth', 'run'),
			'shell': import_sub_folders('assets', 'graphics','enemies', 'shell'),
			'pearl': import_image('assets',  'graphics', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('assets', 'graphics', 'items'),
			'particle': import_folder('assets', 'graphics', 'effects', 'particle'),
			'water_top': import_folder('assets', 'graphics', 'level', 'water', 'top'),
			'water_body': import_image('assets', 'graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('assets', 'graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('assets', 'graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('assets', 'graphics','level', 'clouds', 'large_cloud')
        }

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
