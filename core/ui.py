# core/ui.py
import pygame

def draw_text(text, font, color, surface, x, y):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_bg(surface, background):
    surface.blit(background, (0, 0))

# Função para desenhar o painel com informações do jogador
def draw_panel(screen, player, font):
    # Desenha um painel retangular
    panel_img = pygame.Surface((200, 100))  # Exemplo: cria uma superfície para o painel
    panel_img.fill((0, 0, 0))  # Cor de fundo do painel
    screen.blit(panel_img, (0, 0))  # Desenha o painel na tela
    
    # Mostra os status do jogador
    draw_text(f'{player.name} HP: {player.hp}', font, (255, 0, 0), screen, 10, 10)  # Corrigido para incluir a posição correta
    # Aqui você pode adicionar mais informações, como o estado dos inimigos ou outros elementos
    # for count, i in enumerate(buggy_list):
        # mostrar nome e saúde dos buggys
        # draw_text(f'{i.name} HP: {i.hp}', font, red, screen)  # Corrigido para incluir a posição correta