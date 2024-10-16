import json
import subprocess
from typing import List, Dict


class ProgramManager:
    """
    Manages the interaction with winget for program discovery and installation.
    """

    def __init__(self):
        self.available_programs: List[str] = []
        self.selected_programs: List[str] = []
        self.applications_data: Dict[str, Dict] = {}
        self.load_applications_data()
        self.fetch_available_programs()

    def load_applications_data(self) -> None:
        try:
            # Try UTF-8 encoding first
            with open('./applications.json', 'r', encoding='utf-8') as f:
                self.applications_data = json.load(f)
        except UnicodeDecodeError:
            # If UTF-8 fails, try with 'cp1252' encoding
            try:
                with open('./applications.json', 'r', encoding='cp1252') as f:
                    self.applications_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                self.applications_data = {}
        except FileNotFoundError:
            print("applications.json not found. Please ensure the file exists.")
            self.applications_data = {}

    def fetch_available_programs(self) -> None:
        self.available_programs = []
        for data in self.applications_data.values():
            if 'content' in data:
                self.available_programs.append(data['content'])

        

    def add_program(self, program: str) -> None:
        """
        Move a program from available to selected.
        """
        if program in self.available_programs:
            self.available_programs.remove(program)
            self.selected_programs.append(program)

    def remove_program(self, program: str) -> None:
        """
        Move a program from selected to available.
        """
        if program in self.selected_programs:
            self.selected_programs.remove(program)
            self.available_programs.append(program)

    def get_install_command(self, program: str) -> str:
        """
        Get the installation command for a program.
        """
        if program in self.applications_data:
            app_data = self.applications_data[program]
            if 'winget' in app_data:
                return f"winget install {app_data['winget']}"
            elif 'choco' in app_data:
                return f"choco install {app_data['choco']}"
        return ""

    def install_programs(self) -> List[str]:
        results = []
        for program in self.selected_programs:
            command = self.get_install_command(program)
            if command:
                subprocess.call(command)
                results.append(f"Would install {program} using command: {command}")
            else:
                results.append(f"No installation command found for {program}")
        return results
    
    def get_logo_path(self, program: str) -> str:
        if program in self.applications_data:
            app_data = self.applications_data[program]
            if 'logo' in app_data:
                return app_data['logo']
        return ""