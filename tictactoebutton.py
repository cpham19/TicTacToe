from PyQt5.QtWidgets import QPushButton

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