import numpy as np 
import random as rd 

from c4Grid import c4Grid

INF = 1000000

RED = 2
YELLOW = 1

class c4Agent:
	def __init__(self, color):
		self.color = color

	def getReward(self, winColor):
		if winColor == -1:
			return 1

		if self.color == winColor:
			return 100 #for win
		return -100 #for loss

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
			
			moveCnt += 1
			if moveCnt == 42:
				return 1 #draw reward

			if grid.checkWinVirtual(vgrid, x, y):
				return self.getReward(colorToMove) #return win 

			colorToMove = self.switchColor(colorToMove)

	def getBestMove(self, actions, n_iterations, root, grid):
		next_node = None
		action = 0
		count = 0 
		node = root

		for action in actions:
			node = node.children[action]

		if node.checkLeaf():
			node.populateNode(self.color)

		curr = node
		change = False

		while count < n_iterations:
			if not change: #to reset curr to the initial node
				curr = node
			if curr.checkLeaf():
				# print("in leaf node")
				if curr.n == 0:
					#start rollout
					if curr.isTerminal:
						# print("is terminal in leaf")
						reward = self.getReward(curr.winColor)
						# print("Backpropagate reward")
						curr.backpropagate(reward)
						
						count += 1
						change = False
						continue
					else:
						# print("rollout in first visit")
						vgrid = curr.state.copy()
						vcols = curr.cols.copy()
						colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED
						
						reward = self.rollout(vgrid, vcols, curr.moveCnt, colorToMove)
						# print("Backpropagate reward")
						curr.backpropagate(reward)
						
						count += 1
						change = False
						continue
				else:
					#get node
					colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED
					# print("Expansion in visited node")

					if curr.isTerminal:
						# print("is terminal node ")
						reward = self.getReward(curr.winColor)
						# print("Backpropagate reward")
						curr.backpropagate(reward)
						
						count += 1
						change = False
						continue

					curr.populateNode(colorToMove)

					if self.color == RED:
						# print("selecting max in expansion")
						curr, _ = curr.getMaxUcbNode(root.n)
					else:
						# print("selecting min in expansion")
						curr, _ = curr.getMinUcbNode(root.n)

					if curr.isTerminal:
						# print("is terminal node after expansion")
						reward = self.getReward(curr.winColor)
						# print("Backpropagate reward")
						curr.backpropagate(reward)
						
						count += 1
						change = False
						continue

					vgrid = curr.state.copy()
					vcols = curr.cols.copy()

					colorToMove = YELLOW if curr.moveCnt%2 == 1 else RED

					# print("Rollout in through expanded node")
					reward = self.rollout(vgrid, vcols, curr.moveCnt, colorToMove)
					# print("Backpropagate reward")
					curr.backpropagate(reward)
					
					count += 1
					change = False
					continue

			else:
				change = True
				if self.color == RED:
					# print("going to max node")
					curr, _ = curr.getMaxUcbNode(root.n)
				else:
					# print("going to min ucb node")
					curr, _ = curr.getMinUcbNode(root.n)

		if self.color == RED:
			next_node, action = node.getMaxUcbNode(root.n)
		else:
			next_node, action = node.getMinUcbNode(root.n) 
		# print("sending action %s and next node"%(str(action)))
		# print("Total iterations", root.n)
		return root, action


