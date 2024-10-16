from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ProgramManager import *
class InstallationThread(QThread):
    """
    A separate thread for running the installation process.
    """

    progress_update = pyqtSignal(int, str)
    installation_complete = pyqtSignal(list)

    def __init__(self, winget_manager: ProgramManager):
        super().__init__()
        self.winget_manager = winget_manager

    def run(self):
        results = self.winget_manager.install_programs()
        for i, result in enumerate(results, 1):
            self.progress_update.emit(int((i / len(results)) * 100), result)
        self.installation_complete.emit(results)