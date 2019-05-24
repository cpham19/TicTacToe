from PyQt5.QtWidgets import QFileDialog
import random, numpy as np, csv, os

# Represents the player
class PlayerAgent:
	def __init__(self, name, mark):
		self.name = name
		self.mark = mark

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@property
	def mark(self):
		return self.__mark

	@mark.setter
	def mark(self, mark):
		self.__mark = mark

	# Random move from player
	def action(self, state):
		numbers = []
		array = np.array(state).ravel()
		for i in range(0, 9):
			if (array[i] == ' '):
				numbers.append(i)
		move = random.sample(numbers, 1)[0]
		return move


# Represents the bot playing against the player, as well as other bots to play against the bot for training
class TicTacToeAgent(PlayerAgent):
	def __init__(self, name, mark):
		super().__init__(name, mark)
		# Used for calculating the value of intermediate states during temporal difference learning
		self.learning_rate = 0.5
		# Used for reducing the reward to pass on for intermediate states
		self.discount_factor = 0.01
		# Floating number < 1.0, probability for the bot to explore the game
		self.exploration_rate = 0.33

		self.states = {}
		self.state_order = []

		self.name = name
		self.mark = mark

	@property
	def name(self):
		return self.__name

	@name.setter
	def name(self, name):
		self.__name = name

	@property
	def learning_rate(self):
		return self.__learning_rate

	@learning_rate.setter
	def learning_rate(self, learning_rate):
		self.__learning_rate = learning_rate

	@property
	def discount_factor(self):
		return self.__discount_factor

	@discount_factor.setter
	def discount_factor(self, discount_factor):
		self.__discount_factor = discount_factor

	@property
	def exploration_rate(self):
		return self.__exploration_rate

	@exploration_rate.setter
	def exploration_rate(self, exploration_rate):
		self.__exploration_rate = exploration_rate

	# Transcode the state matrix into a string (used for recording the state before making the winning move)
	def serializeState(self, state):
		string = ""
		for row in range(0, len(state)):
			for col in range(0, len(state[row])):
				if(state[row][col] == 'O'):
					string += '1'
				elif(state[row][col] == 'X'):
					string += '2'
				else:
					string += '0'

		return string

	# Determine the move for bot
	def action(self, state):
		# One dimensional array of the current state of the game
		current_state = np.array(state).ravel()

		# State key for recording movements
		state_key = self.serializeState(state)

		# Determining if the bot explores or not
		exploration = np.random.random() < self.exploration_rate

		possible_moves = []

		# Checking if the board only has one move left
		for i in range(0, 9):
			if (current_state[i] == " "):
				possible_moves.append(i)

		if (len(possible_moves) == 1):
			move = possible_moves[0]
			self.state_order.append((state_key, move))
			return move


		possible_moves = []
		# For Exploiting: If the bot remembers the current state, it can make a calculated move
		if (not exploration and state_key in self.states):
			#print("EXPLOITING")
			# Get the q values of the currnt state (these are the numbers that are constantly changing after rewarding and punishing the bot)
			state_values = self.states[state_key].ravel()
			#print(state_values)

			max_reward = np.max(state_values)
			for i in range(0, 9):
				if (state_values[i] == max_reward):
					possible_moves.append(i)


		# For Exploring: Making a random move based on the current state
		else:
			#print("EXPLORING")
			for i in range(0, 9):
				if (current_state[i] == ' '):
					possible_moves.append(i)

		#print("POSSIBLE MOVES")
		#print(possible_moves)
		move = random.choice(possible_moves)
		self.state_order.append((state_key, move))
		return move

	# Load States
	def loadStates(self, widget):
		path = os.getcwd() + '/bot_states/'

		fileName = QFileDialog.getOpenFileName(widget, "Open States CSV File", path, "Comma-Separated Values File (*.csv);;All Files (*)")

		# Return if user doesn't select a file
		if (fileName[0] == ''):
			print("User didn't open a file.")
			return

		# Start loading the states into the bot's dictionary
		self.states = {}
		with open(fileName[0]) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')

			counter = 0
			for row in csv_reader:
				# Skip the header row
				if counter == 0:
					counter += 1
					continue
				else:
					state = row[0]
					box0 = float(row[1])
					box1 = float(row[2])
					box2 = float(row[3])
					box3 = float(row[4])
					box4 = float(row[5])
					box5 = float(row[6])
					box6 = float(row[7])
					box7 = float(row[8])
					box8 = float(row[9])

					rewardMatrix = np.zeros((3, 3))
					rewardMatrix[0][0] = box0
					rewardMatrix[0][1] = box1
					rewardMatrix[0][2] = box2
					rewardMatrix[1][0] = box3
					rewardMatrix[1][1] = box4
					rewardMatrix[1][2] = box5
					rewardMatrix[2][0] = box6
					rewardMatrix[2][1] = box7
					rewardMatrix[2][2] = box8
					self.states[state] = rewardMatrix
				counter += 1

	# Save States
	def saveStates(self):
		columns = ['state','box0','box1','box2','box3','box4','box5','box6','box7','box8']
		path = os.getcwd() +  '/bot_states/'

		with open(path + self.name + '.csv', mode='w') as csv_file:
			writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(columns)
			for state in self.states:
				# One-dimensional array of the rewards matrix
				rewardsArray = np.array(self.states[state]).ravel()
				writer.writerow([state, str(rewardsArray[0]), str(rewardsArray[1]), str(rewardsArray[2]), str(rewardsArray[3]), str(rewardsArray[4]), str(rewardsArray[5]), str(rewardsArray[6]), str(rewardsArray[7]), str(rewardsArray[8])])