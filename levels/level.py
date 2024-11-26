from utils.settings import *
from utils.sprites import *
from entities.player import *
from core.groups import *
from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()
        
        # Grupos
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # Tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == "Terrain": groups.append(self.collision_sprites)
                if layer == "Platforms": groups.append(self.semi_collision_sprites)
                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

        # Objetos
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames['player'])
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    # frames 
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]

                    # groups 
                    groups = [self.all_sprites]
                    if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
                    # if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

                    # z index
                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

                    # animation speed
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1)
                    AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
            if obj.name == 'flag':
                self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))

        # Objetos que se movem
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'spike':
                pass
            else:
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.collision_sprites)
                if obj.width > obj.height: # horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height)
                else: # vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height / 2)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed)


    def run(self, delta_time):
        self.display_surface.fill('gray')
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player.hitbox_rect.center)
