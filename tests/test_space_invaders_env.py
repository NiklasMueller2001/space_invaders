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
