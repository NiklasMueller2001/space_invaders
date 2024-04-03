import pygame
from typing import Any
from space_invaders.components import (
    Player,
    BlockadeGroup,
    BlockadeController,
    EnemyCreator,
    EnemyController,
    LaserController,
    GameObjectController,
    GameHandler,
    LevelGenerator,
    ScoreBoard,
    config,
)


def load_assets() -> list[Any]:
    player_im = pygame.image.load("space_invaders/assets/player.png")
    enemy_im = pygame.image.load("space_invaders/assets/alien.gif")
    blockade_im = pygame.image.load("space_invaders/assets/blockade.png")
    return [player_im, enemy_im, blockade_im]


def rescale_image(image: pygame.Surface, scale: tuple[int, int]) -> pygame.Surface:
    image = pygame.transform.scale(image, scale)
    return image


def main():
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]

    player_im, enemy_im, blockade_im = load_assets()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player_im = rescale_image(player_im, (0.05 * WIDTH, 0.08 * HEIGHT))
    enemy_im = rescale_image(enemy_im, (0.05 * WIDTH, 0.08 * HEIGHT))
    blockade_im = rescale_image(blockade_im, (0.007 * WIDTH, 0.007 * WIDTH))
    enemy_laser_controller = LaserController(laser_direction="down")
    player_laser_controller = LaserController(laser_direction="up")
    player = Player(
        player_im,
        (
            screen.get_rect().centerx - player_im.get_rect().width / 2,
            screen.get_rect().bottom - player_im.get_rect().height,
        ),
        PLAYER_BASE_SPEED,
        player_laser_controller,
    )
    weak_enemy_creator = EnemyCreator(type="weak")
    level_generator = LevelGenerator(weak_enemy_creator)
    enemy_controller = EnemyController(enemy_laser_controller)
    blockade_group = BlockadeGroup()
    blockade_controller = BlockadeController(blockade_im, blockade_group)
    scoreboard = ScoreBoard(player_im)
    game_obj_controller = GameObjectController(
        player, enemy_controller, blockade_controller
    )
    game = GameHandler(game_obj_controller, level_generator, scoreboard)
    game.game_loop()


if __name__ == "__main__":
    main()
