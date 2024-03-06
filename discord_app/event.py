from discord_app.bot import bot
from gas.post import user_post

#================================================================================================
        
@bot.event
async def on_member_update(before, after):
    await member_update(after)

@bot.event
async def on_member_join(member):
    await member_update(member)

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

@bot.event
async def on_ready():
    for member in bot.guilds[0].members:
        match member.id:
            case 965544842576949248:
                member.nick = 'Vn.林 颯太朗'
                break
            case 943171796755181621:
                member.nick = 'Va.成田真衣'
                break
            case 855780754360238132:
                member.nick = 'Vn.星野 真輝'