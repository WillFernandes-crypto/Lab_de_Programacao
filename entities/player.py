# entities/player.py
import pygame
import os
from utils.settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((23,60))
        self.image.fill('black')

        # Rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Movimentação
        self.direction = vector(0, 0)
        self.speed = 200
        self.gravity = 1300

        # Colisões
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        '''if keys[pygame.K_s]:
            input_vector.y += 1
        if keys[pygame.K_w]:
            input_vector.y -= 1'''

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, delta_time):
        # Movimentação horizontal
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # Movimentação vertical
        self.direction.y += self.gravity / 2 * delta_time
        self.rect.y += self.direction.y * delta_time
        self.direction.y += self.gravity / 2 * delta_time
        self.collision('vertical')

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # Colisão horizontal: ajuste da posição
                    if self.direction.x > 0:  # movendo para a direita
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:  # movendo para a esquerda
                        self.rect.left = sprite.rect.right
                else: # vertical
                    # top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(delta_time)