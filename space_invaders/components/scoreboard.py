from typing import Any
import pygame
import yaml


def get_config() -> Any:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = get_config()


BACKGROUND = config["BACKGROUND"]


class LiveIcon(pygame.sprite.Sprite):
    """
    Class for sprite representing the live icon for the player lives in the
    scoreboard.
    """

    def __init__(self, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = image.get_rect()


class ScoreBoard(pygame.sprite.Group):
    """
    Represents displayed scoreboard that keeps track of current score and player
    lives.
    """

    def __init__(self, live_icon_image: pygame.Surface) -> None:
        super().__init__()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.live_icon_image = live_icon_image
        self._score = 0
        self.lives = 0
        self.live_icon_order: dict[int, LiveIcon] = dict()
        self.text_size = (0, 0)

    @property
    def score(self) -> int:
        """Return the current score."""
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        """Set the score to specified value."""
        self._score = value

    def add_live(self) -> None:
        """Add one live."""
        newest_live_icon = LiveIcon(self.live_icon_image)
        pos = (self.lives * newest_live_icon.rect.width, newest_live_icon.rect.height)
        newest_live_icon.rect = newest_live_icon.rect.move(pos)
        self.add(newest_live_icon)
        self.lives += 1
        self.live_icon_order.update({self.lives: newest_live_icon})

    def remove_live(self) -> None:
        """Remove one live."""
        if self.lives <= 0:
            raise ValueError("Error! Player has no lives left.")
        self.remove(self.live_icon_order[self.lives])
        del self.live_icon_order[self.lives]
        self.lives -= 1

    def draw_score(self, surf: pygame.Surface) -> None:
        """
        Helper method to draw text on screen displaying the current score.
        """
        score_text = self.font.render(f"Score: {self.score}", True, (0, 255, 0))
        self.text_size = score_text.get_size()
        surf.blit(score_text, (0, 0))

    def clear_score(self, surf: pygame.Surface) -> None:
        """
        Helper method to clear text from screen displaying the current score.
        """
        surf.fill(
            BACKGROUND,
            pygame.Rect(0, 0, *self.text_size),
        )
