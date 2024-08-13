import discord
from datetime import datetime
from os import getenv

from discord_app.bot import bot
from discord_app.delete import deleteMessageView
from discord_app.status import UserStatusButton
from gas.get import user_info
        
        

@bot.user_command(name="ユーザー情報を取得する")
async def get_user_info(ctx, member: discord.Member):
    if member.bot: 
        await ctx.respond("ボットの情報は取得できません。", ephemeral=True)
        return

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
            "practice_contact": -> 活動連絡を受信できるかどうか。True なら権限有り、False なら権限無し
            "attend_status":    -> 出席率。0~1の小数で表されます。
        }
        """

        if result_json["practice_contact"]:
            practice_contact = "受信する"
        else:
            practice_contact = "受信しない"

        view_attend_code = "閲覧不可"

        for channel in bot.guilds[0].channels:
            if str(channel.id) == getenv("VIEW_ATTEND_CODE_CHANNEL_ID"):
                for Member in channel.members:
                    if member.id == Member.id:
                        view_attend_code = "閲覧可能"
                        break

        embed = discord.Embed(
            title=f"{member.display_name}の情報",
            url=getenv("SPREADSHEET_URL"),
            fields=[
                discord.EmbedField(name="📺出席コード閲覧", value=view_attend_code, inline=True),
                discord.EmbedField(name="📧乗り番連絡", value=practice_contact, inline=True),
                discord.EmbedField(name="📈通常練習", value=result_json['attend_status'], inline=False),
                discord.EmbedField(name="📈Tutti練習", value=result_json['tutti_attend_status'], inline=False),
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

    view=deleteMessageView()
    view.add_item(UserStatusButton())   

    await author.send(embed=embed, view=view)