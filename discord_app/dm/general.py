import discord

from discord_app.dm.select_user import SelectSendView

#-------------------------------------------------------------

class DmGeneralModal(discord.ui.Modal):
    def __init__(self, **kwargs):
        super().__init__(title=kwargs['title'])
        self.kwargs=kwargs

        self.add_item(discord.ui.InputText(label="タイトル"))
        self.add_item(discord.ui.InputText(label="URL", placeholder="有効なURLを指定してください。", required=False))
        self.add_item(discord.ui.InputText(label="内容", style = discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = self.children[0].value,
            url = self.children[1].value,
            description=self.children[2].value,
            colour=discord.Color.from_rgb(r=self.kwargs['colour'][0], g=self.kwargs['colour'][1], b=self.kwargs['colour'][2])
        )

        embed.set_author(
            name = interaction.user.display_name,
            icon_url = interaction.user.display_avatar, 
            url = interaction.user.jump_url
        )

        try:
            await interaction.response.send_message(
                "送信先を選んでください。",
                view=SelectSendView(embeds=[embed], **self.kwargs),
                ephemeral=True,
                embeds=[embed]
            )
        except:
            await interaction.response.send_message("有効なURLを指定してください。", ephemeral=True)
