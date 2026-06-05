"""Script to refresh Strava access token using the refresh token."""
import requests
import dlt
import os

def refresh_access_token():
    """Refreshes the Strava access token using the refresh token."""
    # Get current secrets
    sec = dlt.secrets.get("sources.strava")
    client_id = sec["client_id"]
    client_secret = sec["client_secret"]
    refresh_token = sec["refresh_token"]
    
    print("🔄 Refreshing Strava access token...")
    
    # Make request to refresh token
    response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    })
    
    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data["access_token"]
        new_refresh_token = token_data["refresh_token"]
        
        print(f"✅ New access token: {new_access_token[:8]}...")
        print(f"✅ New refresh token: {new_refresh_token[:8]}...")
        
        # Update the secrets file
        update_secrets_file(new_access_token, new_refresh_token, client_id, client_secret)
        
        return True
    else:
        print(f"❌ Failed to refresh token. Status: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def update_secrets_file(access_token, refresh_token, client_id, client_secret):
    """Updates the DLT secrets file with the new tokens."""
    temp_secret_path = ".dlt/temp_secret.toml"
    
    lines = [
        "[sources.strava]",
        f'access_token  = "{access_token}"',
        f'refresh_token = "{refresh_token}"',
        f'client_id     = "{client_id}"',
        f'client_secret = "{client_secret}"',
        ""
    ]
    
    os.makedirs(os.path.dirname(temp_secret_path), exist_ok=True)
    with open(temp_secret_path, "w") as f:
        f.write("\n".join(lines))
    
    print(f"✅ Updated {temp_secret_path} with new credentials.")

if __name__ == "__main__":
    success = refresh_access_token()
    if success:
        print("🎉 Token refresh successful! You can now run your pipeline.")
    else:
        print("💥 Token refresh failed. You may need to re-authorize.")
