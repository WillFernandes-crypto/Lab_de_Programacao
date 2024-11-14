# core/game.py
import pygame
from entities.player import Player
from entities.player import Sword
from levels.initial_level import InitialLevel

class Game:
    def __init__(self, screen, screen_width, screen_height, gravity):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = InitialLevel(screen_width, screen_height)
        self.player = Player(200, 200, 2, 5, gravity)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.is_fullscreen = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()

        if event.type == pygame.VIDEORESIZE:
            self.screen_width = event.w
            self.screen_height = event.h
            self.level.update_size(self.screen_width, self.screen_height)

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            self.is_fullscreen = False
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True

    def run(self):
        self.level.update_scroll()
        self.level.draw(self.screen)

        self.player.update()
        self.player.draw(self.screen)
        self.player.update_animation()

    def update_player(self, moving_left, moving_right, jump, attack, sword_group):
        if self.player.alive:
            # Ataque com espada
            if attack:
                sword = Sword(self.player.rect.centerx + (0.6 * self.player.rect.size[0] * self.player.direction), 
                              self.player.rect.centery, self.player.direction)
                sword_group.add(sword)
                self.player.update_action(3)  # 3: ataque
            elif self.player.in_air:
                self.player.update_action(2)  # 2: jump
            elif moving_left or moving_right:
                self.player.update_action(1)  # 1: walk
            else:
                self.player.update_action(0)  # 0: idle
            
            self.player.move(moving_left, moving_right, jump)
