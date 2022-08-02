import pygame
import constants

# Index 0 matches to green, index 1 matches to red


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, state = 0):
        super().__init__()

        # Ship state controls color of ship and color of lasers fired
        self.state = state
        self.images = [pygame.image.load('assets/ship_green.png').convert_alpha(), pygame.image.load('assets/ship_red.png').convert_alpha()]
        self.rect = self.images[0].get_rect(midbottom = (constants.WIDTH / 2, constants.HEIGHT - 20))
        for image in self.images:
            image.set_colorkey((255, 65, 255))

    def move_left(self):
        self.rect.x -= constants.P_SPD

    def move_right(self):
        self.rect.x += constants.P_SPD

    def flip_state(self):
        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 0

    def get_surf(self):
        return self.images[self.state]


class LaserSprite(pygame.sprite.Sprite):
    def __init__(self, spawn_dir, color):
        super().__init__()
        self.spawn_dir = spawn_dir
        self.color = color

        self.image = pygame.Surface(constants.L_DIM)
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom = (0, 0))

    def update(self):
        self.rect.y += self.spawn_dir * constants.L_SPD

        if self.rect.top > constants.HEIGHT or self.rect.bottom < 0:
            self.kill()

class EnemySprite(pygame.sprite.Sprite):
    def __init__(self, e_type):
        super().__init__()
        self.fire_ready = False
        self.fire_time = 0
        self.e_type = e_type
        
        if e_type == 0:
            self.image = pygame.image.load('assets/enemy_green.png').convert_alpha()
        elif e_type == 1:
            self.image = pygame.image.load('assets/enemy_red.png').convert_alpha()
        self.image.set_colorkey((255, 65, 255))
        self.rect = self.image.get_rect(midbottom = (0, 0))

    def update(self):
        self.rect.y += constants.E_SPD

        if self.rect.top > constants.HEIGHT:
            self.kill()

            
