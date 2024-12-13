from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QCheckBox, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from Settings import Settings

class TweaksWindow(QMainWindow):
    """
    Window for system and application tweaks configuration.
    """
    # Navigation signals
    back_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Replicator - System Tweaks")
        self.setGeometry(560, 240, 800, 600)

        # Set background color
        self.setStyleSheet("""
QMainWindow {
    background-color: #222831   ;
    color: #CC784E;
}

QListWidget {
    background-color: #0b0907;
    color: #ea560a;
    border: 1px solid #ea560a;
}

QCheckBox {
    background-color: #0b0907;
    color: #ea560a;
}

QScrollArea {
    background-color: #0b0907;
}

QPushButton {
    background-color: #ea560a;
    color: #0b0907;
    border: none;
    padding: 8px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #ff6b1c;
}
        """)

        self.stt = Settings()
        
        # Create and set central widget
        self.central_widget = TweaksWindowContent()
        self.setCentralWidget(self.central_widget)

        # Connect navigation signals
        self.central_widget.back_clicked.connect(self.back_clicked.emit)
        self.central_widget.next_clicked.connect(self.next_clicked.emit)


class TweaksWindowContent(QWidget):
    """
    Content widget for system and application tweaks.
    """
    back_clicked = pyqtSignal()
    next_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header_label = QLabel("System and Application Tweaks")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #CC784E; ")
        header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header_label)

        # Scroll area for tweaks
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #393E46;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)

        # Tweak Categories
        self.create_tweak_categories(scroll_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_clicked.emit)
        nav_layout.addWidget(self.back_button)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_clicked.emit)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

    def create_tweak_categories(self, scroll_layout):
        tweak_categories = [
            "Performance Optimizations",
            "Privacy Settings",
            "Power Management",
            "UI Customizations",
            "Security Enhancements"
        ]

        for category in tweak_categories:
            category_label = QLabel(category)
            category_label.setStyleSheet("font-weight: bold; color: #CC784E; ")
            scroll_layout.addWidget(category_label)
            
            self.add_tweak_checkboxes(scroll_layout, category)

    def add_tweak_checkboxes(self, scroll_layout, category):
        if category == "Performance Optimizations":
            tweaks = [
                "Disable Startup Programs",
                "Reduce Visual Effects",
                "Optimize Memory Usage",
                "Disable Background Apps"
            ]
        elif category == "Privacy Settings":
            tweaks = [
                "Disable Telemetry",
                "Limit Data Collection",
                "Disable Location Tracking",
                "Enhance Privacy Settings"
            ]
        elif category == "Power Management":
            tweaks = [
                "Balanced Power Plan",
                "High Performance Mode",
                "Disable Unnecessary Services",
                "Battery Saver Tweaks"
            ]
        elif category == "UI Customizations":
            tweaks = [
                "Dark Mode",
                "Custom Accent Colors",
                "Taskbar Modifications",
                "Desktop Icon Settings"
            ]
        else:  # Security Enhancements
            tweaks = [
                "Windows Defender Optimization",
                "Firewall Configuration",
                "Update Settings",
                "App Permissions"
            ]

        for tweak in tweaks:
            checkbox = QCheckBox(tweak)
            checkbox.setStyleSheet("color: #CC784E")
            scroll_layout.addWidget(checkbox)