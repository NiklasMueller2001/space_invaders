from dataclasses import dataclass
from space_invaders.components.objects import Enemy
from space_invaders.components.laser import Laser
from space_invaders.components.blockade import Blockade, BlockadeGroup
from space_invaders.components.player import Player
from typing import Any
import pygame
import random
import yaml
from typing import Iterable
import pygame
import yaml


def get_config() -> Any:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()
WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
BACKGROUND = config["BACKGROUND"]
laser_im = pygame.image.load("space_invaders/assets/laser.png")
laser_im = pygame.transform.scale(laser_im, (0.005 * WIDTH, 0.01 * HEIGHT))


class LaserController(pygame.sprite.GroupSingle):
    """Class for handling Laser objects."""

    def __init__(self, laser_direction: str) -> None:
        super().__init__()
        self.laser_direction = laser_direction

    def move_laser(self, dt) -> None:
        self.update(direction=self.laser_direction, dt=dt)


class EnemyController(pygame.sprite.Group):
    def __init__(self, lasercontroller: LaserController) -> None:
        super().__init__()
        self.laser_controller = lasercontroller
        self.current_enemy_speed = ENEMY_BASE_SPEED
        self.is_blocked = True

    def set_enemy_speed(self, new_speed) -> None:
        self.current_enemy_speed = new_speed
        for enemy in self.sprites():
            enemy.speed = self.current_enemy_speed

    def move_enemies(self, dt) -> None:
        self.update(dt=dt)

    def move_enemies_row_down(self) -> None:
        for enemy in self.sprites():
            enemy.move_row_down()

    def switch_movement_direction(self) -> None:
        for enemy in self.sprites():
            enemy.switch_movement_direction()

    def choose_random_enemy(self) -> Enemy:
        chosen_enemy = random.choice(self.sprites())
        return chosen_enemy

    def enemy_is_out_of_screen(self) -> bool:
        for enemy in self.sprites():
            if enemy.rect.left < 0:
                return True
            if enemy.rect.right > WIDTH:
                return True
        return False

    def shoot_laser(self, enemy: Enemy) -> None:
        self.laser_controller.add(
            Laser(laser_im, enemy.rect.midbottom, LASER_BASE_SPEED)
        )


class BlockadeController:
    """Controller for all Blockade objects."""

    def __init__(
        self,
        blockade_im: pygame.surface.Surface,
        blockade_group: BlockadeGroup,
    ) -> None:
        self.blockade_group = blockade_group
        self.blockade_im = blockade_im
        self.block_len = self.blockade_im.get_rect().width

    def create_all_blockade_structures(self) -> None:
        """Creates 4 evenly spaced blockade structures."""

        bottom_left_edge_positions = [
            (
                int(i * 0.7 * WIDTH / 3 + 0.15 * WIDTH - 10 * self.block_len),
                int(0.8 * HEIGHT),
            )
            for i in range(4)
        ]
        for pos in bottom_left_edge_positions:
            self.blockade_group.add(
                *self.create_blockade_structure(
                    bottom_left_edge_pos=pos,
                    blockade_im=self.blockade_im,
                )
            )

    def create_blockade_structure(
        self,
        bottom_left_edge_pos: tuple[int, int],
        blockade_im: pygame.surface.Surface,
    ) -> Iterable[Blockade]:
        """
        Create one large blockade structure shaped like an upside down U made
        out of connected Blockade objects.

        Parameters
        ----------
        bottom_left_edge_pos: tuple[int, int]
            The pixel position of the bottom left edge of the structure.
        blockade_im: pygame.surface.Surface
            The image of each Blockade square.
        """

        positions = []
        num_of_blocks_x = 20
        num_of_blocks_y = 15
        # Collect blockade positions for one blockade structure
        for i in range(0, num_of_blocks_x):
            for j in range(0, num_of_blocks_y):
                if i == 2 and j == num_of_blocks_y - 1:
                    continue
                if i == num_of_blocks_x - 3 and j == num_of_blocks_y - 1:
                    continue
                if i == 0 and j == num_of_blocks_y - 3:
                    continue
                if i == num_of_blocks_x - 1 and j == num_of_blocks_y - 3:
                    continue
                if i in range(num_of_blocks_x - 2, num_of_blocks_x) and j in range(
                    num_of_blocks_y - 2, num_of_blocks_y
                ):
                    continue
                if i in range(0, 2) and j in range(
                    num_of_blocks_y - 2, num_of_blocks_y
                ):
                    continue
                if i in range(4, num_of_blocks_x - 4) and j in range(0, 5):
                    continue
                if i in range(4, num_of_blocks_x - 4) and j == 5:
                    continue
                if i in range(5, num_of_blocks_x - 5) and j == 6:
                    continue
                if i in range(6, num_of_blocks_x - 6) and j == 7:
                    continue
                if i in range(7, num_of_blocks_x - 7) and j == 8:
                    continue
                x, y = (
                    bottom_left_edge_pos[0] + self.block_len * i,
                    bottom_left_edge_pos[1] - self.block_len * j,
                )
                positions.append((x, y))
        # Carve out pieces of square
        blockades = [Blockade(blockade_im, position) for position in positions]
        return blockades

    def draw(self, *args, **kwargs) -> list[pygame.Rect]:
        """Draw all blockade objects."""

        return self.blockade_group.draw(*args, **kwargs)

    def remove(self, *bloackades: Blockade | Iterable[Blockade]) -> None:
        """Remove blockade objects."""

        return self.blockade_group.remove(*bloackades)


@dataclass
class GameObjectController:
    """
    Controller class that gives control over all controller classes in the game.

    Attributes
    ----------
    player : Player
        The controller class for the player.
    enemy_controller : EnemyController
        The controller class for all enemies.
    blockade_controller : BlockadeController
        The controller class for all blockades.
    """

    player: Player
    enemy_controller: EnemyController
    blockade_controller: BlockadeController

    @property
    def screen(self) -> pygame.Surface:
        return pygame.display.get_surface()

    def _clear_all_objects(self) -> None:
        """Helper method that clears all visible objects from screen."""

        self.enemy_controller.clear(self.screen, self._clear_callback)
        self.enemy_controller.laser_controller.clear(self.screen, self._clear_callback)
        self.player.laser_controller.clear(self.screen, self._clear_callback)
        self.blockade_controller.blockade_group.clear(self.screen, self._clear_callback)
        self._clear_callback(self.screen, self.player.rect)

    def _draw_all_objects(self) -> None:
        """Helper method that draws all visible objects on screen."""

        self.player.draw()
        self.enemy_controller.draw(self.screen)
        self.player.laser_controller.draw(self.screen)
        self.enemy_controller.laser_controller.draw(self.screen)
        # print(self.blockade_controller.blockade_group)
        self.blockade_controller.draw(self.screen)

    def _clear_callback(self, surf, rect):
        """Helper function to blit background onto specified position."""

        surf.fill(BACKGROUND, rect)

    def _check_player_hit(self) -> bool:
        """Helper method that checks if player is hit by laser and removes a life if he was."""

        for laser in pygame.sprite.spritecollide(
            self.player, self.enemy_controller.laser_controller, dokill=False
        ):
            laser.kill()
            return True
        return False

    def _check_enemy_hit(self) -> bool:
        """Helper method that checks if an enemy is hit by laser and removes enemy if it was."""

        if pygame.sprite.groupcollide(
            self.player.laser_controller,
            self.enemy_controller,
            dokilla=True,
            dokillb=True,
        ):
            return True
        return False

    def _check_blockade_hit_by_enemy_laser(self) -> None:
        """
        Helper function that checks if a blockade is hit by a laser shot by an enemy
        and removes both laser and blockade if it was.
        """

        pygame.sprite.groupcollide(
            self.enemy_controller.laser_controller,
            self.blockade_controller.blockade_group,
            dokilla=True,
            dokillb=True,
        )

    def _check_blockade_hit_by_player_laser(self) -> None:
        """
        Helper function that checks if a blockade is hit by a laser shot by the player
        and removes both laser and blockade if it was.
        """

        pygame.sprite.groupcollide(
            self.player.laser_controller,
            self.blockade_controller.blockade_group,
            dokilla=True,
            dokillb=True,
        )
