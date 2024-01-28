import yaml

def get_config() -> None:
    with open("space_invaders/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config

config = get_config()
HEIGHT = config["HEIGHT"]

class Laser:
    directions = {"up": -1, "down": 1}

    def __init__(self, image, initial_pos: tuple, speed: int) -> None:
        self.image = image
        self.speed = speed
        self.pos = image.get_rect(topleft=(0, 0)).move(initial_pos)

    def move(self, direction: str):
        self.pos.centery += Laser.directions[direction] * self.speed


class LaserController:
    """Class for handling Laser objects."""

    def __init__(self, laser_direction: str) -> None:
        self.lasers: list[Laser] = []
        self.laser_direction = laser_direction

    def add_laser(self, laser: Laser) -> None:
        self.lasers.append(laser)

    def remove_laser(self, laser: Laser) -> None:
        self.lasers.remove(laser)

    def laser_is_out_of_screen(self, laser: Laser) -> bool:
        if laser.pos.bottom < 0:
            return True
        elif laser.pos.top > HEIGHT:
            return True
        return False

    def move_lasers(self) -> None:
        for laser in self.lasers:
            laser.move(direction=self.laser_direction)
