from typing import Iterable
from space_invaders.components.base_objects import BaseObject
import pygame
import yaml

with open("space_invaders/config.yaml", "r") as file:
    config = yaml.safe_load(file)

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]


class Blockade(BaseObject):
    """Simple class for bloackade pieces that provide the player with cover from enemy shots ."""

    def __init__(self, image, initial_pos: tuple) -> None:
        super().__init__(image, initial_pos)


class BlockadeGroup(pygame.sprite.Group):
    """Group for all Blockade objects."""

    def __init__(self) -> None:
        super().__init__()

    def add(self, *sprites: Blockade | Iterable[Blockade]) -> None:
        return super().add(*sprites)


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
