import numpy as np 
import random as rd 

from c4Grid import c4Grid

INF = 1000000

RED = 2
YELLOW = 1

class Node:
	def __init__(self, total_score, ni, parent, state, cols, moveCnt):
		self.t = total_score
		self.n = ni
		self.parent = parent
		self.children = []
		self.n_actions = 7

		self.state = state
		self.cols = cols
		self.moveCnt = moveCnt

		self.isTerminal = False
		self.winColor = 0

	def showParams(self):
		print("Total score: %s"%(str(self.t)))
		print("Total visits: %s"%(str(self.n)))
		print("Grid: \n", self.state)
		print("Column values: \n", self.cols)
		print("Move count: %s"%(str(self.moveCnt)))
		print("Is Terminal: %s"%(str(self.isTerminal)))

	def showStates(self):
		if len(self.children) == 0:
			print(None)
		else:
			k = 0
			for node in self.children:
				print("---- State %s ----"%(str(k+1)))
				print(node.state)
				print()
				k += 1

	def goUp(self):
		return self.parent

	def populateNode(self, player):
		if self.isTerminal:
			return None

		grid = c4Grid()

		for i in range(self.n_actions):
			cols = self.cols.copy()
			if cols[i] <= -1: #check if valid move 
				self.children.append(None)
				continue

			next_state = self.state.copy()  #copying next state for child node
			next_state[cols[i]][i] = player  #making move for child node state
			
			node = Node(0, 0, self, next_state, cols, self.moveCnt+1)

			if grid.checkWinVirtual(next_state, cols[i], i):
				node.isTerminal = True
				node.winColor = player #win for RED/YELLOW

			if node.moveCnt == 42:
				node.isTerminal = True
				node.winColor = -1 #draw
			node.cols[i] -= 1

			self.children.append(node)

	def calculateUCB(self, N):
		if self.n == 0:
			return INF
		ucb = (self.t/self.n) + (2*(np.log(N)/self.n)**0.5)
		return ucb

	def getMaxUcbNode(self, N):
		ucbs = []

		if self.isTerminal:
			return None

		inc = 0

		for node in self.children:
			if node:
				ucbs.append(node.calculateUCB(N))
			else:
				ucbs.append(None)

		max_ind = 0
		max_val = -1*INF
		l = len(self.children)
		for i in range(l):
			if ucbs[i] != None and ucbs[i] > max_val:
				max_ind = i
				max_val = ucbs[i]

		max_node = self.children[max_ind]
		return max_node, max_ind

	def getMinUcbNode(self, N):
		ucbs = []

		if self.isTerminal:
			return None

		for node in self.children:
			if node:
				ucbs.append(node.calculateUCB(N))
			else:
				ucbs.append(None)

		min_ind = 0
		min_val = INF+1
		l = len(self.children)
		for i in range(l):
			if ucbs[i] != None and ucbs[i] < min_val:
				min_ind = i
				min_val = ucbs[i]

		min_node = self.children[min_ind]
		return min_node, min_ind

	def checkLeaf(self):
		if len(self.children) == 0:
			return True
		return False

	def backpropagate(self, reward):
		self.n += 1
		self.t += reward
		curr = self.parent

		while curr:
			curr.n += 1
			curr.t += reward
			curr = curr.goUp()



