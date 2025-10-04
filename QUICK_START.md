# Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### What You Need
- ✅ Your Dexcom Client ID and Secret (already in `.env`)
- ✅ Your Dexcom account login (ejh2151@gmail.com + password)

### Steps

#### 1️⃣ Run Authorization Script
```bash
python authorize_dexcom.py
```

#### 2️⃣ Login in Browser
- Script opens browser → Dexcom login page
- Enter: ejh2151@gmail.com
- Enter your Dexcom password (the one you use in the app)
- Click "Authorize"

#### 3️⃣ Copy the Code
After authorizing, your browser will redirect to something like:
```
http://localhost:8080/callback?code=abcd1234efgh5678
```

The page won't load (that's normal!). Just copy the ENTIRE URL from the address bar.

#### 4️⃣ Paste Back into Terminal
The script is waiting for you to paste the URL. Paste it and hit Enter.

#### 5️⃣ Save the Tokens
The script will print something like:
```
DEXCOM_ACCESS_TOKEN=eyJhbGciOiJSUzI1...
DEXCOM_REFRESH_TOKEN=def50200a8f4c3b2...
```

**Copy these two lines** and paste them into your `.env` file (replacing the empty values).

#### 6️⃣ Run Your Bot
```bash
python bot.py
```

#### 7️⃣ Test in Discord
```
!glucose
```

## 🔄 If Tokens Expire

Don't worry! The bot will automatically refresh them. If that fails, just run step 1 again.

## ❓ Troubleshooting

### Browser doesn't open?
Copy the URL from the terminal and paste it in your browser manually.

### "Invalid client" error?
Check that your Client ID and Secret in `.env` are correct.

### "Redirect URI mismatch"?
Go to https://developer.dexcom.com and set your app's redirect URI to:
```
http://localhost:8080/callback
```

### Still stuck?
Check `OAUTH_FIX_SUMMARY.md` for detailed explanation.
