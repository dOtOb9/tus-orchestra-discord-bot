import discord

from discord_app.dm.select_user import SelectUsersButtons

#-------------------------------------------------------------

class DmGeneralModal(discord.ui.Modal):
    def __init__(self, colour, send_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.colour = colour
        self.send_type = send_type

        self.add_item(discord.ui.InputText(label="タイトル"))
        self.add_item(discord.ui.InputText(label="内容", style = discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = self.children[0].value,
            description=self.children[1].value,
            colour=discord.Color.from_rgb(r=self.colour[0], g=self.colour[1], b=self.colour[2])
        )

        embed.set_author(
            name = interaction.user.display_name,
            icon_url = interaction.user.display_avatar, 
            url = interaction.user.jump_url
        )

        await interaction.response.send_message(
            "送信先を選んでください。",
            view=SelectUsersButtons(embeds=[embed], send_type=self.send_type),
            ephemeral=True,
            embeds=[embed]
        )
