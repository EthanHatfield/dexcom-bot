# Dexcom Discord Bot

A Discord bot that integrates with Dexcom to provide glucose readings through Discord commands.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables:
- Copy `.env` file and fill in your credentials:
  - `DISCORD_TOKEN`: Your Discord bot token
  - `DEXCOM_USERNAME`: Your Dexcom account username
  - `DEXCOM_PASSWORD`: Your Dexcom account password

5. Run the bot:
```bash
python bot.py
```

## Available Commands

- `!glucose`: Get current glucose reading (to be implemented)

## Note

This is a basic implementation. Make sure to comply with Dexcom's terms of service and handle your credentials securely.