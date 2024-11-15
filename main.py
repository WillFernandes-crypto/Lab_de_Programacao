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
            datetime = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(datetime)
            pygame.display.update()

if __name__ == '__main__':
    game = Main()
    game.run()

'''clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

# Inicializa o jogo com a gravidade
game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY)

# Criar grupo de espadas
sword_group = pygame.sprite.Group()

# Inicia o loop do jogo
run = True
while run:
    clock.tick(FPS)
    moving_left, moving_right, jump, attack = get_user_input()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        game.handle_event(event)

    # Atualizar e desenhar grupo de espadas
    sword_group.update()
    sword_group.draw(screen)

    # Atualiza o player (passando a variável de ataque)
    game.update_player(moving_left, moving_right, jump, attack, sword_group)
    game.run()
    pygame.display.update()

pygame.quit()
'''