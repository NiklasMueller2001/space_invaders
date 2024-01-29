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
ENEMY_SHOOT_DELAY = config["ENEMY_SHOOT_DELAY"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
laser_im = pygame.image.load("space_invaders/assets/laser.png")
laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))


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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Clear old images
            self.enemy_controller.clear(self.screen, self._clear_callback)
            self.enemy_controller.laser_controller.clear(self.screen, self._clear_callback)
            self.player.laser_controller.clear(self.screen, self._clear_callback)
            self._clear_callback(self.screen, self.player.rect)
            # Check for user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.update(left=True)
            if keys[pygame.K_RIGHT]:
                self.player.update(right=True)
            if keys[pygame.K_SPACE]:
                if not self.player.laser_controller:
                    self.player.laser_controller.add(
                        Laser(laser_im, self.player.rect.midtop, LASER_BASE_SPEED)
                    )
            # Update enemies and laser positions
            if self.player.laser_controller:
                self.player.laser_controller.move_laser()
            self.enemy_controller.laser_controller.move_laser()
            self.enemy_controller.move_enemies()
            if self.enemy_controller.enemy_is_out_of_screen():
                self.enemy_controller.move_enemies_row_down()
                self.enemy_controller.switch_movement_direction()
            # Shoot new laser once old one is killed
            if not self.enemy_controller.laser_controller:
                chosen_enemy = self.enemy_controller.choose_random_enemy()
                self.enemy_controller.laser_controller.add(
                    Laser(
                        laser_im,
                        chosen_enemy.rect.midbottom,
                        LASER_BASE_SPEED,
                    )
                )
            self.screen.blit(self.player.image, self.player.rect)
            self.enemy_controller.draw(self.screen)
            self.player.laser_controller.draw(self.screen)
            self.enemy_controller.laser_controller.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def _clear_callback(self, surf, rect):
        surf.fill(self.background, rect)
