import discord

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)