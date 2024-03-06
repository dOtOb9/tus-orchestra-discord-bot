import discord

#-------------------------------------------------------------

class ChannelSendButton(discord.ui.View):
    def __init__(self, embed, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embed = embed

    @discord.ui.button(label="チャンネルに表示する", emoji="📺", style=discord.ButtonStyle.success)
    async def send_callback(self, button, interaction):
        await interaction.channel.send(embed=self.embed)

        button.disabled = True
        button.label = "表示済み"
        await interaction.response.edit_message(view=self)