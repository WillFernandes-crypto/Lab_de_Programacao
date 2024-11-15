# level.py
from utils.settings import *
from utils.sprites import *
from entities.player import *

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        # grupos
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def run(self, delta_time):
        self.all_sprites.update(delta_time)
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.display_surface)