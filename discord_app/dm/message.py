from os import getenv
from urllib.parse import quote

from datetime import datetime, timedelta
import discord

from discord_app.status import UserStatusButton
from discord_app.dm.ui import viewSendListButton

#====================================================================================================

class ActivityTime():
    def __init__(self, year : int, month : int, day : int):
        default = datetime(year=year, month=month, day=day)

        self.start = default
        self.finish = default
        self.open = default
        self.close = default
        self.meeting = default

    def set_start_finish(self, start : tuple, finish : tuple):
        self.start = self.start.replace(hour=start[0], minute=start[1])

        self.finish = self.finish.replace(hour=finish[0], minute=finish[1])


    def set_open_close(self, open : tuple, close : tuple):
        self.open = self.open.replace(hour=open[0], minute=open[1])

        self.close = self.close.replace(hour=close[0], minute=close[1])


    def set_meeting(self, minutes : int):
        self.meeting = self.start - timedelta(minutes=minutes)

#=====================================================================================================

class ActivityTimeSlots():
    def __init__(self, first: str, second: str, third: str, forth: str):

        for slot in [first, second, third, forth]:
            if slot == "無し":
                slot = ""

        self.first = first
        self.second = second
        self.third = third
        self.forth = forth


#=====================================================================================================

class ActivityDetails():
    def __init__(self, time: ActivityTime, time_slots: ActivityTimeSlots, section: str):
        self.time = time
        self.time_slots = time_slots
        self.section = section
        self.place: str = None
        self.title: str = None
        self.description: str = None
        self.date_text: str = None


    def set_activity_embed(self, user: discord.User) -> discord.Embed:
        main_embed = discord.Embed(
            title=self.title,
            url=getenv("SCHEDULE_FILE_URL"),
            colour = discord.Color.from_rgb(0, 255, 0),
            fields = [
                discord.EmbedField(
                    name = "📆日付",
                    value = self.time.start.strftime("%Y/%m/%d (%a)"),
                    inline = True
                ),
                discord.EmbedField(
                    name = "🕙時間",
                    value = f"{self.time.start.strftime('%H:%M')}~{self.time.finish.strftime('%H:%M')}\n**{self.time.meeting.strftime('%H:%M')}**集合",
                    inline = True
                ),
                discord.EmbedField(
                    name = "🏢会場",
                    value = f"[{self.place}](https://www.google.co.jp/maps/search/{self.place})",
                    inline = False
                ),
                discord.EmbedField(
                    name = "🔓利用可能時間",
                    value = f"**{self.time.open.strftime('%H:%M')}~{self.time.close.strftime('%H:%M')}**", 
                    inline = True
                ),
                discord.EmbedField(
                    name = "📝詳細",
                    value = self.description,
                    inline = False
                ),
            ],
            )
        
        return main_embed.set_author(
            name = user.display_name, 
            icon_url = user.display_avatar,
            url = user.jump_url,
            )
    

    def set_google_map_embed(self) -> discord.Embed:
        google_map_embed = discord.Embed(
            title = "現在地からの経路を検索",
            url = f"https://www.google.com/maps/dir/?api=1&destination={self.place}",
            colour = discord.Color.dark_green()
        )

        return google_map_embed.set_footer(
            text = "Google Map",
            icon_url = getenv("GOOGLE_MAP_ICON_URL"),
        )
    
    
    def set_google_calendar_embed(self) -> discord.Embed:
        details_text = f"{self.time.open.strftime('%H:%M')}~{self.time.close.strftime('%H:%M')}\n\n{self.description}"
        google_calendar_embed = discord.Embed(
            title = "カレンダーに追加",
            url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&dates={self.time.meeting.strftime('%Y%m%dT%H%M%S')}/{self.time.finish.strftime('%Y%m%dT%H%M%S')}&text={quote(self.title)}&location={quote(self.place)}&details=🔓利用可能時間\n{quote(details_text)}",
            colour = discord.Color.dark_blue()
        )

        return google_calendar_embed.set_footer(
            text = "Google Calendar", 
            icon_url=getenv("GOOGLE_CALENDAR_ICON_URL"), 
            
        )
    
    def set_verify_attendance_embed(self, id) -> discord.Embed:
        verify_attendance_embed = discord.Embed(
            title = "出席認証",
            url = getenv("VERIFY_ATTENDANCE_URL") + "&id=" + str(id),
            colour = discord.Color.from_rgb(153, 0, 153), # 紫色
        )

        return verify_attendance_embed.set_footer(
            text = "出欠表",
            icon_url = getenv("SPREADSHEET_ICON_URL"),
        )
    

    def set_all_embeds(self, user: discord.User)-> list:
        activity_embed = self.set_activity_embed(user=user)
        google_map_embed = self.set_google_map_embed()
        google_calendar_embed = self.set_google_calendar_embed()
        verify_attendance_embed = self.set_verify_attendance_embed(user.id)
        
        return [activity_embed, google_map_embed, google_calendar_embed, verify_attendance_embed]
    
#=====================================================================================================
    

class DmMessage():
    def __init__(self):
        self.view = discord.ui.View(disable_on_timeout=True, timeout=60 * 60 * 24 * 30) # 30日間
        self.view_editted = False
        self.activity: ActivityDetails = None
        self.send_type: str = None
        self.send_list: list= None
        self.embeds: list = None
        self.send_list_embed: discord.Embed = None


    def generate_send_list_embed(self):
        name_list = [member.display_name for member in self.send_list]
        name_list = sorted(name_list)

        name_list_text = ','.join([f"`{name}`" for name in name_list])

        self.send_list_embed = discord.Embed(
            title=f"送信先リスト（{len(name_list)}）",
            description=name_list_text,
        )

        if self.send_type == "Bcc":
            self.send_list_embed.title += " (非公開）"


        return self.send_list_embed
    

    def set_view(self, user: discord.User):
        view = discord.ui.View(disable_on_timeout=True, timeout=60 * 60 * 24 * 30) # 30日間

        view.add_item(viewSendListButton(send_list_embed=self.send_list_embed, row=0, disabled = self.send_type == "Bcc"))
        
        if self.activity != None:
            view.add_item(UserStatusButton(row=1, user_id=user.id, date_text=self.activity.time.start.strftime("%Y%m%d")))

        return view