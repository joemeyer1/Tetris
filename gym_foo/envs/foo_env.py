
from tetris import Tetris

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class FooEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		t = Tetris()

	def step(self, action):
		t.take_action(action)
		
	def reset(self):
		t = Tetris()
		
	def render(self, mode='human', close=False):
		pass