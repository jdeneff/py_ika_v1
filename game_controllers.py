import pygame
import constants
from game_sprites import PlayerSprite, LaserSprite, EnemySprite
from random import randint
from pygame.locals import K_SPACE, K_LSHIFT, K_LEFT, K_RIGHT


class PlayerController:
    def __init__(self, player_group):
        self.keys_pressed = []

        self.player_sprite = PlayerSprite(0)
        player_group.add(self.player_sprite)

        self.flip_ready = True
        self.flip_time = 0
        
        self.fire_ready = True
        self.fire_time = 0

    def player_move(self):
        if self.keys_pressed[K_LEFT]:
            self.player_sprite.move_left()
        if self.keys_pressed[K_RIGHT]:
            self.player_sprite.move_right()

        if self.player_sprite.rect.left < 0:
            self.player_sprite.rect.left = 0
        if self.player_sprite.rect.right > constants.WIDTH:
            self.player_sprite.rect.right= constants.WIDTH

    def player_flip(self):
        if self.keys_pressed[K_LSHIFT] and self.flip_ready:
            self.player_sprite.flip_state()
            self.flip_ready = False
            self.flip_time = pygame.time.get_ticks()
        
    def player_fire(self, g_group, r_group):
        if self.keys_pressed[K_SPACE] and self.fire_ready:
            if self.player_sprite.state == 0:
                g_laser = LaserSprite(-1, 'green')
                g_laser.rect.midbottom = self.player_sprite.rect.midtop
                g_group.add(g_laser)
            elif self.player_sprite.state == 1:
                r_laser = LaserSprite(-1, 'red')
                r_laser.rect.midbottom = self.player_sprite.rect.midtop
                r_group.add(r_laser)
            self.fire_ready = False
            self.fire_time = pygame.time.get_ticks()

    def player_reset(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.flip_time >= constants.P_FLIP:
            self.flip_ready = True
        if time_now - self.fire_time >= constants.P_RECHARGE:
            self.fire_ready = True

    def run(self, g_group, r_group):
        self.player_move()
        self.player_flip()
        self.player_fire(g_group, r_group)
        self.player_reset()

class EnemyController:
    def __init__(self):

        self.spawn_ready = False
        self.spawn_time = 0

    def enemy_spawn(self, g_group, r_group):
        e_type = randint(0, 1)
        spawn_x = randint(20, constants.WIDTH - 20)
        if self.spawn_ready:
            enemy = EnemySprite(e_type)
            enemy.rect.centerx = spawn_x
            if e_type == 0:
                g_group.add(enemy)
            elif e_type == 1:
                r_group.add(enemy)
            self.spawn_ready = False
            self.spawn_time = pygame.time.get_ticks()

    def enemy_fire(self, e_group, l_group):
        for enemy in e_group:
            if enemy.fire_ready and (enemy.rect.bottom < constants.HEIGHT / 2):
                if enemy.e_type == 0:
                    g_laser = LaserSprite(1, 'green4')
                    g_laser.rect.center = enemy.rect.center
                    l_group.add(g_laser)
                elif enemy.e_type == 1:
                    r_laser = LaserSprite(1, 'red4')
                    r_laser.rect.center = enemy.rect.center
                    l_group.add(r_laser)

                enemy.fire_ready = False
                enemy.fire_time = pygame.time.get_ticks()
                
    def enemy_reset_spawn(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.spawn_time >= constants.E_SPAWN:
            self.spawn_ready = True

    def enemy_reset_fire(self, e_group):
        time_now = pygame.time.get_ticks()
        for enemy in e_group:
            if time_now - enemy.fire_time >= constants.E_RECHARGE:
                enemy.fire_ready = True

    def run(self, g_enemy_group, r_enemy_group, g_laser_group, r_laser_group):
        self.enemy_spawn(g_enemy_group, r_enemy_group)
        self.enemy_fire(g_enemy_group, g_laser_group)
        self.enemy_fire(r_enemy_group, r_laser_group)
        self.enemy_reset_spawn()
        self.enemy_reset_fire(g_enemy_group)
        self.enemy_reset_fire(r_enemy_group)



    
    











        
