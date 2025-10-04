"""
Dexcom Discord Bot

A Discord bot that provides glucose readings from Dexcom CGM via Discord commands.
Uses OAuth 2.0 for secure authentication with Dexcom's API.

Commands:
    !glucose - Get current glucose reading
    !commands - Show available commands
"""

import os
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
from dexcom_api import DexcomAPI

# Load environment variables from .env file
load_dotenv()

# Initialize Dexcom API
# Set use_sandbox=True for testing (no real data)
# Set use_sandbox=False for production (requires Dexcom approval)
dexcom = DexcomAPI(use_sandbox=True)

# Configure Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when the bot successfully connects to Discord"""
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'📊 Bot is ready to provide glucose readings!')

@bot.command(name='glucose')
async def get_glucose(ctx):
    """Get current glucose reading from Dexcom
    
    Usage: !glucose
    Returns the most recent glucose reading with trend arrow and timestamp.
    """
    reading = dexcom.get_latest_glucose_reading()
    
    if reading:
        trend_arrow = dexcom.get_trend_arrow(reading['trend'])
        time_diff = (datetime.now() - reading['timestamp']).total_seconds() // 60
        
        response = (
            f"📊 **Current Glucose Reading**\n"
            f"🩸 Glucose: **{reading['value']} mg/dL** {trend_arrow}\n"
            f"⏰ Last updated: {int(time_diff)} minutes ago"
        )
    else:
        response = (
            "❌ Unable to fetch glucose reading.\n"
            "This could be due to:\n"
            "• Using sandbox API (no real data available)\n"
            "• Expired access token (try restarting the bot)\n"
            "• No recent glucose readings available"
        )
    
    await ctx.send(response)

@bot.command(name='commands')
async def show_commands(ctx):
    """Show available bot commands"""
    commands_list = (
        "📋 **Available Commands**\n"
        "`!glucose` - Get your current glucose reading\n"
        "`!commands` - Show this help message"
    )
    await ctx.send(commands_list)

def main():
    """Main function to start the Discord bot"""
    # Get Discord token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("❌ No Discord token found in .env file")
    
    print("🚀 Starting Dexcom Discord Bot...")
    
    # Verify Dexcom authentication
    if not dexcom.authenticate():
        print("⚠️  Warning: Could not authenticate with Dexcom.")
        print("   The bot will still start, but glucose commands may not work.")
        print("   Run 'python authorize_dexcom.py' to set up Dexcom authentication.")
    
    bot.run(token)

if __name__ == '__main__':
    main()