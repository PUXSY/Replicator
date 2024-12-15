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
        """
        Updated to use 'content' field from applications.json
        """
        self.available_programs = []
        for program_id, program_data in self.applications_data.items():
            if 'content' in program_data:
                self.available_programs.append(program_data['content'])

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

    def get_install_command(self, program_name: str) -> str:
        """
        Get the installation command for a program using its display name.
        """
        # Find the program ID by matching the content/name
        for program_id, program_data in self.applications_data.items():
            if program_data.get('content') == program_name:
                if 'winget' in program_data:
                    return f"winget install {program_data['winget']}"
                elif 'choco' in program_data:
                    return f"choco install {program_data['choco']}"
        return ""

    def install_programs(self) -> List[str]:
        """Install selected programs and return results."""
        # Get the list of selected programs from the selected_programs list
        if not self.selected_programs:
            return ["No programs selected for installation"]
            
        results = []
        for program in self.selected_programs:
            command = self.get_install_command(program)
            if command:
                try:
                    # Use subprocess.run instead of call for better error handling
                    process = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if process.returncode == 0:
                        results.append(f"Successfully installed {program}")
                    else:
                        results.append(f"Failed to install {program}: {process.stderr}")
                except Exception as e:
                    results.append(f"Error installing {program}: {str(e)}")
            else:
                results.append(f"No installation command found for {program}")
        return results
    
    def get_logo_path(self, program_name: str) -> str:
        """
        Get the logo path for a program using its display name.
        """
        for program_data in self.applications_data.values():
            if program_data.get('content') == program_name:
                return program_data.get('logo', "")
        return ""
    
    def install_single_program(self, program):
        """
        Install a single program using winget.
        
        Args:
            program (str): Name of the program to install
        
        Returns:
            str: Installation result message
        """
        try:
            # Example winget installation command 
            # You'll need to replace this with your actual installation method
            import subprocess
            
            result = subprocess.run(
                ['winget', 'install', '--id', program, '-e', '--silent'], 
                capture_output=True, 
                text=True, 
                timeout=600  # 10-minute timeout
            )
            
            if result.returncode == 0:
                return f"{program} installed successfully"
            else:
                return f"Failed to install {program}: {result.stderr}"
        
        except subprocess.TimeoutExpired:
            return f"Installation of {program} timed out"
        except Exception as e:
            return f"Error installing {program}: {str(e)}"