# Code inspired by ...
# apoddar573 at https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa and https://github.com/apoddar573/Tic-Tac-Toe-Gym_Environment/ for basic Tic Tac Toe Gym Environment
# giladariel at https://towardsdatascience.com/reinforcement-learning-and-deep-reinforcement-learning-with-tic-tac-toe-588d09c41dda and https://github.com/giladariel/TicTacToe_RL/ for Reinforcement Learning implementation
# AmreshVenugopal at https://github.com/AmreshVenugopal/tic_tac_toe for Tic Tac Toe Agent that resides in the Tic Tac Toe Gym environment


from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout, QStackedLayout, QDesktopWidget, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QLabel
from PyQt5.QtCore import *
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent
from log import Log
from gamepage import GamePageForPlayerVsComputer
from trainingpage import TrainingPage
from matchhistorypage import MatchHistoryPage, HistoryTable, HistoryTableViewModel
import sys, winsound, pygame, gym, gym_tictactoe, numpy as np

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

        self.show()

    # QStackedLayout (layout that allows you to switch between pages)
    def createMainLayout(self):
        self.layout = QStackedLayout()

        self.layout.addWidget(self.createMainPage())

        nameDialog = QDialog()
        buttonBox = QDialogButtonBox(Qt.Horizontal, nameDialog)
        buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(nameDialog.accept)
        formLayout = QFormLayout()
        playerNameLineEdit = QLineEdit()
        playerNameLineEdit.setText("Calvin")
        bot1NameLineEdit = QLineEdit()
        bot1NameLineEdit.setText("Mr. Roboto")
        bot2NameLineEdit = QLineEdit()
        bot2NameLineEdit.setText("Terminator")
        formLayout.addRow(QLabel("Player's Name:"), playerNameLineEdit)
        formLayout.addRow(QLabel("Bot #1's Name:"), bot1NameLineEdit)
        formLayout.addRow(QLabel("Bot #2;s Name:"), bot2NameLineEdit)
        formLayout.addWidget(buttonBox)
        nameDialog.setWindowTitle("Enter names for you and the bots")
        nameDialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        nameDialog.setLayout(formLayout)
        nameDialog.exec()

        while (playerNameLineEdit.text() == '' or bot1NameLineEdit.text() == '' or bot2NameLineEdit.text() == ''):
            nameDialog.exec()
            winsound.Beep(1000, 100)
            if (playerNameLineEdit.text() != '' or bot1NameLineEdit.text() != '' or bot2NameLineEdit.text() != ''):
                break

        player = PlayerAgent(playerNameLineEdit.text(), 'O')
        bot1 = TicTacToeAgent(bot1NameLineEdit.text(), 'X')
        bot2 = TicTacToeAgent(bot2NameLineEdit.text(), "O")

        self.env = gym.make('tictactoe-v0')
        self.env.init(player, bot1, bot2)

        self.historyTableViewModel = HistoryTableViewModel(self, self.env.formattedMatchHistory)
        self.gamePageForPlayerVsComputer = GamePageForPlayerVsComputer(self.env, self.layout, self.historyTableViewModel, self.log)

        # History table displaying various info about the matches
        self.historyTable = HistoryTable(self.env)
        self.historyTable.setModel(self.historyTableViewModel)
        self.trainingPage = TrainingPage(self.env, self.layout, self.historyTableViewModel, self.log)
        self.viewMatchHistoryPage = MatchHistoryPage(self.env, self.layout, self.historyTable, self.log)


        self.layout.addWidget(self.gamePageForPlayerVsComputer)
        self.layout.addWidget(self.trainingPage)
        self.layout.addWidget(self.viewMatchHistoryPage)

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

        viewMatchHistoryButton = QPushButton('Match History')
        viewMatchHistoryButton.setStyleSheet('font: bold;background-color: green;font-size: 36px;height: 80px')
        viewMatchHistoryButton.clicked.connect(self.viewMatchHistory)

        quitGameButton = QPushButton('Quit Game')
        quitGameButton.setStyleSheet('font: bold;background-color: red;font-size: 36px;height: 80px')
        quitGameButton.clicked.connect(self.exitGame)

        layout.addWidget(newGameForPlayerVsComputerButton)
        layout.addWidget(trainingButton)
        layout.addWidget(viewMatchHistoryButton)
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
        dialog.close()

    # Start the game (player vs cpu)
    def startGameForPlayerVsComputer(self):
        winsound.Beep(1000, 100)
        self.displayDifficultyDialog()
        self.gamePageForPlayerVsComputer.newGame()
        self.env.training = False
        self.layout.setCurrentIndex(1)
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()

    # Train the CPU for playing
    def trainingCPU(self):
        winsound.Beep(1000, 100)
        self.env.training = True
        self.layout.setCurrentIndex(2)

    # Viewing Match History
    def viewMatchHistory(self):
        winsound.Beep(1000, 100)
        self.layout.setCurrentIndex(3)

    # Close the application
    def exitGame(self):
        winsound.Beep(1000, 100)
        sys.exit()

def main():
    # Create an instance of QtApplication
    app = QApplication([])

    # Create an instance of MainWindow
    w = MainWindow()

    app.exec_()


if __name__ == '__main__':
    main()
