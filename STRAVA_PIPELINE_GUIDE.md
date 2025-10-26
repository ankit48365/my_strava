# Strava Pipeline Guide

This guide explains how to use all the scripts in the correct sequence to ensure your Strava data pipeline runs successfully.

## 📁 Script Overview

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `strava_authorize.py` | Initial authorization & re-authorization | First time setup or when refresh token expires |
| `refresh_strava_token.py` | Refresh expired access tokens | When access token expires (every 6 hours) |
| `test_strava_token.py` | Test token validity and permissions | Before running pipeline to verify setup |
| `dlt_strava_bigquery.py` | Main pipeline script | Load Strava data into BigQuery |


## 🚀 Quick Start (Recommended)


## 📋 Manual Step-by-Step Process

### First Time Setup
1. **Initial Authorization** (only needed once or when refresh token expires):
   ```bash
   uv run strava_authorize.py
   ```
   - Opens browser for Strava authorization
   - Paste the authorization code when prompted
   - Updates your credentials automatically

2. **Test Setup**:
   ```bash
   uv run test_strava_token.py
   ```
   - Verifies token has correct permissions
   - Should show "Activities endpoint works!"

3. **Run Pipeline**:
   ```bash
   uv run dlt_strava_bigquery.py
   ```

### Regular Pipeline Runs
1. **Refresh Token** (access tokens expire every 6 hours):
   ```bash
   uv run refresh_strava_token.py
   ```

2. **Test Token**:
   ```bash
   uv run test_strava_token.py
   ```

3. **Run Pipeline**:
   ```bash
   uv run dlt_strava_bigquery.py
   ```

## 🔧 Troubleshooting

### 401 Unauthorized Errors
1. **Try refreshing the token first**:
   ```bash
   uv run refresh_strava_token.py
   ```

2. **If refresh fails, re-authorize**:
   ```bash
   uv run strava_authorize.py
   ```

3. **Test the new token**:
   ```bash
   uv run test_strava_token.py
   ```

### Missing Permissions Error
If you see `"activity:read_permission","code":"missing"`:
```bash
uv run strava_authorize.py
```
This will get a new token with the correct `activity:read_all` scope.

### BigQuery Credentials Missing
Update `.dlt/secrets.toml` with your Google Cloud credentials:
```toml
[destination.bigquery.credentials]
project_id = "your-gcp-project-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
```

## 📅 Recommended Workflow

### Daily/Regular Use
```bash
# One command does everything:
uv run run_strava_pipeline.py
```

### When Things Go Wrong
```bash
# Step 1: Try refreshing token
uv run refresh_strava_token.py

# Step 2: Test if it worked
uv run test_strava_token.py

# Step 3: If still failing, re-authorize
uv run strava_authorize.py

# Step 4: Test again
uv run test_strava_token.py

# Step 5: Run pipeline
uv run dlt_strava_bigquery.py
```

## 🔄 Token Lifecycle

1. **Access Token**: Expires every 6 hours
2. **Refresh Token**: Long-lived, used to get new access tokens
3. **Authorization**: Only needed when refresh token expires (rare)

## 💡 Pro Tips

- **Use the master script** (`run_strava_pipeline.py`) for regular runs
- **Set up a cron job** to run the master script daily/weekly
- **Monitor the output** - the scripts provide clear success/failure messages
- **Keep your secrets file secure** - never commit `.dlt/secrets.toml` to version control

## 🆘 Quick Reference

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | `uv run refresh_strava_token.py` |
| Missing permissions | `uv run strava_authorize.py` |
| BigQuery errors | Check `.dlt/secrets.toml` credentials |
| General issues | `uv run run_strava_pipeline.py` |


#### Big Query Notes

 - uses ak83 gmail account 
 - https://console.cloud.google.com/

##### ./dlt/Config.toml should have tis section

```python
[destination.bigquery]
location = "northamerica-northeast1"
```

##### ./dlt/secrets.toml
Get these from Google Cloud Console > IAM & Admin > Service Accounts  , delete any old key, becuase its only used here, {ensure its mydataswamp project in cloud} , download new json and get below stuff out of it

```python
[destination.bigquery.credentials]
# BigQuery credentials - you need to fill these in with your actual values
# Get these from Google Cloud Console > IAM & Admin > Service Accounts
project_id = "mystrava-464501"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIVvEEH5Uv8=\n-----END PRIVATE KEY-----\n"
client_email = "sv-account-strava@mystrava-464501.iam.gserviceaccount.com"
```

##### Check dataset

run below code {PS D:\mygit\my_strava> uv run check_dataset_location.py  }

```python
                                                                                                                  
Dataset: landing
Project: mystrava-464501
Location: northamerica-northeast1
Full ID: mystrava-464501:landing
```