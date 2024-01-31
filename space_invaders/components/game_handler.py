from space_invaders.components.objects import Player, Enemy
from space_invaders.components.enemy_controller import EnemyController
from space_invaders.components.laser_controller import Laser
from space_invaders.components.level import LevelGenerator
import pygame
import sys
import yaml


def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
ENEMY_BLOCK_TIME = config["ENEMY_BLOCK_TIME"]
ENEMY_UNBLOCK_TIME = config["ENEMY_UNBLOCK_TIME"]
ENEMY_SHOOT_DELAY = config["ENEMY_SHOOT_DELAY"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
laser_im = pygame.image.load("space_invaders/assets/laser.png")
laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))


class GameHandler:
    def __init__(
        self,
        player: Player,
        enemy_controller: EnemyController,
        level_generator: LevelGenerator,
    ) -> None:
        self.player = player
        self.enemy_controller = enemy_controller
        self.level_generator = level_generator
        self.background = 0, 0, 0
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        pygame.display.flip()

    def _clear_all_objects(self) -> None:
        """Helper method that clears all visible objects from screen."""
        self.enemy_controller.clear(self.screen, self._clear_callback)
        self.enemy_controller.laser_controller.clear(self.screen, self._clear_callback)
        self.player.laser_controller.clear(self.screen, self._clear_callback)
        self._clear_callback(self.screen, self.player.rect)

    def _draw_all_objects(self) -> None:
        """Helper method that draws all visible objects on screen."""
        self.screen.blit(self.player.image, self.player.rect)
        self.enemy_controller.draw(self.screen)
        self.player.laser_controller.draw(self.screen)
        self.enemy_controller.laser_controller.draw(self.screen)

    def _player_is_hit(self) -> None:
        """Helper method that checks if player is hit by laser and removes a life if he was."""
        for laser in pygame.sprite.spritecollide(
            self.player, self.enemy_controller.laser_controller, dokill=False
        ):
            laser.kill()
            self.player.lives -= 1

    def _enemy_is_hit(self) -> None:
        """Helper method that checks if an enemy is hit by laser and removes enemy if it was."""
        pygame.sprite.groupcollide(
            self.player.laser_controller,
            self.enemy_controller,
            dokilla=True,
            dokillb=True,
        )

    def unblock_enemy_movement(self) -> None:
        """unblock the enemy"""
        self.enemy_controller.is_blocked = False

    def block_enemy_movement(self) -> None:
        self.enemy_controller.is_blocked = True

    def load_new_level(self) -> None:
        """Start the next level."""
        initial_enemies = next(self.level_generator)
        self.enemy_controller.add(initial_enemies)
        self.player.rect.move(
            (
                self.screen.get_rect().centerx - self.player.rect.width / 2,
                self.screen.get_rect().bottom - self.player.rect.height,
            )
        )
        self._clear_all_objects()
        self._draw_all_objects()
        pygame.display.update()

    def game_loop(self) -> None:
        self.load_new_level()
        UNBLOCK_ENEMIES = pygame.USEREVENT + 1
        BLOCK_ENEMIES = pygame.USEREVENT + 2
        pygame.time.set_timer(
            UNBLOCK_ENEMIES, ENEMY_BLOCK_TIME + ENEMY_UNBLOCK_TIME
        )
        pygame.time.wait(ENEMY_UNBLOCK_TIME)
        pygame.time.set_timer(
            BLOCK_ENEMIES, ENEMY_BLOCK_TIME + ENEMY_UNBLOCK_TIME
        )
        while True:
            # Check if level is finished
            if not self.enemy_controller:
                self.load_new_level()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # Block enemy movement to create interrupted movement
                if event.type == BLOCK_ENEMIES:
                    self.block_enemy_movement()
                if event.type == UNBLOCK_ENEMIES:
                    self.unblock_enemy_movement()
            # Clear old images
            self._clear_all_objects()
            # Check for user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.update(left=True)
            if keys[pygame.K_RIGHT]:
                self.player.update(right=True)
            if keys[pygame.K_SPACE]:
                if not self.player.laser_controller:
                    self.player.laser_controller.add(
                        Laser(laser_im, self.player.rect.midtop, LASER_BASE_SPEED)
                    )
            # Update enemies and laser positions
            if self.player.laser_controller:
                self.player.laser_controller.move_laser()
            self.enemy_controller.laser_controller.move_laser()
            if not self.enemy_controller.is_blocked:
                self.enemy_controller.move_enemies()
            if self.enemy_controller.enemy_is_out_of_screen():
                self.enemy_controller.move_enemies_row_down()
                self.enemy_controller.switch_movement_direction()
            # Shoot new laser once old one is removed from screen and enemies arent blocked
            if not (self.enemy_controller.laser_controller or self.enemy_controller.is_blocked):
                chosen_enemy = self.enemy_controller.choose_random_enemy()
                self.enemy_controller.laser_controller.add(
                    Laser(
                        laser_im,
                        chosen_enemy.rect.midbottom,
                        LASER_BASE_SPEED,
                    )
                )
            # Check if player or enemy was hit
            self._player_is_hit()
            self._enemy_is_hit()
            # Check if player still has 0 lives left
            if self.player.lives == 0:
                sys.exit()
            # Draw all objects on screen
            self._draw_all_objects()
            pygame.display.update()
            self.clock.tick(60)

    def _clear_callback(self, surf, rect):
        surf.fill(self.background, rect)
