from space_invaders.components.objects import Enemy
from space_invaders.components.laser import LaserController, Laser
from typing import Any
import pygame
import random
import yaml


def get_config() -> Any:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
laser_im = pygame.image.load("space_invaders/assets/laser.png")
laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))


class EnemyController(pygame.sprite.Group):
    def __init__(self, lasercontroller: LaserController) -> None:
        super().__init__()
        self.laser_controller = lasercontroller
        self.current_enemy_speed = ENEMY_BASE_SPEED
        self.is_blocked = True

    def set_enemy_speed(self, new_speed) -> None:
        self.current_enemy_speed = new_speed
        for enemy in self.sprites():
            enemy.speed = self.current_enemy_speed

    def move_enemies(self, dt) -> None:
        self.update(dt=dt)

    def move_enemies_row_down(self) -> None:
        for enemy in self.sprites():
            enemy.move_row_down()

    def switch_movement_direction(self) -> None:
        for enemy in self.sprites():
            enemy.switch_movement_direction()

    def choose_random_enemy(self) -> Enemy:
        chosen_enemy = random.choice(self.sprites())
        return chosen_enemy

    def enemy_is_out_of_screen(self) -> bool:
        for enemy in self.sprites():
            if enemy.rect.left < 0:
                return True
            if enemy.rect.right > WIDTH:
                return True
        return False

    def shoot_laser(self, enemy: Enemy) -> None:
        self.laser_controller.add(
            Laser(laser_im, enemy.rect.midbottom, LASER_BASE_SPEED)
        )
