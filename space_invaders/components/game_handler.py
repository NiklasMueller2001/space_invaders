from abc import ABC, abstractmethod
from space_invaders.components.laser import Laser
from space_invaders.components.level import LevelGenerator
from space_invaders.components.controller import GameObjectController
from typing import Any
import pygame
import sys
import yaml


def get_config() -> Any:
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
laser_im = pygame.transform.scale(laser_im, (0.0025 * WIDTH, 0.03 * HEIGHT))


class GameHandlerBase(ABC):
    """
    Base class for all GameHandler objects.
    """

    def __init__(
        self,
        game_object_controller: GameObjectController,
        level_generator: LevelGenerator,
    ) -> None:
        self.game_object_controller = game_object_controller
        self.level_generator = level_generator
        self.player = game_object_controller.player
        self.enemy_controller = game_object_controller.enemy_controller
        self.blockade_controller = game_object_controller.blockade_controller

    def unblock_enemy_movement(self) -> None:
        """Unblock all enemies."""

        self.enemy_controller.is_blocked = False

    def block_enemy_movement(self) -> None:
        """Block all enemies."""

        self.enemy_controller.is_blocked = True

    @abstractmethod
    def load_new_level(self) -> None:
        pass

    @abstractmethod
    def game_loop(self) -> None:
        pass


class GameHandler(GameHandlerBase):
    def __init__(
        self,
        game_object_controller: GameObjectController,
        level_generator: LevelGenerator,
    ) -> None:
        super().__init__(game_object_controller, level_generator)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.is_paused = False
        self.game_time = 0
        self.killed_enemies = 0
        pygame.init()
        pygame.display.flip()

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
        self.game_object_controller._clear_all_objects()
        self.game_object_controller._draw_all_objects()
        pygame.display.update()

    def game_loop(self) -> None:
        self.load_new_level()
        UNBLOCK_ENEMIES = pygame.USEREVENT + 1
        BLOCK_ENEMIES = pygame.USEREVENT + 2
        pygame.time.set_timer(BLOCK_ENEMIES, ENEMY_BLOCK_TIME + ENEMY_UNBLOCK_TIME)
        self.blockade_controller.create_all_blockade_structures()
        unblock_timer_set = False
        last_player_shot_time = 0
        while True:
            dt = self.clock.tick_busy_loop(50)
            if unblock_timer_set == False:
                if self.game_time * dt > ENEMY_BLOCK_TIME:
                    pygame.time.set_timer(
                        UNBLOCK_ENEMIES, ENEMY_BLOCK_TIME + ENEMY_UNBLOCK_TIME
                    )
                    unblock_timer_set = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Block enemy movement to create interrupted movement
                if event.type == BLOCK_ENEMIES:
                    self.block_enemy_movement()
                if event.type == UNBLOCK_ENEMIES:
                    self.unblock_enemy_movement()
            if not self.is_paused:
                # Clear old images
                self.game_object_controller._clear_all_objects()
                # Check for user input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.update(left=True, dt=dt)
                if keys[pygame.K_RIGHT]:
                    self.player.update(right=True, dt=dt)
                if keys[pygame.K_SPACE]:
                    if (
                        not self.player.laser_controller
                        and self.game_time - last_player_shot_time > 10
                    ):
                        self.player.laser_controller.add(
                            Laser(laser_im, self.player.rect.midtop, LASER_BASE_SPEED)
                        )
                        last_player_shot_time = self.game_time
                # Update laser positions
                if self.player.laser_controller:
                    self.player.laser_controller.move_laser(dt)
                self.enemy_controller.laser_controller.move_laser(dt)
                # Check if something was hit by laser
                if self.enemy_controller.laser_controller:
                    self.game_object_controller._check_blockade_hit_by_enemy_laser()
                if self.player.laser_controller:
                    self.game_object_controller._check_blockade_hit_by_player_laser()
                if self.game_object_controller._check_player_hit():
                    self.player.lives -= 1
                if self.game_object_controller._check_enemy_hit():
                    self.killed_enemies += 1
                    if self.killed_enemies % 9 == 0:
                        # Increase enemy speed based on number of remaining enemies
                        new_enemy_speed = (
                            1.1 * self.enemy_controller.current_enemy_speed
                        )
                        self.enemy_controller.set_enemy_speed(new_enemy_speed)
                # Check if level is finished
                if not self.enemy_controller:
                    self.load_new_level()
                    self.enemy_controller.set_enemy_speed(
                        ENEMY_BASE_SPEED * 1.05 * self.level_generator.level_number
                    )
                # Update enemy positions
                if not self.enemy_controller.is_blocked:
                    self.enemy_controller.move_enemies(dt)
                    if self.enemy_controller.enemy_is_out_of_screen():
                        self.enemy_controller.move_enemies_row_down()
                        self.enemy_controller.switch_movement_direction()
                # Shoot new laser once old one is removed from screen and enemies aren't blocked
                if not (
                    self.enemy_controller.laser_controller
                    or self.enemy_controller.is_blocked
                ):
                    chosen_enemy = self.enemy_controller.choose_random_enemy()
                    self.enemy_controller.laser_controller.add(
                        Laser(
                            laser_im,
                            chosen_enemy.rect.midbottom,
                            LASER_BASE_SPEED,
                        )
                    )
                # Check if player has 0 lives left
                if self.player.lives == 0:
                    sys.exit()
                # Draw all objects on screen
                self.game_object_controller._draw_all_objects()
                pygame.display.update()
                self.game_time += 1
