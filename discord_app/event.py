import discord
from os import getenv
import asyncio
import datetime as dt

from discord_app.bot import bot
from gas.post import user_post
from gas.get import can_send_attend_code

#================================================================================================
        
@bot.event
async def on_member_update(before, after):
    await member_update(after)

#-----------------------------------------------------------------------------------

@bot.event
async def on_member_join(member):
    await member_update(member)

#-----------------------------------------------------------------------------------
            
@bot.event
async def on_ready():
    print("再起動しました。")

    while True:
        now = dt.datetime.now()

        if (now.hour == 5):
            await send_attend_code()
            await asyncio.sleep(60 * 60) # 1時間

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


#================================================================================================
    
async def send_attend_code():
    json_data = await can_send_attend_code()
    if json_data['exist_date'] == 'FALSE': return

    embed = discord.Embed(
        title=json_data['code'],
        description=json_data['date_text'] + "の出席認証コード",
        color=discord.Color.orange(),
    )
    embed.set_author(
        name="出欠表",
        icon_url=getenv("SPREADSHEET_ICON_URL"),
        url=getenv("SPREADSHEET_URL"),  
    )
    embed.set_footer(
        text="Apps Script",
        icon_url=getenv("APPS_SCRIPT_ICON_URL"),
    )

    for member in bot.guilds[0].members:
        if member.bot:
            continue

        if str(member.id) in list(json_data['member_list']):
            await member.send(embed=embed)
