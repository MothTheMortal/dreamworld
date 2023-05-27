import discord
from mainclient import DreamBot
from dotenv import load_dotenv
from os import getenv


if __name__ == "__main__":

    load_dotenv()

    client = DreamBot(command_prefix="?", intents=discord.Intents.all(), case_insensitive=True, help_command=None,
                      mongodb_uri=getenv("MONGODB_URI"))
    client.run(getenv("BOT_TOKEN"))
