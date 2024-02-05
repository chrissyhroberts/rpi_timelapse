import os
import time
from datetime import datetime
import subprocess

# Define the base directory where videos will be saved
base_dir = "vid"

def capture_and_transcode(video_path):
    # Capture video
    subprocess.run(["libcamera-vid", "-o", video_path, "-t", "60000", "--framerate", "1", "--inline", "--codec", "h264"])
    print(f"Video captured: {video_path}")
    
    # Transcode to MP4
    mp4_path = video_path.replace('.h264', '.mp4')
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-c", "copy", mp4_path])
    print(f"Transcoded to MP4: {mp4_path}")
    
    # Optionally, remove the original .h264 file
    os.remove(video_path)
    print(f"Original video removed: {video_path}")

while True:
    # Get the current date and time for folder and filename
    now = datetime.now()
    date_folder = now.strftime("%Y%m%d")
    filename = now.strftime("%Y%m%d_%H%M%S") + ".h264"
    
    # Create today's directory if it doesn't exist
    today_dir = os.path.join(base_dir, date_folder)
    os.makedirs(today_dir, exist_ok=True)
    
    # Full path for the video file
    video_path = os.path.join(today_dir, filename)
    
    # Capture and transcode
    capture_and_transcode(video_path)
    
    # Calculate sleep time to start next capture at the start of the next minute
    sleep_time = 60 - datetime.now().second
    time.sleep(sleep_time)
