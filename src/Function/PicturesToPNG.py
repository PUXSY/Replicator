from pathlib import Path
from PIL import Image

def convert_images_to_png(folder_path):
    """
    Convert image files in the specified folder to PNG format.
    
    Args:
        folder_path (Path): Path to the folder containing images
    """
    # List of common image extensions to convert
    image_extensions = ['.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']
    
    # Counter for converted files
    converted_count = 0
    
    # Iterate through all files in the folder
    for file_path in folder_path.iterdir():
        # Check if it's a file and has an image extension
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            try:
                # Open the image
                with Image.open(file_path) as img:
                    # Generate new filename with .png extension
                    new_file_path = file_path.with_suffix('.png')
                    
                    # Save the image in PNG format
                    img.save(new_file_path, 'PNG')
                    
                    # Remove the original file
                    file_path.unlink()
                    
                    # Increment conversion counter
                    converted_count += 1
                    print(f"Converted: {file_path.name} -> {new_file_path.name}")
            
            except Exception as e:
                print(f"Error converting {file_path.name}: {e}")
    
    # Print summary
    print(f"\nConversion complete. {converted_count} files converted to PNG.")

def main():
    # Prompt user for folder path
    folder_path_str = input("Enter the full path to the folder containing images: ").strip()
    
    # Convert to Path object
    folder_path = Path(folder_path_str)
    
    # Validate folder path
    if not folder_path.is_dir():
        print("Error: Invalid folder path.")
        return
    if not folder_path.exists():
        print("Error: Folder doesn't exists.")
    
    # Confirm before conversion
    confirm = input(f"Are you sure you want to convert images in {folder_path} to PNG? (y/n): ").lower()
    
    if confirm == 'y':
        convert_images_to_png(folder_path)
    else:
        print("Conversion cancelled.")

if __name__ == "__main__":
    main()