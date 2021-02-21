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
		print("Grid: ", self.state)
		print("Column values:", self.cols)
		print("Move count: %s"%(str(self.moveCnt)))
		print("Is Terminal: %s"%(str(self.isTerminal)))

	def goUp(self):
		return self.parent

	def populateNode(self, grid, player):
		if self.isTerminal:
			return None

		for i in range(self.n_actions):
			cols = self.cols.copy()
			if cols[i] == -1: #check if valid move 
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
			cols[i] -= 1
			self.children.append(node)

	def calculateUCB(self, N):
		if self.n == 0:
			return INF
		ucb = (self.t/self.n) + (np.log(N)/self.n)**0.5
		return ucb

	def getMaxUcbNode(self, N):
		ucbs = []

		if self.isTerminal:
			return None

		for node in self.children:
			ucbs.append(node.calculateUCB(N))

		ucbs = np.array(ucbs)
		index = np.argmax(ucbs)
		max_node = self.children[index]
		return max_node, index

	def getMinUcbNode(self, N):
		ucbs = []

		if self.isTerminal:
			return None

		for node in self.children:
			ucbs.append(node.calculateUCB(N))

		ucbs = np.array(ucbs)
		index = np.argmin(ucbs)
		min_node = self.children[index]
		return min_node, index

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

class c4Agent:
	def __init__(self, color):
		self.color = color

	def getReward(self, winColor):
		if winColor == -1:
			return 9

		if self.color == winColor:
			return 20 #for win
		return 0 #for loss

	def makeRandomVirtualMove(self, state, cols, color):
		ok = True
		action = -1
		while ok:
			action = rd.randrange(7)
			if cols[action] >= 0 :
				ok = False

		state[cols[action]][action] = color
		x = cols[action]
		y = action
		cols[action] -= 1

		return state, cols, x, y

	def switchColor(self, color):
		if color == RED:
			return YELLOW
		return RED


	def rollout(self, vgrid, vcols, moveCnt, colorToMove):
		grid = c4Grid()
		while True:
			vgrid, vcols, x, y = self.makeRandomVirtualMove(vgrid, vcols, colorToMove)
			colorToMove = self.switchColor(colorToMove)
			moveCnt += 1
			if moveCnt == 42:
				return 9 #draw reward
			if grid.checkWinVirtual(vgrid, x, y):
				return self.getReward(colorToMove) #return win 

	def getBestMove(self, node, n_iterations, N, grid):
		next_node = None
		action = 0
		count = 0 
		if node.checkLeaf():
			node.populateNode(c4Grid(), self.color)
		curr = node
		change = False

		while count < n_iterations:
			if not change: #to reset curr to the initial node
				curr = node
			if curr.checkLeaf():
				print("in leaf node")
				if curr.n == 0:
					#start rollout
					if curr.isTerminal:
						print("is terminal in leaf")
						reward = self.getReward(curr.winColor)
						print("Backpropagate reward")
						curr.backpropagate(reward)
						N += 1
						
						count += 1
						change = False
						continue
					else:
						print("rollout in first visit")
						vgrid = curr.state.copy()
						vcols = curr.cols.copy()
						colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED
						reward = self.rollout(vgrid, vcols, curr.moveCnt, colorToMove)
						print("Backpropagate reward")
						curr.backpropagate(reward)
						N += 1
						
						count += 1
						change = False
						continue
				else:
					#get node
					colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED
					print("Expansion in visited node")

					if curr.isTerminal:
						print("is terminal in leaf")
						reward = self.getReward(curr.winColor)
						print("Backpropagate reward")
						curr.backpropagate(reward)
						N += 1
						
						count += 1
						change = False
						continue

					curr.populateNode(grid, colorToMove)

					if self.color == RED:
						curr, _ = curr.getMaxUcbNode(N)
					else:
						curr, _ = curr.getMinUcbNode(N)

					vgrid = curr.state.copy()
					vcols = curr.cols.copy()
					colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED
					print("Rollout in through expanded node")
					reward = self.rollout(vgrid, vcols, curr.moveCnt, colorToMove)
					print("Backpropagate reward")
					curr.backpropagate(reward)
					N += 1
					
					count += 1
					change = False
					continue

			else:
				change = True
				if self.color == RED:
					print("going to max node")
					curr, _ = curr.getMaxUcbNode(N)
				else:
					print("going to min ucb node")
					curr, _ = curr.getMinUcbNode(N)

		if self.color == RED:
			next_node, action = node.getMaxUcbNode(N)
		else:
			next_node, action = node.getMinUcbNode(N) 
		print("sending action %s and next node"%(str(action)))
		return action, next_node

