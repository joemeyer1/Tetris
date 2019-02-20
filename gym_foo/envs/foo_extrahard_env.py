
from tetris import Tetris

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class FooExtraHardEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.t = Tetris()

	def step(self, action):
		self.t.take_action(action)
		
	def reset(self):
		self.t = Tetris()
		
	def render(self, mode='human', close=False):
		pass