from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QStackedLayout, QDesktopWidget, QDialog, QDialogButtonBox, QGroupBox, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtCore import *
from gym_tictactoe.envs.tictactoe_agent import PlayerAgent, TicTacToeAgent
from log import Log
from gamepage import GamePageForPlayerVsComputer
from trainingpage import TrainingPage
import sys, winsound, pygame, gym, gym_tictactoe

class HistoryTableViewModel(QAbstractTableModel):
    def __init__(self, parent, matchHistory, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # self.matchHistory = [[1, 2, '3', '4', '5', '6'],
        #                      ['7', '8', '9', '10', '11' ,'12']]
        self.matchHistory = matchHistory
        self.header = ['#', 'Type', 'Player #1', 'Player #2', 'Number of Turns', 'Winner']

    # Set the Headers
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def setDataList(self, matchHistory):
        self.layoutAboutToBeChanged.emit()
        self.matchHistory = matchHistory
        print(self.matchHistory)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif index.isValid():
            if (role == Qt.DisplayRole):
                return QVariant(self.matchHistory[index.row()][index.column()])

    def rowCount(self, parent):
        return len(self.matchHistory)

    def columnCount(self, parent):
        return len(self.header)

# Match History Page
class MatchHistoryPage(QWidget):
    def __init__(self, env, layout, historyTable, log):
        super().__init__()
        self.env = env
        self.layout = layout
        self.historyTable = historyTable
        self.log = log
        self.setup()

    def setup(self):
        # Outer layout for the page
        self.historyLayout = QGridLayout()

        leaveButton = QPushButton('Main Menu')
        leaveButton.setStyleSheet('font: bold;background-color: red;font-size: 18px;height: 30px;width:30px')
        leaveButton.clicked.connect(self.leave)
        self.historyLayout.addWidget(leaveButton, 0, 0)

        # Inner layout for the groupbox
        self.innerLayout = QGridLayout()
        self.innerLayout.addWidget(self.historyTable)

        # Groupbox to contain widgets
        self.historyGroupBox = QGroupBox("Match History");
        self.historyGroupBox.setLayout(self.innerLayout)

        # Add Groupbox to outer layout
        self.historyLayout.addWidget(self.historyGroupBox)

        self.setLayout(self.historyLayout)

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

        # History table displaying various info about the matches
        self.historyTable = QTableView()
        self.historyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.historyTable.verticalHeader().setVisible(True)
        self.historyTable.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.historyTable.verticalHeader().setDefaultSectionSize(50)
        self.historyTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.historyTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.historyTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.historyTable.setSortingEnabled(True)
        self.historyTableViewModel = HistoryTableViewModel(self, self.env.formattedMatchHistory)
        self.historyTable.setModel(self.historyTableViewModel)

        self.trainingPage = TrainingPage(self.env, self.layout, self.historyTableViewModel, self.log)
        self.layout.addWidget(self.trainingPage)

        self.viewMatchHistoryPage = MatchHistoryPage(self.env, self.layout, self.historyTable, self.log)
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
        print(self.env.bot1.exploration_rate)
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
