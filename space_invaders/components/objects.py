import yaml
import pygame
from space_invaders.components.base_objects import PlayerObject, BaseObject
from space_invaders.components.laser_controller import Laser, LaserController


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Player(PlayerObject):
    def update(self, left: bool = False, right: bool = False) -> None:
        if left:
            self.rect.right -= self.speed
        if right:
            self.rect.right += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot_laser(self, laser: Laser):
        self.laser_controller.add_laser(laser)


class Enemy(BaseObject):
    def __init__(self, image: pygame.surface.Surface, initial_pos: tuple, speed: int) -> None:
        super().__init__(image, initial_pos, speed)
        self.movement_direction = -1

    def switch_movement_direction(self):
        self.movement_direction *= -1

    def update(self) -> None:
        self.rect.left += self.movement_direction * self.speed

    def move_row_down(self) -> None:
        self.rect.centery += 30


class EnemyCreator:
    """Factory class for creating Enemies different types."""

    def __init__(self, type: str) -> None:
        self.created_enemies = {"weak": 0}
        self.type = type

    def create_enemy(self, image: pygame.surface.Surface, initial_pos: tuple, speed: int):
        """Factory method for creating an Enemy instance."""
        self.created_enemies[self.type] += 1
        if self.type == "weak":
            return Enemy(image, initial_pos, speed)
