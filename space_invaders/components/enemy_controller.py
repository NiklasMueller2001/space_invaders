from space_invaders.components.objects import Enemy
from space_invaders.components.laser_controller import LaserController, Laser
import pygame
import random
import yaml


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
laser_im = pygame.image.load("space_invaders/assets/laser.png")
laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))


class EnemyController(pygame.sprite.Group):
    def __init__(self, lasercontroller: LaserController) -> None:
        super().__init__()
        self.laser_controller = lasercontroller
        self.is_blocked = False

    def move_enemies(self) -> None:
        self.update()

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
        self.laser_controller.add(Laser(laser_im, enemy.rect.midbottom, LASER_BASE_SPEED))
