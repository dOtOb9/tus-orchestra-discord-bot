import discord

from discord_app.ui import deleteMessageView

class SelectChannelButtons(discord.ui.View):
    def __init__(self, embeds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embeds = embeds

    @discord.ui.button(label="自分のDMチャンネルに送信する", emoji="📧", style=discord.ButtonStyle.success)
    async def send_me_dm(self, button, interaction):
        button.disabled = True
        button.label = "自分のDMチャンネルに送信済み"
        await interaction.response.edit_message(view=self)

        await interaction.user.send(embeds=self.embeds, view=deleteMessageView())

    @discord.ui.button(label="チャンネルに送信する", emoji="📺", style=discord.ButtonStyle.primary)
    async def select_channel(self, button, interaction):
        await interaction.response.send_message(view=SelectChannelsMenu(embeds=self.embeds), ephemeral=True)

class SelectChannelsMenu(discord.ui.View):
    def __init__(self, embeds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.embeds = embeds

    @discord.ui.channel_select(placeholder="チャンネルを選択", min_values=1, max_values=25)
    async def callback(self, select, interaction):
        channels = select.values
        for channel in channels.copy():
            if channel.type != discord.ChannelType.text:
                channels.remove(channel)

        if len(channels):
            await interaction.response.send_message(f"送信するチャンネル\n{', '.join([channel.mention for channel in channels])}", 
                                                view=SendChannelsButton(channels=channels, embeds=self.embeds), ephemeral=True)
        else:
            await interaction.response.send_message("テキストチャンネルを選択してください。", ephemeral=True)


class SendChannelsButton(discord.ui.View):
    def __init__(self, channels, embeds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = channels
        self.embeds = embeds

    @discord.ui.button(label="送信", emoji="📧", style=discord.ButtonStyle.success)
    async def call_back(self, button, interaction):
        button.disabled = True
        button.label = "送信済み"
        await interaction.response.edit_message(view=self)

        for channel in self.channels:
            await channel.send(embeds=self.embeds)
