from space_invaders.components.objects import Enemy
from space_invaders.components.laser_controller import LaserController
import random
import yaml


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class EnemyController:
    def __init__(self) -> None:
        self.enemies: list[Enemy] = []
        self.laser_controllers: list[LaserController] = []

    def add_enemy(self, enemy: Enemy) -> None:
        self.enemies.append(enemy)
        self.laser_controllers.append(enemy.laser_controller)

    def remove_enemy(self, enemy: Enemy) -> None:
        self.enemies.remove(enemy)
        self.laser_controllers.remove(enemy.laser_controller)

    def move_enemies(self) -> None:
        for enemy in self.enemies:
            enemy.move()

    def move_enemies_row_down(self) -> None:
        for enemy in self.enemies:
            enemy.move_row_down()

    def switch_movement_direction(self) -> None:
        for enemy in self.enemies:
            enemy.switch_movement_direction()

    def choose_random_enemy(self) -> Enemy:
        chosen_enemy = random.choice(self.enemies)
        return chosen_enemy

    def enemy_is_out_of_screen(self) -> bool:
        for enemy in self.enemies:
            if enemy.pos.left < 0:
                return True
            if enemy.pos.right > WIDTH:
                return True
        return False

    def move_all_lasers(self) -> None:
        for laser_controller in self.laser_controllers:
            laser_controller.move_lasers()
