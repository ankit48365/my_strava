import requests
import json
from datetime import date, timedelta

def save_flattened_weather_next_week():
    # Concord, NH coordinates
    lat = 43.2081
    lon = -71.5376

    # Today and next 7 days
    start_date = date.today()
    end_date = start_date + timedelta(days=7)

    # Open-Meteo free API (daily forecast)
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        f"&start_date={start_date}&end_date={end_date}"
        "&timezone=America/New_York"
    )

    response = requests.get(url)
    data = response.json().get("daily", {})

    # Flatten into list of row JSON objects
    flattened_rows = []
    for i, day in enumerate(data.get("time", [])):
        row = {
            "date": day,
            "city": "Concord",
            "state": "New Hampshire",
            "country": "United States",
            "latitude": lat,
            "longitude": lon,
            "temp_max": data["temperature_2m_max"][i],
            "temp_min": data["temperature_2m_min"][i],
            "windspeed_max": data["windspeed_10m_max"][i],
            "precipitation_sum": data["precipitation_sum"][i]
        }
        flattened_rows.append(row)

    # Filename with date range
    filename = f"weather_{start_date}_{end_date}.json"

    # Save to file
    with open(filename, "w") as f:
        json.dump(flattened_rows, f, indent=2)

    return filename


# Example usage
if __name__ == "__main__":
    saved_file = save_flattened_weather_next_week()
    print(f"Saved weather data to: {saved_file}")