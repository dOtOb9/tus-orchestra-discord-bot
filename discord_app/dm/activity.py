from os import getenv
from urllib.parse import quote

import discord
import datetime as dt

from discord_app.dm.select_user import SelectUsersView
from discord_app.dm.send import verify_gas_send_dm

#-------------------------------------------------------------

class DmActivityModal(discord.ui.Modal):
    def __init__(self, **kwargs) -> None:
        super().__init__(title="活動連絡フォーム")
        self.kwargs = kwargs

        meeting_dt = kwargs['start_dt'] - dt.timedelta(minutes=kwargs['prepare_minutes'])

        self.actibity_date_text = f"{kwargs['year']:04}/{kwargs['month']:02}/{kwargs['day']:02} ({kwargs['start_dt'].strftime('%a')})"
        self.actibity_time_text = f"{kwargs['start_hour']}:{kwargs['start_minute']:02} ~ {kwargs['finish_hour']}:{kwargs['finish_minute']:02}"
        self.meeting_time_text = f"**{meeting_dt.hour}:{meeting_dt.minute:02} 集合**"

        self.google_calendar_plan_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&dates={kwargs['start_dt'].strftime('%Y%m%dT%H%M%S')}/{kwargs['finish_dt'].strftime('%Y%m%dT%H%M%S')}"

        #----------------------------------------------------------------

        title_input = discord.ui.InputText(label="タイトル", placeholder="練習内容を入力")
        if kwargs['is_tutti']:
            title_input.value = "Tutti"
        #----------------------------------------------------------------

        self.add_item(title_input)
        self.add_item(discord.ui.InputText(label="会場", placeholder="GoogleMapで検索できるワードを推奨"))
        self.add_item(discord.ui.InputText(label="備考", value="- 部屋\n\n\n- 練習内容\n１コマ目：\n２コマ目：\n３コマ目：\n４コマ目：", style = discord.InputTextStyle.long, required=False))


    async def callback(self, interaction: discord.Interaction):
        title = self.children[0].value
        place = self.children[1].value
        content = self.children[2].value

        main_embed = discord.Embed(
            title=title,
            colour = discord.Color.from_rgb(0, 255, 0),
            fields = [
                discord.EmbedField(
                    name = "📆日付",
                    value = self.actibity_date_text,
                    inline = True
                ),
                discord.EmbedField(
                    name = "🕙時間",
                    value = self.actibity_time_text + "\n" + self.meeting_time_text,
                    inline = True
                ),
                discord.EmbedField(
                    name = "🏢会場",
                    value = f"[{place}](https://www.google.co.jp/maps/search/{place})",
                    inline = False
                ),
                discord.EmbedField(
                    name = "📝詳細",
                    value = content,
                    inline = False
                ),
            ],
            )
        
        main_embed.set_author(
            name = interaction.user.display_name, 
            icon_url = interaction.user.display_avatar,
            url = interaction.user.jump_url,
            )
        
        #------------------------------------------------------------------

        google_map_embed = discord.Embed(
            title = "現在地からの経路を検索",
            url = f"https://www.google.com/maps/dir/?api=1&destination={quote(place)}",
            colour = discord.Color.dark_green()
        )

        google_map_embed.set_footer(
            text = "Google Map",
            icon_url = getenv("GOOGLE_MAP_ICON_URL"),
        )

        #--------------------------------------------------------------------

        google_calendar_embed = discord.Embed(
            title = "カレンダーに追加",
            url = self.google_calendar_plan_url + f"&text={quote(title)}&location={quote(place)}&details={quote(content)}",
            colour = discord.Color.dark_blue()
        )

        google_calendar_embed.set_footer(
            text = "Google Calendar", 
            icon_url=getenv("GOOGLE_CALENDAR_ICON_URL"), 
        )

        #---------------------------------------------------------------------

        embeds = [main_embed, google_map_embed, google_calendar_embed]

        if self.kwargs['is_tutti']:
            await verify_gas_send_dm(mode='strings', interaction=interaction, **self.kwargs)
        else:
            await interaction.response.send_message(
                "送信先を選んでください。",
                view=SelectUsersView(embeds=embeds, **self.kwargs),
                ephemeral=True,
                embeds=embeds,
                )
    
#-------------------------------------------------------------
    
async def activity_modal(ctx, **kwargs):
    try:
        start_dt = dt.datetime(year=kwargs['year'], month=kwargs['month'], day=kwargs['day'], hour=kwargs['start_hour'], minute=kwargs['start_minute'])
        finish_dt = dt.datetime(year=kwargs['year'], month=kwargs['month'], day=kwargs['day'], hour=kwargs['finish_hour'], minute=kwargs['finish_minute'])
    except:
        await ctx.respond("時間に変換できませんでした。", ephemeral=True)
        return
    
    contact_modal = DmActivityModal(start_dt=start_dt, finish_dt=finish_dt, **kwargs)

    await ctx.send_modal(contact_modal)