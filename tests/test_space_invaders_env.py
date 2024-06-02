import pytest
import space_invaders
import gymnasium


def test_observation_space_shape():
    rgb_env = gymnasium.make("CustomSpaceInvaders-v0", render_mode="rgb_array")
    gray_scale_env = gymnasium.make(
        "CustomSpaceInvaders-v0", render_mode="gray_scale_array"
    )
    for env in [rgb_env, gray_scale_env]:
        obs, _ = env.reset()
        assert obs.shape == env.observation_space.shape


def test_reward():
    env = gymnasium.make(
        "CustomSpaceInvaders-v0",
        render_mode="rgb_array",
        reward={"player_damage": -5, "enemy_kill": 10},
        max_episode_steps=500,
    )
    env.reset()
    total_reward = 0
    terminated = False
    truncated = False
    while not (terminated or truncated):
        obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
        total_reward += reward  # type: ignore
        assert any((reward == 0, reward == -5, reward == 10))
