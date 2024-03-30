from space_invaders.components.blockade import (
    Blockade,
    BlockadeGroup,
)
from space_invaders.components.player import Player, PlayerObject
from space_invaders.components.laser import Laser
from space_invaders.components.base_objects import BaseObject, MovableObject
from space_invaders.components.objects import Enemy, EnemyCreator
from space_invaders.components.level import LevelGenerator
from space_invaders.components.game_handler import GameHandler, GameHandlerBase
from space_invaders.components.controller import (
    EnemyController,
    LaserController,
    BlockadeController,
    GameObjectController,
)
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
    GameHandlerBase,
    GameObjectController,
    config,
]
