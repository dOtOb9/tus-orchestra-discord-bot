import discord 

from discord_app.ch.send import ChannelSendButton

#-------------------------------------------------------------

class ChannelTrackModal(discord.ui.Modal):
    def __init__(self, time, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time = time

        self.add_item(discord.ui.InputText(label="出発地"))
        self.add_item(discord.ui.InputText(label="到着地"))

    async def callback(self, interaction):
        depareture_location = self.children[0].value
        arrival_location = self.children[1].value

        embed = discord.Embed(
            title = depareture_location + "▶︎" + arrival_location + " 積み込みフォーム",
            description = self.time,
            colour = discord.Colour.from_rgb(r=0, g=255, b=255)
        )

        embed.set_author(
            name = interaction.user.display_name,
            icon_url = interaction.user.display_avatar, 
            url = interaction.user.jump_url
        )

        await interaction.response.send_message(view=ChannelSendButton(embed=embed), ephemeral=True, embed=embed)