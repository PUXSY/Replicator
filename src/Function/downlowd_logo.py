import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

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
    
    def get_all_names(self) -> List[str]:
        return list(self.applications_data.keys())

    def save_applications_data(self) -> None:
        with open(self.json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.applications_data, f, indent=4)

def download_image(url: str, save_path: str) -> bool:
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
    except IOError as e:
        print(f"Failed to save image {save_path}: {e}")
    return False

def search_for_logo(software_name: str) -> str | None:
    search_url = f"https://www.google.com/search?q={software_name}+logo&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        img_tag = soup.find("img")
        if img_tag and "src" in img_tag.attrs:
            return img_tag["src"]
        else:
            print(f"No image found for {software_name}")
            return None
    except requests.RequestException as e:
        print(f"Error searching for {software_name} logo: {e}")
        return None

def process_app(app_name: str, app_data: Dict, logo_folder: str) -> Dict:
    if 'logo' not in app_data:
        img_url = search_for_logo(app_name)
        if img_url:
            logo_save_path = os.path.join(logo_folder, f"{app_name}_logo.png")
            if download_image(img_url, logo_save_path):
                app_data['logo'] = logo_save_path
    return {app_name: app_data}

def main():
    json_file_path = r'C:\Users\User\Desktop\code\Replicator\applications.json'
    logo_folder = r'C:\Users\User\Desktop\code\Replicator\logs'
    os.makedirs(logo_folder, exist_ok=True)

    app = Application(json_file_path)
    app.load_applications_data()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for app_name, app_data in app.applications_data.items():
            future = executor.submit(process_app, app_name, app_data, logo_folder)
            futures.append(future)

        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing apps"):
            results.append(future.result())

    # Update applications_data with results
    for result in results:
        app.applications_data.update(result)

    app.save_applications_data()
    print("JSON file updated with logos!")

if __name__ == "__main__":
    main()