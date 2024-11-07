# InstallWindow.py
from typing import List
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QListWidget, QListWidgetItem, QPushButton, QLabel, 
                           QProgressBar, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont
from ProgramManager import ProgramManager
from InstallationThread import InstallationThread
from Settings import Settings
import os

