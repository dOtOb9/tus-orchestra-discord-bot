from discord_app.bot import bot
from gas.post import user_post

from os import getenv


import discord

#================================================================================================
        
@bot.event
async def on_member_update(before, after):
    if after.bot: return
    await member_update(after)

#-----------------------------------------------------------------------------------
            
@bot.event
async def on_ready():
    print("起動しました。")

    for key_channel_id in list(getenv("KEY_CHANNEL_ID").split(",")):
        for channel in bot.guilds[0].channels:
            if channel.id == key_channel_id:
                await channel.send()


#================================================================================================
async def member_update(member):
    div_point = member.display_name.find(".")

    grade = ""
    for role in member.roles:
        if role.name in ["1年", "2年", "3年", "4年"]:
            grade = role.name[0]

    name = ""
    part = ""
    if div_point != -1:
        part = member.display_name[:div_point]
        name = member.display_name[div_point+1:]

    json_data = {
        "mode": "edit_user",
        "name": name,
        "part": part,
        "id": str(member.id),
        "grade": grade,
    }

    await user_post(json_data)
