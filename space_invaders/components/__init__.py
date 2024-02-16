from space_invaders.components.blockade import Blockade, BlockadeGroup, BlockadeController 
from space_invaders.components.enemy_controller import EnemyController
from space_invaders.components.laser import Laser, LaserController
from space_invaders.components.base_objects import BaseObject, MovableObject, PlayerObject
from space_invaders.components.objects import Player, Enemy, EnemyCreator
from space_invaders.components.level import LevelGenerator
from space_invaders.components.game_handler import GameHandler
import yaml

with open("space_invaders/config.yaml", "r") as file:
    config = yaml.safe_load(file)

all = [
    BaseObject,
    MovableObject,
    PlayerObject,
    Player,
    Enemy,
    Laser,
    Blockade,
    BlockadeGroup,
    BlockadeController,
    EnemyCreator,
    EnemyController,
    LaserController,
    LevelGenerator,
    GameHandler,
    config
]
