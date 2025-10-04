# OAuth Authentication Fix Summary

## The Problem

Your bot was trying to authenticate with Dexcom using `client_credentials` grant type with just the Client ID and Client Secret. **This doesn't work with Dexcom's API.**

Dexcom requires full OAuth 2.0 Authorization Code flow, which means:
- ❌ You CANNOT just pass username/password to the API
- ❌ You CANNOT authenticate with just client credentials
- ✅ You MUST have a user authorize your app through their web interface
- ✅ You MUST exchange an authorization code for access tokens

## What Changed

### 1. Updated `dexcom_api.py`

**Removed:**
- `client_credentials` grant type authentication
- Direct username/password usage

**Added:**
- `get_authorization_url()` - Generates the URL for user authorization
- `exchange_code_for_token()` - Exchanges authorization code for tokens
- `refresh_access_token()` - Refreshes expired access tokens
- Better error handling with automatic token refresh on 401 errors

### 2. Created `authorize_dexcom.py`

A new helper script that:
- Generates the authorization URL
- Opens it in your browser
- Guides you through the OAuth flow
- Exchanges the code for tokens
- Shows you what to put in your `.env` file

### 3. Updated `.env`

**Removed:**
- `DEXCOM_USERNAME` (not used by OAuth)
- `DEXCOM_PASSWORD` (not used by OAuth)

**Added:**
- `DEXCOM_ACCESS_TOKEN` (obtained via OAuth)
- `DEXCOM_REFRESH_TOKEN` (obtained via OAuth)

## How to Fix Your Bot

### Step 1: Run the authorization script

```bash
python authorize_dexcom.py
```

### Step 2: Follow the prompts

1. Browser will open to Dexcom login
2. Log in with your Dexcom credentials (ejh2151@gmail.com / your password)
3. Authorize the application
4. Copy the redirect URL you're sent to
5. Paste it back into the script

### Step 3: Save the tokens

The script will print:
```
DEXCOM_ACCESS_TOKEN=abc123...
DEXCOM_REFRESH_TOKEN=xyz789...
```

Copy these into your `.env` file.

### Step 4: Run your bot

```bash
python bot.py
```

## Why This Is Required

Dexcom's API is designed for third-party applications that need user consent. The OAuth flow ensures:

1. **Security**: Users explicitly authorize your app
2. **Scope Control**: Users know what data you're accessing
3. **Token Expiration**: Access tokens expire, refresh tokens allow renewal
4. **Revocation**: Users can revoke access at any time

## Token Lifecycle

```
Initial Authorization
    ↓
Authorization Code (short-lived, one-time use)
    ↓
Exchange for Tokens
    ↓
Access Token (expires after ~hours/days) + Refresh Token (long-lived)
    ↓
Use Access Token for API calls
    ↓
When expired → Use Refresh Token to get new Access Token
    ↓
Repeat
```

## Common Issues

### "The redirect URI doesn't match"
- Go to your Dexcom Developer Portal
- Edit your application settings
- Set redirect URI to exactly: `http://localhost:8080/callback`

### "Invalid authorization code"
- Authorization codes expire quickly (usually 10 minutes)
- Run `authorize_dexcom.py` again and complete it faster
- Make sure you copied the entire code

### "401 Unauthorized" when calling API
- Your access token expired
- The bot will automatically try to refresh it
- If refresh fails, run `authorize_dexcom.py` again

## Next Steps

After getting your tokens:
1. Test with `!glucose` command in Discord
2. Monitor for any 401 errors
3. The bot will auto-refresh tokens when needed
4. Keep your `.env` file secure and backed up
