from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox, QLabel
from PyQt5.QtCore import *
from tictactoebutton import TicTacToeButton
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent
import random, winsound, playsound, pygame

# Gamepage for Player vs Computer
class GamePageForPlayerVsComputer(QWidget):
    def __init__(self, env, layout, log):
        super().__init__()
        self.env = env
        self.layout = layout
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
            self.playerTurn = self.env.bot1.name
            self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

            stateObj = self.env.step(button.number, self.env.player.mark)
            print("PLAYERS MOVE")
            print(stateObj)
            print()

            if (stateObj['done'] == 1 and stateObj['winner'] != 'None'):
                self.playerWinsLabel.setText(self.env.player.name + " Wins: " + str(self.env.playerWins))
                self.computerWinsLabel.setText(self.env.bot1.name + " Wins: " + str(self.env.bot1Wins))
                playsound.playsound('sounds/victory.mp3', False)
                reply = QMessageBox.question(self, stateObj['winner'] + ' wins the game!', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)
            elif (stateObj['done'] == 1  and stateObj['winner'] == 'None'):
                self.drawsLabel.setText("Draws: " + str(self.env.draws))
                playsound.playsound('sounds/gasp.mp3', False)
                reply = QMessageBox.question(self, 'Draw! No one won the game.', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)
            else:
                # Make a move for the bot after player's move
                self.makeBotMove()

    # Bot makes a move
    def makeBotMove(self):
        winsound.Beep(400, 100)
        action = self.env.bot1.action(self.gameboard)
        stateObj = self.env.step(action, self.env.bot1.mark)
        self.playerTurn = self.env.player.name
        self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

        while (type(self.env.bot1) == TicTacToeAgent and stateObj['validMove'] != True):
            action = self.env.bot1.action(self.gameboard)
            stateObj = self.env.step(action, self.env.bot1.mark)
            print(stateObj)
            break

        print("BOTS MOVE")
        print(stateObj)
        print()

        for button in self.arrayOfButtons:
            if (button.number == action):
                button.setText(self.env.bot1.mark)
                self.gameboard[int(button.number / 3)][button.number % 3] = self.env.bot1.mark
                button.setDisabled(True)
                button.setStyleSheet("font: bold;background-color: blue;font-size: 36px;height: 80px")

        if (stateObj['done'] == 1 and stateObj['winner'] != 'None'):
            self.playerWinsLabel.setText(self.env.player.name + " Wins: " + str(self.env.playerWins))
            self.computerWinsLabel.setText(self.env.bot1.name + " Wins: " + str(self.env.bot1Wins))
            playsound.playsound('sounds/victory.mp3', False)
            reply = QMessageBox.question(self, stateObj['winner'] + ' wins the game!', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.newGame()
            else:
                pygame.mixer.music.stop()
                self.layout.setCurrentIndex(0)
        elif (stateObj['done'] == 1 and stateObj['winner'] == 'None'):
            self.drawsLabel.setText("Draws: " + str(self.env.draws))
            playsound.playsound('sounds/gasp.mp3', False)
            reply = QMessageBox.question(self, 'Draw! No one won the game.', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.newGame()
            else:
                pygame.mixer.music.stop()
                self.layout.setCurrentIndex(0)

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