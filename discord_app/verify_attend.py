import discord

from gas.post import user_post

#================================================================================================

class AttendAuthButton(discord.ui.Button):
    def __init__(self, label="出席認証", style=discord.ButtonStyle.primary, disabled=False, row=None):
        super().__init__(label=label, style=style, disabled=disabled, row=row)

    async def callback(self, interaction):
        await interaction.response.send_modal(AttendAuthModal())

#================================================================================================

class AttendAuthModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="出席登録フォーム")

        self.add_item(discord.ui.InputText(label="認証コード", placeholder="半角数字4桁で入力してください。", min_length=4, max_length=4))

    async def callback(self, interaction):
        
        json_data = {
            "mode": "auth_attend",
            "id": str(interaction.user.id),
            "code": self.children[0].value,
        }

        await interaction.response.send_message("認証コードを送信しました。", ephemeral=True)
        await user_post(json_data)