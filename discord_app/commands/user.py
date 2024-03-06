import discord
from datetime import datetime
from os import getenv

from discord_app.bot import bot
from gas.get import user_info
        
@bot.user_command(name="ユーザー情報を取得する")
async def get_user_info(ctx, member: discord.Member):
    if member.bot: await ctx.respond("ボットの情報は取得できません。", ephemeral=True)

    author = ctx.author
    await ctx.respond(f"ユーザー情報を取得中... {member.display_name}", ephemeral=True)
    result_json = await user_info(member.id)

    if type(result_json) == str:
        embed = discord.Embed(
            title=result_json,
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
    else:
        """
        result_json には、以下のような情報が格納されています。
        {
            "view_attend_code": -> 出席コードを閲覧できるかどうか。True なら権限有り、False なら権限無し
            "practice_contact": -> 活動連絡を受信できるかどうか。True なら権限有り、False なら権限無し
            "attend_status":    -> 出席率。0~1の小数で表されます。
        }
        """

        if result_json["view_attend_code"]:
            view_attend_code = "権限有り"
        else:
            view_attend_code = "権限無し"

        if result_json["practice_contact"]:
            practice_contact = "権限有り"
        else:
            practice_contact = "権限無し"


        embed = discord.Embed(
            title=f"{member.display_name}の情報",
            fields=[
                discord.EmbedField(name="出席率", value=f"{int(result_json['attend_status'] * 100)}%", inline=True),
                discord.EmbedField(name="出席コード閲覧", value=view_attend_code, inline=True),
                discord.EmbedField(name="活動連絡受信", value=practice_contact, inline=True),
            ],
            color=discord.Color.orange(),
            timestamp=datetime.now()
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

    await author.send(embed=embed)