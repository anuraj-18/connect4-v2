import numpy as np 
import random as rd 

from c4Grid import c4Grid

INF = 1000000

RED = 2
YELLOW = 1
DRAW = -1

MAX_MOVES = 42

class c4Agent:
	def __init__(self, color):
		self.color = color

	def getReward(self, winColor):
		if winColor == DRAW:
			return 0

		if self.color == winColor:
			return 1 #for win
		return -1 #for loss

	def makeRandomVirtualMove(self, state, cols, color):
		ok = True
		action = -1
		while ok:
			#check for if win possible in next move or loss can be avoided
			l = len(cols) 
			grid = c4Grid()
			#checking win if any on next move for particular color
			for i in range(l):
				if cols[i] != -1:
					state[cols[i]][i] = color
				if grid.checkWinVirtual(state, cols[i], i):
					x = cols[i]
					y = i
					cols[i] -= 1
					return state, cols, x, y
				else:
					state[cols[i]][i] = 0 #revert change

			#checking loss to avoid, first loss potential found will be used as move
			color = self.switchColor(color)
			for i in range(l):
				if cols[i] != -1:
					state[cols[i]][i] = color
				if grid.checkWinVirtual(state, cols[i], i):
					x = cols[i]
					y = i
					cols[i] -= 1
					color = self.switchColor(color)
					state[x][y] = color #reverting change made for checking loss potential
					return state, cols, x, y
				else:
					state[cols[i]][i] = 0 #revert change
			color = self.switchColor(color)
			#no win found and no loss potential found, continue as normal with random playout
			action = rd.randrange(l)
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
				return 0 #draw reward

			if grid.checkWinVirtual(vgrid, x, y):
				return self.getReward(colorToMove) #return win 

			colorToMove = self.switchColor(colorToMove)

	def getRewardTerminal(self, winColor):
		if winColor == DRAW:
			return 2

		if self.color == winColor:
			return 10 #for win
		return -100000 #for loss


	def getBestMove(self, actions, n_iterations, root, grid):
		next_node = None
		action = 0
		count = 0 
		node = root
		prev_node = root
		color = YELLOW

		for action in actions:
			prev_node = node

			if len(node.children) > 0:
				node = node.children[action]
			else:
				node = None
			color = self.switchColor(color)

			if not node: #check for when playing against human
				prev_node.populateNode(color)
				node = prev_node.children[action]

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
						reward = self.getRewardTerminal(curr.winColor)
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
						reward = self.getRewardTerminal(curr.winColor)
						# print("Backpropagate reward")
						curr.backpropagate(reward)
						
						count += 1
						change = False
						continue

					curr.populateNode(colorToMove)


					curr, _, _ = curr.getMaxUcbNode(root.n)

					if curr.isTerminal:
						# print("is terminal node after expansion")
						reward = self.getRewardTerminal(curr.winColor)
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
				curr, _ , _= curr.getMaxUcbNode(root.n)

		next_node, action, ucbs = node.getMaxUcbNode(root.n)
		
		# print("sending action %s and next node"%(str(action)))
		# print("Total iterations", root.n)
		print(ucbs)
		return root, action


