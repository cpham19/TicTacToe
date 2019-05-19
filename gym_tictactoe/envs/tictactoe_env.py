from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import *
import gym, numpy as np, random, copy
from gym import error, spaces, utils
from gym.utils import seeding
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent

class TicTacToe(gym.Env):
	metadata = {'render.modes': ['human']}

	"""
	Description:
		Tic Tac Toe is a simple game that you win by having the same marks on a row, column, or diagonal

    Observation: 
        Type: Discrete (9)
        Num		Observation
		0		First square in the first row is marked/unmarked
		1		Second square in the first row is marked/unmarked
		2		Third square in the first row is marked/unmarked
		3		First square in the second row is marked/unmarked
		4		Second square in the second row is marked/unmarked
		5		Third square in the second row is marked/unmarked
		6		First square in the third row is marked/unmarked
		7		Second square in the third row is marked/unmarked
		8		Third square in the third row is marked/unmarked
        
    Actions:
        Type: Discrete(9)
        Num	Action
        0	Mark the first square in the first row
        1	Mark the second square in the first row
        2	Mark the third square in the first row
        3	Mark the first square in the second row
        4	Mark the second square in the second row
        5	Mark the third square in the second row
        6	Mark the first square in the third row
        7	Mark the second square in the third row
        8	Mark the third square in the third row

    Reward:
        Reward is 100 for every step taken, including the termination step
        
    Starting State:
        The gameboard is empty.
        
    Episode Termination:
        The game is completed when someone wins by having three marks on a row, column, or diagonal or when the game reaches a draw by depleting the number of turns (9)
    """


	def __init__(self):
		self.matchHistory = []
		self.formattedMatchHistory = []

		self.playerWins = 0
		self.bot1Wins = 0

		self.totalTrainingWinsForBot1 = 0
		self.totalTrainingWinsForBot2 = 0
		self.totalTrainingDraws = 0

		self.state = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
		self.turns = 0
		self.matchs = 1
		self.done = 0
		self.draws = 0
		self.validMove = True
		self.training = False

	def init(self, player1, bot1, bot2):
		# Represents the player
		self.player = player1

		# The Bot that will play against the player
		self.bot1 = bot1

		# Create a bot to play against the second bot (Player 2) for training
		self.bot2 = bot2

	# Check if each column or row is occupied and has the same mark
	def checkRowsAndCols(self):
		stateObj = {'win': False, 'winner': "None"}
		for i in range(3):
			if (self.state[i][0] != " " and self.state[i][0] == self.state[i][1] and self.state[i][1] == self.state[i][2]):
				if (self.state[i][0] == "O" or self.state[0][i] == "O"):
					stateObj['winner'] = self.player.name if (self.player.mark == "O") else self.bot1.name
					stateObj['win']  = True
				else:
					stateObj['winner'] =  self.player.name if (self.player.mark == "X") else self.bot1.name
					stateObj['win'] = True
			elif(self.state[0][i] != " " and self.state[0][i] == self.state[1][i] and self.state[1][i] ==self.state[2][i]):
				if (self.state[0][i] == "O"):
					stateObj['winner'] = self.player.name if (self.player.mark == "O") else self.bot1.name
					stateObj['win'] = True
				else:
					stateObj['winner'] = self.player.name if (self.player.mark == "X") else self.bot1.name
					stateObj['win'] = True

		return stateObj

	# Check if minor or major diagonal is occupied and has the same mark
	def checkDiagonals(self):
		stateObj = {'win': False, 'winner': "None"}
		if (self.state[0][0] != " " and self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]):
			if (self.state[0][0] == "O"):
				stateObj['winner']  = self.player.name if (self.player.mark == "O") else self.bot1.name
				stateObj['win'] = True
			else:
				stateObj['winner']  = self.player.name if (self.player.mark == "X") else self.bot1.name
				stateObj['win'] = True
		elif (self.state[0][2] != " " and self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]):
			if (self.state[0][2] == "O"):
				stateObj['winner']  = self.player.name if (self.player.mark == "O") else self.bot1.name
				stateObj['win'] = True
			else:
				stateObj['winner']  = self.player.name if (self.player.mark == "X") else self.bot1.name
				stateObj['win'] = True

		return stateObj

	# Check the game if someone won, if the game reaches a draw, or game is still going on
	def check(self):
		stateObj = {'win': False, 'winner': "None"}
		if (self.turns < 5):
			return stateObj

		outcome = self.checkDiagonals()
		if(outcome['win'] == True):
			return outcome

		outcome = self.checkRowsAndCols()
		if (outcome['win'] == True):
			return outcome

		return stateObj

	#  Change the state after every action made by player or computer
	def step(self, target, mark):
		stateObj = {}

		# Pointless if you and the bot knows how to make proper moves!!! (for example, prevent the player from pressing a square on a GUI or rerandomizing a random move from a bot if it's invalid)
		if self.state[int(target/3)][target%3] != " ":
			#print("Invalid Step")
			if (mark == self.player.mark and type(self.player) == TicTacToeAgent):
				self.punishBotForInvalidMove(self.player, -0.5)
			elif (mark == self.bot1.mark and type(self.bot1) == TicTacToeAgent):
				self.punishBotForInvalidMove(self.bot1, -0.5)

			self.validMove = False
		else:
			self.state[int(target/3)][target%3] = mark
			self.validMove = True
			self.turns += 1
			if(self.turns == 9):
				self.done = 1

		checkState = self.check()

		# Reward Bot for winning/Punish Bot for losing
		if(checkState['win'] == True):
			self.done = 1;

			if (checkState['winner'] == self.player.name):
				if (type(self.player) == TicTacToeAgent):
					self.rewardBot(self.player, 1)

				if (type(self.bot1) == TicTacToeAgent):
					self.rewardBot(self.bot1, -1)
					self.reward = -1

				self.playerWins += 1
			else:
				if (type(self.bot1) == TicTacToeAgent):
					self.rewardBot(self.bot1, 1)
					self.reward = 1

				if (type(self.player) == TicTacToeAgent):
					self.rewardBot(self.player, -1)

				self.bot1Wins += 1

			#print(checkState['winner'] + " wins.", sep="", end="\n")
			self.matchs += 1

		# If the game's outcome is draw
		elif (checkState['win'] == False and self.done == 1):
			self.draws += 1
			if (type(self.player) == TicTacToeAgent):
				self.rewardBot(self.player, 0.5)

			if (type(self.bot1) == TicTacToeAgent):
				self.rewardBot(self.bot1, 0.5)
				self.reward = 0.5

			#print("DRAW! No one wins!")
			self.matchs += 1

		stateObj['state'] = self.state
		stateObj['turn'] = self.turns
		stateObj['done'] = self.done
		stateObj['reward'] = self.reward
		stateObj['winner'] = checkState['winner']
		stateObj['validMove'] = self.validMove

		return stateObj

	def punishBotForInvalidMove(self, player, reward):
		# Last move made by player
		last_state_key, last_move = player.state_order.pop()
		# Zero matrix
		player.states[last_state_key] = np.zeros((3, 3))
		# Punishing the player's invalid move
		player.states[last_state_key].itemset(last_move, reward)

	# Rewarding or Punishing the bot
	def rewardBot(self, player, reward):
		# Used for comparing from old to new
		self.old_state_order = copy.deepcopy(player.state_order)
		self.old_states = copy.deepcopy(player.states)

		# Last move made by bot
		last_state_key, last_move = player.state_order.pop()
		# Zero matrix
		player.states[last_state_key] = np.zeros((3, 3))
		# Rewarding or punishing the state
		player.states[last_state_key].itemset(last_move, reward)

		print("Original Reward: " + str(reward))
		print("Learning Rate: " + str(self.bot1.learning_rate))

		# Going through the rest of the moves that the bot has made
		while (player.state_order):
			# Move made by bot
			state_key, move = player.state_order.pop()

			# Reducing reward
			reward *= player.discount_factor
			print("Reduced Reward by Discount Factor: " + str(reward))

			# Calculating temporal difference formula (difference between values of state on the basis of time)
			# Found at https://en.wikipedia.org/wiki/Temporal_difference_learning and https://detailed.af/reinforcement/)
			last_state = player.states[last_state_key]
			current_state = player.states.get(state_key, np.zeros((3, 3)))
			temporal_difference = current_state + player.learning_rate * ((reward * last_state) - current_state)

			print()
			print("CURRENT STATE")
			print(current_state)
			print()

			print("LAST STATE")
			print(player.states[last_state_key])
			print()

			print("Temporal Difference Calculation: " + str(current_state.item(last_move)) + " + " + str(player.learning_rate) + " *  ((" + str(reward) + " * " + str(last_state.item(last_move)) + ") - " + str(current_state.item(last_move)) + ") = " + str(temporal_difference.item(last_move)))
			print("Temporal Difference")
			print(temporal_difference)
			print()

			# State was encountered before so we increase the reward
			if (state_key in player.states):
				reward += temporal_difference.item(last_move)

				print("State was encountered before so we increase the reward")
				print("Reward is now " + str(reward))
				print()

				player.states[state_key].itemset(move, reward)

			# State was not encountered before so we set the reward to a new one
			else:
				# Assign a new key to the array of states and set its reward
				player.states[state_key] = np.zeros((3,3))
				reward = temporal_difference.item(last_move)
				print("State was not encountered before")
				print("Reward is now " + str(reward))
				player.states[state_key].itemset(move, reward)

			# Last state key and move are now the previous state key and move (as we pop moves out of the state_order array)
			last_state_key = state_key
			last_move = move

	#Reset the board and counters
	def reset(self):
		# Randomize the player who goes first
		self.turn = self.player.mark if (random.randint(0, 1) == 0) else self.bot1.mark
		for row in range(0, len(self.state)):
			for col in range(0, len(self.state[row])):
				self.state[row][col] = ' '
		self.turns = 0
		self.done = 0
		self.reward = 0
		self.validMove = True

		return self.state

	# Print the Tic Tac Toe board
	def render(self):
		for row in range(3):
			for col in range(3):
				if (col != 2):
					print(self.state[row][col], end=" | ")
				else:
					print(self.state[row][col], end=" ")
			if (row != 2):
				print('\n---------')
		print("\n")

	def convertMatchHistory(self, matchHistory):
		formattedMatchHistory = []

		for match in matchHistory:
			array = []
			array.append(match['number'])
			array.append(match['type'])
			array.append(match['player1'])
			array.append(match['player2'])
			array.append(len(match['turns']))
			array.append(match['winner'])
			formattedMatchHistory.append(array)

		return formattedMatchHistory

	def train(self, games, page):
		progress = QProgressDialog("Please wait, the bot is being trained!", "Cancel", 0, games, page)
		progress.setWindowModality(Qt.WindowModal)
		progress.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
		progress.setAutoReset(False)
		progress.setAutoClose(True)
		progress.setCancelButton(None)
		progress.setMinimum(0)
		progress.setMaximum(games)
		progress.resize(500, 100)
		progress.setWindowTitle("Training the bot..")
		progress.setValue(0)
		progress.show()

		trainObj = {}

		# Save the wins from playing actual games
		player = self.player
		playerWins = self.playerWins
		bot1Wins = self.bot1Wins
		draws = self.draws

		self.player = self.bot2
		self.playerWins = 0
		self.bot1Wins = 0
		self.draws = 0

		# Bots playing each other
		for i in range(1, games + 1):
			self.reset()
			progress.setValue(i)
			match = {}
			match['number'] = self.matchs
			match['type'] = 'Training'
			match['player1'] = self.player.name
			match['player2'] = self.bot1.name
			match['turns'] = []

			while (True):
				stateObj = None
				if(self.turn == self.bot2.name):
					action = self.bot2.action(self.state)
					stateObj = self.step(action, self.bot2.mark)

					# Bot makes invalid move
					while (type(self.bot2) == TicTacToeAgent and stateObj['validMove'] != True):
						action = self.bot2.action(self.state)
						stateObj = self.step(action, self.bot2.mark)

					turn = {}
					turn['number'] = stateObj['turn']
					turn['playerTurn'] = self.bot2.name
					turn['state'] = copy.deepcopy(stateObj['state'])
					match['turns'].append(turn)

					self.turn = self.bot1.name

				else:
					action = self.bot1.action(self.state)
					stateObj = self.step(action, self.bot1.mark)

					# Bot makes invalid move
					while(type(self.bot1) == TicTacToeAgent and stateObj['validMove'] != True):
						action = self.bot1.action(self.state)
						stateObj = self.step(action, self.bot1.mark)

					turn = {}
					turn['number'] = stateObj['turn']
					turn['playerTurn'] = self.bot1.name
					turn['state'] = copy.deepcopy(stateObj['state'])
					match['turns'].append(turn)

					self.turn = self.bot2.name


				if (stateObj['done'] == 1):
					match['winner'] = stateObj['winner']
					self.matchHistory.append(match)
					break

		progress.close()

		# Record the wins during training phase
		trainObj['bot1Wins'] = self.bot1Wins
		self.totalTrainingWinsForBot1 += self.bot1Wins
		trainObj['bot2Wins'] = self.playerWins
		self.totalTrainingWinsForBot2 += self.playerWins
		trainObj['draws'] = self.draws
		self.totalTrainingDraws += self.draws

		# Put back the real stats from actual games
		self.bot2 = self.player
		self.player = player
		self.playerWins = playerWins
		self.bot1Wins = bot1Wins
		self.draws = draws

		self.formattedMatchHistory = self.convertMatchHistory(self.matchHistory)

		return trainObj