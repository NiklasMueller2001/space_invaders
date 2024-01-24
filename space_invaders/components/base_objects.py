from abc import ABC, abstractmethod
import pygame


class BaseObject(ABC):
    """Abstract base class for player and all enemies in game."""

    def __init__(self, image, initial_pos: tuple, speed: int) -> None:
        self.image = image
        self.speed = speed
        self.pos = image.get_rect(topleft=(0, 0)).move(initial_pos)

    def rescale(self, size: tuple[int, int]) -> None:
        """Method for rescaling imag of object"""
        self.image = pygame.transform.scale_by(self.image, size)
        return self

    @abstractmethod
    def move(self, *args):
        """Define movement of object"""
        pass
