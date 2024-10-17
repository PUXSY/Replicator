from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    """
    Main application window with a welcome screen and navigation button.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Replicator - Welcome")
        self.setGeometry(560, 240, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add welcome message
        welcome_label = QLabel("Welcome to Replicator")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_font = QFont()
        welcome_font.setPointSize(24)
        welcome_font.setBold(True)
        welcome_label.setFont(welcome_font)
        layout.addWidget(welcome_label)
        
        # Add description
        desc_label = QLabel("Your Personal Program Installation Assistant")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(14)
        desc_label.setFont(desc_font)
        layout.addWidget(desc_label)
        
        # Add spacer
        layout.addStretch()
        
        # Create download button
        self.download_button = QPushButton("Start Download Manager")
        self.download_button.setFixedSize(200, 50)
        self.download_button.setFont(QFont("Arial", 12))
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        
        # Add bottom spacer
        layout.addStretch()