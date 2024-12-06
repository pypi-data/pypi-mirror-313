import gymnasium as gym
import gym_minigrid     # noqa: F401
from syllabus.examples.task_wrappers import MinigridTaskWrapper
from syllabus.tests import evaluate_random_policy


def make_env():
    env = gym.make("MiniGrid-Empty-8x8-v0")
    env = gym.wrappers.RecordEpisodeStatistics(env)
    env = MinigridTaskWrapper(env)
    return env


evaluate_random_policy(make_env, num_episodes=2000)
