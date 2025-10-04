import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='glucose')
async def get_glucose(ctx):
    # TODO: Implement Dexcom API integration
    await ctx.send("This command will show your current glucose reading (not implemented yet)")

def main():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No Discord token found in .env file")
    bot.run(token)

if __name__ == '__main__':
    main()