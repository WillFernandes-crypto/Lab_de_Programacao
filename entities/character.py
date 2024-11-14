# entities/character.py
import pygame

class Character:
    def __init__(self, x, y, name, max_hp, mana, potions, damage):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.mana = mana
        self.potions = potions
        self.alive = True
        self.damage = damage
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack, 2: dano, 3: morto, 4: andar, 5: pular
        self.update_time = pygame.time.get_ticks()
        self.is_attacking = False

        # Ajuste do caminho com base no tipo de personagem
        base_path = self.get_base_path()

        # Carregar animações
        self.load_animations(base_path)

        self.facing_left = False
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.is_dead = False
        self.hitbox = self.rect

    def get_base_path(self):
        """Retorna o caminho base para as imagens do personagem"""
        if self.name == 'Player':
            return './img/player'
        else:
            return f'./img/mobs/{self.name}'

    def load_animations(self, base_path):
        """Carrega todas as animações do personagem"""
        self.animation_list = []
        for action in ['idle', 'attack', 'damage', 'dead', 'walk', 'jump']:
            temp_list = []
            for i in range(self.get_frame_count(action)):
                img = pygame.image.load(f'{base_path}/{action}/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def get_frame_count(self, action):
        """Retorna o número de frames para uma animação específica"""
        if action == 'idle':
            return 6
        elif action == 'attack':
            return 7
        elif action == 'damage':
            return 4
        elif action == 'dead':
            return 7
        elif action == 'walk':
            return 11
        elif action == 'jump':
            return 14
        return 0

    def move(self, move_left, move_right):
        """Movimenta o personagem"""
        if move_left:
            self.rect.x -= 5
            self.facing_left = True
            self.action = 4  # Andando
        elif move_right:
            self.rect.x += 5
            self.facing_left = False
            self.action = 4  # Andando
        else:
            self.idle()

    def jump_action(self):
        """Define o pulo"""
        if not self.jump:
            self.vel_y = -10
            self.jump = True
            self.action = 5  # Pulo

    def attack(self):
        """Ataca o inimigo"""
        self.action = 1

    def idle(self):
        """Define o estado de inatividade"""
        self.action = 0
        self.frame_index = 0

    def update(self):
        """Atualiza a animação e estado do personagem"""
        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Se a ação for morte
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

        if self.facing_left:
            self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False)
        else:
            self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, surface):
        """Desenha o personagem na tela"""
        surface.blit(self.image, self.rect)
