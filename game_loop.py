import pygame
import constants
from game_controllers import PlayerController, EnemyController

class Game:
    def __init__(self):
        self.playing = False
        
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.screen.fill(constants.BG_COLOR)
        self.keys_pressed = []

        self.player = pygame.sprite.GroupSingle()
        self.p_laser_green = pygame.sprite.Group()
        self.p_laser_red = pygame.sprite.Group()

        self.green_enemies = pygame.sprite.Group()
        self.red_enemies = pygame.sprite.Group()
        self.e_laser_green = pygame.sprite.Group()
        self.e_laser_red = pygame.sprite.Group()

        self.player_con = PlayerController(self.player)
        self.enemy_con = EnemyController()

        self.score = 0
        self.score_band = pygame.Surface((constants.WIDTH, 50))
        self.score_band.fill('white')
        self.score_band_rect = self.score_band.get_rect(topleft = (0, 0))
        self.font = pygame.font.SysFont('arial', 30, True)
        self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
        self.score_rect = self.score_text.get_rect(topleft = (0, 0))

        self.splash_text = self.font.render('PRESS SPACE TO START GAME', False, 'black')
        self.splash_rect = self.splash_text.get_rect(center = (constants.WIDTH / 2, constants.HEIGHT / 2))

    def get_input(self):
        self.keys_pressed = pygame.key.get_pressed()

    def run_entities(self):
        self.player_con.keys_pressed = self.keys_pressed
        self.player_con.run(self.p_laser_green, self.p_laser_red)
        self.enemy_con.run(self.green_enemies, self.red_enemies, self.e_laser_green, self.e_laser_red)

    def update(self):
        self.p_laser_green.update()
        self.p_laser_red.update()

        self.e_laser_green.update()
        self.e_laser_red.update()

        self.green_enemies.update()
        self.red_enemies.update()

    def player_collisions(self):
        if pygame.sprite.groupcollide(self.player, self.green_enemies, False, False) and self.player.sprite.state == 1:
            self.playing = False
        elif pygame.sprite.groupcollide(self.player, self.red_enemies, False, False) and self.player.sprite.state == 0:
            self.playing = False
        elif pygame.sprite.groupcollide(self.player, self.e_laser_green, False, False) and self.player.sprite.state == 1:
            self.playing = False
        elif pygame.sprite.groupcollide(self.player, self.e_laser_red, False, False) and self.player.sprite.state == 0:
            self.playing = False

    def enemy_collisions(self):
        if pygame.sprite.groupcollide(self.p_laser_red, self.green_enemies, True, True):
            self.score += 1
        if pygame.sprite.groupcollide(self.p_laser_green, self.red_enemies, True, True):
            self.score+= 1

    def draw_running(self):
        self.screen.fill(constants.BG_COLOR)
        self.screen.blit(self.score_text, self.score_rect)
        
        self.screen.blit(self.player.sprite.get_surf(), self.player.sprite.rect)

        self.green_enemies.draw(self.screen)
        self.red_enemies.draw(self.screen)

        self.p_laser_green.draw(self.screen)
        self.p_laser_red.draw(self.screen)

        self.e_laser_green.draw(self.screen)
        self.e_laser_red.draw(self.screen)
        
        self.screen.blit(self.score_band, self.score_band_rect)
        self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
        self.screen.blit(self.score_text, self.score_rect)

        pygame.display.flip()

    def restart(self):
        if self.keys_pressed[pygame.K_SPACE]:
            self.p_laser_green.empty()
            self.p_laser_red.empty()

            self.green_enemies.empty()
            self.red_enemies.empty()
            self.e_laser_green.empty()
            self.e_laser_red.empty()
            self.player.sprite.rect.midbottom = ((constants.WIDTH / 2, constants.HEIGHT - 20))
            self.score = 0
            self.score_text = self.font.render(f'Score = {self.score}', False, 'black')
            self.playing = True
            pygame.time.wait(300)

    def run(self):
        self.get_input()
        if self.playing:
            self.run_entities()
            self.player_collisions()
            self.enemy_collisions()
            self.update()
            self.draw_running()
        elif not self.playing:
            self.screen.fill(constants.BG_COLOR)
            self.screen.blit(self.splash_text, self.splash_rect)
            self.restart()
            pygame.display.flip()


if __name__ == '__main__':

    pygame.init()

    clock = pygame.time.Clock()

    game = Game()
    run = True

    while run:
        game.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        clock.tick(constants.FPS)

    pygame.quit()








