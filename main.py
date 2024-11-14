# main.py
import pygame
from core.game import Game
from core.input import get_user_input

# Inicializa o Pygame
pygame.init()

# Configuração da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Emptiness Machine")

clock = pygame.time.Clock()
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
