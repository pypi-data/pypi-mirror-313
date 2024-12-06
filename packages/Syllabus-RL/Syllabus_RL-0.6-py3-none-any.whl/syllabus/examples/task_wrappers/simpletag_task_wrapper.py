""" Task wrapper for NLE that can change tasks at reset using the NLE's task definition format. """
from pettingzoo.mpe import simple_tag_v3
from pettingzoo.utils.env import ParallelEnv

from syllabus.core import PettingZooTaskWrapper
from syllabus.task_space import MultiDiscreteTaskSpace


class SimpleTagTaskWrapper(PettingZooTaskWrapper):
    """
    This wrapper simply changes the seed of a Minigrid environment.
    """

    def __init__(self, env: ParallelEnv):
        super().__init__(env)
        self.env = env
        self.env.unwrapped.task = 1
        self.task = None

        # Task completion metrics
        self.episode_return = 0
        self.task_space = MultiDiscreteTaskSpace((4, 4, 4), [["1g", "2g", "3g", "4g"], [
                                                 "1a", "2a", "3a", "4a"], ["1o", "2o", "3o", "4o"]])

    def reset(self, new_task: int = None, **kwargs):
        # Change task if new one is provided
        # if new_task is not None:
        #     self.change_task(new_task)

        self.episode_return = 0
        if new_task is not None:
            good, adversary, obstacle = new_task
            # Inject current_task into the environment
            self.env = simple_tag_v3.parallel_env(
                num_good=good, num_adversaries=adversary, num_obstacels=obstacle, continuous=False, max_cycles=125
            )
            self.task = new_task
        return self.observation(self.env.reset(**kwargs))
