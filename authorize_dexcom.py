"""
Dexcom OAuth Authorization Script

This script helps you obtain the initial access and refresh tokens
from Dexcom's OAuth API.

Steps:
1. Run this script
2. It will open a browser with Dexcom's login page
3. Log in with your Dexcom credentials
4. After authorizing, you'll be redirected to a localhost URL
5. Copy the 'code' parameter from the URL
6. Paste it back into this script
7. The script will exchange it for access and refresh tokens
8. Save those tokens to your .env file
"""

import os
import webbrowser
from dotenv import load_dotenv
from dexcom_api import DexcomAPI

def main():
    print("=" * 60)
    print("Dexcom OAuth Authorization")
    print("=" * 60)
    print("\nUsing SANDBOX API (for testing)")
    print("Note: Production API requires special approval from Dexcom")
    print("=" * 60)
    
    # Initialize the API with sandbox mode
    api = DexcomAPI(use_sandbox=True)
    
    if not api.client_id or not api.client_secret:
        print("\n❌ Error: DEXCOM_CLIENT_ID and DEXCOM_CLIENT_SECRET must be set in .env file")
        return
    
    # Step 1: Get authorization URL
    auth_url = api.get_authorization_url()
    
    print("\nStep 1: Authorize the application")
    print("-" * 60)
    print("Opening Dexcom authorization page in your browser...")
    print(f"\nIf the browser doesn't open, visit this URL manually:")
    print(auth_url)
    
    # Try to open browser
    try:
        webbrowser.open(auth_url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
    
    print("\nStep 2: After logging in and authorizing:")
    print("-" * 60)
    print("1. You'll be redirected to a URL like:")
    print("   http://localhost:8080/callback?code=XXXXXXXXXXXXX")
    print("2. Copy the ENTIRE URL from your browser's address bar")
    print("3. Or just copy the 'code' parameter value")
    
    # Step 2: Get the authorization code from user
    print("\n" + "=" * 60)
    redirect_url = input("\nPaste the redirect URL (or just the code): ").strip()
    
    # Extract code from URL if full URL was pasted
    if "code=" in redirect_url:
        code = redirect_url.split("code=")[1].split("&")[0]
    else:
        code = redirect_url
    
    if not code:
        print("❌ No authorization code provided. Exiting.")
        return
    
    print(f"\nUsing authorization code: {code[:20]}...")
    
    # Step 3: Exchange code for tokens
    print("\nStep 3: Exchanging authorization code for tokens")
    print("-" * 60)
    
    if api.exchange_code_for_token(code):
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Authorization complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy the tokens printed above")
        print("2. Add them to your .env file:")
        print("   DEXCOM_ACCESS_TOKEN=...")
        print("   DEXCOM_REFRESH_TOKEN=...")
        print("3. Run your Discord bot: python bot.py")
        print("\n⚠️  Keep these tokens secure and never share them!")
    else:
        print("\n❌ Failed to exchange authorization code for tokens.")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
