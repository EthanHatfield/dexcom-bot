# Troubleshooting Guide

## Issue: Not Getting the Authorization Code

### Problem
After logging in and clicking "Authorize", you're not seeing a URL that starts with `http://localhost:8080/callback?code=`

### Possible Causes & Solutions

#### 1. Redirect URI Not Registered in Dexcom Developer Portal

**Check your Dexcom Developer Portal settings:**

1. Go to https://developer.dexcom.com
2. Log in with your developer credentials
3. Click on your application
4. Check the "Redirect URIs" section
5. Make sure it contains EXACTLY: `http://localhost:8080/callback`
   - No trailing slash
   - No extra spaces
   - Exact case match

**If it's wrong or missing:**
- Edit your application
- Add or fix the redirect URI
- Save changes
- Wait a few minutes for changes to propagate
- Try the authorization again

#### 2. Dexcom UAM Service is Down (502 Error)

**Error message:**
```
UAM is down. HTTP code returned by uam1.dexcom.com : 502 BAD_GATEWAY
```

**What this means:**
Dexcom's authentication service (UAM - User Account Management) is temporarily unavailable.

**Solutions:**
- Wait 10-15 minutes and try again
- Check Dexcom Developer status page (if available)
- Try during off-peak hours
- Contact Dexcom developer support if issue persists

#### 3. Wrong URL Being Copied

**Common mistakes:**

❌ **Copying the login page URL** (Keycloak URL):
```
https://keycloak-prod.dexcom.com/auth/realms/Dexcom/protocol/openid-connect/auth?client_id=...
```

❌ **Copying URL-encoded parameters:**
```
http%3A%2F%2Flocalhost%3A8080%2Fcallback&response_type=...
```

✅ **What you SHOULD copy** (after authorization completes):
```
http://localhost:8080/callback?code=abc123def456ghi789...
```

**Steps to get the right URL:**

1. Start at login page (Keycloak URL - this is normal)
2. Enter Dexcom credentials
3. Click "Authorize" or "Allow"
4. Browser will try to load a new page
5. Page will show "Unable to connect" or similar error
6. **NOW look at the address bar** - it should show `http://localhost:8080/callback?code=...`
7. Copy that entire URL

#### 4. Browser Redirecting to Wrong Place

Some browsers or security software might block the redirect.

**Try:**
- Use a different browser (Chrome, Firefox, Edge)
- Disable VPN or proxy
- Try in incognito/private mode
- Check browser console for errors (F12 → Console tab)

## Current Issue: UAM Service Down

Based on your error, the main issue is:

```
UAM is down. HTTP code returned by uam1.dexcom.com : 502 BAD_GATEWAY
```

**Recommendation:**
1. Wait 15-30 minutes
2. Try the authorization process again
3. If it persists, check if Dexcom has any service status updates
4. Consider trying during different times of day

## Alternative: Manual Token Request (Advanced)

If the authorization keeps failing, you might need to contact Dexcom Developer Support to:
1. Verify your application is properly configured
2. Check if there are any account restrictions
3. Get help with OAuth setup
4. Confirm UAM service status

## Next Steps

1. **Verify redirect URI** in developer portal
2. **Wait for UAM service** to come back online
3. **Try authorization again** in 15-30 minutes
4. **Contact Dexcom support** if issue persists after 24 hours
