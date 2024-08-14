from os import getenv

from discord_app.bot import bot
from discord_app.commands import app, user, message
import discord_app.event


bot.run(getenv("DISCORD_TOKEN"))