import numpy as np 
import os

from c4Node import Node, c4Agent
from c4Grid import c4Grid

# import pdb 

# pdb.set_trace()

RED = 2
YELLOW = 1

class c4:
	def __init__(self, root, grid):
		self.root = root
		self.grid = grid
		self.root.populateNode(grid, RED)
		self.rAgent = c4Agent(RED)
		self.yAgent = c4Agent(YELLOW)
		

	def play(self, n_games, n_iterations):
		for i in range(n_games):
			win = False
			print("-----  GAME %s  -----"%(str(i+1)))
			curr = self.root
			for j in range(42):
				if j%2 == 0:  #red move
					action, curr = self.rAgent.getBestMove(curr, n_iterations, self.root.n, self.grid)
					self.grid.makeMove(RED, action)
					self.grid.displayGrid()
					if self.grid.checkWin():
						print("RED WINS")
						win = True
						break
				else: #yellow move
					# self.root.children[0].showParams()
					action, curr = self.yAgent.getBestMove(curr, n_iterations, self.root.n, self.grid)
					self.grid.makeMove(YELLOW, action)
					self.grid.displayGrid()
					if self.grid.checkWin():
						print("YELLOW WINS")
						win = True
						break	
			if not win:
				print("DRAW")
			print("-----  GAME %s ENDS  -----"%(str(i+1)))		
			self.grid.resetGrid()		



grid = c4Grid()
root = Node(0, 0, None, grid.grid, grid.cols, grid.moveCnt)
c4 = c4(root, grid)
c4.play(5, 7)

