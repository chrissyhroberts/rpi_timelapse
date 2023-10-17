import requests
from datetime import date, timedelta
import json

# Define your location's latitude and longitude
latitude = "52.077463"
longitude = "-0.054215"

# Start date and end date
start_date = date.today()
end_date = date(2025, 1, 1)

# API endpoint
api_url = "https://api.sunrise-sunset.org/json"

# Initialize a dictionary to store sunrise and sunset times
sunrise_sunset_data = {}

while start_date <= end_date:
    # Format date in YYYY-MM-DD
    date_str = start_date.strftime("%Y-%m-%d")

    # Create API request URL
    params = {
        "lat": latitude,
        "lng": longitude,
        "date": date_str,
    }

    # Make the API request
    response = requests.get(api_url, params=params)
    data = response.json()

    # Extract sunrise and sunset times
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    # Store the data in the dictionary
    sunrise_sunset_data[date_str] = {
        "sunrise": sunrise,
        "sunset": sunset,
    }

    # Move to the next day
    start_date += timedelta(days=1)

# Save the data to a JSON file
with open("sunrise_sunset_data.json", "w") as json_file:
    json.dump(sunrise_sunset_data, json_file, indent=4)

print("Sunrise and sunset data saved to sunrise_sunset_data.json")
