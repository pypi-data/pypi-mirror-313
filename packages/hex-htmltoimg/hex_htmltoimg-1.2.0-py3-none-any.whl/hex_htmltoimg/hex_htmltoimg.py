import random
import string
import os
from html2image import Html2Image
from PIL import Image

def generate_unique_filename(length=None):
    """Generate a unique alphanumeric filename with all uppercase characters and digits."""
    if length is None:
        length = random.randint(17, 30)  # Default random length between 17 and 30
    characters = string.ascii_uppercase + string.digits  # Uppercase letters and digits
    return ''.join(random.choices(characters, k=length))

def generate_image_from_html(file_path, replacements, width=650, height=1250):
    """Generate an image from an HTML file with specified dimensions, replacing placeholders."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"HTML file does not exist: {file_path}")

    # Read the HTML file
    with open(file_path, 'r') as html_file:
        html_content = html_file.read()

    # Replace placeholders with actual values
    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, str(value))

    # Initialize Html2Image
    hti = Html2Image()

    # Validate width and height values
    if not isinstance(width, int) or width <= 0:
        raise ValueError("Width must be a positive integer.")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("Height must be a positive integer.")

    # Set the size to the specified dimensions
    size = (width, height)

    # Generate a unique filename for the output image
    image_filename = f"{generate_unique_filename()}.jpg"
    
    # Attempt to create the screenshot
    try:
        # Create the screenshot with specified dimensions
        hti.screenshot(html_str=html_content, save_as=image_filename, size=size)
        
        # Check if the image is generated and has content
        if os.path.getsize(image_filename) == 0:
            raise Exception(f"Generated image is empty: {image_filename}")

        # Load and resize the image to the specified dimensions
        img = Image.open(image_filename)
        img = img.resize(size, Image.LANCZOS)  # Resize to target dimensions
        img.save(image_filename)  # Save the resized image

    except Exception as e:
        raise Exception(f"Failed to create image: {str(e)}")

    return image_filename
