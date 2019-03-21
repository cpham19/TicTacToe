from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton, QGroupBox, QVBoxLayout, QGridLayout, QStackedLayout, QDesktopWidget, QMessageBox
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput
import sys
import random
import winsound
from os import getcwd
import playsound
import pygame

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Tic Tac Toe"
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setupUI()

    def setupUI(self):
        # Setting title and size of window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create our main widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Setting the layout
        self.createMainLayout()
        self.centralWidget.setLayout(self.layout)

        # Centering the window when running application by getting geometry of window, getting center of the screen, and setting the window to the cetner
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.show()

    # QStackedLayout (layout that allows you to switch between pages)
    def createMainLayout(self):
        self.layout = QStackedLayout()
        self.layout.addWidget(self.createMainPage())
        self.layout.addWidget(self.createGamePage())

        self.layout.setCurrentIndex(0)

    # The main page of the app
    def createMainPage(self):
        widget = QWidget()

        layout = QVBoxLayout()
        newGameButton = QPushButton('New Game')
        newGameButton.setStyleSheet('font: bold;background-color: green;font-size: 36px;height: 80px')
        newGameButton.clicked.connect(self.startGame)
        quitGameButton = QPushButton('Quit Game')
        quitGameButton.setStyleSheet('font: bold;background-color: red;font-size: 36px;height: 80px')
        quitGameButton.clicked.connect(self.exitGame)

        layout.addWidget(newGameButton)
        layout.addWidget(quitGameButton)

        widget.setLayout(layout)

        return widget

    def createGamePage(self):
        widget = QWidget()

        self.gameLayout = QGridLayout()

        self.gameLayout.setColumnStretch(0, 3)
        self.gameLayout.setColumnStretch(1, 3)
        self.gameLayout.setColumnStretch(2, 3)

        self.gameboard = [['', '', ''],
                          ['', '', ''],
                          ['', '', '']]

        forfeitButton = QPushButton('Forfeit')
        forfeitButton.setStyleSheet('font: bold;background-color: red;font-size: 18px;height: 30px')
        forfeitButton.clicked.connect(self.forfeitGame)
        self.gameLayout.addWidget(forfeitButton, 0, 0)

        self.playerTurnLabel = QLabel("Player's Turn: ")
        self.playerTurnLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.gameLayout.addWidget(self.playerTurnLabel, 0, 1)

        self.button1 = TicTacToeButton(0, 0)
        self.button1.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button1.clicked.connect(lambda: self.makeMove(self.button1))
        self.gameLayout.addWidget(self.button1, 1, 0)

        self.button2 = TicTacToeButton(0, 1)
        self.button2.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button2.clicked.connect(lambda: self.makeMove(self.button2))
        self.gameLayout.addWidget(self.button2, 1, 1)

        self.button3 = TicTacToeButton(0, 2)
        self.button3.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button3.clicked.connect(lambda: self.makeMove(self.button3))
        self.gameLayout.addWidget(self.button3, 1, 2)

        self.button4 = TicTacToeButton(1, 0)
        self.button4.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button4.clicked.connect(lambda: self.makeMove(self.button4))
        self.gameLayout.addWidget(self.button4, 2, 0)

        self.button5 = TicTacToeButton(1, 1)
        self.button5.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button5.clicked.connect(lambda: self.makeMove(self.button5))
        self.gameLayout.addWidget(self.button5, 2, 1)

        self.button6 = TicTacToeButton(1, 2)
        self.button6.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button6.clicked.connect(lambda: self.makeMove(self.button6))
        self.gameLayout.addWidget(self.button6, 2, 2)

        self.button7 = TicTacToeButton(2, 0)
        self.button7.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button7.clicked.connect(lambda: self.makeMove(self.button7))
        self.gameLayout.addWidget(self.button7, 3, 0)

        self.button8 = TicTacToeButton(2, 1)
        self.button8.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button8.clicked.connect(lambda: self.makeMove(self.button8))
        self.gameLayout.addWidget(self.button8, 3, 1)

        self.button9 = TicTacToeButton(2, 2)
        self.button9.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button9.clicked.connect(lambda: self.makeMove(self.button9))
        self.gameLayout.addWidget(self.button9, 3, 2)

        self.XWins = 0
        self.draws = 0
        self.OWins = 0

        self.XWinsLabel = QLabel("X Wins: " + str(self.XWins))
        self.XWinsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.drawsLabel = QLabel("Draws: " + str(self.draws))
        self.drawsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.OWinsLabel = QLabel("O Wins: " + str(self.OWins))
        self.OWinsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")

        self.gameLayout.addWidget(self.OWinsLabel, 4, 0)
        self.gameLayout.addWidget(self.drawsLabel, 4, 1)
        self.gameLayout.addWidget(self.XWinsLabel, 4, 2)

        widget.setLayout(self.gameLayout)

        return widget

    # Make a move
    def makeMove(self, button):
        if (self.checkVictory()['state'] is False and self.gameboard[button.row][button.col] == ''):
            winsound.Beep(400, 100)
            button.setText(self.playerTurn)
            self.gameboard[button.row][button.col] = self.playerTurn
            button.setDisabled(True)

            if (self.playerTurn == "X"):
                button.setStyleSheet("font: bold;background-color: pink;font-size: 36px;height: 80px")
                self.playerTurn = "O"
            else:
                button.setStyleSheet("font: bold;background-color: blue;font-size: 36px;height: 80px")
                self.playerTurn = "X"

            self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)
            self.turns = self.turns + 1

            stateObj = self.checkVictory()
            if (stateObj['state'] is True):
                playsound.playsound('sounds/victory.mp3', False)
                reply = QMessageBox.question(self, stateObj['playerWon'] + ' wins the game!', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:

                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)
            elif (stateObj['state'] is False and self.turns == 9):
                self.draws = self.draws + 1
                self.drawsLabel.setText('Draws: ' + str(self.draws))
                playsound.playsound('sounds/gasp.mp3', False)
                
                reply = QMessageBox.question(self, 'Draw! No one won the game.', 'Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)

    def checkVictory(self):
        stateObj = {'state': False, 'playerWon': "None"}
        # for X
        # Check if one of the three rows have three X's
        if ((self.gameboard[0][0] == 'X' and self.gameboard[0][1] == 'X' and self.gameboard[0][2] == 'X') or (
                self.gameboard[1][0] == 'X' and self.gameboard[1][1] == 'X' and self.gameboard[1][2] == 'X') or (
                self.gameboard[2][0] == 'X' and self.gameboard[2][1] == 'X' and self.gameboard[2][2] == 'X')
                # Check if one of the three columns have three X's
                or (self.gameboard[0][0] == 'X' and self.gameboard[1][0] == 'X' and self.gameboard[2][0] == 'X') or (
                        self.gameboard[0][1] == 'X' and self.gameboard[1][1] == 'X' and self.gameboard[2][
                    1] == 'X') or (
                        self.gameboard[0][2] == 'X' and self.gameboard[1][2] == 'X' and self.gameboard[2][2] == 'X')
                # Check if the minor or major diagonal has three X's
                or (self.gameboard[0][0] == 'X' and self.gameboard[1][1] == 'X' and self.gameboard[2][2] == 'X') or (
                        self.gameboard[0][2] == 'X' and self.gameboard[1][1] == 'X' and self.gameboard[2][0] == 'X')):
            stateObj['state'] = True
            stateObj['playerWon'] = "X"
            self.XWins = self.XWins + 1
            self.XWinsLabel.setText("X Wins: " + str(self.XWins))

        # for O
        # Check if one of the three rows have three O's
        elif ((self.gameboard[0][0] == 'O' and self.gameboard[0][1] == 'O' and self.gameboard[0][2] == 'O') or (
                self.gameboard[1][0] == 'O' and self.gameboard[1][1] == 'O' and self.gameboard[1][2] == 'O') or (
                      self.gameboard[2][0] == 'O' and self.gameboard[2][1] == 'O' and self.gameboard[2][2] == 'O')
              # Check if one of the three columns have three O's
              or (self.gameboard[0][0] == 'O' and self.gameboard[1][0] == 'O' and self.gameboard[2][0] == 'O') or (
                      self.gameboard[0][1] == 'O' and self.gameboard[1][1] == 'O' and self.gameboard[2][1] == 'O') or (
                      self.gameboard[0][2] == 'O' and self.gameboard[1][2] == 'O' and self.gameboard[2][2] == 'O')
              # Check if the minor or major diagonal has three O's
              or (self.gameboard[0][0] == 'O' and self.gameboard[1][1] == 'O' and self.gameboard[2][2] == 'O') or (
                      self.gameboard[0][2] == 'O' and self.gameboard[1][1] == 'O' and self.gameboard[2][0] == 'O')):
            stateObj['state'] = True
            stateObj['playerWon'] = "O"
            self.OWins = self.OWins + 1
            self.OWinsLabel.setText("O Wins: " + str(self.OWins))

        return stateObj

    def newGame(self):
        self.turns = 0

        # Randomize the player who goes first
        if (random.randint(0, 2) == 0):
            self.playerTurn = 'X'
        else:
            self.playerTurn = 'O'

        self.playerTurnLabel.setText("Player's Turn: " + self.playerTurn)

        # Reset the board
        for row in range(0, len(self.gameboard)):
            for col in range(0, len(self.gameboard[row])):
                self.gameboard[row][col] = ''

        # Reset the texts on the buttons
        self.button1.setText("")
        self.button1.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button2.setText("")
        self.button2.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button3.setText("")
        self.button3.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button4.setText("")
        self.button4.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button5.setText("")
        self.button5.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button6.setText("")
        self.button6.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button7.setText("")
        self.button7.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button8.setText("")
        self.button8.setStyleSheet("font: bold;font-size: 36px;height: 80px")
        self.button9.setText("")
        self.button9.setStyleSheet("font: bold;font-size: 36px;height: 80px")

        # Reset the buttons states
        self.button1.setDisabled(False)
        self.button2.setDisabled(False)
        self.button3.setDisabled(False)
        self.button4.setDisabled(False)
        self.button5.setDisabled(False)
        self.button6.setDisabled(False)
        self.button7.setDisabled(False)
        self.button8.setDisabled(False)
        self.button9.setDisabled(False)

    # Start the game
    def startGame(self):
        winsound.Beep(1000, 100)
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()
        self.newGame()
        self.layout.setCurrentIndex(1)

    # Leave the game (when user is in a game)
    def forfeitGame(self):
        winsound.Beep(1000, 100)

        reply = QMessageBox.question(self, 'Player ' + self.playerTurn + ' wants to forfeit!', 'Do you want to forfeit the game, Player ' + self.playerTurn, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            playsound.playsound('sounds/clapping.mp3', False)
            if (self.playerTurn == "X"):
                self.OWins = self.OWins + 1
                self.OWinsLabel.setText("O Wins: " + str(self.OWins))
                reply2 = QMessageBox.question(self, 'X forfeits the game!', 'O Wins the game! Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply2 == QMessageBox.Yes:
                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)
            else:
                self.XWins = self.XWins + 1
                self.XWinsLabel.setText("X Wins: " + str(self.XWins))
                reply2 = QMessageBox.question(self, 'O forfeits the game!', 'X Wins the game! Do you want to play a new game?', QMessageBox.Yes, QMessageBox.No)
                if reply2 == QMessageBox.Yes:
                    self.newGame()
                else:
                    pygame.mixer.music.stop()
                    self.layout.setCurrentIndex(0)


    # Close the application
    def exitGame(self):
        winsound.Beep(1000, 100)
        sys.exit()

class TicTacToeButton(QPushButton):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row):
        self.__row = row

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, col):
        self.__col = col


def main():
    # Create an instance of QtApplication
    app = QApplication([])

    # Create an instance of MainWindow
    w = MainWindow()

    app.exec_()


if __name__ == '__main__':
    main()
