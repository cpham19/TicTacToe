from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QGroupBox, QTableView, QHeaderView, QAbstractItemView, QDialog, QTextEdit, QLabel
from PyQt5.QtCore import *
import winsound

class HistoryTable(QTableView):
    def __init__(self, env):
        QTableView.__init__(self)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultSectionSize(50)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.doubleClicked.connect(self.viewMatch)
        self.env = env
        #self.setSortingEnabled(True)

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

    def viewMatch(self):
        index = self.currentIndex()
        row = index.row()

        selectedMatch = self.env.matchHistory[row]

        matchWindow = QDialog()
        matchWindow.setWindowTitle("Match #" + str(selectedMatch['number']))
        matchWindow.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        matchWindowLayout = QGridLayout()
        matchWindow.setLayout(matchWindowLayout)

        player1Label = QLabel("Player #1: " + selectedMatch['player1'])
        player2Label = QLabel("Player #2: " + selectedMatch['player2'])

        matchWindowLayout.addWidget(player1Label, 0, 0)
        matchWindowLayout.addWidget(player2Label, 0, 2)

        row = 2
        col = 0

        for turn in selectedMatch['turns']:
            turnGroupBox = QGroupBox("Turn #" + str(turn['number']))
            turnGridLayout = QGridLayout()
            turnGroupBox.setLayout(turnGridLayout)

            playerTurnLabel = QLabel("Player's Turn: " + turn['playerTurn'])
            turnGridLayout.addWidget(playerTurnLabel, 0, 0)

            gameboard = self.gameboardToString(turn['state'])
            gameboardTextEdit = QTextEdit()
            gameboardTextEdit.setReadOnly(True);
            gameboardTextEdit.setText(gameboard)
            turnGridLayout.addWidget(gameboardTextEdit, 2, 0, 1, 4)

            matchWindowLayout.addWidget(turnGroupBox, row, col)

            if (col != 2):
                col += 1
            else:
                row += 1
                col = 0


        matchWindow.exec()



class HistoryTableViewModel(QAbstractTableModel):
    def __init__(self, parent, matchHistory, *args):
        QAbstractTableModel.__init__(self, parent, *args)
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