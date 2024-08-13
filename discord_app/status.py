import discord


class UserStatusButton(discord.ui.Button):
    def __init__(self, disabled: bool = False, row: int = None) -> None:
        super().__init__(label="出席状況", style=discord.ButtonStyle.gray, row=row, disabled=disabled, url="https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.Button.url")