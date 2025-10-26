"""Test script to verify Strava access token is working."""
import requests
import dlt

def test_strava_token():
    """Test the current Strava access token by making a simple API call."""
    # Get current secrets
    sec = dlt.secrets.get("sources.strava")
    access_token = sec["access_token"]
    
    print(f"🔍 Testing access token: {access_token[:8]}...")
    
    # Test with a simple API call to get athlete info
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # First try to get athlete info (basic endpoint)
    print("📡 Testing athlete endpoint...")
    response = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    
    if response.status_code == 200:
        athlete_data = response.json()
        print(f"✅ Athlete endpoint works! Hello {athlete_data.get('firstname', 'Unknown')}!")
        
        # Now test the activities endpoint
        print("📡 Testing activities endpoint...")
        activities_response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities?per_page=1", 
            headers=headers
        )
        
        if activities_response.status_code == 200:
            print("✅ Activities endpoint works!")
            activities = activities_response.json()
            print(f"📊 Found {len(activities)} activities in test call")
            return True
        else:
            print(f"❌ Activities endpoint failed: {activities_response.status_code}")
            print(f"Response: {activities_response.text}")
            return False
    else:
        print(f"❌ Athlete endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    success = test_strava_token()
    if not success:
        print("\n💡 The token might be expired or have insufficient scopes.")
        print("   You may need to re-authorize using: uv run strava_authorize.py")
