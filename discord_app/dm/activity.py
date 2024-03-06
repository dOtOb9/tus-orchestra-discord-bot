import discord
import datetime as dt

from discord_app.dm.select_user import SelectUsersButtons

#-------------------------------------------------------------

class DmActivityModal(discord.ui.Modal):
    def __init__(self, start_dt, finish_dt, prepare_minutes, send_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.send_type = send_type

        meeting_dt = start_dt - dt.timedelta(minutes=prepare_minutes)

        self.actibity_date_text = f"{start_dt.year:04}/{start_dt.month:02}/{start_dt.day:02} ({start_dt.strftime('%a')})"
        self.actibity_time_text = f"{start_dt.hour}:{start_dt.minute:02} ~ {finish_dt.hour}:{finish_dt.minute:02}"
        self.meeting_time_text = f"**{meeting_dt.hour}:{meeting_dt.minute:02} 集合**"

    
        self.add_item(discord.ui.InputText(label="タイトル", placeholder="練習内容を入力"))
        self.add_item(discord.ui.InputText(label="会場", placeholder="GoogleMapで検索できるワードを推奨"))
        self.add_item(discord.ui.InputText(label="備考", style = discord.InputTextStyle.long, required=False))


    async def callback(self, interaction: discord.Interaction):
        title = self.children[0].value
        place = self.children[1].value
        content = self.children[2].value

        embed = discord.Embed(
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
                    name = "📝備考",
                    value = content,
                    inline = False
                ),
            ],
            )
        
        embed.set_author(
            name = interaction.user.display_name, 
            icon_url = interaction.user.display_avatar,
            url = interaction.user.jump_url,
            )
        
        await interaction.response.send_message(
            "送信先を選んでください。",
            view=SelectUsersButtons(embed=embed, send_type=self.send_type),
            ephemeral=True,
            embed=embed
            )
        
#-------------------------------------------------------------
    
def judge_time_can_converted(year, month, day, hour, minute) -> bool:
    try:
        judge_dt = dt.datetime(year=year, month=month, day=day, hour = hour, minute = minute)
        return True
    except:
        return False
    
#-------------------------------------------------------------
    
async def activity_modal(ctx, year, month, day, start_hour, start_minute, finish_hour, finish_minute, prepare_minutes, send_type):

    start_time_can_converted = judge_time_can_converted(year, month, day, start_hour, start_minute)
    finish_time_can_converted = judge_time_can_converted(year, month, day, finish_hour, finish_minute)

    if not (start_time_can_converted and finish_time_can_converted): 
        await ctx.respond("時間に変換できませんでした。", ephemeral=True)
        return
    
    start_dt = dt.datetime(year=year, month=month, day=day, hour=start_hour, minute=start_minute)
    finish_dt = dt.datetime(year=year, month=month, day=day, hour=finish_hour, minute=finish_minute)
    
    contact_modal = DmActivityModal(title="活動連絡フォーム", 
                                    start_dt=start_dt, finish_dt=finish_dt, 
                                    prepare_minutes=prepare_minutes,
                                    send_type=send_type
                                )

    await ctx.send_modal(contact_modal)