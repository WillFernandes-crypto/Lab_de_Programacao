import pygame
import os
from utils.settings import *

class Botao:
    def __init__(self, x, y, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.topleft = (x, y)
        self.clicado = False

    def desenhar(self, superficie):
        acao = False
        pos_mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos_mouse):
            if pygame.mouse.get_pressed()[0] and not self.clicado:
                self.clicado = True
                acao = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicado = False

        superficie.blit(self.imagem, self.rect)
        return acao

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.tela_cheia = False
        self.scroll = 0
        self.clock = pygame.time.Clock()
        
        # Primeiro definimos todos os métodos auxiliares
        self.carregar_imagens()
        self.criar_botoes()
        self.criar_titulo()
        
        # Depois chamamos os métodos que dependem dos anteriores
        self.redimensionar_parallax(SCREEN_WIDTH, SCREEN_HEIGHT)
        
    def criar_titulo(self):
        self.fonte = pygame.font.Font(os.path.join('assets', 'fonts', 'pixellari.ttf'), 60)
        self.titulo = self.fonte.render("The Emptiness Machine", True, (255, 0, 0))
        self.titulo_rect = self.titulo.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
    def carregar_imagens(self):
        # Carrega botões
        start_img = pygame.image.load(os.path.join('assets', 'buttons', 'start.png')).convert_alpha()
        exit_img = pygame.image.load(os.path.join('assets', 'buttons', 'exit.png')).convert_alpha()
        
        # Redimensiona botões
        novo_tamanho = (int(start_img.get_width() * 0.6), int(start_img.get_height() * 0.6))
        self.start_img = pygame.transform.scale(start_img, novo_tamanho)
        self.exit_img = pygame.transform.scale(exit_img, novo_tamanho)
        
        # Carrega imagens do parallax
        self.ground_image = pygame.image.load(os.path.join('assets', 'parallax', 'ground.png')).convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()
        
        self.bg_images = []
        for i in range(1, 6):
            bg_image = pygame.image.load(os.path.join('assets', 'parallax', f'plx-{i}.png')).convert_alpha()
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()
        
    def criar_botoes(self):
        self.start_button = Botao(SCREEN_WIDTH // 2 - self.start_img.get_width() // 2, 200, self.start_img)
        self.exit_button = Botao(SCREEN_WIDTH // 2 - self.exit_img.get_width() // 2, 350, self.exit_img)
        
    def redimensionar_parallax(self, nova_largura, nova_altura):
        # Mantém a proporção original das imagens
        proporcao_tela = nova_largura / nova_altura
        proporcao_imagem = self.bg_images[0].get_width() / self.bg_images[0].get_height()
        
        if proporcao_tela > proporcao_imagem:
            # Tela mais larga que a imagem
            nova_altura_img = nova_altura
            nova_largura_img = nova_altura * proporcao_imagem
        else:
            # Tela mais alta que a imagem
            nova_largura_img = nova_largura
            nova_altura_img = nova_largura / proporcao_imagem
        
        # Redimensiona as imagens do background
        bg_images_temp = []
        for img in self.bg_images:
            img_redimensionada = pygame.transform.scale(img, (int(nova_largura_img), int(nova_altura_img)))
            bg_images_temp.append(img_redimensionada)
        self.bg_images = bg_images_temp
        self.bg_width = self.bg_images[0].get_width()
        
        # Redimensiona a imagem do chão proporcionalmente
        proporcao_ground = self.ground_height / nova_altura
        nova_altura_ground = int(nova_altura * proporcao_ground)
        self.ground_image = pygame.transform.scale(self.ground_image, (nova_largura, nova_altura_ground))
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()

    def reposicionar_elementos(self):
        # Calcula posições relativas à tela atual
        largura_tela = self.display_surface.get_width()
        altura_tela = self.display_surface.get_height()
        
        # Posiciona o título a 15% da altura da tela
        posicao_titulo_y = altura_tela * 0.15
        self.titulo_rect = self.titulo.get_rect(center=(largura_tela // 2, posicao_titulo_y))
        
        # Posiciona os botões em 40% e 60% da altura da tela
        self.start_button.rect.centerx = largura_tela // 2
        self.start_button.rect.centery = altura_tela * 0.4
        
        self.exit_button.rect.centerx = largura_tela // 2
        self.exit_button.rect.centery = altura_tela * 0.6

    def draw_bg(self):
        largura_tela = self.display_surface.get_width()
        altura_tela = self.display_surface.get_height()
        
        # Calcula o offset para centralizar as imagens
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                offset_x = (largura_tela - self.bg_width) // 2
                offset_y = (altura_tela - i.get_height()) // 2
                pos_x = offset_x + (x * self.bg_width) - self.scroll * speed
                self.display_surface.blit(i, (pos_x, offset_y))
                speed += 0.2

    def draw_ground(self):
        largura_tela = self.display_surface.get_width()
        altura_tela = self.display_surface.get_height()
        
        for x in range(15):
            pos_x = (x * self.ground_width) - self.scroll * 2.5
            pos_y = altura_tela - self.ground_height
            self.display_surface.blit(self.ground_image, (pos_x, pos_y))

    def run(self):
        rodando = True
        while rodando:
            self.clock.tick(60)
            
            self.scroll += 0.5
            if self.scroll > 3000:
                self.scroll = 0

            # Limpa a tela com cor preta para evitar artefatos visuais
            self.display_surface.fill((0, 0, 0))
            
            self.draw_bg()
            self.draw_ground()
            self.display_surface.blit(self.titulo, self.titulo_rect)

            if self.start_button.desenhar(self.display_surface):
                return True
                
            if self.exit_button.desenhar(self.display_surface):
                return False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                    
                elif evento.type == pygame.VIDEORESIZE:
                    if not self.tela_cheia:
                        # Atualiza as dimensões globais
                        global SCREEN_WIDTH, SCREEN_HEIGHT
                        SCREEN_WIDTH = evento.w
                        SCREEN_HEIGHT = evento.h
                        # Recria a superfície com o novo tamanho
                        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                        # Atualiza todos os elementos
                        self.redimensionar_parallax(SCREEN_WIDTH, SCREEN_HEIGHT)
                        self.reposicionar_elementos()

            pygame.display.update()
