from space_invaders.components import BaseObject


class Player(BaseObject):
    def move(self, left: bool = False, right: bool = False) -> None:
        if left:
            self.pos.right -= self.speed
        if right:
            self.pos.right += self.speed


class Enemy(BaseObject):
    def move(self) -> None:
        pass


class EnemyCreator:
    """Factory class for creating Enemies different types."""

    def __init__(self) -> None:
        self.created_enemies = {"weak": 0}

    def create_enemy(self, type: str):
        """Factory method for creating an Enemy instance."""
        if self.type == "weak":
            return Enemy()
        self.created_enemies[self.type] += 1
