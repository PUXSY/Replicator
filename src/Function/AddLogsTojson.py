import os
import json
import logging
from pathlib import Path

def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def get_user_folder_path():
    """
    Prompt user for folder path and validate it.
    
    Returns:
        Path: Validated folder path or None if invalid
    """
    while True:
        try:
            # Prompt user for folder path
            folder_path_str = input("Enter the full path to the folder containing logos: ").strip()
            
            # Convert to Path object
            folder_path = Path(folder_path_str)
            
            # Validate folder path
            if not folder_path.exists():
                print("Error: Folder doesn't exist.")
                continue
            
            if not folder_path.is_dir():
                print("Error: Invalid folder path. Please provide a directory.")
                continue
            
            # Confirm folder selection
            confirm = input(f"Use folder: {folder_path}? (y/n): ").lower()
            
            if confirm == 'y':
                return folder_path
            else:
                print("Folder selection cancelled.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

def get_user_json_path():
    """
    Prompt user for application.json file path and validate it.
    
    Returns:
        Path: Validated JSON file path or None if invalid
    """
    while True:
        try:
            # Prompt user for JSON file path
            json_path_str = input("Enter the full path to the application.json file: ").strip()
            
            # Convert to Path object
            json_path = Path(json_path_str)
            
            # Validate JSON file path
            if not json_path.exists():
                print("Error: File doesn't exist.")
                continue
            
            if not json_path.is_file():
                print("Error: Invalid file path. Please provide a valid JSON file.")
                continue
            
            # Confirm JSON file selection
            confirm = input(f"Use file: {json_path}? (y/n): ").lower()
            
            if confirm == 'y':
                return json_path
            else:
                print("File selection cancelled.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")


def collect_logo_files(logos_folder):
    """
    Collect logo filenames (without extension) and their corresponding paths.
    
    Args:
        logos_folder (Path): Path to logos folder
    
    Returns:
        dict: Dictionary mapping logo filenames (without extension) to their paths
    """
    logo_files = {
        os.path.splitext(filename)[0].lower(): os.path.join(logos_folder, filename)
        for filename in os.listdir(logos_folder)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))
    }
    return logo_files

def find_matching_logo(logo_files, entry):
    """
    Find the first matching logo for the given entry.
    
    Args:
        logo_files (dict): Dictionary mapping logo filenames to their paths
        entry (dict): JSON entry to match with a logo
    
    Returns:
        str or None: Path to the matching logo, or None if no match is found
    """
    matching_keys = [
        entry.get('content', '').lower(),  # match with content
        entry.get('choco', '').lower(),  # match with Chocolatey package name
        entry.get('winget', '').lower()  # match with Winget package name
    ]
    
    return next((logo_files[match] for match in matching_keys if match in logo_files), None)

def update_entry_with_logo(entry, logo_path, json_path):
    """
    Update the given entry with the logo path.
    
    Args:
        entry (dict): JSON entry to update
        logo_path (str): Path to the logo file
        json_path (Path): Path to the application.json file
    
    Returns:
        bool: True if the entry was updated, False otherwise
    """
    try:
        # Normalize path to use forward slashes and make relative
        relative_logo_path = os.path.relpath(logo_path, os.path.dirname(json_path)).replace(os.path.sep, '/')
        
        # Add logo path
        entry['logo'] = relative_logo_path
        return True
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error updating entry with logo: {e}")
        return False

def update_json_with_logos(logos_folder, json_path):
    """
    Update JSON file with logo paths.
    
    Args:
        logos_folder (Path): Path to logos folder
        json_path (Path): Path to application.json
    
    Returns:
        dict: Summary of updates
    """
    logger = setup_logging()
    
    # Summary tracking
    summary = {
        'total_logos_found': 0,
        'updated_entries': 0,
        'skipped_entries': 0,
        'errors': []
    }
    
    try:
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Collect logo files
        logo_files = collect_logo_files(logos_folder)
        summary['total_logos_found'] = len(logo_files)
        
        # Update entries with logos
        for entry in data.values():
            # Find matching logo
            logo_path = find_matching_logo(logo_files, entry)
            
            if logo_path:
                if update_entry_with_logo(entry, logo_path, json_path):
                    summary['updated_entries'] += 1
                    logger.info(f"Updated logo for entry: {entry.get('content', '')}")
                else:
                    summary['skipped_entries'] += 1
                    logger.warning(f"Failed to update logo for entry: {entry.get('content', '')}")
            else:
                summary['skipped_entries'] += 1
                logger.warning(f"No logo found for entry: {entry.get('content', '')}")
        
        # Confirm before writing
        confirm = input("Do you want to save the changes to application.json? (y/n): ").lower()
        
        if confirm == 'y':
            # Write updated JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("JSON file successfully updated.")
        else:
            print("Changes were not saved.")
            summary['skipped_entries'] = summary['total_logos_found']
            summary['updated_entries'] = 0
    
    except FileNotFoundError as e:
        summary['errors'].append(str(e))
        logger.error(f"File not found: {e}")
    except json.JSONDecodeError as e:
        summary['errors'].append(str(e))
        logger.error(f"JSON decoding error: {e}")
    except Exception as e:
        summary['errors'].append(str(e))
        logger.error(f"Unexpected error: {e}")
    
    return summary

def main():
    """Main script execution function."""
    logger = setup_logging()
    
    # Get logos folder from user
    logos_folder = get_user_folder_path()
    
    if not logos_folder:
        logger.error("No valid logos folder selected.")
        return
    
    # Get application.json path from user
    json_path = get_user_json_path()
    
    if not json_path:
        logger.error("No valid application.json file selected.")
        return
    
    logger.info(f"Logos Folder: {logos_folder}")
    logger.info(f"JSON File: {json_path}")
    
    # Update JSON with logos
    summary = update_json_with_logos(logos_folder, json_path)
    
    # Print summary
    print("\n--- Update Summary ---")
    print(f"Total Logos Found: {summary['total_logos_found']}")
    print(f"Updated Entries: {summary['updated_entries']}")
    print(f"Skipped Entries: {summary['skipped_entries']}")
    
    if summary['errors']:
        print("\nErrors:")
        for error in summary['errors']:
            print(f"- {error}")

if __name__ == "__main__":
    main()