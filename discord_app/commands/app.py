import discord

from discord_app.bot import bot
from discord_app.ch.general import ChannelGeneralModal
from discord_app.ch.dbx import FileRequestModal
from discord_app.dm.general import DmGeneralModal
from discord_app.dm.activity import activity_modal
from discord_app.preview import PreviewModal
from discord_app.commands.user import get_user_info

from gas.post import can_send_activity_dm


#-------------------------------------------------------------

channel = bot.create_group("ch")

#-------------------------------------------------------------

@channel.command(description="チャンネルに通常連絡を送信します。")
async def normal(ctx):
    await ctx.send_modal(ChannelGeneralModal(title="通常連絡フォーム", colour=(0, 255, 255))) # 水色

#-------------------------------------------------------------
    
@channel.command(description="チャンネルに緊急連絡を送信します。")
async def alert(ctx):
    await ctx.send_modal(ChannelGeneralModal(title="緊急連絡フォーム", colour=(255, 0, 0))) # 赤色

#-------------------------------------------------------------
    
@channel.command(description="チャンネルにファイルを共有します。")
async def upload_file(ctx):
    await ctx.send_modal(FileRequestModal(title="ファイル共有フォーム"))

#-------------------------------------------------------------
    
dm = bot.create_group("dm")


#-------------------------------------------------------------

@dm.command(description="DMで活動連絡を送信します。")
async def activity(
    ctx, 
    year: int, month: int, day: int, start_hour :int = 10, 
    start_minute :int = 0, finish_hour : int = 16, finish_minute : int =  30,
    prepare_minutes : int = 15,
    send_type: discord.Option(str, choices=["Cc", "Bcc"]) = "Cc",
    ):
    await activity_modal(ctx, year, month, day, start_hour, start_minute, finish_hour, finish_minute, prepare_minutes, send_type)

#-------------------------------------------------------------

@dm.command(description="DMで通常連絡を送信します。")
async def normal(
    ctx, 
    send_type: discord.Option(str, choices=["Cc", "Bcc"]) = "Cc"
    ):
    await ctx.send_modal(DmGeneralModal(title="通常連絡フォーム", send_type = send_type, colour=(0, 255, 255))) # 水色

#-------------------------------------------------------------
    
@dm.command(description="DMで緊急連絡を送信します。")
async def alert(
    ctx,
    send_type: discord.Option(str, choices=["Cc", "Bcc"]) = "Cc"
    ):
    await ctx.send_modal(DmGeneralModal(title="緊急連絡フォーム", send_type = send_type, colour=(255, 0, 0))) # 赤色

#-------------------------------------------------------------
    
github_logo_url = "https://raw.githubusercontent.com/dOtOb9/tus-orchestra-discord-bot/main/image/github-mark-white.png"
author_avatar_github_url = "https://avatars.githubusercontent.com/u/124516137?v=4"
author_github_url = "https://github.com/dOtOb9"
repo_url = "https://github.com/dOtOb9/tus-orchestra-discord-bot"
server_execution_log = "https://railway.app/project/149f3467-5a17-4aaf-b362-460be8e9a670/logs"
Railway_logo_url = "https://railway.app/brand/logo-light.png"

#-------------------------------------------------------------
    
dev = bot.create_group("dev")

#-------------------------------------------------------------

@dev.command(description="ソースのGitHubリポジトリを表示します。")
async def repo(ctx):
    embed = discord.Embed(
        title="tus-orchestra-discord-bot",
        description="ソースのGitHubリポジトリ",
        colour=discord.Color.from_rgb(127, 0, 255), # 紫色
        url=repo_url,
    )

    embed.set_author(
        name = "dOtOb9",
        icon_url = author_avatar_github_url,
        url = author_github_url,
    )

    embed.set_footer(
        icon_url = github_logo_url,
        text = "GitHub",
    )

    await ctx.respond(embed=embed, ephemeral=True)

#-------------------------------------------------------------

@dev.command(description="サーバーの実行ログを表示します。")
async def server(ctx):
    embed = discord.Embed(
    title="サーバーの実行ログ",
        description="ホスティングサーバーの実行ログ",
        url=server_execution_log,
        colour=discord.Color.from_rgb(127, 0, 255), # 紫色
    )
    embed.set_author(
        name = "dOtOb9",
        icon_url = author_avatar_github_url,
        url = author_github_url,
    )
    embed.set_footer(
        icon_url = Railway_logo_url,
        text = "Railway",
    )
    await ctx.respond(embed=embed, ephemeral=True)

#-------------------------------------------------------------
    
set = bot.create_group("set")

#-------------------------------------------------------------
    
@set.command(description="乗り番連絡DMを受信するかどうかを設定します。")
async def activity_dm(ctx, types: discord.Option(str, choices=["受信する", "受信しない"])):
    Bool = types == "受信する"

    await ctx.respond("設定を更新しました。\n\n設定を確認するには、`/set get_me_info`を実行してください。", ephemeral=True)
    await can_send_activity_dm(ctx.user.id, Bool)

#-------------------------------------------------------------

@bot.slash_command(description="自身の設定を表示します。")
async def status(ctx):
    await get_user_info(ctx, ctx.user)

#-------------------------------------------------------------

@bot.slash_command(description="入力したいテキストをプレビューできます。")
async def preview(ctx):
    await ctx.send_modal(PreviewModal(title="テキスト表示のプレビュー"))

#-------------------------------------------------------------
    
@bot.slash_command(description="使い方ガイドを表示します。")
async def guide(ctx):
    embed = discord.Embed(
        title="使い方ガイド(README.md)",
        colour=discord.Color.from_rgb(255, 102, 255), # ピンク色
        url="https://github.com/dOtOb9/tus-orchestra-discord-bot/blob/main/README.md"
    )

    embed.set_author(
        name = "dOtOb9",
        icon_url = author_avatar_github_url,
        url = author_github_url,
    )

    embed.set_footer(
        icon_url = github_logo_url,
        text = "GitHub",
    )

    await ctx.respond(embed=embed, ephemeral=True)
