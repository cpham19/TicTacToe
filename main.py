from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, \
    QGridLayout, QStackedLayout, QDesktopWidget, QMessageBox, QTextEdit, QLineEdit, QDialog, QDialogButtonBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent
import sys, time, random, winsound, playsound, pygame, gym, gym_tictactoe


class Log(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTextInteractionFlags(self.textInteractionFlags() | Qt.TextSelectableByKeyboard)
        self.setReadOnly(False);
        self.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard);

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

# Training Page
class TrainingPage(QWidget):
    def __init__(self, env, layout, log):
        super().__init__()
        self.env = env
        self.layout = layout
        self.log = log
        self.setup()

    def setup(self):
        self.trainingLayout = QGridLayout()

        # Bot 1

        leaveButton = QPushButton('Main Menu')
        leaveButton.setStyleSheet('font: bold;background-color: red;font-size: 18px;height: 30px')
        leaveButton.clicked.connect(self.leave)
        self.trainingLayout.addWidget(leaveButton, 0, 0)

        self.botNameLabelForBot1 = QLabel("Bot Name: " + self.env.bot1.name)
        self.botNameLabelForBot1.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.botNameLabelForBot1, 1, 0)

        self.learningRateLabelForBot1 = QLabel("Learning rate: ")
        self.learningRateLabelForBot1.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.learningRateLabelForBot1, 2, 0)

        self.learningLineEditForBot1 = QLineEdit()
        floatValidator1 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.learningLineEditForBot1)
        self.learningLineEditForBot1.setValidator(floatValidator1)
        self.learningLineEditForBot1.setText(str(self.env.bot1.learning_rate))
        self.trainingLayout.addWidget(self.learningLineEditForBot1, 2, 1)

        self.discountFactorLabelForBot1 = QLabel("Discount factor: ")
        self.discountFactorLabelForBot1.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.discountFactorLabelForBot1, 3, 0)

        self.discountFactorLineEditForBot1 = QLineEdit()
        floatValidator2 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.discountFactorLineEditForBot1)
        self.discountFactorLineEditForBot1.setValidator(floatValidator2)
        self.discountFactorLineEditForBot1.setText(str(self.env.bot1.discount_factor))
        self.trainingLayout.addWidget(self.discountFactorLineEditForBot1, 3, 1)

        self.explorationRateLabelForBot1 = QLabel("Exploration rate: ")
        self.explorationRateLabelForBot1.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.explorationRateLabelForBot1, 4, 0)

        self.explorationRateLineEditForBot1 = QLineEdit()
        floatValidator3 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.explorationRateLineEditForBot1)
        self.explorationRateLineEditForBot1.setValidator(floatValidator3)
        self.explorationRateLineEditForBot1.setText(str(self.env.bot1.exploration_rate))
        self.trainingLayout.addWidget(self.explorationRateLineEditForBot1, 4, 1)

        self.numberOfGamesLabel= QLabel("Number of Games: ")
        self.numberOfGamesLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.numberOfGamesLabel, 5, 0, 1, 2)

        self.numberOfGamesLineEdit= QLineEdit()
        intValidator = QRegExpValidator(QRegExp("^[1-9]\\d*"), self.numberOfGamesLineEdit)
        self.numberOfGamesLineEdit.setValidator(intValidator)
        self.numberOfGamesLineEdit.setText(str(1000))
        self.trainingLayout.addWidget(self.numberOfGamesLineEdit, 5, 1, 1, 4)

        # Bot 2

        self.botNameLabelForBot2 = QLabel("Bot Name: " + self.env.bot2.name)
        self.botNameLabelForBot2.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.botNameLabelForBot2, 1, 3)

        self.learningRateLabelForBot2 = QLabel("Learning rate: ")
        self.learningRateLabelForBot2.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.learningRateLabelForBot2, 2, 3)

        self.learningLineEditForBot2 = QLineEdit()
        floatValidator4 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.learningLineEditForBot2)
        self.learningLineEditForBot2.setValidator(floatValidator4)
        self.learningLineEditForBot2.setText(str(self.env.bot2.learning_rate))
        self.trainingLayout.addWidget(self.learningLineEditForBot2, 2, 4)

        self.discountFactorLabelForBot2 = QLabel("Discount factor: ")
        self.discountFactorLabelForBot2.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.discountFactorLabelForBot2, 3, 3)

        self.discountFactorLineEditForBot2 = QLineEdit()
        floatValidator5 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.discountFactorLineEditForBot2)
        self.discountFactorLineEditForBot2.setValidator(floatValidator5)
        self.discountFactorLineEditForBot2.setText(str(self.env.bot2.discount_factor))
        self.trainingLayout.addWidget(self.discountFactorLineEditForBot2, 3, 4)

        self.explorationRateLabelForBot2 = QLabel("Exploration rate: ")
        self.explorationRateLabelForBot2.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.explorationRateLabelForBot2, 4, 3)

        self.explorationRateLineEditForBot2 = QLineEdit()
        floatValidator6 = QRegExpValidator(QRegExp("^[0-0]\\.\\d\\d"), self.explorationRateLineEditForBot2)
        self.explorationRateLineEditForBot2.setValidator(floatValidator6)
        self.explorationRateLineEditForBot2.setText(str(self.env.bot2.exploration_rate))
        self.trainingLayout.addWidget(self.explorationRateLineEditForBot2, 4, 4)

        self.trainButton = QPushButton('Train')
        self.trainButton.setStyleSheet('font: bold;background-color: blue;font-size: 18px;height: 30px')
        self.trainButton.clicked.connect(self.train)
        self.trainingLayout.addWidget(self.trainButton, 7, 0, 1, 5)

        self.totalTrainingWinsForBot1Label = QLabel(self.env.bot1.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot1))
        self.totalTrainingWinsForBot1Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingWinsForBot1Label, 8, 0)

        self.totalTrainingDrawsLabel = QLabel("Total Draws: " + str(self.env.totalTrainingDraws))
        self.totalTrainingDrawsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingDrawsLabel, 8, 2)

        self.totalTrainingWinsForBot2Label = QLabel(self.env.bot2.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot2))
        self.totalTrainingWinsForBot2Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingWinsForBot2Label, 8, 4)


        self.setLayout(self.trainingLayout)

    def train(self):
        if (self.learningLineEditForBot1.text() == '' or self.discountFactorLineEditForBot1.text() == '' or self.explorationRateLineEditForBot1.text() == '' or
            self.learningLineEditForBot2.text() == '' or self.discountFactorLineEditForBot2.text() == '' or self.explorationRateLineEditForBot2.text() == '' or
            self.numberOfGamesLineEdit.text() == ''):
            self.log.append("A textField is empty. Please enter a floating number between 0.00 and 1.00 (exclusive)")
            return

        try:
            float(self.learningLineEditForBot1.text())
            float(self.discountFactorLineEditForBot1.text())
            float(self.explorationRateLineEditForBot1.text())
            float(self.learningLineEditForBot2.text())
            float(self.discountFactorLineEditForBot2.text())
            float(self.explorationRateLineEditForBot2.text())
            int(self.numberOfGamesLineEdit.text())
        except ValueError:
            self.log.append("Please enter float numbers between 0.00 and 1.00 (exclusive)!")
            return

        self.env.bot1.learning_rate = float(self.learningLineEditForBot1.text())
        self.env.bot1.discount_factor = float(self.discountFactorLineEditForBot1.text())
        self.env.bot1.exploration_rate = float(self.explorationRateLineEditForBot1.text())

        self.env.bot2.learning_rate = float(self.learningLineEditForBot2.text())
        self.env.bot2.discount_factor = float(self.discountFactorLineEditForBot2.text())
        self.env.bot2.exploration_rate = float(self.explorationRateLineEditForBot2.text())

        numberOfGames = int(self.numberOfGamesLineEdit.text())

        trainStats = self.env.train(numberOfGames, self)

        self.totalTrainingWinsForBot1Label.setText(self.env.bot1.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot1))
        self.totalTrainingWinsForBot2Label.setText(self.env.bot2.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot2))
        self.totalTrainingDrawsLabel.setText("Total Draws: " + str(self.env.totalTrainingDraws))

        self.log.append("Training Stats: " + str(trainStats))

    # Go to main menu
    def leave(self):
        winsound.Beep(1000, 100)
        self.layout.setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Tic Tac Toe"
        self.left = 10
        self.top = 10
        self.width = 1280
        self.height = 300
        self.setupUI()

    def setupUI(self):
        # Setting title and size of window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        # Create our main widget
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        # Create our top widget
        self.topWidget = QWidget()

        # Create our bottom widget (log)
        self.log = Log()

        # Setting the layout
        self.createMainLayout()
        self.topWidget.setLayout(self.layout)

        # Central Widget layout
        layout.addWidget(self.topWidget)
        layout.addWidget(self.log)
        self.centralWidget.setLayout(layout)

        # Centering the window when running application by getting geometry of window, getting center of the screen, and setting the window to the cetner
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.log.append("Started Tic Tac Toe.")

        self.show()

    # QStackedLayout (layout that allows you to switch between pages)
    def createMainLayout(self):
        self.layout = QStackedLayout()

        self.layout.addWidget(self.createMainPage())

        player = PlayerAgent('Calvin', 'O')
        bot1 = TicTacToeAgent('Botinator', 'X')
        bot2 = TicTacToeAgent("Terminator", "O")
        self.env = gym.make('tictactoe-v0')
        self.env.init(player, bot1, bot2)

        self.gamePageForPlayerVsComputer = GamePageForPlayerVsComputer(self.env, self.layout, self.log)
        self.layout.addWidget(self.gamePageForPlayerVsComputer)

        self.trainingPage = TrainingPage(self.env, self.layout, self.log)
        self.layout.addWidget(self.trainingPage)

        self.layout.setCurrentIndex(0)

    # The main page of the app
    def createMainPage(self):
        widget = QWidget()

        layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignCenter)
        # widget.setFixedWidth(700)

        newGameForPlayerVsComputerButton = QPushButton('New Game (Player vs CPU)')
        newGameForPlayerVsComputerButton.setStyleSheet('font: bold;background-color: green;font-size: 36px;height: 80px')
        newGameForPlayerVsComputerButton.clicked.connect(self.startGameForPlayerVsComputer)

        trainingButton = QPushButton('Train CPU')
        trainingButton.setStyleSheet('font: bold;background-color: green;font-size: 36px;height: 80px')
        trainingButton.clicked.connect(self.trainingCPU)

        quitGameButton = QPushButton('Quit Game')
        quitGameButton.setStyleSheet('font: bold;background-color: red;font-size: 36px;height: 80px')
        quitGameButton.clicked.connect(self.exitGame)

        layout.addWidget(newGameForPlayerVsComputerButton)
        layout.addWidget(trainingButton)
        layout.addWidget(quitGameButton)

        widget.setLayout(layout)

        return widget

    def displayDifficultyDialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Select the CPU's Difficulty")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(160, 150)
        dialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        buttonBox = QDialogButtonBox(Qt.Vertical, dialog)

        superEasyButton = QPushButton("Super Easy")
        superEasyButton.setStyleSheet("font: bold;font-size: 10px;width: 30px")
        superEasyButton.clicked.connect(lambda: self.selectDifficulty(1.00, dialog))

        easyButton = QPushButton("Easy")
        easyButton.setStyleSheet("font: bold;font-size: 10px;width: 30px")
        easyButton.clicked.connect(lambda: self.selectDifficulty(0.75, dialog))

        mediumButton = QPushButton("Medium")
        mediumButton.setStyleSheet("font: bold;font-size: 10px;width: 30px")
        mediumButton.clicked.connect(lambda: self.selectDifficulty(0.50, dialog))

        hardButton = QPushButton("Hard")
        hardButton.setStyleSheet("font: bold;font-size: 10px;width: 30px")
        hardButton.clicked.connect(lambda: self.selectDifficulty(0.25, dialog))

        veryHardButton = QPushButton("Very Hard")
        veryHardButton.setStyleSheet("font: bold;font-size: 10px;width: 150px")
        veryHardButton.clicked.connect(lambda: self.selectDifficulty(0.00, dialog))

        buttonBox.addButton(superEasyButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(easyButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(mediumButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(hardButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(veryHardButton, QDialogButtonBox.ActionRole)

        dialog.exec()

    def selectDifficulty(self, exploration_rate, dialog):
        self.env.bot1.exploration_rate = exploration_rate
        print(self.env.bot1.exploration_rate)
        dialog.close()

    # Start the game (player vs cpu)
    def startGameForPlayerVsComputer(self):
        winsound.Beep(1000, 100)
        self.displayDifficultyDialog()
        self.gamePageForPlayerVsComputer.newGame()
        self.layout.setCurrentIndex(1)
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()

    # Train the CPU for playing
    def trainingCPU(self):
        winsound.Beep(1000, 100)
        self.layout.setCurrentIndex(2)

    # Close the application
    def exitGame(self):
        winsound.Beep(1000, 100)
        sys.exit()


class TicTacToeButton(QPushButton):
    def __init__(self, number):
        super().__init__()
        self.number = number

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number


def main():
    # Create an instance of QtApplication
    app = QApplication([])

    # Create an instance of MainWindow
    w = MainWindow()

    app.exec_()


if __name__ == '__main__':
    main()
