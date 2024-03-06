from os import getenv

from discord_app.bot import bot
from discord_app.commands import app,  user, message
import discord_app.event


@bot.event
async def on_ready():
    print("再起動しました。")


bot.run(getenv("DISCORD_TOKEN"))
