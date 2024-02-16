import pygame
import yaml
from typing import Any


def get_config() -> Any:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
HEIGHT = config["HEIGHT"]


class Laser(pygame.sprite.Sprite):
    directions = {"up": -1, "down": 1}

    def __init__(self, image, initial_pos: tuple, speed: int) -> None:
        super().__init__()
        self.image = image
        self.speed = speed
        self.rect = image.get_rect(topleft=(0, 0)).move(initial_pos)

    def update(self, direction: str, dt):
        self.rect.centery += Laser.directions[direction] * self.speed * dt
        if self._is_out_of_screen():
            self.kill()

    def _is_out_of_screen(self) -> bool:
        if self.rect.bottom < 0:
            return True
        elif self.rect.top > HEIGHT:
            return True
        return False


class LaserController(pygame.sprite.GroupSingle):
    """Class for handling Laser objects."""

    def __init__(self, laser_direction: str) -> None:
        super().__init__()
        self.laser_direction = laser_direction

    def move_laser(self, dt) -> None:
        self.update(direction=self.laser_direction, dt=dt)
