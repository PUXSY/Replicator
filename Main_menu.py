from typing import List
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ProgramManager import ProgramManager
from InstallationThread import InstallationThread
import os


class MainMenuUI(QMainWindow):
    def __init__(self, winget_manager: ProgramManager):
        super().__init__()
        self.winget_manager = winget_manager
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = QLabel("Software Manager")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(title_label)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Create Software button
        create_software_button = QPushButton("Create Software")
        create_software_button.clicked.connect(self.open_install_software_widget)
        button_layout.addWidget(create_software_button)

        # Settings button
        settings_button = QPushButton(QIcon("path/to/settings_icon.png"), "")
        settings_button.setFixedSize(40, 40)
        settings_button.clicked.connect(self.open_settings)
        button_layout.addWidget(settings_button)

        self.layout.addLayout(button_layout)

        # Add spacer to push buttons to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

    def open_install_software_widget(self):
        # Import here to avoid circular imports
        from Install_software_widgetUI import InstallSoftwareWidgetUI
        self.install_software_widget = InstallSoftwareWidgetUI(self.winget_manager)
        self.install_software_widget.show()

    def open_settings(self):
        # Implement settings functionality
        print("Settings button clicked")