from bs4 import BeautifulSoup
import requests
import json
from typing import List, Dict

class Application:
    def __init__(self, json_file_path: str = './applications.json') -> None:
        self.json_file_path = json_file_path
        self.applications_data: Dict[str, Dict] = {}
        
    def load_applications_data(self) -> None:
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.applications_data = json.load(f)
        except UnicodeDecodeError:
            try:
                with open(self.json_file_path, 'r', encoding='cp1252') as f:
                    self.applications_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                self.applications_data = {}
        except FileNotFoundError:
            print(f"{self.json_file_path} not found. Please ensure the file exists.")
            self.applications_data = {}
    
    def fetch_available_programs(self) -> List[str]:
        """
        Updated to use 'content' field from applications.json
        """
        available_programs = []
        for program_id, program_data in self.applications_data.items():
            if 'content' in program_data:
                available_programs.append(program_data['content'])
        return available_programs


class SerchForLogo:
    def __init__(self) -> str | None:
        self.app: Application = app
        self.app.load_applications_data()
        self.software_name: list[str] = self.app.fetch_available_programs()
        
    def SerchForLogo(self, software_name: list[str]) -> None:
        headers = {"User-Agent": "Mozilla/5.0"}
        url: str = f"https://www.google.com/search?q={software_name}+logo&tbm=isch"
        print(url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img")
        if img_tag and "src" in img_tag.attrs:
            return img_tag["src"]
        else:
            print(f"No image found for {software_name}")
            return None

if __name__ == "__main__":
    app = Application()
    SerchLogo = SerchForLogo()
    app.load_applications_data()
    
    available_programs = app.fetch_available_programs()
    for i in range(len(available_programs)):
        SerchLogo.SerchForLogo(available_programs[i])
    

