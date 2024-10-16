from ProgramManager import *
from Install_software_widgetUI import *
from Main_menu import *

class Window_manager(QMainWindow):
    """
    Main application class that integrates WingetManager and ReplicatorUI.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Replicator")
        self.setGeometry(100, 100, 940, 720)

        self.winget_manager = ProgramManager()
        self.winget_manager.fetch_available_programs()
        
    def install_software_window(self) -> None:
        self.Install_software_widget = Install_software_widgetUI(self.winget_manager)
        self.setCentralWidget(self.Install_software_widget)

    def main_menu_window(self) -> None:
        self.main_menu_widget = MainMenuUI(self.winget_manager)
        self.setCentralWidget(self.main_menu_widget)
    