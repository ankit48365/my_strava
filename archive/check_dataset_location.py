"""Script to check BigQuery dataset location."""
from google.cloud import bigquery
from google.oauth2 import service_account

# Path to service account key file
key_path = r"C:\Users\ankit\Downloads\mystrava-464501-32eb6aa1b1b8.json"

# Create credentials from service account file
credentials = service_account.Credentials.from_service_account_file(key_path)

# Create BigQuery client
client = bigquery.Client(credentials=credentials, project="mystrava-464501")

# Get dataset
try:
    dataset = client.get_dataset("landing")
    print(f"Dataset: {dataset.dataset_id}")
    print(f"Project: {dataset.project}")
    print(f"Location: {dataset.location}")
    print(f"Full ID: {dataset.full_dataset_id}")
except Exception as e:
    print(f"Error: {e}")
