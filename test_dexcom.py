"""
Quick test script to verify your Dexcom tokens work
Run this after running authorize_dexcom.py
"""

import os
from dotenv import load_dotenv
from dexcom_api import DexcomAPI

def main():
    print("=" * 60)
    print("Testing Dexcom API Connection")
    print("=" * 60)
    
    # Force reload environment variables
    load_dotenv(override=True)
    
    # Initialize API with sandbox mode
    api = DexcomAPI(use_sandbox=True)
    
    # Check authentication
    print("\n1. Checking authentication...")
    if api.authenticate():
        print("✅ Authentication successful!")
    else:
        print("❌ Authentication failed!")
        print("\nPlease run: python authorize_dexcom.py")
        return
    
    # Try to get glucose reading
    print("\n2. Fetching latest glucose reading...")
    reading = api.get_latest_glucose_reading()
    
    if reading:
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Dexcom API is working!")
        print("=" * 60)
        print(f"\nGlucose: {reading['value']} mg/dL")
        print(f"Trend: {reading['trend']}")
        print(f"Time: {reading['timestamp']}")
        print("\nYour bot is ready to use! Run: python bot.py")
    else:
        print("\n❌ Could not fetch glucose reading")
        print("This could mean:")
        print("  - No recent glucose data available")
        print("  - Token needs to be refreshed")
        print("  - API permissions issue")
        print("\nCheck the error messages above for details.")

if __name__ == "__main__":
    main()
