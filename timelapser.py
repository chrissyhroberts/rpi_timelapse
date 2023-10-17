import json
from datetime import datetime, timedelta
import time
import subprocess
import os  # Import the os module for directory creation

# Load sunrise and sunset data from your JSON file
with open("/home/icrucrob/picam/sunrise_sunset_data.json", "r") as json_file:
    sunrise_sunset_data = json.load(json_file)

# Define your location
latitude = "52.5200"
longitude = "13.4050"

# Define absolute paths for output folders
output_folder_hourly = "/home/icrucrob/picam/hourly/"
output_folder_sunrise = "/home/icrucrob/picam/sunrise/"
output_folder_sunset = "/home/icrucrob/picam/sunset/"

# Function to calculate time until the next event
def time_until_next_event(event_time):
    now = datetime.now()
    event_datetime = datetime.combine(now.date(), datetime.strptime(event_time, "%I:%M:%S %p").time())
    
    # If the event time is in the past, add one day
    if now > event_datetime:
        event_datetime += timedelta(days=1)
    
    time_difference = event_datetime - now
    return time_difference.total_seconds()

# Function to capture a photo
def capture_photo(output_folder):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"photo_{timestamp}.jpg"
    subprocess.run(["libcamera-jpeg", "-o", f"{output_folder}/{file_name}"])

try:
    while True:
        now = datetime.now()
        today_date = now.strftime("%Y-%m-%d")
        
        # Calculate time until the next hourly event
        remaining_seconds_hourly = 3600 - (now.minute * 60 + now.second)

        # Calculate time until sunrise - 15 minutes
        sunrise_time = sunrise_sunset_data[today_date].get("sunrise")
        if sunrise_time:
            sunrise_minus_15 = (datetime.strptime(sunrise_time, "%I:%M:%S %p") - timedelta(minutes=15)).strftime("%I:%M:%S %p")
            remaining_seconds_sunrise_minus_15 = time_until_next_event(sunrise_minus_15)
        else:
            remaining_seconds_sunrise_minus_15 = float('inf')

        # Calculate time until sunset + 15 minutes
        sunset_time = sunrise_sunset_data[today_date].get("sunset")
        if sunset_time:
            sunset_plus_15 = (datetime.strptime(sunset_time, "%I:%M:%S %p") + timedelta(minutes=15)).strftime("%I:%M:%S %p")
            remaining_seconds_sunset_plus_15 = time_until_next_event(sunset_plus_15)
        else:
            remaining_seconds_sunset_plus_15 = float('inf')
        
        # Determine the next event and sleep accordingly
        min_remaining_seconds = min(remaining_seconds_hourly, remaining_seconds_sunrise_minus_15, remaining_seconds_sunset_plus_15)
        
        if min_remaining_seconds == remaining_seconds_hourly:
            capture_photo(output_folder_hourly)
            print(f"Hourly photo captured at {now.strftime('%H:%M:%S')}")
        elif min_remaining_seconds == remaining_seconds_sunrise_minus_15:
            capture_photo(output_folder_sunrise)
            print(f"Sunrise - 15 minutes photo captured at {now.strftime('%H:%M:%S')}")
        elif min_remaining_seconds == remaining_seconds_sunset_plus_15:
            capture_photo(output_folder_sunset)
            print(f"Sunset + 15 minutes photo captured at {now.strftime('%H:%M:%S')}")
        
        # Sleep until the next event
        print(f"Sleeping until {now + timedelta(seconds=min_remaining_seconds)} ({min_remaining_seconds} seconds)")
        time.sleep(min_remaining_seconds)
        
except KeyboardInterrupt:
    pass
except Exception as e:
    # Catch and log exceptions
    error_message = "Exception: " + str(e)
    print(error_message)  # Optional: Print the error to the console
    # log_error(error_message)  # You can log errors to a file if needed
else:
    # Log a success message with timestamp
    success_message = "Code execution completed successfully at {}".format(datetime.now().isoformat())
    print(success_message)  # Optional: Print the success message to the console
    # log_message(success_message)  # You can log success messages to a file if needed

# Close the log file when done
# sys.stderr.close()  # Commented out as it's not needed for basic functionality
