import numpy as np 
import os

from c4Node import Node 
from c4Agent import c4Agent
from c4Grid import c4Grid

# import pdb 

# pdb.set_trace()

RED = 2
YELLOW = 1

class c4:
	def __init__(self, yroot, rroot, grid):
		self.yroot = yroot
		self.rroot = rroot
		self.grid = grid
		self.yroot.populateNode(RED)
		self.rroot.populateNode(RED)
		self.rAgent = c4Agent(RED)
		self.yAgent = c4Agent(YELLOW)
		self.actions = ["0", "1", "2", "3", "4", "5", "6"]

	def play(self, n_games, n_iterations):
		for i in range(n_games):
			win = False
			print("-----  GAME %s  -----\n"%(str(i+1)))
			actions = []
			for j in range(42):
				if j%2 == 0:  #red move
					self.rroot, action = self.rAgent.getBestMove(actions, n_iterations, self.rroot, self.grid)
					actions.append(action)
					self.grid.makeMove(RED, action)
					self.grid.displayGrid()
					if self.grid.checkWin():
						print("RED WINS\n")
						win = True
						break
				else: #yellow move
					self.yroot, action = self.yAgent.getBestMove(actions, n_iterations, self.yroot, self.grid)
					actions.append(action)
					self.grid.makeMove(YELLOW, action)
					self.grid.displayGrid()
					if self.grid.checkWin():
						print("YELLOW WINS\n")
						win = True
						break	
			if not win:
				print("DRAW\n")
			print("-----  GAME %s ENDS  -----\n"%(str(i+1)))		
			self.grid.resetGrid()	

	def playAgainstHuman(self, n_games, n_iterations):
			for i in range(n_games):
				win = False
				print("-----  GAME %s  -----\n"%(str(i+1)))
				
				actions = []
				for j in range(42):
					if j%2 == 0:  #red move
						self.rroot, action = self.rAgent.getBestMove(actions, n_iterations, self.rroot, self.grid)
						actions.append(action)
						self.grid.makeMove(RED, action)
						self.grid.displayGrid()
						if self.grid.checkWin():
							print("RED WINS\n")
							win = True
							break
					else: #yellow move
						while True:
							action = input("Enter move:")
							if action in self.actions:
								action = int(action)
								break
							else:
								print("---Enter a number between 0 and 6---")

						actions.append(action)
						self.grid.makeMove(YELLOW, action)
						self.grid.displayGrid()
						if self.grid.checkWin():
							print("YELLOW WINS\n")
							win = True
							break	
				if not win:
					print("DRAW\n")
				print("-----  GAME %s ENDS  -----\n"%(str(i+1)))		
				self.grid.resetGrid()	



grid = c4Grid()
yroot = Node(0, 0, None, grid.grid, grid.cols, grid.moveCnt)
rroot = Node(0, 0, None, grid.grid, grid.cols, grid.moveCnt)
c4 = c4(yroot, rroot, grid)
c4.play(5, 10000)
c4.playAgainstHuman(2, 10000)

