import numpy as np
from PIL import Image
import pygame
from typing import Any, Literal, Optional
from gymnasium import spaces, Env
from space_invaders.components import (
    Player,
    BlockadeGroup,
    BlockadeController,
    EnemyCreator,
    EnemyController,
    LaserController,
    GameObjectController,
    GameHandlerBase,
    LevelGenerator,
    Laser,
    config,
)


def load_assets() -> list[Any]:
    player_im = pygame.image.load("space_invaders/assets/player.png")
    blockade_im = pygame.image.load("space_invaders/assets/blockade.png")
    laser_im = pygame.image.load("space_invaders/assets/laser.png")
    return [player_im, blockade_im, laser_im]

WIDTH = config["WIDTH"]
HEIGHT = config["HEIGHT"]
PLAYER_BASE_SPEED = config["PLAYER_BASE_SPEED"]
ENEMY_BASE_SPEED = config["ENEMY_BASE_SPEED"]
ENEMY_BLOCK_TIME = config["ENEMY_BLOCK_TIME"]
ENEMY_UNBLOCK_TIME = config["ENEMY_UNBLOCK_TIME"]
ENEMY_SHOOT_DELAY = config["ENEMY_SHOOT_DELAY"]
LASER_BASE_SPEED = config["LASER_BASE_SPEED"]
BACKGROUND = config["BACKGROUND"]
player_im, blockade_im, laser_im = load_assets()
player_im = pygame.transform.scale(player_im, (0.05 * WIDTH, 0.08 * HEIGHT))
blockade_im = pygame.transform.scale(blockade_im, (0.007 * WIDTH, 0.007 * WIDTH))
laser_im = pygame.transform.scale(laser_im, (0.0025 * WIDTH, 0.03 * HEIGHT))
enemy_laser_controller = LaserController(laser_direction="down")
player_laser_controller = LaserController(laser_direction="up")
player = Player(
    player_im,
    (
        WIDTH / 2 - player_im.get_rect().width / 2,
        HEIGHT - player_im.get_rect().height,
    ),
    PLAYER_BASE_SPEED,
    player_laser_controller,
)
weak_enemy_creator = EnemyCreator(type="weak")
level_generator = LevelGenerator(weak_enemy_creator)
enemy_controller = EnemyController(enemy_laser_controller)
blockade_group = BlockadeGroup()
blockade_controller = BlockadeController(blockade_im, blockade_group)
game_obj_controller = GameObjectController(
    player, enemy_controller, blockade_controller
)


class SpaceInvadersEnv(Env, GameHandlerBase):
    metadata = {"render_modes": ["human", "rgb_array", "gray_scale_array"], "render_fps": 20}

    def __init__(
        self,
        game_object_controller: GameObjectController = game_obj_controller,
        level_generator: LevelGenerator = level_generator,
        width: int = 200,
        heigth: int = 150,
        render_mode: Literal["human", "rgb_array", "gray_scale_array"] = "human",
        reward: Optional[dict[Literal["enemy_kill", "player_damage"], int]] = None
    ) -> None:
        self.width = width
        self.height = heigth
        self.render_mode = render_mode
        self.enemy_kill_reward : int = 1
        self.player_damage_reward : int = -1
        if reward is not None:
            self.enemy_kill_reward = reward.get("enemy_kill") # type: ignore
            self.player_damage_reward = reward.get("player_damage") # type: ignore
        super().__init__(game_object_controller, level_generator)
        # Observations will be entire visible screen, resized to specified shape
        if self.render_mode == "gray_scale_array":
            self.observation_space = spaces.Box(
                low=0, high=255, shape=(width, heigth), dtype=np.uint8
            )
        elif self.render_mode in ["rgb_array", "human"]:
            self.observation_space = spaces.Box(
                low=0, high=255, shape=(width, heigth, 3), dtype=np.uint8
            )
        else:
            raise ValueError(f"Render mode should be one of {self.metadata["render_modes"]}.")
        # Actions are: (0) Do nothing, (1) move left, (2) move right and (3) shoot laser
        self.action_space = spaces.Discrete(4)
        self.clock = None
        self.screen = None
        # Helper variable for blocking/unblocking logic
        self.last_enemy_block_time = 0
        self.last_enemy_unblock_time = 0

    def load_new_level(self, surf: pygame.Surface) -> pygame.Surface:
        """Start the next level."""

        initial_enemies = next(self.level_generator)
        self.enemy_controller.add(initial_enemies)
        self.player.rect.move(
            (
                WIDTH / 2 - self.player.rect.width / 2,
                HEIGHT - self.player.rect.height,
            )
        )
        if self.render_mode == "human":
            self.game_object_controller._clear_all_objects(surf)
            self.game_object_controller._draw_all_objects(surf)
        return surf

    def step(self, action) -> tuple[np.ndarray, int, bool, bool, dict]:
        """
        Compute one step in the game. The received action is applied and a tuple
        containing the current observation as an array, the current reward, a
        boolean specifying wether the game has finished, a boolean specifying
        wether the game was truncated and a dictionary containing information
        about the state of the game.
        """
        terminated = False
        reward = 0
        dt = 40
        if (
            self.enemy_controller.is_blocked
            and self.game_time - self.last_enemy_block_time > 40
        ):
            self.enemy_controller.is_blocked = False
            self.last_enemy_unblock_time = self.game_time
        elif (
            not self.enemy_controller.is_blocked
            and self.game_time - self.last_enemy_unblock_time > 12
        ):
            self.enemy_controller.is_blocked = True
            self.last_enemy_block_time = self.game_time
        last_player_shot_time = 0
        if action == 0:
            pass
        elif action == 1:
            self.player.update(left=True, dt=dt)
        elif action == 2:
            self.player.update(right=True, dt=dt)
        elif action == 3:
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
            reward += self.player_damage_reward
        if self.game_object_controller._check_enemy_hit():
            reward += self.enemy_kill_reward
            # Increase enemy speed based on number of remaining enemies
            if self.number_of_remaining_enemies % 9 == 0:
                new_enemy_speed = 1.1 * self.enemy_controller.current_enemy_speed
                self.enemy_controller.set_enemy_speed(new_enemy_speed)
        # Check if level is finished
        if not self.enemy_controller:
            self.canvas = self.load_new_level(self.canvas)
            self.enemy_controller.set_enemy_speed(
                ENEMY_BASE_SPEED * 1.05 * self.level_generator.level_number
            )
        # Update enemy positions
        if not self.enemy_controller.is_blocked:
            self.enemy_controller.move_enemies(dt)
            if self.enemy_controller.enemy_is_out_of_screen():
                self.enemy_controller.move_enemies_row_down()
                self.enemy_controller.switch_movement_direction()
        # Exit game if enemy makes it to the bottom
        if self.enemy_controller.enemy_height >= HEIGHT:
            terminated = True
        # Shoot new laser once old one is removed from screen
        if not (self.enemy_controller.laser_controller):
            chosen_enemy = self.np_random.choice(self.enemy_controller.sprites())
            self.enemy_controller.laser_controller.add(
                Laser(
                    laser_im,
                    chosen_enemy.rect.midbottom,
                    LASER_BASE_SPEED,
                )
            )
        # Check if player has no lives left
        if self.player.lives <= 0:
            terminated = True
        raw_obs = self.render_frame()
        obs = np.array(Image.fromarray(raw_obs).resize((self.height, self.width)))
        if self.render_mode == "gray_scale_array":
            obs = obs[..., :3] @ [0.299, 0.587, 0.114]
            obs = obs.round().astype(np.uint8)
        self.game_time += 1
        info = self.info
        return obs, reward, terminated, False, info

    def render_frame(self) -> np.ndarray:
        """
        Render one frame and return the pixels that define the screen as an
        array.
        """
        self.canvas.fill(BACKGROUND)
        # Draw all objects on canvas
        self.game_object_controller._draw_all_objects(self.canvas)
        if self.render_mode == "human":
            if self.screen is None:
                pygame.init()
                pygame.display.init()
                self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            if self.clock is None:
                self.clock = pygame.time.Clock()
            # Copy canvas to visible screen
            self.screen.blit(self.canvas, self.canvas.get_rect())
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.update()
        return pygame.surfarray.pixels3d(self.canvas)

    @property
    def number_of_remaining_enemies(self) -> int:
        return len(self.enemy_controller)

    @property
    def enemy_advance(self) -> float:
        """
        Return the y-position of the most advanced enemy in the game relative to
        the distance between top and bottom of the screen.
        """
        return self.enemy_controller.enemy_height / HEIGHT

    @property
    def info(self) -> dict:
        """
        Provide some information about how the game is going. Returns the
        vertical distance of the most advanced enemy, the number of enemies left
        in the current level,the number of lives the player has left and the
        current game time.
        """
        return {
            "enemy_advance": self.enemy_advance,
            "num_remaining_enemies": self.number_of_remaining_enemies,
            "player_lives": self.player.lives,
            "game_time": self.game_time,
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> tuple[np.ndarray, dict]:
        """
        Reset the state of the game. This function is called at the beginning of
        every new game.
        """
        super().reset(seed=seed)
        if options is not None:
            raise NotImplemented
        # Create empty canvas
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.canvas.fill(BACKGROUND)
        # Create blockades and enemies
        self.blockade_controller.blockade_group.empty()
        self.blockade_controller.create_all_blockade_structures()
        initial_enemies = next(self.level_generator)
        self.enemy_controller.empty()
        self.enemy_controller.add(initial_enemies)
        self.player.rect.move(
            (
                WIDTH / 2 - self.player.rect.width / 2,
                HEIGHT - self.player.rect.height,
            )
        )
        self.game_object_controller._clear_all_objects(self.canvas)
        self.game_object_controller._draw_all_objects(self.canvas)
        self.max_num_enemies = len(self.enemy_controller)
        self.canvas.blit(self.player.image, self.player.rect)
        raw_obs = self.render_frame()
        obs = np.array(Image.fromarray(raw_obs).resize((self.height, self.width)))
        if self.render_mode == "gray_scale_array":
            obs = obs[...,:3] @ [0.299, 0.587, 0.114]
            obs = obs.round().astype(np.uint8)
        return obs, self.info

    def close(self) -> None:
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
