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
        encodings = ['utf-8', 'cp1252']
        for encoding in encodings:
            try:
                with open('./applications.json', 'r', encoding=encoding) as f:
                    self.applications_data = json.load(f)
                return
            except UnicodeDecodeError:
                continue
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON with {encoding} encoding: {e}")
                continue
            except FileNotFoundError:
                print("applications.json not found. Please ensure the file exists.")
                break
        
        print("Failed to load applications data. Using empty dictionary.")
        self.applications_data = {}

    def fetch_available_programs(self) -> None:
        self.available_programs = []
        self.program_id_to_content = {}
        self.content_to_program_id = {}
        for program_id, data in self.applications_data.items():
            if 'content' in data:
                content = data['content']
                self.available_programs.append(content)
                self.program_id_to_content[program_id] = content
                self.content_to_program_id[content] = program_id


    def add_program(self, content: str) -> None:
        """
        Move a program from available to selected.
        """
        if content in self.available_programs:
            self.available_programs.remove(content)
            self.selected_programs.append(content)

    def remove_program(self, content: str) -> None:
        """
        Move a program from selected to available.
        """
        if content in self.selected_programs:
            self.selected_programs.remove(content)
            self.available_programs.append(content)


    def get_install_command(self, content: str) -> str:
        """
        Get the installation command for a program.
        """
        program_id = self.content_to_program_id.get(content)
        if program_id in self.applications_data:
            app_data = self.applications_data[program_id]
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
    
    def get_logo_path(self, program: str) -> list[str]:
        """Retrieve the logo path for a given program."""
        logo_path = []
        if program in self.applications_data:
            app_data = self.applications_data[program]
            if 'logo' in app_data:
                logo_path.append(app_data['logo'])
        return logo_path
    