# core/timer.py
import pygame


class Timer:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()

    def reset(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        return pygame.time.get_ticks() - self.start_time
