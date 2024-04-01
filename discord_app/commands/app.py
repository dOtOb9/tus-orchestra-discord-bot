import discord

from discord_app.bot import bot
from discord_app.ch.general import ChannelGeneralModal
from discord_app.ch.key import KeyView
from discord_app.ch.send import ChannelSendButton
from discord_app.dm.general import DmGeneralModal
from discord_app.dm.activity import activity_modal
from discord_app.preview import PreviewModal
from discord_app.commands.user import get_user_info

from gas.post import can_send_activity_dm

github_logo_url = "https://raw.githubusercontent.com/dOtOb9/tus-orchestra-discord-bot/main/image/github-mark-white.png"
author_avatar_github_url = "https://avatars.githubusercontent.com/u/124516137?v=4"
author_github_url = "https://github.com/dOtOb9"
repo_url = "https://github.com/dOtOb9/tus-orchestra-discord-bot"
server_execution_log = "https://railway.app/project/149f3467-5a17-4aaf-b362-460be8e9a670/logs"
Railway_logo_url = "https://railway.app/brand/logo-light.png"
qiita_logo_url = "https://github.com/dOtOb9/tus-orchestra-discord-bot/blob/main/image/qiita-icon.png?raw=true"

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
    
@channel.command(description="鍵開閉連絡を送信します。")
async def key(ctx):
    start_embed = discord.Embed(
        title="開始",
    )

    start_embed.set_author(
        name=ctx.user.display_name, 
        icon_url=ctx.user.display_avatar,
        url=ctx.user.jump_url,
    )

    view = KeyView()
    view.disable_all_items()
    view.add_item(ChannelSendButton(view=KeyView(), embed=start_embed))

    await ctx.response.send_message(view=view, embed=start_embed, ephemeral=True)

#-------------------------------------------------------------
    
dm = bot.create_group("dm")


#-------------------------------------------------------------

@dm.command(description="DMで活動連絡を送信します。")
async def activity(
    ctx, 
    year: int, month: int, day: int, start_hour :int = 10, 
    start_minute :int = 0, finish_hour : int = 16, finish_minute : int =  30,
    prepare_minutes : int = 15,
    tutti: discord.Option(str, choices=["Yes", "No"]) = "No",
    send_type: discord.Option(str, choices=["Cc", "Bcc"]) = "Cc",
    ):

    params = {
        "year": year,
        "month": month,
        "day": day,
        "start_hour": start_hour,
        "start_minute": start_minute,
        "finish_hour": finish_hour,
        "finish_minute": finish_minute,
        "prepare_minutes": prepare_minutes,
        "is_tutti": tutti == 'Yes',
        "send_type": send_type,
    }

    await activity_modal(ctx, **params)

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
    
set = bot.create_group("set")

#-------------------------------------------------------------
    
@set.command(description="乗り番連絡DMを受信するかどうかを設定します。")
async def activity_dm(ctx, types: discord.Option(str, choices=["受信する", "受信しない"])):
    Bool = types == "受信する"

    await ctx.respond(f"設定を「{types}」に更新しました。\n\n設定を確認するには、`/status`と送信してください。", ephemeral=True)
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
        title="使い方ガイド",
        colour=discord.Color.from_rgb(255, 102, 255), # ピンク色
        url="https://qiita.com/dOtOb9/private/74f95daf03e3301f67d7"
    )

    embed.set_author(
        name = "dOtOb9",
        icon_url = author_avatar_github_url,
        url = author_github_url,
    )

    embed.set_footer(
        icon_url = qiita_logo_url,
        text = "Qiita",
    )

    await ctx.respond(embed=embed, ephemeral=True)

#-------------------------------------------------------------

dev = bot.create_group("dev")

#-------------------------------------------------------------

@dev.command(description="ソースのGitHubリポジトリを表示します。")
async def repo(ctx):
    embed = discord.Embed(
        title="tus-orchestra-discord-bot",
        description="ソースコードのGitHubリポジトリ",
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
