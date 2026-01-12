import requests
from datetime import datetime, timedelta
import json

API_URL = "https://json.freeastrologyapi.com/rahu-kalam"
API_KEY = "VT0mrAZWf64oIqoTgUfZg6AmH91Cfasv87YYOxbR"

LOCATION = {
    "latitude": 43.2081,    # Concord, NH
    "longitude": -71.5376, # Concord, NH
    "timezone": -5          # EST (UTC-5)
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def get_rahu_kalam_for_date(year, month, day):
    """Fetch Rahu Kaal for a specific date using the API"""
    payload = {
        "year": year,
        "month": month,
        "date": day,
        "hours": 12,      # These seem to be ignored for Rahu Kaal calculation
        "minutes": 1,
        "seconds": 0,
        "latitude": LOCATION["latitude"],
        "longitude": LOCATION["longitude"],
        "timezone": LOCATION["timezone"]
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except:
            print(f"Error parsing JSON for {year}-{month:02d}-{day:02d}")
            return None
    else:
        print(f"API error {response.status_code} for {year}-{month:02d}-{day:02d}")
        return None

def generate_rahu_json(start_date, end_date):
    """Generate JSON file with Rahu Kaal for date range"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    results = []
    current = start
    
    print(f"Generating Rahu Kaal data from {start_date} to {end_date}...")
    
    while current <= end:
        year, month, day = current.year, current.month, current.day
        
        rahu_data = get_rahu_kalam_for_date(year, month, day)
        
        if rahu_data:
            entry = {
                "location": {
                    "city": "Concord",
                    "state": "New Hampshire", 
                    "country": "United States",
                    "latitude": LOCATION["latitude"],
                    "longitude": LOCATION["longitude"],
                    "timezone": LOCATION["timezone"]
                },
                "date": current.strftime("%Y-%m-%d"),
                "rahuKaal": rahu_data  # Raw API response
            }
            results.append(entry)
            print(f"Added {current.strftime('%Y-%m-%d')}")
        else:
            print(f"Skipped {current.strftime('%Y-%m-%d')} (API error)")
        
        current += timedelta(days=1)
    
    # Save to JSON file
    filename = f"rahu_kalam_concord_{start_date}_to_{end_date}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Generated {len(results)} entries in {filename}")
    print(f"📁 File saved: {filename}")
    
    return results

if __name__ == "__main__":
    # Define your date range here
    START_DATE = "2026-1-11"
    END_DATE = "2026-2-28"
    
    # Generate the JSON file
    data = generate_rahu_json(START_DATE, END_DATE)
    
    # Optional: Print first entry to verify
    if data:
        print("\n📋 Sample entry:")
        print(json.dumps(data[0], indent=2))
