from space_invaders.components.objects import EnemyCreator, Enemy
from typing import Any, Iterator
import pygame
import yaml

with open("space_invaders/config.yaml", "r") as file:
    config = yaml.safe_load(file)

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
enemy_im = pygame.image.load("space_invaders/assets/alien.gif")
enemy_im = pygame.transform.scale(enemy_im, (0.05 * WIDTH, 0.08 * HEIGHT))


class LevelGenerator:
    def __init__(self, enemy_creator: EnemyCreator) -> None:
        self.enemy_creator = enemy_creator
        self.level_number = 0

    def initial_enemies(self, y_offset) -> list[Enemy]:
        enemies = []
        for x in range(0, 11):
            for y in range(0, 5):
                new_enemy = self.enemy_creator.create_enemy(
                    enemy_im,
                    (
                        x * 0.6 * WIDTH / 10 + 0.2 * WIDTH,
                        y * enemy_im.get_rect().height + y_offset,
                    ),
                    ENEMY_BASE_SPEED,
                )
                enemies.append(new_enemy)
        return enemies

    def __next__(self) -> list[Enemy]:
        self.level_number += 1
        y_offset = 0.05 * HEIGHT * (self.level_number - 1)
        return self.initial_enemies(y_offset)
