from abc import ABC, abstractmethod
import pygame

class BaseObject(ABC):
    """Abstract base class for player and all enemies in game."""

    def __init__(self, image, height: int, speed: int) -> None:
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def rescale(self, size: tuple[int, int]) -> None:
        """Method for rescaling imag of object"""
        self.image = pygame.transform.scale(self.image, size)

    @abstractmethod
    def move(self, *args):
        """Define movement of object"""
        pass