from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from space_invaders.components.controller import LaserController
from space_invaders.components.base_objects import MovableObject
from space_invaders.components.laser import Laser
import yaml

def get_config() -> Any:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class PlayerObject(MovableObject):
    def __init__(
        self, image, initial_pos: tuple, speed: int, laser_controller: LaserController
    ) -> None:
        super().__init__(image, initial_pos, speed)
        self.lives = 3
        self.laser_controller = laser_controller


class Player(PlayerObject):
    def update(self, dt, left: bool = False, right: bool = False) -> None:
        if left:
            self.rect.right -= self.speed * dt
        if right:
            self.rect.right += self.speed * dt
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot_laser(self, laser: Laser):
        self.laser_controller.add(laser)

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
