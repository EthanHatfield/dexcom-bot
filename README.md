# Dexcom Discord Bot

A Discord bot that fetches and displays real-time glucose readings from Dexcom CGM using OAuth 2.0.

## 🚀 Features

- **Real-time glucose monitoring** via Discord commands
- **OAuth 2.0 authentication** with Dexcom API
- **Automatic token refresh** when access tokens expire
- **Sandbox & Production support** (production requires Dexcom approval)

## 📋 Prerequisites

1. **Python 3.7+**
2. **Discord Bot Token** - [Create one here](https://discord.com/developers/applications)
3. **Dexcom Developer Account** - [Sign up here](https://developer.dexcom.com)

## 🛠️ Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd dexcom-bot
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your tokens:
- `DISCORD_TOKEN` - From Discord Developer Portal
- `DEXCOM_CLIENT_ID` - From Dexcom Developer Portal
- `DEXCOM_CLIENT_SECRET` - From Dexcom Developer Portal

### 3. Configure Dexcom Developer Application

1. Go to [Dexcom Developer Portal](https://developer.dexcom.com)
2. Create a new application
3. **Important**: Set the redirect URI to: `https://localhost:8080/callback` (must be HTTPS!)
4. Save your Client ID and Client Secret

### 4. Authorize with Dexcom (OAuth Flow)

Run the authorization script:

```bash
python authorize_dexcom.py
```

This will:
1. ✅ Open Dexcom's login page in your browser
2. ✅ Log in with your Dexcom account credentials
3. ✅ Authorize the application
4. ✅ Copy the redirect URL from your browser
5. ✅ Paste it into the terminal
6. ✅ Receive your access and refresh tokens

**Copy the tokens** printed by the script and add them to your `.env` file:

```env
DEXCOM_ACCESS_TOKEN=eyJhbGci...
DEXCOM_REFRESH_TOKEN=US_abc123...
```

### 5. Test the Connection (Optional)

```bash
python test_dexcom.py
```

### 6. Run the Bot

```bash
python bot.py
```

## 💬 Discord Commands

| Command | Description |
|---------|-------------|
| `!glucose` | Get current glucose reading |
| `!commands` | Show available commands |

## 🔐 OAuth 2.0 Authentication

⚠️ **Important**: Dexcom's API uses OAuth 2.0 - you cannot authenticate with username/password directly!

### OAuth Flow:
1. **User Authorization** → Browser login
2. **Authorization Code** → Temporary code from redirect
3. **Token Exchange** → Code traded for access/refresh tokens
4. **API Access** → Use access token for API calls
5. **Auto Refresh** → Refresh tokens automatically when they expire

## 🏖️ Sandbox vs Production

### Sandbox (Default)
- ✅ No approval required
- ✅ Great for testing OAuth flow
- ❌ No real glucose data
- Used for development and testing

### Production
- ✅ Real glucose data
- ❌ Requires Dexcom approval
- ❌ Longer application process
- Used for live deployments

To switch to production (after approval), change `use_sandbox=False` in `bot.py`.

## 🐛 Troubleshooting

### "max user count exceeded"
- Your developer app has hit its user limit
- Create a new application in the Dexcom Developer Portal
- Update credentials in `.env`

### "401 Unauthorized" errors
- Access token expired (bot will auto-refresh)
- If refresh fails, run `authorize_dexcom.py` again

### "Invalid redirect URI"
- Must be exactly: `https://localhost:8080/callback` (HTTPS, not HTTP!)
- Update in Dexcom Developer Portal application settings

### Browser shows "Can't reach this page" after authorizing
- **This is normal!** Just copy the URL from the address bar
- It will look like: `https://localhost:8080/callback?code=...`

### No glucose data in sandbox
- Sandbox API doesn't provide real data
- Request production API access from Dexcom for real data

For more troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📁 Project Structure

```
dexcom-bot/
├── bot.py                    # Discord bot main file
├── dexcom_api.py            # Dexcom API wrapper with OAuth
├── authorize_dexcom.py      # OAuth authorization helper script
├── test_dexcom.py           # Test script for API connection
├── requirements.txt         # Python dependencies
├── .env                     # Your credentials (DO NOT COMMIT!)
├── .env.example            # Template for .env
├── .gitignore              # Prevents committing sensitive files
├── README.md               # This file
├── QUICK_START.md          # 5-minute setup guide
├── OAUTH_FIX_SUMMARY.md    # OAuth implementation details
└── TROUBLESHOOTING.md      # Detailed troubleshooting guide
```

## 🔒 Security

⚠️ **NEVER commit your `.env` file to version control!**

The `.env` file contains sensitive tokens:
- Discord bot token
- Dexcom API credentials
- Access and refresh tokens

These tokens provide access to your accounts and data. Keep them secure!

## 📝 License

This project is for personal use. Make sure to comply with:
- [Dexcom's Terms of Service](https://developer.dexcom.com/terms-of-service)
- [Discord's Terms of Service](https://discord.com/terms)

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📚 Additional Resources

- [Dexcom Developer Portal](https://developer.dexcom.com)
- [Discord Developer Portal](https://discord.com/developers)
- [OAuth 2.0 Documentation](https://oauth.net/2/)