# WindowManager.py
from MainWindow import MainWindow
from InstallWindow import InstallWindow
from ProgramManager import ProgramManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from typing import Optional

class WindowManager:
    """
    Manages all application windows and their interactions.
    """
    def __init__(self):
        """Initialize the window manager with all required components."""
        self.program_manager = ProgramManager()
        self.main_window: Optional[MainWindow] = None
        self.install_window: Optional[InstallWindow] = None
        self._setup_windows()

    def _setup_windows(self) -> None:
        """Create and configure all application windows."""
        # Setup main welcome window
        self.main_window = MainWindow()
        self.main_window.download_button.clicked.connect(self.show_install_window)
        
        # Setup install window
        self.install_window = InstallWindow()
        
        # Connect window-level signals
        if hasattr(self.install_window, 'central_widget'):
            self.install_window.central_widget.installation_requested.connect(
                self.show_install_confirmation
            )

    def show_main_window(self) -> None:
        """Display the main welcome window."""
        if self.install_window and not self.install_window.isHidden():
            self.install_window.hide()
        if self.main_window:
            self.main_window.show()

    def show_install_window(self) -> None:
        """Switch to the install window."""
        if self.main_window and not self.main_window.isHidden():
            self.main_window.hide()
        if self.install_window:
            self.install_window.show()

    def show_install_confirmation(self) -> None:
        """Show installation confirmation dialog."""
        if not self.install_window:
            return

        selected_count = len(self.program_manager.selected_programs)
        if selected_count == 0:
            QMessageBox.warning(
                self.install_window,
                "No Programs Selected",
                "Please select at least one program to install."
            )
            return

        msg = QMessageBox(self.install_window)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirm Installation")
        msg.setText(f"Do you want to install {selected_count} selected program{'s' if selected_count > 1 else ''}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            self.start_installation()

    def start_installation(self) -> None:
        """Start the installation process."""
        if self.install_window:
            self.install_window.central_widget._install_programs()

    def show_error_message(self, title: str, message: str) -> None:
        """Display an error message to the user."""
        active_window = self.install_window if self.install_window and not self.install_window.isHidden() else self.main_window
        QMessageBox.critical(active_window, title, message)

    def show_info_message(self, title: str, message: str) -> None:
        """Display an information message to the user."""
        active_window = self.install_window if self.install_window and not self.install_window.isHidden() else self.main_window
        QMessageBox.information(active_window, title, message)