import os
import subprocess
from datetime import datetime

# Directory containing image files
image_dir = "./picam_downloads"  # Change this to the directory containing your image files

# List all image files in the directory and sort them by filename
image_files = sorted([file for file in os.listdir(image_dir) if file.endswith(".jpg")])

# Get the current date and time for the timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Output video file with a date-stamped filename
output_file = f"output/my_video_{timestamp}.mp4"

# Build and run the ffmpeg command
ffmpeg_cmd = [
    "ffmpeg",
    "-framerate", "6",
    "-i", os.path.join(image_dir, "%*.jpg"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-vf", "scale=1920:1080",
    "-y",
    output_file
]

subprocess.run(ffmpeg_cmd)

print(f"Video saved as {output_file}")
