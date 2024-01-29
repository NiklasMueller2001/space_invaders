from abc import ABC, abstractmethod
from space_invaders.components.laser_controller import LaserController
import pygame


class BaseObject(pygame.sprite.Sprite):
    """Base class for player and all enemies in game."""

    def __init__(self, image, initial_pos: tuple, speed: int) -> None:
        super().__init__()
        self.image = image
        self.speed = speed
        self.rect = image.get_rect(topleft=(0, 0)).move(initial_pos)

    def rescale(self, size: tuple[int, int]) -> None:
        """Method for rescaling imag of object"""
        self.image = pygame.transform.scale_by(self.image, size)
        return self


class PlayerObject(BaseObject):
    def __init__(
        self, image, initial_pos: tuple, speed: int, laser_controller: LaserController
    ) -> None:
        super().__init__(image, initial_pos, speed)
        self.laser_controller = laser_controller
