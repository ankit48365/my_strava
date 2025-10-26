"""
Master script to run the complete Strava pipeline with proper token management.
This script handles token refresh, validation, and pipeline execution in the correct sequence.
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle its output."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
            
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            return True
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to run {description}: {str(e)}")
        return False

def main():
    """Main function to run the complete Strava pipeline sequence."""
    print("🏃‍♂️ Strava Pipeline Runner")
    print("This script will:")
    print("1. Refresh your Strava access token")
    print("2. Test the token permissions")
    print("3. Run the DLT pipeline to load data into BigQuery")
    
    # Step 1: Refresh the Strava token
    if not run_command("uv run refresh_strava_token.py", "Refreshing Strava Access Token"):
        print("\n💡 If token refresh fails, you may need to re-authorize:")
        print("   Run: uv run strava_authorize.py")
        return False
    
    # Step 2: Test the token
    if not run_command("uv run test_strava_token.py", "Testing Strava Token Permissions"):
        print("\n💡 If token test fails, try re-authorizing:")
        print("   Run: uv run strava_authorize.py")
        return False
    
    # Step 3: Run the main pipeline
    if not run_command("uv run dlt_strava_bigquery.py", "Running Strava to BigQuery Pipeline"):
        print("\n💡 Pipeline failed. Check your BigQuery credentials in .dlt/secrets.toml")
        return False
    
    print("\n🎉 Complete! Your Strava data has been successfully loaded into BigQuery.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
