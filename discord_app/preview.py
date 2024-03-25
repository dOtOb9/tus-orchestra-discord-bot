import discord

#-------------------------------------------------------------
        
class PreviewModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="入力したいテキストを書いてください。", 
            style = discord.InputTextStyle.long)
        )

    async def callback(self, interaction: discord.Interaction):
        text = f"`送信者`:`{interaction.user.display_name}`\n\n{self.children[0].value}"

        await interaction.response.send_message(text, view=PreviewView(text), ephemeral=True)

#-------------------------------------------------------------
        
class PreviewView(discord.ui.View):
    def __init__(self, text, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.text = text

    @discord.ui.button(label="チャンネルに表示する", emoji="📺", style=discord.ButtonStyle.success)
    async def send_callback(self, button, interaction):
        await interaction.channel.send(self.text)

        button.disabled = True
        button.label = "送信済み"
        await interaction.response.edit_message(view=self)
