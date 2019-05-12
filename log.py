from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import *

class Log(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.setTextInteractionFlags(self.textInteractionFlags() | Qt.TextSelectableByKeyboard)
        self.setReadOnly(False);
        self.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard);