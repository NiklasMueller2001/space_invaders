from space_invaders.components.base_objects import MovableObject
from space_invaders.components.laser import LaserController

class PlayerObject(MovableObject):
    def __init__(
        self, image, initial_pos: tuple, speed: int, laser_controller: LaserController
    ) -> None:
        super().__init__(image, initial_pos, speed)
        self.lives = 3
        self.laser_controller = laser_controller
