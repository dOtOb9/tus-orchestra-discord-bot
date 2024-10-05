import discord
from datetime import datetime

from discord_app.bot import bot
from discord_app.general_embed import generalMessageModal
from discord_app.ch.key import KeyView
from discord_app.ch.send import ChannelSendButton
from discord_app.dm.message import ActivityTime, ActivityTimeSlots, ActivityDetails, DmMessage
from discord_app.dm.activity import ActivityModal
from discord_app.preview import PreviewModal
from discord_app.commands.user import get_user_info
from discord_app.commands.components.options import YearOption, MonthOption, DayOption, HourOption, MinuteOption, SendTypeOption, TrainingOption, SectionOption

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
    await ctx.send_modal(generalMessageModal(title="通常連絡フォーム",mode='ch', colour=discord.Color.from_rgb(r=0, g=255, b=255))) # 水色

#-------------------------------------------------------------
    
@channel.command(description="チャンネルに緊急連絡を送信します。")
async def alert(ctx):
    await ctx.send_modal(generalMessageModal(title="緊急連絡フォーム",mode='ch', colour=discord.Color.from_rgb(r=255, g=0, b=0))) # 赤色

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

    pre_view = KeyView()

    pre_view.disable_all_items()

    pre_view.add_item(ChannelSendButton(send_view=KeyView(), embed=start_embed))

    await ctx.response.send_message(view=pre_view, embed=start_embed, ephemeral=True)

#-------------------------------------------------------------
    
dm = bot.create_group("dm")


#-------------------------------------------------------------

@dm.command(description="DMで活動連絡を送信します。")
async def activity(
    ctx, 
    year: YearOption(add_desc="活動年が"), 
    month: MonthOption(add_desc="活動月が"), 
    day: DayOption(add_desc="活動日が"), 
    first_training: TrainingOption(),
    second_training: TrainingOption(),
    third_training: TrainingOption(),
    forth_training: TrainingOption(),
    section: SectionOption(),
    start_hour : HourOption(add_desc="開始時間が") = 10, 
    start_minute : MinuteOption(add_desc="開始時間が") = 0, 
    finish_hour : HourOption(add_desc="終了時間が") = 16, 
    finish_minute : MinuteOption(add_desc="終了時間が") = 30,
    open_hour : HourOption(add_desc="入室可能時間が") = 9,
    open_minute : MinuteOption(add_desc="入室可能時間が") = 0,
    close_hour : HourOption(add_desc="退出最終時間が") = 18,
    close_minute : MinuteOption(add_desc="退出最終時間が") = 0,
    prepare_minutes : int = 15,
    send_type: SendTypeOption() = "Cc",
    ):

    # Tutti練習の場合、開始時間と終了時間のデフォルト値を変更
    if section == "Tutti" and open_hour == 9 and open_minute == 0 and close_hour == 18 and close_minute == 0:
        open_hour = 7
        close_hour = 21
        prepare_minutes = 30

    try:
        default = datetime(year=year, month=month, day=day)
    except:
        await ctx.respond(f"存在しない日付です。\nyear: {year}\nmonth: {month}\nday: {day}", ephemeral=True)
        return 


    dm_message = DmMessage()

    activity_time = ActivityTime(year=year, month=month, day=day)

    time_slots = ActivityTimeSlots(first=first_training, second=second_training, third=third_training, forth=forth_training)

    dm_message.activity = ActivityDetails(time=activity_time, time_slots=time_slots, section=section)
    dm_message.send_type = send_type

    #------------------------------------------------------------------------------------------------------
    # 活動時間の設定

    dm_message.activity.time.set_start_finish(start=(start_hour, start_minute), finish=(finish_hour, finish_minute))
    dm_message.activity.time.set_open_close(open=(open_hour, open_minute), close=(close_hour, close_minute))
    dm_message.activity.time.set_meeting(prepare_minutes)

    #-----------------------------------------------------------------------------------------------------
    # Tuttiの設定
    if section == 'Tutti':
        dm_message.activity.title = "Tutti"
        dm_message.activity.place = "野田キャンパス多目的トレーニングホール"

    await ctx.send_modal(ActivityModal(dm_message=dm_message))

#-------------------------------------------------------------

@dm.command(description="DMで通常連絡を送信します。")
async def normal(
    ctx, 
    send_type: SendTypeOption() = "Cc"
    ):
    await ctx.send_modal(generalMessageModal(title="通常連絡フォーム", mode='dm', send_type = send_type, colour=discord.Color.from_rgb(r=0, g=255, b=255))) # 水色

#-------------------------------------------------------------
    
@dm.command(description="DMで緊急連絡を送信します。")
async def alert(
    ctx,
    send_type: SendTypeOption() = "Cc"
    ):
    await ctx.send_modal(generalMessageModal(title="緊急連絡フォーム", mode='dm', send_type = send_type, colour=discord.Color.from_rgb(r=255, g=0, b=0))) # 赤色

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
