# initial_level.py
import pygame
import math

class InitialLevel:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg = pygame.image.load("assets/images/initial_level/bg.png").convert()

        # Redimensionando a imagem para caber na tela
        self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))

        self.bg_width = self.bg.get_width()
        self.scroll = 0
        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

        # Velocidade de rolagem adaptada ao tamanho da tela
        self.scroll_speed = 5  # Velocidade fixa de rolagem
        self.scroll_factor = self.scroll_speed / self.screen_width  # Ajuste da rolagem proporcional à largura da tela

    def draw(self, screen):
        for i in range(self.tiles):
            screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))

    def update_scroll(self):
        # Ajusta a velocidade do scroll proporcional à largura da tela
        self.scroll -= self.scroll_speed * self.scroll_factor
        if abs(self.scroll) > self.bg_width:
            self.scroll = 0

    def update_size(self, new_width, new_height):
        """Atualiza o tamanho da tela e redimensiona o fundo"""
        self.screen_width = new_width
        self.screen_height = new_height
        # Redimensiona a imagem de fundo sempre que a tela for redimensionada
        self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))
        self.bg_width = self.bg.get_width()
        self.tiles = math.ceil(self.screen_width / self.bg_width) + 1

        # Recalcula o fator de rolagem baseado no novo tamanho da tela
        self.scroll_factor = self.scroll_speed / self.screen_width
