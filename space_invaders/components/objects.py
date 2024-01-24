import yaml
from space_invaders.components import BaseObject


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Player(BaseObject):
    def move(self, left: bool = False, right: bool = False) -> None:
        if left:
            self.pos.right -= self.speed
        if right:
            self.pos.right += self.speed
        if self.pos.right > WIDTH:
            self.pos.right = WIDTH
        if self.pos.left < 0:
            self.pos.left = 0


class Enemy(BaseObject):
    def move(self) -> None:
        pass


class EnemyCreator:
    """Factory class for creating Enemies different types."""

    def __init__(self) -> None:
        self.created_enemies = {"weak": 0}

    def create_enemy(self, type: str):
        """Factory method for creating an Enemy instance."""
        if type == "weak":
            return Enemy()
        self.created_enemies[self.type] += 1
