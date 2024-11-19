import pygame
import os
from utils.settings import *
from utils.timer import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((23, 60))
        self.image.fill('black')

        # Rects
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()

        # Movimentação
        self.direction = pygame.math.Vector2()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 800

        # Colisões
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.plataform = None

        # Timer
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250)
        }

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = pygame.math.Vector2(0, 0)
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_a]:
                input_vector.x -= 1
            self.direction.x = input_vector.normalize().x if input_vector.length() > 0 else 0
        
        if keys[pygame.K_w]:
            self.jump = True

    def move(self, delta_time):
        # Movimentação horizontal
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # Movimentação vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * delta_time
        else:
            self.direction.y += self.gravity * delta_time
            self.rect.y += self.direction.y * delta_time

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.rect.bottom -= 1
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.collision('vertical')

    def platform_move(self, delta_time):
        if self.plataform:
            # Calcular a diferença de posição da plataforma
            platform_movement = pygame.math.Vector2(self.plataform.rect.topleft) - pygame.math.Vector2(self.plataform.old_rect.topleft)
            self.rect.topleft += platform_movement

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + pygame.math.Vector2(0, self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + pygame.math.Vector2(-2, self.rect.height / 4), (2, self.rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Colisões
        self.on_surface['floor'] = floor_rect.collidelist(collide_rects) >= 0
        self.on_surface['right'] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(collide_rects) >= 0

        self.plataform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.plataform = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                elif axis == 'vertical': # vertical
                    # top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.platform_move(delta_time)  # Mover o player com a plataforma antes de mover o player
        self.input()
        self.move(delta_time)
        self.check_contact()
