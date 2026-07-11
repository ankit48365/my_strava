import refresh_strava_token
import dlt_strava_bigquery

def run_all():
    print("Starting refresh_access_token...")
    success = refresh_strava_token.refresh_access_token()
    if success:
        print("🎉 Token refresh successful! You can now run your pipeline.")
    else:
        print("💥 Token refresh failed. You may need to re-authorize.").main()

    input("\nCopy Access Token from temp to secrets toml (.dlt) file and press ENTER to start script 2...")

    print("Starting script 2...")
    dlt_strava_bigquery.load_strava()

if __name__ == "__main__":
    run_all()
