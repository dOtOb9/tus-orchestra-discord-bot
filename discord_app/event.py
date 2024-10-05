from discord_app.bot import bot
from gas.post import user_post

import discord

#================================================================================================

            
@bot.event
async def on_ready():
    print("起動しました。")


#================================================================================================
@bot.event
async def member_update(before, after):
    if after.bot: return

    div_point = after.display_name.find(".")

    grade = ""
    for role in after.roles:
        if role.name in ["1年", "2年", "3年", "4年"]:
            grade = role.name[0]

    name = ""
    part = ""
    if div_point != -1:
        part = after.display_name[:div_point]
        name = after.display_name[div_point+1:]

    json_data = {
        "mode": "edit_user",
        "name": name,
        "part": part,
        "id": str(after.id),
        "grade": grade,
    }

    await user_post(json_data)


#================================================================================================
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot: return
    
    if message.channel.type == 'private': return  # DM以外のチャンネルでのメッセージは無視


    if message.attachments != []:
        for attachment in message.attachments:
            await message.author.send(f"ファイルを受け取りました。\nファイル名: {attachment.filename}\nファイルサイズ: {attachment.size}byte\nファイルURL: {attachment.url}")
