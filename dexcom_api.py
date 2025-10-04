"""
Dexcom API Wrapper

Handles OAuth 2.0 authentication and API interactions with Dexcom's CGM platform.
Supports both sandbox (testing) and production (real data) environments.

OAuth Flow:
    1. User authorizes app via browser (get_authorization_url)
    2. Dexcom redirects with authorization code
    3. Exchange code for access/refresh tokens (exchange_code_for_token)
    4. Use access token for API calls
    5. Auto-refresh when expired (refresh_access_token)
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

class DexcomAPI:
    # Dexcom has both sandbox and production APIs
    # Sandbox: For testing with simulated data
    # Production: For real user data (requires special approval)
    SANDBOX_BASE_URL = "https://sandbox-api.dexcom.com"
    PRODUCTION_BASE_URL = "https://api.dexcom.com"
    REDIRECT_URI = "https://localhost:8080/callback"  # You'll need to register this with Dexcom
    
    def __init__(self, use_sandbox=True):
        # Load all environment variables
        load_dotenv()  # Make sure we reload the environment variables
        
        # Use sandbox by default (production requires special approval from Dexcom)
        self.use_sandbox = use_sandbox
        self.BASE_URL = self.SANDBOX_BASE_URL if use_sandbox else self.PRODUCTION_BASE_URL
        
        self.client_id = os.getenv('DEXCOM_CLIENT_ID')
        self.client_secret = os.getenv('DEXCOM_CLIENT_SECRET')
        self.access_token = os.getenv('DEXCOM_ACCESS_TOKEN')
        self.refresh_token = os.getenv('DEXCOM_REFRESH_TOKEN')
        
        print("\nDexcom Credentials Check:")
        print("Environment variables found:")
        for var in ['DEXCOM_CLIENT_ID', 'DEXCOM_CLIENT_SECRET', 'DEXCOM_ACCESS_TOKEN', 'DEXCOM_REFRESH_TOKEN']:
            value = os.getenv(var)
            if value:
                print(f"- {var}: Present (length: {len(value)})")
            else:
                print(f"- {var}: Missing")
    
    def get_authorization_url(self):
        """Generate the URL where users authorize your app"""
        auth_url = f"{self.BASE_URL}/v2/oauth2/login"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.REDIRECT_URI,
            "response_type": "code",
            "scope": "offline_access"
        }
        url = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        print(f"\nAuthorization URL:\n{url}\n")
        return url
    
    def exchange_code_for_token(self, authorization_code):
        """Exchange authorization code for access and refresh tokens"""
        url = f"{self.BASE_URL}/v2/oauth2/token"
        print(f"Exchanging authorization code for tokens...")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.REDIRECT_URI
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers)
            print(f"Token Exchange Response Status: {response.status_code}")
            
            if response.status_code == 200:
                auth_data = response.json()
                self.access_token = auth_data.get('access_token')
                self.refresh_token = auth_data.get('refresh_token')
                
                print("Successfully obtained tokens!")
                print(f"Access Token: {self.access_token[:20]}..." if self.access_token else "None")
                print(f"Refresh Token: {self.refresh_token[:20]}..." if self.refresh_token else "None")
                print("\n⚠️  IMPORTANT: Save these tokens to your .env file:")
                print(f"DEXCOM_ACCESS_TOKEN={self.access_token}")
                print(f"DEXCOM_REFRESH_TOKEN={self.refresh_token}")
                return True
            else:
                print(f"Token exchange failed: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Token exchange error: {e}")
            return False
    
    def refresh_access_token(self):
        """Refresh the access token using the refresh token"""
        if not self.refresh_token:
            print("No refresh token available. Need to authorize first.")
            return False
            
        url = f"{self.BASE_URL}/v2/oauth2/token"
        print(f"Refreshing access token...")
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": self.REDIRECT_URI
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers)
            print(f"Refresh Token Response Status: {response.status_code}")
            
            if response.status_code == 200:
                auth_data = response.json()
                self.access_token = auth_data.get('access_token')
                self.refresh_token = auth_data.get('refresh_token')  # Sometimes a new refresh token is issued
                
                print("Successfully refreshed access token!")
                print(f"\n⚠️  Update your .env file with new access token:")
                print(f"DEXCOM_ACCESS_TOKEN={self.access_token}")
                if self.refresh_token != os.getenv('DEXCOM_REFRESH_TOKEN'):
                    print(f"DEXCOM_REFRESH_TOKEN={self.refresh_token}")
                return True
            else:
                print(f"Token refresh failed: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Token refresh error: {e}")
            return False
            
    def authenticate(self):
        """Check if we have valid tokens, refresh if needed"""
        if not self.access_token:
            if self.refresh_token:
                print("No access token but have refresh token. Attempting to refresh...")
                return self.refresh_access_token()
            else:
                print("\n❌ No access token or refresh token found!")
                print("You need to authorize the app first.")
                print("\nRun the authorization script:")
                print("python authorize_dexcom.py")
                return False
        
        # Assume token is valid if we have it
        # If API call fails with 401, we'll refresh then
        return True
            
    def get_latest_glucose_reading(self):
        """Get the most recent glucose reading"""
        if not self.access_token:
            if not self.authenticate():
                return None
                
        url = f"{self.BASE_URL}/v2/users/self/egvs"
        print(f"Using glucose URL: {url}")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }
        
        # Get readings from last hour
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(hours=1)
        
        params = {
            'startDate': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'endDate': end_date.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Glucose reading response status: {response.status_code}")
            
            # If unauthorized, try to refresh token and retry once
            if response.status_code == 401:
                print("Access token expired. Attempting to refresh...")
                if self.refresh_access_token():
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    response = requests.get(url, headers=headers, params=params)
                    print(f"Retry glucose reading response status: {response.status_code}")
            
            print(f"Glucose reading response: {response.text[:200]}...")  # Print first 200 chars
            
            response.raise_for_status()
            data = response.json()
            
            if data and 'egvs' in data and len(data['egvs']) > 0:
                latest = data['egvs'][-1]  # Get most recent reading
                return {
                    'value': latest['value'],
                    'trend': latest.get('trend', 'NONE'),
                    'timestamp': datetime.fromisoformat(latest['timestamp'].replace('Z', '+00:00'))
                }
            return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to get glucose reading: {e}")
            try:
                if e.response:
                    print(f"Error response: {e.response.text}")
            except:
                pass
            return None
            
    def get_trend_arrow(self, trend):
        """Convert Dexcom trend to arrow symbol"""
        trends = {
            'NONE': "?",
            'DOUBLE_UP': "↑↑",
            'SINGLE_UP': "↑",
            'FORTY_FIVE_UP': "↗",
            'FLAT': "→",
            'FORTY_FIVE_DOWN': "↘",
            'SINGLE_DOWN': "↓",
            'DOUBLE_DOWN': "↓↓",
            'NOT_COMPUTABLE': "?",
            'RATE_OUT_OF_RANGE': "?"
        }
        return trends.get(str(trend).upper(), "?")