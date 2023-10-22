import time
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

# Define the interval for photos in seconds (e.g., 20 minutes)
photo_interval = 1 * 60  # 20 minutes * 60 seconds/minute

# Define the output folder
output_folder = "/home/icrucrob/picam/high_street"

# Function to capture a photo and add a timestamp
def capture_photo():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"photo_{timestamp}.jpg"
    file_path = os.path.join(output_folder, file_name)
    subprocess.run(["libcamera-jpeg", "-o", file_path])

    # Open the captured photo using Pillow
    img = Image.open(file_path)
    draw = ImageDraw.Draw(img)
    
    # Define timestamp text and font properties
    text = time.strftime("%Y-%m-%d %H:%M:%S")
    font_size = 60
    font_color = (255, 0, 0)  # Red
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"  # Replace with the path to your TrueType font file

    # Create a font object with the specified font size
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the text size and position (bottom right corner)
    text_width, text_height = draw.textsize(text, font=font)
    img_width, img_height = img.size
    text_x = img_width - text_width - 10
    text_y = img_height - text_height - 10

    # Add the timestamp to the photo
    draw.text((text_x, text_y), text, font=font, fill=font_color)
    
    # Save the modified photo
    img.save(file_path)

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

try:
    # Capture an initial photo
    capture_photo()
    print("Initial photo captured.")

    while True:
        # Sleep for the specified photo interval
        time.sleep(photo_interval)

        # Capture the next photo
        capture_photo()
        print("Photo captured.")

except KeyboardInterrupt:
    pass
except Exception as e:
    # Handle exceptions as needed
    print(f"Exception: {str(e)}")
else:
    print("Code execution completed successfully.")
