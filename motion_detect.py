import subprocess
import os
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Define the base output folder
base_output_folder = "motioncam"

# Function to capture a photo and save it in a day structured folder
def capture_photo(photo_number):
    # Create a timestamp for the filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # Create folder structure: base_output_folder/YYYYMMDD
    day_folder = time.strftime("%Y%m%d")  # e.g., 20230207
    output_folder = os.path.join(base_output_folder, day_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    file_name = f"{timestamp}.jpg"
    file_path = os.path.join(output_folder, file_name)
    subprocess.run(["libcamera-jpeg", "-o", file_path])
    print(f"Photo {photo_number} captured with filename {file_name}.")
    return file_path, timestamp

# Function to add a timestamp watermark to a photo
def add_timestamp_watermark(file_path, timestamp):
    img = Image.open(file_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()  # Using default font
    text_position = (10, 10)  # Change as needed
    draw.text(text_position, timestamp, fill=(255, 255, 255))
    img.save(file_path)
    print(f"Timestamp added to photo: {timestamp}")

# Function to compare two images
def images_are_different(img1_path, img2_path, threshold=50):
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')
    
    img1_array = np.array(img1)
    img2_array = np.array(img2)
    
    diff = np.sum((img1_array - img2_array) ** 2)
    diff /= float(img1_array.shape[0] * img1_array.shape[1])
    
    print(f"Image difference score: {diff}")
    return diff > threshold

# Initialize the first photo outside the loop
photo_number = 1
previous_photo_path, _ = capture_photo(photo_number)
add_timestamp_watermark(previous_photo_path, time.strftime("%Y%m%d_%H%M%S"))

while True:
    time.sleep(10)  # Wait for 10 seconds before capturing the next photo
    photo_number += 1
    current_photo_path, current_timestamp = capture_photo(photo_number)
    
    if images_are_different(previous_photo_path, current_photo_path):
        print("Significant difference detected, motion likely occurred.")
        add_timestamp_watermark(current_photo_path, current_timestamp)
        # Update the previous photo to the current one for the next comparison
        previous_photo_path = current_photo_path
    else:
        print("No significant difference detected, discarding the current photo.")
        os.remove(current_photo_path)  # Remove the current photo if not significantly different
