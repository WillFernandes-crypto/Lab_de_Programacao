# entities/player.py
import pygame
import os
from utils.settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((23,60))
        self.image.fill('black')
        self.rect = self.image.get_frect(topleft = pos)

        # Movimentação
        self.direction = vector()
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self, datetime):
        self.rect.topleft += self.direction * self.speed * datetime


    def update(self, datetime):
        self.input()
        self.move(datetime)
'''
        self.alive = True
        self.speed = speed
        self.gravity = gravity
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Carregar animações
        animation_types = ['idle', 'walk', 'jump', 'attack']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'assets/images/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/images/player/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, moving_left, moving_right, jump):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if jump and not self.in_air:
            self.vel_y = -11
            self.in_air = True

        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('assets/images/player/{animation}/{i}.png').convert_alpha()  # Ajuste o caminho da imagem
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x) > 800:
            self.kill()
'''