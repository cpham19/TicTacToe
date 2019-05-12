from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QGridLayout, QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
import winsound

# Training Page
class TrainingPage(QWidget):
    def __init__(self, env, layout, historyTableViewModel, log):
        super().__init__()
        self.env = env
        self.layout = layout
        self.historyTableViewModel = historyTableViewModel
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

        self.currentTrainingWinsForBot1Label = QLabel(self.env.bot1.name + " Current Wins: " + str(0))
        self.currentTrainingWinsForBot1Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.currentTrainingWinsForBot1Label, 8, 0)

        self.currentTrainingDrawsLabel = QLabel("Current Draws: " + str(0))
        self.currentTrainingDrawsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.currentTrainingDrawsLabel, 8, 2)

        self.currentTrainingWinsForBot2Label = QLabel(self.env.bot2.name + " Current Wins: " + str(0))
        self.currentTrainingWinsForBot2Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.currentTrainingWinsForBot2Label, 8, 4)

        self.totalTrainingWinsForBot1Label = QLabel(self.env.bot1.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot1))
        self.totalTrainingWinsForBot1Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingWinsForBot1Label, 9, 0)

        self.totalTrainingDrawsLabel = QLabel("Total Draws: " + str(self.env.totalTrainingDraws))
        self.totalTrainingDrawsLabel.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingDrawsLabel, 9, 2)

        self.totalTrainingWinsForBot2Label = QLabel(self.env.bot2.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot2))
        self.totalTrainingWinsForBot2Label.setStyleSheet("font: bold;font-size: 18px;height: 30px")
        self.trainingLayout.addWidget(self.totalTrainingWinsForBot2Label, 9, 4)


        self.setLayout(self.trainingLayout)

    def train(self):
        if (self.learningLineEditForBot1.text() == '' or self.discountFactorLineEditForBot1.text() == '' or self.explorationRateLineEditForBot1.text() == '' or
            self.learningLineEditForBot2.text() == '' or self.discountFactorLineEditForBot2.text() == '' or self.explorationRateLineEditForBot2.text() == '' or
            self.numberOfGamesLineEdit.text() == ''):
            winsound.Beep(1000, 100)
            self.log.append("A textfield is empty. Please enter a floating number between 0.00 and 1.00 (exclusive)")
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

        self.currentTrainingWinsForBot1Label.setText(self.env.bot1.name + " Current Wins: " + str(trainStats['bot1Wins']))
        self.currentTrainingDrawsLabel.setText("Current Draws: " + str(trainStats['draws']))
        self.currentTrainingWinsForBot2Label.setText(self.env.bot2.name + " Current Wins: " + str(trainStats['bot2Wins']))
        self.totalTrainingWinsForBot1Label.setText(self.env.bot1.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot1))
        self.totalTrainingWinsForBot2Label.setText(self.env.bot2.name + " Total Wins: " + str(self.env.totalTrainingWinsForBot2))
        self.totalTrainingDrawsLabel.setText("Total Draws: " + str(self.env.totalTrainingDraws))

        self.historyTableViewModel.setDataList(self.env.formattedMatchHistory)


    # Go to main menu
    def leave(self):
        winsound.Beep(1000, 100)
        self.layout.setCurrentIndex(0)