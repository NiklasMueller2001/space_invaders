import sys, pygame
import yaml
from space_invaders.components import Player, Enemy


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def load_assets() -> list[Player, Enemy]:
    player_im = pygame.image.load("space_invaders/assets/player.png")
    enemy_im = pygame.image.load("space_invaders/assets/alien.gif")
    background = pygame.image.load("space_invaders/assets/background.jpg")
    return [player_im, enemy_im, background]


def main():
    config = get_config()
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
    ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()

    player_im, enemy_im, background = load_assets()
    player = Player(player_im, 700, PLAYER_BASE_SPEED)
    enemy = Enemy(enemy_im, 10, ENEMY_BASE_SPEED)

    while True:
        screen.blit(background, player.pos, player.pos)
        screen.blit(background, enemy.pos, enemy.pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(left=True)
        if keys[pygame.K_RIGHT]:
            player.move(right=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(player.image, player.pos)
        screen.blit(enemy.image, enemy.pos)
        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    main()
