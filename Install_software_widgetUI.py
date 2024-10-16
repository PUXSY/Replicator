from typing import List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QPushButton, QLabel, QProgressBar, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from ProgramManager import ProgramManager
from InstallationThread import InstallationThread
import os


class Install_software_widgetUI(QWidget):
    def __init__(self, winget_manager: ProgramManager):
        super().__init__()
        self.winget_manager = winget_manager
        self.layout = QVBoxLayout(self)
        self.available_list = QListWidget()
        self.selected_list = QListWidget()
        self.available_search = QLineEdit()
        self.selected_search = QLineEdit()
        self.progress_bar = QProgressBar()
        self.status_label = QLabel()
        self.setup_ui()

    def setup_ui(self) -> None:
        self._create_header()
        self._create_list_layout()
        self._create_install_button()
        self._create_progress_bar()
        self._create_status_label()
        self._populate_available_list()

    def _create_header(self) -> None:
        header_label = QLabel("Replicator: Your Personalized Digital Twin")
        header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header_label)

    def _create_list_layout(self) -> None:
        list_layout = QHBoxLayout()
        
        available_layout = QVBoxLayout()
        self.available_search.setPlaceholderText("Search available programs...")
        self.available_search.textChanged.connect(self._filter_available_list)
        available_layout.addWidget(self.available_search)
        available_layout.addWidget(self.available_list)
        list_layout.addLayout(available_layout)
        
        button_layout = QVBoxLayout()
        add_button = QPushButton("Add >>")
        remove_button = QPushButton("<< Remove")
        add_button.clicked.connect(self._add_selected_programs)
        remove_button.clicked.connect(self._remove_selected_programs)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        list_layout.addLayout(button_layout)
        
        selected_layout = QVBoxLayout()
        self.selected_search.setPlaceholderText("Search selected programs...")
        self.selected_search.textChanged.connect(self._filter_selected_list)
        selected_layout.addWidget(self.selected_search)
        selected_layout.addWidget(self.selected_list)
        list_layout.addLayout(selected_layout)
        
        self.layout.addLayout(list_layout)

    def _create_install_button(self) -> None:
        install_button = QPushButton("Install Selected Programs")
        install_button.clicked.connect(self._install_programs)
        self.layout.addWidget(install_button)

    def _create_progress_bar(self) -> None:
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

    def _create_status_label(self) -> None:
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

    def _populate_available_list(self) -> None:
        self.available_list.clear()
        for content in self.winget_manager.available_programs:
            self._add_item_with_icon(self.available_list, content)

    def _populate_available_list(self) -> None:
        """Clear and repopulate the available programs list."""
        self.available_list.clear()
        for program in self.winget_manager.available_programs:
            self._add_item_with_icon(self.available_list, program)


    def _add_item_with_icon(self, list_widget: QListWidget, program: str) -> None:
        """Add a program item with its corresponding icon to the list widget."""
        item = QListWidgetItem(program)
        icon_path = self.winget_manager.get_logo_path(program)

        if icon_path:
            for icon_path in icon_path:
                if os.path.exists(icon_path):
                    icon = QIcon(icon_path)
                    pixmap = icon.pixmap(64, 64)
                    item.setIcon(QIcon(pixmap))
                    item.setSizeHint(QSize(item.sizeHint().width(), max(item.sizeHint().height(), 70)))
                    break  # Use the first valid icon path

        list_widget.addItem(item)


    def _add_selected_programs(self) -> None:
        for item in self.available_list.selectedItems():
            program = item.text()
            self.winget_manager.add_program(program)
            self._add_item_with_icon(self.selected_list, program)
            self.available_list.takeItem(self.available_list.row(item))

    def _remove_selected_programs(self) -> None:
        for item in self.selected_list.selectedItems():
            program = item.text()
            self.winget_manager.remove_program(program)
            self.selected_list.takeItem(self.selected_list.row(item))

    def _filter_available_list(self, text: str) -> None:
        for i in range(self.available_list.count()):
            item = self.available_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _filter_selected_list(self, text: str) -> None:
        for i in range(self.selected_list.count()):
            item = self.selected_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def _install_programs(self) -> None:
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Installation in progress...")
        
        self.install_thread = InstallationThread(self.winget_manager)
        self.install_thread.progress_update.connect(self._update_progress)
        self.install_thread.installation_complete.connect(self._installation_complete)
        self.install_thread.start()

    def _update_progress(self, value: int, status: str) -> None:
        self.progress_bar.setValue(value)
        self.status_label.setText(status)

    def _installation_complete(self, results: List[str]) -> None:
        self.status_label.setText("Installation complete!")
        self.progress_bar.setVisible(False)
        self.selected_list.clear()
        self.winget_manager.selected_programs.clear()