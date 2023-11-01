import os
from PIL import Image, ImageStat

# Define the source folder containing the JPG images.
source_folder = "picam_downloads"

# Define the destination folder for night images.
night_folder = "picam_downloads/night"

# Define the luminance threshold. Adjust as needed.
luminance_threshold = 20  # You can change this value according to your needs.

# Create the night folder if it doesn't exist.
if not os.path.exists(night_folder):
    os.mkdir(night_folder)

# Iterate through all files in the source folder.
for filename in os.listdir(source_folder):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        # Get the full path of the image file.
        file_path = os.path.join(source_folder, filename)

        # Open the image using Pillow.
        try:
            img = Image.open(file_path)
        except Exception as e:
            print(f"Error opening {filename}: {str(e)}")
            continue

        # Calculate the average luminance of the image.
        stat = ImageStat.Stat(img)
        luminance = stat.mean[0]

        # Check if the average luminance is below the threshold.
        if luminance < luminance_threshold:
            # Move the image to the night folder.
            destination_path = os.path.join(night_folder, filename)
            try:
                os.rename(file_path, destination_path)
                print(f"Moved {filename} to {night_folder}")
            except Exception as e:
                print(f"Error moving {filename}: {str(e)}")
        else:
            print(f"{filename} is not a night photo (Luminance: {luminance})")

# Print a message when the script completes.
print("Processing complete.")
