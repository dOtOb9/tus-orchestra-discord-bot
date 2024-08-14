from os import getenv

import discord


class UserStatusButton(discord.ui.Button):
    def __init__(self, date_text: str = "", disabled: bool = False, row: int = None) -> None:
        redirect_url = getenv("SPREADSHEET_EXEC_URL") + "?mode=dashboard" + "&date=" + date_text

        super().__init__(label="出席状況", style=discord.ButtonStyle.gray, row=row, disabled=disabled, url=redirect_url)