import pygame
import yaml
from space_invaders.components import (
    Player,
    Enemy,
    EnemyCreator,
    EnemyController,
    LaserController,
    GameHandler,
)


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def load_assets() -> list[Player, Enemy]:
    player_im = pygame.image.load("space_invaders/assets/red_rect.jpg")
    enemy_im = pygame.image.load("space_invaders/assets/alien.gif")
    # background = pygame.image.load("space_invaders/assets/background.jpg")
    return [player_im, enemy_im]


def rescale_image(image: pygame.Surface, scale: tuple[int, int]) -> pygame.Surface:
    image = pygame.transform.scale(image, scale)
    return image


def main():
    config = get_config()
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
    ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]

    player_im, enemy_im = load_assets()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player_im = rescale_image(player_im, (0.05 * WIDTH, 0.08 * HEIGHT))
    enemy_im = rescale_image(enemy_im, (0.05 * WIDTH, 0.08 * HEIGHT))
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
    positions = [((0.15 + 0.06 * i) * WIDTH, enemy_im.get_height()) for i in range(11)]
    weak_enemy_creator = EnemyCreator(type="weak")
    enemy_controller = EnemyController()
    for position in positions:
        enemy_controller.add_enemy(
            weak_enemy_creator.create_enemy(
                enemy_im, position, ENEMY_BASE_SPEED, enemy_laser_controller
            )
        )
    game = GameHandler(player, enemy_controller)
    game.game_loop()


if __name__ == "__main__":
    main()
