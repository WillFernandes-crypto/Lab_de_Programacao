# entities/mob.py
import pygame
from entities.character import Character

class Mob(Character):
    def __init__(self, x, y, name, max_hp, mana, potions, damage):
        super().__init__(x, y, name, max_hp, mana, potions, damage)
        # Outras configurações ou atributos específicos para mobs podem ser definidos aqui

    def move(self, move_left, move_right):
        # Movimentação específica para mobs
        super().move(move_left, move_right)

    def attack(self):
        # Lógica de ataque específica para mobs
        super().attack()

    # Outros métodos comuns aos mobs podem ser adicionados aqui
