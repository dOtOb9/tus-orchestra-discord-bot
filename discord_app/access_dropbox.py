import discord

from dropbox_app import verify_access_token

class accessTokenModal(discord.ui.Modal):
    def __init__(self, auth_flow, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_flow = auth_flow
        
        self.add_item(discord.ui.InputText(label="アクセスコード", placeholder="取得したアクセスコードを入力してください。"))

    async def callback(self, interaction):
        auth_code = self.children[0].value

        result = verify_access_token(auth_code, self.auth_flow, interaction.user.id)

        interaction.send_message(result, ephemeral=True)


class verifyAccessTokenButton(discord.ui.View):
    def __init__(self, auth_flow):
        super().__init__()
        self.auth_flow = auth_flow

    @discord.ui.button(label="アクセスコードの入力", emoji="🔑", style=discord.ButtonStyle.primary)
    async def callback(self, button, interaction):
        await interaction.response.send_modal(accessTokenModal(title="アクセストークン入力フォーム", auth_flow=self.auth_flow))