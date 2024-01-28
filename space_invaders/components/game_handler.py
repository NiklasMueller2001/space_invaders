from space_invaders.components.objects import Player, Enemy
from space_invaders.components.enemy_controller import EnemyController
from space_invaders.components.laser_controller import Laser
import pygame
import sys
import yaml


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
ENEMY_SHOOT_DELAY = config["ENEMY_SHOOT_DELAY"]


class GameHandler:
    def __init__(self, player: Player, enemy_controller: EnemyController) -> None:
        self.player = player
        self.enemy_controller = enemy_controller
        self.background = 0, 0, 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        pygame.display.flip()

    def game_loop(self) -> None:
        laser_im = pygame.image.load("space_invaders/assets/laser.png")
        laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))
        last_shot_time = 0
        while True:
            keys = pygame.key.get_pressed()
            self.screen.fill(self.background)
            for enemy in self.enemy_controller.enemies:
                self.screen.blit(enemy.image, enemy.pos)
            if keys[pygame.K_LEFT]:
                self.player.move(left=True)
            if keys[pygame.K_RIGHT]:
                self.player.move(right=True)
            if keys[pygame.K_SPACE]:
                if not self.player.laser_controller.lasers:
                    self.player.shoot_laser(
                        Laser(laser_im, self.player.pos.midtop, LASER_BASE_SPEED)
                    )
            self.player.laser_controller.move_lasers()
            for enemy_laser_controller in self.enemy_controller.laser_controllers:
                enemy_laser_controller.move_lasers()
            self.enemy_controller.move_enemies()
            for laser in self.player.laser_controller.lasers:
                if self.player.laser_controller.laser_is_out_of_screen(laser):
                    self.player.laser_controller.lasers.remove(laser)
            for laser_controller in self.enemy_controller.laser_controllers:
                for laser in laser_controller.lasers:
                    if laser_controller.laser_is_out_of_screen(laser):
                        laser_controller.remove_laser(laser)
            if self.enemy_controller.enemy_is_out_of_screen():
                self.enemy_controller.move_enemies_row_down()
                self.enemy_controller.switch_movement_direction()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= ENEMY_SHOOT_DELAY:
                chosen_enemy = self.enemy_controller.choose_random_enemy()
                chosen_enemy.shoot_laser(
                    Laser(laser_im, chosen_enemy.pos.midbottom, LASER_BASE_SPEED / 20)
                )
                last_shot_time = current_time
            self.screen.blit(self.player.image, self.player.pos)
            for enemy in self.enemy_controller.enemies:
                self.screen.blit(enemy.image, enemy.pos)
            for laser in self.player.laser_controller.lasers:
                self.screen.blit(laser.image, laser.pos)
            for laser_controller in self.enemy_controller.laser_controllers:
                for laser in laser_controller.lasers:
                    self.screen.blit(laser.image, laser.pos)
            pygame.display.flip()
            self.clock.tick(60)
