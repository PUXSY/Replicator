from ProgramManager import *
from ReplicatorUI import *

class ReplicatorApp(QMainWindow):
    """
    Main application class that integrates WingetManager and ReplicatorUI.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Replicator")
        self.setGeometry(100, 100, 940, 720)

        self.winget_manager = ProgramManager()
        self.winget_manager.fetch_available_programs()
        self.central_widget = ReplicatorUI(self.winget_manager)
        self.setCentralWidget(self.central_widget)
