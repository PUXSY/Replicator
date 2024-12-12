from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class WindowsSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to the third page!")
        layout.addWidget(label)
        self.setLayout(layout)
