from pathlib import Path
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_background(input_path: Path, output_path: Path) -> None:
    """
    Removes the background from an image and saves the result as a PNG file.

    Args:
        input_path (pathlib.Path): The path to the input image file.
        output_path (pathlib.Path): The path to save the output image file (will be a PNG file).
    """
    try:
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()

        # Remove the background
        output_data = remove(input_data)

        # Save the image without the background as a PNG file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path = output_path.with_suffix('.png')
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
    except UnidentifiedImageError:
        logging.warning(f"Error: {input_path.name} is not a valid image file.")
    except Exception as e:
        logging.error(f"Error processing {input_path.name}: {e}")

def process_images_in_directory(directory_path: Path) -> None:
    """
    Processes all image files in a directory, removing the background and saving the results as PNG files.

    Args:
        directory_path (pathlib.Path): The path to the directory containing the images.
    """
    image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp')
    for extension in image_extensions:
        for image_file in directory_path.glob(extension):
            output_path = (directory_path / 'processed' / image_file.stem)
            logging.info(f'Processing {image_file.name}...')
            remove_background(image_file, output_path)

# Example usage
directory_path = Path(r"C:\Users\User\Desktop\code\Replicator\logs")
process_images_in_directory(directory_path)
print("All Done!!")