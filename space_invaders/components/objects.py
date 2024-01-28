import yaml
from space_invaders.components.base_objects import PlayerObject, Alien
from space_invaders.components.laser_controller import Laser, LaserController


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Player(PlayerObject):
    def move(self, left: bool = False, right: bool = False) -> None:
        if left:
            self.pos.right -= self.speed
        if right:
            self.pos.right += self.speed
        if self.pos.right > WIDTH:
            self.pos.right = WIDTH
        if self.pos.left < 0:
            self.pos.left = 0

    def shoot_laser(self, laser: Laser):
        self.laser_controller.add_laser(laser)


class Enemy(Alien):
    def __init__(
        self, image, initial_pos: tuple, speed: int, laser_controller: LaserController
    ) -> None:
        super().__init__(image, initial_pos, speed, laser_controller)
        self.movement_direction = -1

    def switch_movement_direction(self):
        self.movement_direction *= -1

    def move(self) -> None:
        self.pos.left += self.movement_direction * self.speed

    def move_row_down(self) -> None:
        self.pos.centery += 30

    def shoot_laser(self, laser: Laser) -> None:
        self.laser_controller.add_laser(laser)


class EnemyCreator:
    """Factory class for creating Enemies different types."""

    def __init__(self, type: str) -> None:
        self.created_enemies = {"weak": 0}
        self.type = type

    def create_enemy(self, *args):
        """Factory method for creating an Enemy instance."""
        self.created_enemies[self.type] += 1
        if self.type == "weak":
            return Enemy(*args)
