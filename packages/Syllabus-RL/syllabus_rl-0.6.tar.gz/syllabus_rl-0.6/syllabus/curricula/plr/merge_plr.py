import time
import wandb
import warnings
from typing import Any, Dict, List, Tuple, Union

import gymnasium as gym
import numpy as np
import torch
from gymnasium.spaces import Discrete, MultiDiscrete

from syllabus.core import Curriculum, UsageError, enumerate_axes
from syllabus.core.evaluator import Evaluator
from syllabus.task_space import TaskSpace

from .task_sampler import TaskSampler


class RolloutStorage():
    def __init__(
        self,
        num_steps: int,
        num_processes: int,
        requires_value_buffers: bool,
        observation_space: gym.Space,   # TODO: Use np array when space is box or discrete
        num_minibatches: int = 1,
        buffer_size: int = 4,
        action_space: gym.Space = None,
        lstm_size: int = None,
        evaluator: Evaluator = None,
        device: str = "cpu",
        provide_score: bool = False,
    ):
        self.num_steps = num_steps
        # Hack to prevent overflow from lagging updates.
        self.buffer_steps = num_steps * buffer_size
        self.num_processes = num_processes
        self.num_minibatches = num_minibatches
        self._requires_value_buffers = requires_value_buffers
        self.evaluator = evaluator
        self.device = device
        self.provide_score = provide_score

        self.tasks = torch.zeros(self.buffer_steps, num_processes, 1, dtype=torch.int)
        self.masks = torch.ones(self.buffer_steps + 1, num_processes, 1)

        self.lstm_states = None
        if lstm_size is not None:
            self.lstm_states = (
                torch.zeros(self.buffer_steps + 1, num_processes, lstm_size),
                torch.zeros(self.buffer_steps + 1, num_processes, lstm_size),
            )

        self.obs = {env_idx: [None for _ in range(self.buffer_steps)] for env_idx in range(self.num_processes)}
        self.env_steps = [0] * num_processes
        self.value_steps = torch.zeros(num_processes, dtype=torch.int)

        self.ready_buffers = set()

        if requires_value_buffers:
            self.returns = torch.zeros(self.buffer_steps + 1, num_processes, 1)
            self.rewards = torch.zeros(self.buffer_steps, num_processes, 1)
            self.value_preds = torch.zeros(self.buffer_steps + 1, num_processes, 1)
        else:
            if action_space is None:
                raise ValueError(
                    "Action space must be provided to PLR for strategies 'policy_entropy', 'least_confidence', 'min_margin'"
                )
            self.action_log_dist = torch.zeros(self.buffer_steps, num_processes, action_space.n)

        if self.provide_score:
            self.scores = torch.zeros(num_steps, num_processes)

        self.num_steps = num_steps
        self.env_to_idx = {}
        self.max_idx = 0
        self.to(self.device)

    @property
    def using_lstm(self):
        return self.lstm_states is not None

    def get_idxs(self, env_ids):
        """ Map the environment ids to indices in the buffer. """
        idxs = []
        for env_id in env_ids:
            if env_id not in self.env_to_idx:
                self.env_to_idx[env_id] = self.max_idx
                self.max_idx += 1
            idxs.append(self.env_to_idx[env_id])
        return idxs

    def to(self, device):
        self.device = device
        self.masks = self.masks.to(device)
        self.tasks = self.tasks.to(device)

        if self.using_lstm:
            self.lstm_states = (
                self.lstm_states[0].to(device),
                self.lstm_states[1].to(device),
            )
        if self._requires_value_buffers:
            self.rewards = self.rewards.to(device)
            self.value_preds = self.value_preds.to(device)
            self.returns = self.returns.to(device)
        else:
            self.action_log_dist = self.action_log_dist.to(device)

    def insert_env_step(self, env_ids, masks, obs=None, reward=None, task=None, steps=1):
        env_index = self.get_idxs([env_ids])[0]
        assert steps < self.buffer_steps, f"Number of steps {steps} exceeds buffer size {self.buffer_steps}. Increase PLR's num_steps or decrease environment wrapper's batch size."
        step = self.env_steps[env_index]
        end_step = step + steps
        assert end_step < self.buffer_steps, f"Number of steps {steps} exceeds buffer size {self.buffer_steps}. Increase PLR's num_steps or decrease environment wrapper's batch size."

        # Insert data into buffer
        self.masks[step + 1:end_step + 1, env_index].copy_(torch.as_tensor(masks[:, None]))

        if obs is not None:
            self.obs[env_index][step: end_step] = obs

        if reward is not None:
            self.rewards[step:end_step, env_index].copy_(torch.as_tensor(reward[:, None]))

        # if action_log_dist is not None:
        #     self.action_log_dist[step:end_step, env_index].copy_(torch.as_tensor(action_log_dist[:, None]))

        if task is not None:
            self.tasks[step:end_step, env_index].copy_(torch.as_tensor(np.array(task)[:, None]))

        self.env_steps[env_index] += steps

        # Get value predictions if batch is ready
        value_steps = self.value_steps.numpy()
        while all((self.env_steps - value_steps) > 0):
            self.get_value_predictions()

        # Check if the buffer is ready to be updated. Wait until we have enough value predictions.
        if env_index not in self.ready_buffers and self.value_steps[env_index] >= self.num_steps + 1:
            self.ready_buffers.add(env_index)

    def insert_learner_step(self, masks, tasks, action_log_dist=None, value_preds=None, rewards=None, next_values=None, scores=None, env_ids=None):
        # Convert env_ids to indices in the buffer
        if env_ids is None:
            env_ids = list(range(self.num_processes))
        env_idxs = self.get_idxs(env_ids)

        if self.provide_score:
            if scores is None:
                raise UsageError("Score must be provided in update when provide_score is enabled for PLR.")
            self.scores[self.env_steps[env_idxs], env_idxs] = torch.as_tensor(scores).reshape((len(env_idxs), 1)).cpu()
        elif self._requires_value_buffers:
            assert (value_preds is not None and rewards is not None), "Selected strategy requires value_preds and rewards"
            if len(rewards.shape) == 3:
                rewards = rewards.squeeze(2)
            self.value_preds[self.env_steps[env_idxs], env_idxs] = torch.as_tensor(
                value_preds).reshape((len(env_idxs), 1)).cpu()
            if next_values is not None:
                self.value_preds[self.env_steps[env_idxs] + 1,
                                 env_idxs] = torch.as_tensor(next_values).reshape((len(env_idxs), 1)).cpu()
            self.rewards[self.env_steps[env_idxs], env_idxs] = torch.as_tensor(
                rewards).reshape((len(env_idxs), 1)).cpu()
        else:
            self.action_log_dist[self.env_steps[env_idxs],
                                 env_idxs] = action_log_dist.reshape((len(env_idxs), -1)).cpu()

        self.masks[self.env_steps[env_idxs] + 1, env_idxs] = torch.IntTensor(masks.cpu()).reshape((len(env_idxs), 1))
        self.tasks[self.env_steps[env_idxs], env_idxs] = torch.IntTensor(tasks).reshape((len(env_idxs), 1))
        self.env_steps[env_idxs] = (self.env_steps[env_idxs] + 1) % (self.num_steps + 1)

        # Check if the buffer is ready to be updated
        for env_index in env_idxs:
            if env_index not in self.ready_buffers and self.env_steps[env_index] >= self.num_steps + 1:
                self.ready_buffers.add(env_index)

    def get_value_predictions(self):
        value_steps = self.value_steps.numpy()
        try:
            process_chunks = np.split(np.arange(self.num_processes), self.num_minibatches)
        except ValueError as e:
            raise UsageError(
                f"Number of processes {self.num_processes} must be divisible by the number of minibatches {self.num_minibatches}."
            ) from e

        for processes in process_chunks:
            obs = [self.obs[env_idx][value_steps[env_idx]] for env_idx in processes]
            lstm_states = dones = None
            if self.using_lstm:
                lstm_states = (
                    torch.unsqueeze(self.lstm_states[0][value_steps[processes], processes], 0),
                    torch.unsqueeze(self.lstm_states[1][value_steps[processes], processes], 0),
                )
                dones = torch.squeeze(1 - self.masks[value_steps[processes], processes], -1).int()

            # Get value predictions and check for common usage errors
            try:
                values, lstm_states, extras = self.evaluator.get_value(obs, lstm_states, dones)
            except RuntimeError as e:
                raise UsageError(
                    "Encountered an error getting values for PLR. Check that lstm_size is set correctly and that there are no errors in the evaluator's get_action_and_value implementation."
                ) from e

            self.value_preds[value_steps[processes], processes] = values.to(self.device)
            self.value_steps[processes] += 1   # Increase index to store lstm_states and next iteration
            value_steps = self.value_steps.numpy()

            if self.using_lstm:
                assert lstm_states is not None, "Evaluator must return lstm_state in extras for PLR."
                # Place new lstm_states in next step
                self.lstm_states[0][value_steps[processes], processes] = lstm_states[0].to(self.lstm_states[0].device)
                self.lstm_states[1][value_steps[processes], processes] = lstm_states[1].to(self.lstm_states[1].device)

    def after_update(self, env_index):
        # After consuming the first num_steps of data, remove them and shift the remaining data in the buffer
        self.tasks[:, env_index] = self.tasks[:, env_index].roll(-self.num_steps, 0)
        self.masks[:, env_index] = self.masks[:, env_index].roll(-self.num_steps, 0)
        self.obs[env_index] = self.obs[env_index][self.num_steps:]

        if self.using_lstm:
            self.lstm_states[0][:, env_index] = self.lstm_states[0][:, env_index].roll(-self.num_steps, 0)
            self.lstm_states[1][:, env_index] = self.lstm_states[1][:, env_index].roll(-self.num_steps, 0)

        if self._requires_value_buffers:
            self.returns[:, env_index] = self.returns[:, env_index].roll(-self.num_steps, 0)
            self.rewards[:, env_index] = self.rewards[:, env_index].roll(-self.num_steps, 0)
            self.value_preds[:, env_index] = self.value_preds[:, env_index].roll(-(self.num_steps), 0)
        else:
            self.action_log_dist[:, env_index] = self.action_log_dist[:, env_index].roll(-self.num_steps, 0)

        self.env_steps[env_index] -= self.num_steps
        self.value_steps[env_index] -= self.num_steps
        self.ready_buffers.remove(env_index)

    def compute_returns(self, gamma, gae_lambda, env_index):
        assert self._requires_value_buffers, "Selected strategy does not use compute_rewards."
        gae = 0
        for step in reversed(range(self.num_steps)):
            delta = (
                self.rewards[step, env_index]
                + gamma * self.value_preds[step + 1, env_index] * self.masks[step + 1, env_index]
                - self.value_preds[step, env_index]
            )
            gae = delta + gamma * gae_lambda * self.masks[step + 1, env_index] * gae
            self.returns[step, env_index] = gae + self.value_preds[step, env_index]
