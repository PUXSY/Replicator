from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ProgramManager import ProgramManager
import subprocess
import time
import re
import threading

class InstallationThread(QThread):
    """
    A thread for installing programs with real-time progress tracking.
    """

    progress_update = pyqtSignal(int, str)
    installation_complete = pyqtSignal(list)

    def __init__(self, winget_manager: ProgramManager):
        super().__init__()
        self.winget_manager = winget_manager

    def _track_download_progress(self, process, program, total_programs, program_index):
        """
        Continuously track download progress for a single program with improved tracking.
        """
        base_progress = int((program_index / total_programs) * 100)
        program_progress_range = 100 // total_programs
    
        # More comprehensive regex patterns for progress indicators
        progress_patterns = [
            r'(\d+(?:\.\d+)?)%',            # Percentage with optional decimal
            r'Downloaded\s*(\d+(?:\.\d+)?)', # Downloaded bytes
            r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?) (MB|GB)', # Download fraction
            r'Progress:\s*(\d+(?:\.\d+)?)'  # Explicit progress keyword
        ]
    
        last_progress = 0
        try:
            while process.poll() is None:
                line = process.stdout.readline().strip()
                if not line:
                    # If no output, gradually increment progress
                    if last_progress < 100:
                        last_progress += 5
                        dynamic_progress = int(base_progress + (last_progress * program_progress_range / 100))
                        self.progress_update.emit(
                            min(dynamic_progress, 100),
                            f"Installing {program}..."
                        )
                    time.sleep(0.5)
                    continue
                
                # Try different regex patterns to extract progress
                for pattern in progress_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        try:
                            # Extract progress value
                            if len(match.groups()) == 1:
                                progress = float(match.group(1))
                            elif len(match.groups()) == 2:
                                # For fractional downloads, calculate percentage
                                current = float(match.group(1))
                                total = float(match.group(2))
                                progress = (current / total) * 100
                            else:
                                progress = float(match.group(1))

                            # Ensure progress is between 0 and 100
                            progress = max(0, min(progress, 100))
                            last_progress = progress

                            # Calculate dynamic progress
                            dynamic_progress = int(base_progress + (progress * program_progress_range / 100))

                            # Emit progress update
                            self.progress_update.emit(
                                dynamic_progress,
                                f"Installing {program}: {progress:.1f}%"
                            )
                        except (ValueError, TypeError) as e:
                            print(f"Progress parsing error: {e}")
                        break

        except Exception as e:
            print(f"Error while tracking progress: {e}")
        
        # Ensure we reach the end of this program's progress
        self.progress_update.emit(
            int((program_index + 1) / total_programs * 100),
            f"Finished installing {program}"
        )

    def run(self):
        results = []
        selected_programs = self.winget_manager.selected_programs.copy()
        total_programs = len(selected_programs)

        for i, program in enumerate(selected_programs, 1):
            command = self.winget_manager.get_install_command(program)

            if command:
                try:
                    # Start the installation process
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )

                    # Create a thread to track download progress
                    progress_thread = threading.Thread(
                        target=self._track_download_progress,
                        args=(process, program, total_programs, i-1)
                    )
                    progress_thread.start()

                    # Wait for the process to complete
                    stdout, stderr = process.communicate()

                    # Wait for progress tracking thread to finish
                    progress_thread.join()

                    # Check final installation result
                    if process.returncode == 0:
                        result = f"Successfully installed {program}"
                    else:
                        result = f"Failed to install {program}: {stderr}"

                except Exception as e:
                    result = f"Error installing {program}: {str(e)}"

            else:
                result = f"No installation command found for {program}"

            results.append(result)

            # Small pause between installations
            time.sleep(0.5)

        # Final completion signal
        self.installation_complete.emit(results)