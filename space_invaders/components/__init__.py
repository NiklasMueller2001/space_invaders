from space_invaders.components.enemy_controller import EnemyController
from space_invaders.components.laser_controller import Laser, LaserController
from space_invaders.components.base_objects import BaseObject, PlayerObject
from space_invaders.components.objects import Player, Enemy, EnemyCreator
from space_invaders.components.level import LevelGenerator
from space_invaders.components.game_handler import GameHandler
import yaml

with open("space_invaders/config.yaml", "r") as file:
    config = yaml.safe_load(file)

all = [
    BaseObject,
    PlayerObject,
    Player,
    Enemy,
    Laser,
    EnemyCreator,
    EnemyController,
    LaserController,
    LevelGenerator,
    GameHandler,
    config
]
