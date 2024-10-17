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


from PyQt5.QtWidgets import QApplication
from WindowManager import WindowManager

def main():
    app = QApplication([])
    window_manager = WindowManager()
    window_manager.show_main_window()
    return app.exec_()

if __name__ == "__main__":
    main()