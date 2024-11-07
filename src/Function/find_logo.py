from bs4 import BeautifulSoup
import concurrent
import requests
import json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from urllib.parse import quote
import logging
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import time
from plyer import notification

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LogoDownloader:
    def __init__(self, save_dir: str = str(Path.home() / "LOGOS")):
        self.save_dir = Path(save_dir)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
    def create_directory(self) -> None:
        """Create the logo directory if it doesn't exist"""
        try:
            self.save_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Download directory ready: {self.save_dir}")
        except Exception as e:
            logger.error(f"Failed to create directory: {e}")
            raise

    def sanitize_filename(self, filename: str) -> str:
        """Create a safe filename from the software name"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()

    def download_image(self, url: str, software_name: str) -> Optional[str]:
        """Download an image and return its path"""
        if not url:
            return None
            
        try:
            response = self.session.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            # Get file extension from content type or URL
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type:
                logger.warning(f"Invalid content type for {software_name}: {content_type}")
                return None
                
            # Determine file extension
            ext = '.jpg' if 'jpeg' in content_type or 'jpg' in content_type else (
                  '.png' if 'png' in content_type else (
                  '.gif' if 'gif' in content_type else '.jpg'))
            
            # Create safe filename
            safe_name = self.sanitize_filename(software_name)
            filename = f"{safe_name}{ext}"
            filepath = self.save_dir / filename
            
            # Download with progress bar
            total_size = int(response.headers.get('content-length', 0))
            with open(filepath, 'wb') as f, tqdm(
                desc=f"Downloading {software_name}",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    size = f.write(data)
                    pbar.update(size)
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to download {software_name} logo: {e}")
            return None

class Application:
    def __init__(self, json_file_path: str = './applications.json') -> None:
        self.json_file_path = json_file_path
        self.applications_data: Dict[str, Dict] = {}
        
    def load_applications_data(self) -> None:
        """Load application data with better error handling"""
        encodings = ['utf-8', 'cp1252', 'latin-1']
        for encoding in encodings:
            try:
                with open(self.json_file_path, 'r', encoding=encoding) as f:
                    self.applications_data = json.load(f)
                    return
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to load with {encoding}: {e}")
                continue
            except FileNotFoundError:
                logger.error(f"File {self.json_file_path} not found")
                self.applications_data = {}
                return
        
        logger.error("Failed to load applications data with any encoding")
        self.applications_data = {}

    def fetch_available_programs(self) -> List[str]:
        """Fetch available programs with validation"""
        return [
            program_data['content'] 
            for program_data in self.applications_data.values() 
            if isinstance(program_data, dict) and 'content' in program_data
        ]

class LogoSearcher:
    def __init__(self, max_workers: int = 5, timeout: int = 10):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.max_workers = max_workers
        self.timeout = timeout
        self.results_queue = Queue()
        self.downloader = LogoDownloader()
        self.progress_bar = None
        self.start_time = None
    
    def sanitize_url(self, url: str) -> str:
        """Sanitize URL by replacing spaces and special characters"""
        return quote(url.replace(" ", "_").lower())
    
    def show_notification(self, title: str, message: str) -> None:
        """Show system notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                app_icon=None,
                timeout=10
            )
        except Exception as e:
            logger.error(f"Failed to show notification: {e}")

    def search_cleanpng(self, software_name: str) -> Optional[str]:
        """Search for logo on CleanPNG"""
        try:
            url = f"https://www.cleanpng.com/free/{self.sanitize_url(software_name)}.html"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            img_tag = soup.find("img", {"class": "img-responsive"})
            
            if img_tag and "src" in img_tag.attrs:
                return img_tag["src"]
            
        except requests.RequestException as e:
            logger.warning(f"CleanPNG search failed for {software_name}: {e}")
        return None

    def search_google_images(self, software_name: str) -> Optional[str]:
        """Search for logo on Google Images"""
        try:
            search_url = f"https://www.google.com/search?q={self.sanitize_url(software_name)}+logo.png&tbm=isch"

            response = self.session.get(search_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            img_tags = soup.find_all("img")
            
            for img in img_tags[1:]:
                if img.get("src", "").startswith("http"):
                    return img["src"]
                    
        except requests.RequestException as e:
            logger.warning(f"Google Images search failed for {software_name}: {e}")
        return None
    
    def search_logo(self, software_name: str) -> Dict[str, Optional[str]]:
        """Search for logo across multiple sources"""
        result = {
            "software": software_name,
            "cleanpng_url": None,
            "google_url": None
        }
        
        result["cleanpng_url"] = self.search_cleanpng(software_name)
        
        if not result["cleanpng_url"]:
            result["google_url"] = self.search_google_images(software_name)
            time.sleep(1)
            
        self.results_queue.put(result)
        return result
    
    def search_and_download(self, software_name: str) -> Dict[str, Optional[str]]:
        """Search for logo and download it"""
        result = self.search_logo(software_name)
        
        local_path = None
        if result["cleanpng_url"]:
            local_path = self.downloader.download_image(result["cleanpng_url"], software_name)
        if not local_path and result["google_url"]:
            local_path = self.downloader.download_image(result["google_url"], software_name)
            
        result["local_path"] = local_path
        return result

    def process_programs(self, programs: List[str]) -> List[Dict[str, Optional[str]]]:
        """Process multiple programs in parallel with progress tracking"""
        self.downloader.create_directory()
        results = []
        self.start_time = time.time()
        
        with tqdm(total=len(programs), desc="Processing programs") as self.progress_bar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_program = {
                    executor.submit(self.search_and_download, program): program 
                    for program in programs
                }
                
                completed_count = 0
                for future in concurrent.futures.as_completed(future_to_program):
                    try:
                        result = future.result()
                        results.append(result)
                        completed_count += 1
                        self.progress_bar.update(1)
                        
                        if completed_count % 5 == 0:
                            self.show_notification(
                                "Logo Download Progress",
                                f"Processed {completed_count}/{len(programs)} programs"
                            )
                            
                    except Exception as e:
                        logger.error(f"Error processing program: {e}")
                        
        elapsed_time = time.time() - self.start_time
        self.show_notification(
            "Logo Download Complete",
            f"Downloaded {len(results)} logos in {elapsed_time:.1f} seconds\n"
            f"Location: {self.downloader.save_dir}"
        )
        
        return results

def main():
    try:
        app = Application()
        app.load_applications_data()
        available_programs = app.fetch_available_programs()

        if not available_programs:
            logger.error("No programs found in applications data")
            return

        logo_searcher = LogoSearcher()
        results = logo_searcher.process_programs(available_programs)

        results_file = Path(logo_searcher.downloader.save_dir) / 'download_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        successful_downloads = sum(1 for r in results if r.get('local_path'))
        logo_searcher.show_notification(
            "Download Summary",
            f"Total programs: {len(results)}\n"
            f"Successfully downloaded: {successful_downloads}\n"
            f"Results saved to: {results_file}"
        )

    except Exception as e:
        logger.error(f"Program terminated with error: {e}")
        notification.notify(
            title="Error",
            message=f"Program terminated with error: {str(e)}",
            timeout=10
        )
    finally:
        logger.info("Program execution completed")

if __name__ == "__main__":
    main()
