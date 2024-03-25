import discord
from os import getenv

from gas.post import user_post

#================================================================================================

class AttendAuthButton(discord.ui.Button):
    def __init__(self, label="出席認証", style=discord.ButtonStyle.primary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.style = style

    async def callback(self, interaction):
        await interaction.response.send_modal(AttendAuthModal(title="出席登録フォーム"))

#================================================================================================

class AttendAuthModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="認証コード", placeholder="半角数字4桁で入力してください。", min_length=4, max_length=4))

    async def callback(self, interaction):
        json_data = {
            "mode": "auth_attend",
            "id": str(interaction.user.id),
            "code": self.children[0].value,
        }

        await interaction.response.send_message("認証中...", ephemeral=True)

        author = interaction.user

        result_text = await user_post(json_data)

        embed = discord.Embed(
                    title = "認証結果",
                    description = result_text,
                    url=getenv("SPREADSHEET_URL"),
                    colour = discord.Color.orange()
                )

        embed.set_author(
            name = "出欠表",
            icon_url = getenv("SPREADSHEET_ICON_URL"),
            url = getenv("SPREADSHEET_URL"),
        )

        embed.set_footer(
            text = "Apps Script",
            icon_url = getenv("APPS_SCRIPT_ICON_URL"),
        )

        await author.send(embed=embed)
