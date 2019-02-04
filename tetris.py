

import numpy as np
import random



class Tetris:

	# tetris shape-type map
	TYPE_MAP = {	0 : "line",
					1 : "square",
					2 : "T",
					3 : "fwd_L",
					4 : "bkwd_L",}


	# make board + a shape
	def __init__(self, width=10):

		random.seed()
		self.width = width
		self.height = width*2
		self.make_ground()
		self.new_shape()
		self.score = 0


	# USER FUNCTIONS:

	def print_board(self):
		board = self.full_board()
		print(board)


	# moves time fwd 1 step
	def step(self):
		# reward for staying alive
		self.score += 1
		if self.bottom_reached():
			self.update_ground()
			self.check_lines()
			if self.check_death():
				print ("GAME OVER")
				print ("Score: ", self.score)
				return self.__init__(self.width)
			# active_squares are now ground
			self.new_shape()
		else:
			self.shape_loc[0] += 1
		self.print_board()


	# rotates active shape
	def rotate(self):
		self.shape_position = (self.shape_position + 1) % 4
		for (y,x) in self.active_squares():
			if not 0<=x<self.width:
				self.shape_position = (self.shape_position - 1) % 4
				break
		self.print_board()

	# moves shape left 1
	def left(self):
		if self.shape_loc[1] > 0:
			self.shape_loc[1] -= 1
		self.print_board()

	# moves shape right 1
	def right(self):
		can_move = True
		for (y,x) in self.active_squares():
			if x == self.width-1:
				# already at edge
				can_move = False
				break
		if can_move:
			self.shape_loc[1] += 1
		self.print_board()


	# HELPER FUNCTIONS:

	def full_board(self):
		board = self.ground.copy()
		for (y, x) in self.active_squares():
			if y>=0:
				board[y][x] = 1
		return board

	# creates new active shape
	def new_shape(self, shape_type=None):
		if not shape_type:
			# leaving this in fn argument yields repetetive results
			shape_type = random.randint(0,4)
		self.shape_type = shape_type
		shape_width = 3
		if self.TYPE_MAP[self.shape_type] is 'square':
			shape_width = 2
		elif self.TYPE_MAP[self.shape_type] is 'line':
			shape_width = 4

		# shape coordinates (bottom-left corner of shape)
		self.shape_loc = [-1, random.randint(0,self.width-shape_width)]
		# shape rotations
		self.shape_position = 0

	# returns array of coordinates of active shape
	def active_squares(self):

		left_corner = self.shape_loc
		shape_before_offset = np.array([left_corner]*4)


		if self.TYPE_MAP[self.shape_type] is "line":
			offset = self.line_offset()

		elif self.TYPE_MAP[self.shape_type] is "square":
			offset = self.sq_offset()

		elif self.TYPE_MAP[self.shape_type] is "T":
			offset = self.T_offset()

		elif self.TYPE_MAP[self.shape_type] is "fwd_L":
			offset = self.fwdL_offset()
			

		elif self.TYPE_MAP[self.shape_type] is "bkwd_L":
			offset = self.bkwdL_offset()
		else:
			raise Exception("Shape not recognized.")

		shape = shape_before_offset + offset
		shape_set = {(y,x) for (y,x) in shape}
		return shape_set
		

	# helper for __init__
	# initializes ground
	def make_ground(self):
		# ground[0][0] is top left corner 
		# 1 indiciates sq is part of ground
		self.ground = np.zeros((self.height, self.width), dtype=int)



	# helper for step
	# ->True iff current shape is at bottom
	def bottom_reached(self):
		active_squares = self.active_squares()
		for (y,x) in active_squares:
			if (y+1,x) not in active_squares:
				if (y+1 == self.height) or (self.ground[y+1][x]):
					return True
		return False

	# helper for step
	# removes any full lines/shift top down
	def check_lines(self):
		row = self.height-1
		while row>=0:
			while self.row_all_ones(row):
				self.score += 100
				self.remove_row(row)
			row -= 1

	# helper for check_lines
	# ->True iff row all ones
	def row_all_ones(self, row):
		for element in self.ground[row]:
			if not element:
				return False
		return True

	# helper for check_lines
	# removes row, shifts top down
	def remove_row(self, row):
		self.ground[:row+1] = np.array([ np.zeros(self.width)] + [line for line in self.ground[:row] ])


	# helper for step
	# ->True iff active-square in top (invisible) row
	def check_death(self):
		for (y, x) in self.active_squares():
			if y<0:
				return True
		return False

	# helper for step
	def update_ground(self):
		for (y,x) in self.active_squares():
			self.ground[y][x] = 1



	# all below is helpers for active_squares()
	def line_offset(self):

		if self.shape_position%2:
			# horizontal
			return np.array([	(0,i) for i in range(4)	])
		else:
			# vertical
			return np.array([	(i-3,0) for i in range(4)	])

	def sq_offset(self):
		return np.array([ (y,x) for y in [-1,0] for x in [0,1]])

	def T_offset(self):

		if self.shape_position is 0:
			return np.array([	(-1,1)] + 
						[(0,i) for i in range(3)	])

		elif self.shape_position is 1:
			return np.array([	(-2,1),
						(-1,0), (-1,1),
								(0, 1)	])

		elif self.shape_position is 2:
			return np.array([	(-1,i) for i in range(3)] +
										[(0,1)	])
		elif self.shape_position is 3:
			return np.array([	(-2,0),
								(-1,0), (-1,1),
								(0, 0)	])

	def fwdL_offset(self):
		if self.shape_position is 0:
			return np.array([	(-1,0)] +
								[[0,i] for i in range(3)])

		elif self.shape_position is 1:
			return np.array([	(-2,1),
								(-1,1),
						 (0,0), (0,1)])

		elif self.shape_position is 2:
			return np.array([	(-1,0), (-1,1), (-1,2),
												(0, 2)	])

		elif self.shape_position is 3:
			return np.array([	(-2,0), (-2,1),
								(-1,0),
								(0, 0)	])

	def bkwdL_offset(self):
		if self.shape_position is 0:
			return np.array([					(-1,2)] +
								[(0,i) for i in range(3)])

		elif self.shape_position is 1:
			return np.array([	(-2,0), (-2,1),
										 (-1,1),
										 (0, 1)	])

		elif self.shape_position is 2:
			return np.array([	(-1,0), (-1,1), (-1,2),
								(0, 0)	])

		elif self.shape_position is 3:
			return np.array([	(-2,0),
								(-1,0),
								(0, 0), (0,1)	])

				










