from discord_app.bot import bot
from gas.post import user_post

#================================================================================================
        
@bot.event
async def on_member_update(before, after):
    if after.bot: return
    await member_update(after)

#-----------------------------------------------------------------------------------
            
@bot.event
async def on_ready():
    print("再起動しました。")


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