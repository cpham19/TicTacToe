from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox, QLabel, QDialog, QDialogButtonBox, QGroupBox, QTextEdit
from PyQt5.QtCore import *
from tictactoebutton import TicTacToeButton
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent
import random, winsound, playsound, pygame, copy, time, numpy as np

# Gamepage for Player vs Computer
class GamePageForPlayerVsComputer(QWidget):
    def __init__(self, env, layout, historyTableViewModel, log):
        super().__init__()
        self.env = env
        self.layout = layout
        self.historyTableViewModel = historyTableViewModel
        self.log = log
        self.setup()

    def setup(self):
        self.gameLayout = QGridLayout()

        self.gameboard = self.env.state

        self.gameLayout.setColumnStretch(0, 3)
        self.gameLayout.setColumnStretch(1, 3)
        self.gameLayout.setColumnStretch(2, 3)

        leaveButton = QPushButton('Main Menu')
        leaveButton.setStyleSheet('font: bold;background-color: red;font-size: 18px;height: 30px')
        leaveButton.clicked.connect(self.leave)
        self.gameLayout.addWidget(leaveButton, 0, 0)

        self.playerTurnLabel = QLabel("Player's Turn: ")
        self.playerTurnLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.gameLayout.addWidget(self.playerTurnLabel, 0, 1)

        self.muteButton = QPushButton('Mute Music')
        self.muteButton.setStyleSheet('font: bold;background-color: yellow;font-size: 18px;height: 30px')
        self.muteButton.clicked.connect(self.muteMusic)
        self.gameLayout.addWidget(self.muteButton, 0, 2)

        self.button1 = TicTacToeButton(0)
        self.button1.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button1.clicked.connect(lambda: self.makeMove(self.button1))
        self.gameLayout.addWidget(self.button1, 1, 0)

        self.button2 = TicTacToeButton(1)
        self.button2.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button2.clicked.connect(lambda: self.makeMove(self.button2))
        self.gameLayout.addWidget(self.button2, 1, 1)

        self.button3 = TicTacToeButton(2)
        self.button3.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button3.clicked.connect(lambda: self.makeMove(self.button3))
        self.gameLayout.addWidget(self.button3, 1, 2)

        self.button4 = TicTacToeButton(3)
        self.button4.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button4.clicked.connect(lambda: self.makeMove(self.button4))
        self.gameLayout.addWidget(self.button4, 2, 0)

        self.button5 = TicTacToeButton(4)
        self.button5.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button5.clicked.connect(lambda: self.makeMove(self.button5))
        self.gameLayout.addWidget(self.button5, 2, 1)

        self.button6 = TicTacToeButton(5)
        self.button6.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button6.clicked.connect(lambda: self.makeMove(self.button6))
        self.gameLayout.addWidget(self.button6, 2, 2)

        self.button7 = TicTacToeButton(6)
        self.button7.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button7.clicked.connect(lambda: self.makeMove(self.button7))
        self.gameLayout.addWidget(self.button7, 3, 0)

        self.button8 = TicTacToeButton(7)
        self.button8.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button8.clicked.connect(lambda: self.makeMove(self.button8))
        self.gameLayout.addWidget(self.button8, 3, 1)

        self.button9 = TicTacToeButton(8)
        self.button9.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button9.clicked.connect(lambda: self.makeMove(self.button9))
        self.gameLayout.addWidget(self.button9, 3, 2)

        self.arrayOfButtons = []
        self.arrayOfButtons.append(self.button1)
        self.arrayOfButtons.append(self.button2)
        self.arrayOfButtons.append(self.button3)
        self.arrayOfButtons.append(self.button4)
        self.arrayOfButtons.append(self.button5)
        self.arrayOfButtons.append(self.button6)
        self.arrayOfButtons.append(self.button7)
        self.arrayOfButtons.append(self.button8)
        self.arrayOfButtons.append(self.button9)

        self.playerWinsLabel = QLabel(self.env.player.name + " Wins: " + str(self.env.playerWins))
        self.playerWinsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.drawsLabel = QLabel("Draws: " + str(self.env.draws))
        self.drawsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.computerWinsLabel = QLabel(self.env.bot1.name + " Wins: " + str(self.env.bot1Wins))
        self.computerWinsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")

        self.gameLayout.addWidget(self.playerWinsLabel, 4, 0)
        self.gameLayout.addWidget(self.drawsLabel, 4, 1)
        self.gameLayout.addWidget(self.computerWinsLabel, 4, 2)

        self.setLayout(self.gameLayout)

    # Make a move
    def makeMove(self, button):
        if (self.gameboard[int(button.number/3)][button.number%3] == ' ' and self.playerTurn == self.env.player.name):
            # Update the game after player's move
            winsound.Beep(400, 100)
            button.setText(self.env.player.mark)
            button.setStyleSheet("font: bold;background-color: pink;font-size: 36px;height: 80px")
            button.setDisabled(True)

            stateObj = self.env.step(button.number, self.env.player.mark)
            turn = {}
            turn['number'] = stateObj['turn']
            turn['playerTurn'] = self.playerTurn
            turn['state'] = copy.deepcopy(stateObj['state'])
            self.match['turns'].append(turn)

            self.playerTurn = self.env.bot1.name
            self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

            self.checkState(stateObj)

            if (stateObj['done'] != 1):
                # Make a move for the bot after player's move
                self.makeBotMove()

    # Bot makes a move
    def makeBotMove(self):
        winsound.Beep(400, 100)

        action = self.env.bot1.action(self.gameboard)
        stateObj = self.env.step(action, self.env.bot1.mark)

        while (type(self.env.bot1) == TicTacToeAgent and stateObj['validMove'] != True):
            action = self.env.bot1.action(self.gameboard)
            stateObj = self.env.step(action, self.env.bot1.mark)
            break

        turn = {}
        turn['number'] = stateObj['turn']
        turn['playerTurn'] = self.playerTurn
        turn['state'] = copy.deepcopy(stateObj['state'])
        self.match['turns'].append(turn)

        self.playerTurn = self.env.player.name
        self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

        for button in self.arrayOfButtons:
            if (button.number == action):
                button.setText(self.env.bot1.mark)
                self.gameboard[int(button.number / 3)][button.number % 3] = self.env.bot1.mark
                button.setDisabled(True)
                button.setStyleSheet("font: bold;background-color: blue;font-size: 36px;height: 80px")

        self.checkState(stateObj)

    def checkState(self, stateObj):
        # Check if the game is done
        if (stateObj['done'] == 1):
            self.match['winner'] = stateObj['winner']
            self.env.matchHistory.append(self.match)
            self.env.formattedMatchHistory = self.env.convertMatchHistory(self.env.matchHistory)
            self.historyTableViewModel.setDataList(self.env.formattedMatchHistory)
            self.playerWinsLabel.setText(self.env.player.name + " Wins: " + str(self.env.playerWins))
            self.computerWinsLabel.setText(self.env.bot1.name + " Wins: " + str(self.env.bot1Wins))
            self.drawsLabel.setText("Draws: " + str(self.env.draws))

            if (stateObj['winner'] != 'None'):
                playsound.playsound('sounds/victory.mp3', False)
            else:
                playsound.playsound('sounds/gasp.mp3', False)

            matchOutput = QDialog()
            matchOutput.setWindowTitle("Match Results: The winner is: " + stateObj['winner'] + "!")
            matchOutput.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
            matchOutput.resize(500, 500)

            matchOutputLayout = QGridLayout()
            matchOutput.setLayout(matchOutputLayout)

            buttonBox = QDialogButtonBox(Qt.Horizontal, matchOutput)
            yesButton = QPushButton("Yes")
            yesButton.clicked.connect(lambda: self.yes(matchOutput))
            noButton = QPushButton("No")
            noButton.clicked.connect(lambda: self.no(matchOutput))

            buttonBox.addButton(yesButton, QDialogButtonBox.ActionRole)
            buttonBox.addButton(noButton, QDialogButtonBox.ActionRole)

            calculationInfoGroupBox = QGroupBox("Calculation Information")
            calculationInfoLayout = QGridLayout()
            calculationInfoGroupBox.setLayout(calculationInfoLayout)
            calculationInfoTextEdit = QTextEdit()
            calculationInfoTextEdit.setReadOnly(True);
            calculationInfoTextEdit.append("This is how the bot's reward system is calculated.")
            calculationInfoTextEdit.append("Original Reward (reward for the last move that the bot makes, 0 for none, 1 for winning, -1 for losing, and 0.5 for draw.): " + str(stateObj['reward']))
            calculationInfoTextEdit.append(self.env.bot1.name + "'s learning rate: " + str(self.env.bot1.learning_rate))
            calculationInfoTextEdit.append(self.env.bot1.name + "'s discount factor: " + str(self.env.bot1.discount_factor))
            calculationInfoTextEdit.append("Reduced Reward (Reward * discount factor): " + str(stateObj['reward'] * self.env.bot1.discount_factor))
            calculationInfoTextEdit.append("Temporal Difference Formula: Learning Rate * ((reward * last_state) - current_state\n")
            calculationInfoTextEdit.append("Suppose that...")
            calculationInfoTextEdit.append("CURRENT STATE\n[[0. 0. 0.]\n [0. 0. 0.] \n [0. 0. 0.]]")
            calculationInfoTextEdit.append("AND")
            calculationInfoTextEdit.append("LAST STATE\n[[0. 1. 0.]\n [0. 0. 0.] \n [0. 0. 0.]] where Bot placed a move on the 2nd box\n")
            calculationInfoTextEdit.append("Temporal Difference = " + str(self.env.bot1.learning_rate) + " * ((" + str(stateObj['reward'] * self.env.bot1.discount_factor) + " * 1) - 0) = " + str(self.env.bot1.learning_rate * (stateObj['reward'] * self.env.bot1.discount_factor)))
            calculationInfoTextEdit.append("So new state is...\n")
            calculationInfoTextEdit.append("NEW STATE\n[[0. -0.005. 0.]\n [0. 0. 0.] \n [0. 0. 0.]] where Bot placed a move on the 2nd box\n")

            calculationInfoLayout.addWidget(calculationInfoTextEdit)

            matchOutputLayout.addWidget(calculationInfoGroupBox, 0, 0, 1, 3)

            row = 1
            for state, move in self.env.old_state_order:
                stateGroupBox = QGroupBox(state + (" (Actual View)"))
                stateLayout = QGridLayout()
                stateGroupBox.setLayout(stateLayout)
                gameboard = self.gameboardToString(self.unserializeState(state))
                gameboardTextEdit = QTextEdit()
                gameboardTextEdit.setReadOnly(True);
                gameboardTextEdit.setText(gameboard)
                stateLayout.addWidget(gameboardTextEdit, 0, 0, 1, 2)
                matchOutputLayout.addWidget(stateGroupBox, row, 0)

                currentStateRewardsGroupBox = QGroupBox("Current State Rewards")
                currentStateRewardsLayout = QGridLayout()
                currentStateRewardsGroupBox.setLayout(currentStateRewardsLayout)
                if state in self.env.old_states:
                    gameboard = self.rewardsToString(self.env.old_states[state].astype(np.str).ravel().tolist(), move)
                    gameboardTextEdit = QTextEdit()
                    gameboardTextEdit.setReadOnly(True);
                    gameboardTextEdit.append("The bot has encountered the state before so we increase the reward.")
                    gameboardTextEdit.setText(gameboard)
                    currentStateRewardsLayout.addWidget(gameboardTextEdit, 0, 0, 1, 2)
                    matchOutputLayout.addWidget(currentStateRewardsGroupBox, row, 1)
                else:
                    gameboard = self.rewardsToString(np.zeros((3,3)).astype(np.str).ravel().tolist(), move)
                    gameboardTextEdit = QTextEdit()
                    gameboardTextEdit.setReadOnly(True);
                    gameboardTextEdit.append("The bot never encountered the state before so we set it to the reward.")
                    gameboardTextEdit.append(gameboard)
                    currentStateRewardsLayout.addWidget(gameboardTextEdit, 0, 0, 1, 2)
                    matchOutputLayout.addWidget(currentStateRewardsGroupBox, row, 1)

                newStateRewardsGroupBox = QGroupBox("New State Rewards")
                newStateRewardsLayout = QGridLayout()
                newStateRewardsGroupBox.setLayout(newStateRewardsLayout)
                gameboard = self.rewardsToString(self.env.bot1.states[state].astype(np.str).ravel().tolist(), move)
                gameboardTextEdit = QTextEdit()
                gameboardTextEdit.setReadOnly(True);
                gameboardTextEdit.append(gameboard)
                newStateRewardsLayout.addWidget(gameboardTextEdit, 0, 0, 1, 2)
                matchOutputLayout.addWidget(newStateRewardsGroupBox, row, 2)

                row += 1

            matchOutputLayout.addWidget(QLabel("Do you want to play a new game?"))
            matchOutputLayout.addWidget(buttonBox)
            matchOutput.exec()

    def yes(self, dialog):
        dialog.close()
        self.newGame()

    def no(self, dialog):
        dialog.close()
        pygame.mixer.music.stop()
        self.layout.setCurrentIndex(0)

    def unserializeState(self, state):
        board = [['', '', ''], ['', '', ''], ['','','']]

        i = 0
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if state[i] == '1':
                    board[row][col] = 'O'
                elif state[i] == '2':
                    board[row][col] = 'X'
                else:
                    board[row][col] = str(i)
                i += 1

        return board

    def rewardsToString(self, rewards, move):
        string = ""

        for reward in range(0, len(rewards)):
            if (reward == move):
                string += "Box #" + str(reward) + ": " + rewards[reward] + " (Bot placed their move here)\n"
            else:
                string += "Box #" + str(reward) + ": " + rewards[reward] + "\n"

        return string

    def gameboardToString(self, gameboard):
        str = ""

        for row in range(3):
            for col in range(3):
                if (col != 2):
                    if (gameboard[row][col] == ' '):
                        str +=  gameboard[row][col] + "  | "
                    else:
                        str += gameboard[row][col] + " | "
                else:
                    str += gameboard[row][col] + " "
            if (row != 2):
                str += '\n---------'
            str += '\n'

        return str

    # Clear or make a new game
    def newGame(self):
        self.log.append("Player has started a new 'Player vs Computer' game.")

        # Randomize the player who goes first
        if (random.randint(0, 1) == 0):
            self.playerTurn = self.env.player.name
        else:
            self.playerTurn = self.env.bot1.name

        self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

        self.env.reset()
        self.gameboard = self.env.state

        self.match = {}
        self.match['number'] = self.env.matchs
        self.match['type'] = 'Actual'
        self.match['player1'] = self.env.player.name
        self.match['player2'] = self.env.bot1.name
        self.match['turns'] = []

        # Reset the texts on the butotns
        for button in self.arrayOfButtons:
            button.setText("")
            button.setStyleSheet("font: bold;font-size: 36px;height: 80px")
            button.setDisabled(False)

        if (self.playerTurn == self.env.bot1.name):
            self.makeBotMove()

    # Leave the game (when user is in a game)
    def leave(self):
        winsound.Beep(1000, 100)
        pygame.mixer.music.stop()
        self.layout.setCurrentIndex(0)

    # Mute the music
    def muteMusic(self):
        if (self.muteButton.text() == 'Mute Music'):
            self.log.append("Muted the game.")
            pygame.mixer.music.set_volume(0.00)
            self.muteButton.setText("Unmute Music")
        else:
            self.log.append("Ummuted the game.")
            pygame.mixer.music.set_volume(0.25)
            self.muteButton.setText("Mute Music")