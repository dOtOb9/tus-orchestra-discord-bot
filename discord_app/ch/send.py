import discord

#-------------------------------------------------------------

class ChannelSendButton(discord.ui.Button):
    def __init__(self, view=None, text=None, embed=None, files=None):
        super().__init__(label="チャンネルに表示する", emoji="📺", style=discord.ButtonStyle.success, row=4)
        self.text = text
        self.embed = embed
        self.files = files
        self.send_view = view

    async def callback(self, interaction):
        await interaction.channel.send(self.text, view=self.send_view, embed=self.embed, files=self.files)

        self.disabled = True
        self.label = "表示済み"
        await interaction.response.edit_message(view=self.send_view)