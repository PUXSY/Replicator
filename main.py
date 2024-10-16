"""
Replicator: Your Personalized Digital Twin

This module implements a GUI application for easy program installation after a fresh Windows setup.
It allows users to select programs from a list of available options and initiate their installation.

Classes:
    ProgramManager: Manages the logic for program selection and installation.
    ReplicatorUI: Handles the user interface for the Replicator application.
    ReplicatorApp: Main application class that integrates ProgramManager and ReplicatorUI.

Usage:
    Run this script directly to start the Replicator application.
"""


from ProgramManager import ProgramManager
from ReplicatorUI import ReplicatorUI
from ReplicatorApp import ReplicatorApp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    program_manager = ProgramManager()
    replicator_ui = ReplicatorUI(program_manager)
    replicator = ReplicatorApp()
    replicator.show()
    sys.exit(app.exec_())