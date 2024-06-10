import discord

from discord_app.dm.message import DmMessage
from discord_app.dm.select_user import SelectSendView
from discord_app.ch.send import ChannelSendButton

#-------------------------------------------------------------

class generalMessageModal(discord.ui.Modal):
    def __init__(self, **kwargs):
        super().__init__(title=kwargs['title'])
        self.kwargs=kwargs

        self.add_item(discord.ui.InputText(label="タイトル"))
        self.add_item(discord.ui.InputText(label="URL", placeholder="有効なURLを指定してください。", required=False))
        self.add_item(discord.ui.InputText(label="内容", style = discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="画像URL", placeholder="有効なURLを指定してください。", required=False))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = self.children[0].value,
            url = self.children[1].value,
            description=self.children[2].value,
            colour=self.kwargs['colour']
        )

        embed.set_image(url=self.children[3].value)

        embed.set_author(
            name = interaction.user.display_name,
            icon_url = interaction.user.display_avatar, 
            url = interaction.user.jump_url
        )

        try:
            if self.kwargs['mode'] == 'dm':
                dm_message = DmMessage()

                dm_message.embeds = [embed]
                dm_message.send_type = self.kwargs['send_type']

                await interaction.response.send_message(
                    "送信先を選んでください。",
                    view=SelectSendView(dm_message=dm_message),
                    ephemeral=True,
                    embeds=dm_message.embeds,
                )
            else:
                await interaction.response.send_message(view=discord.ui.View(ChannelSendButton(embed=embed)), ephemeral=True, embed=embed)
        except discord.errors.HTTPException:
            await interaction.response.send_message("有効なURLを指定してください。", ephemeral=True)
