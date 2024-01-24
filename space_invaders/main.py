import sys, pygame
import yaml
from space_invaders.components import Player, Enemy


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def load_assets() -> list[Player, Enemy]:
    player_im = pygame.image.load("space_invaders/assets/red_rect.jpg")
    enemy_im = pygame.image.load("space_invaders/assets/alien.gif")
    background = pygame.image.load("space_invaders/assets/background.jpg")
    return [player_im, enemy_im, background]


def rescale_image(image: pygame.Surface, scale: tuple[int, int]) -> pygame.Surface:
    image = pygame.transform.scale(image, scale)
    return image


def main():
    config = get_config()
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
    ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
    pygame.init()

    clock = pygame.time.Clock()
    player_im, enemy_im, background = load_assets()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player_im = rescale_image(player_im, (0.1 * WIDTH, 0.1 * HEIGHT))
    pygame.display.flip()
    player = Player(
        player_im,
        (screen.get_rect().centerx - player_im.get_rect().width / 2, screen.get_rect().bottom - player_im.get_rect().height),
        PLAYER_BASE_SPEED,
    )
    enemy = Enemy(enemy_im, (0, 10), ENEMY_BASE_SPEED)
    print(screen.get_width())
    print(player.pos)
    black = 0, 0, 0
    while True:
        screen.fill(black)
        # screen.blit(background, enemy.pos, enemy.pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(left=True)
        if keys[pygame.K_RIGHT]:
            player.move(right=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(player.image, player.pos)
        # screen.blit(enemy.image, enemy.pos)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
