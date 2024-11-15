# level.py
from utils.settings import *
from utils.sprites import *
from entities.player import *

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        # grupos
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites)
                print(obj.x)
                print(obj.y)

    def run(self, datetime):
        self.all_sprites.update(datetime)
        self.display_surface.fill('gray')
        self.all_sprites.draw(self.display_surface)