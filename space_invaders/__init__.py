from gymnasium.envs.registration import register

register(
    id="CustomSpaceInvaders-v0",
    entry_point="space_invaders.gym_env:SpaceInvadersEnv",
    max_episode_steps=3000,
)
