from space_invaders.components.laser import LaserController
from typing import Self
import pygame


class BaseObject(pygame.sprite.Sprite):
    """Base class for all visible objects in the game."""

    def __init__(self, image, initial_pos: tuple) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(0, 0)).move(initial_pos)
        self.screen = pygame.display.get_surface()

    def rescale(self, size: tuple[int, int]) -> Self:
        """Method for rescaling imag of object"""
        self.image = pygame.transform.scale_by(self.image, size)
        return self


class MovableObject(BaseObject):
    """Base class for all movable visible objects in the game."""

    def __init__(self, image, initial_pos: tuple, speed: int) -> None:
        super().__init__(image, initial_pos)
        self.speed = speed
        self.rect = image.get_rect(topleft=(0, 0)).move(initial_pos)

    def rescale(self, size: tuple[int, int]) -> Self:
        """Method for rescaling imag of object"""
        self.image = pygame.transform.scale_by(self.image, size)
        return self


class PlayerObject(MovableObject):
    def __init__(
        self, image, initial_pos: tuple, speed: int, laser_controller: LaserController
    ) -> None:
        super().__init__(image, initial_pos, speed)
        self.lives = 3
        self.laser_controller = laser_controller
