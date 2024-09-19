import requests
import json
import toml

# Make Strava auth API call with your client_id, client_secret, and code
response = requests.post(
    url='https://www.strava.com/oauth/token',
    data={
        'client_id': '143057',
        'client_secret': 'f8b21641bf7b70598a72d34b1',
        'code': '[INSERT_CODE_FROM_URL_HERE]',
        'grant_type': 'authorization_code'
    }
)

# Save JSON response as a variable
strava_tokens = response.json()

# Load the existing TOML file
with open('.dlt/secrets.toml', 'r') as toml_file:
    config = toml.load(toml_file)

# Update the Strava section with new tokens
config['strava']['access_token'] = strava_tokens['access_token']

# Save the updated TOML file
with open('.dlt/secrets.toml', 'w') as toml_file:
    toml.dump(config, toml_file)

# Print the updated Strava section to verify
print(config['strava'])
