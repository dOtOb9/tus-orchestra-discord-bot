import discord

from discord_app.bot import bot
from discord_app.dm.send import verify_send_dm_text, verify_gas_send_dm
from discord_app.dm.message import DmMessage


class SelectSendView(discord.ui.View):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__()
        self.dm_message = dm_message

        self.timeout = None


    @discord.ui.button(label="全員", emoji="👥", style=discord.ButtonStyle.primary)
    async def all_callback(self, button, interaction):
        send_list = []
        for member in bot.guilds[0].members:
            send_list.append(member)

        self.dm_message.send_list = send_list

        await verify_send_dm_text(dm_message=self.dm_message, interaction=interaction)

    @discord.ui.button(label="ロールで決める", emoji="👑", style=discord.ButtonStyle.primary)
    async def role_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectRolesView(dm_message=self.dm_message),
            ephemeral=True
        )

    @discord.ui.button(label="チャンネルで決める", emoji="📢", style=discord.ButtonStyle.primary)
    async def channel_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectChannelView(dm_message=self.dm_message),
            ephemeral=True
        )
    @discord.ui.button(label="個人で決める", emoji="👤", style=discord.ButtonStyle.primary)
    async def personal_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectUsersView(dm_message=self.dm_message),
            ephemeral=True
        )

    @discord.ui.button(label="活動連絡DMを受け取る弦楽器団員", emoji="🎻",row=1)
    async def string_callback(self, button, interaction):
        await verify_gas_send_dm(party='strings', interaction=interaction, dm_message=self.dm_message)

    @discord.ui.button(label="活動連絡DMを受け取る金管楽器団員", emoji="🎺",row=2)
    async def wind_callback(self, button, interaction):
        await verify_gas_send_dm(party='brass', interaction=interaction, dm_message=self.dm_message)

    @discord.ui.button(label="活動連絡DMを受け取る木管楽器団員", emoji="🎹",row=2)
    async def woodwind_callback(self, button, interaction):
        await verify_gas_send_dm(party='woodwind', interaction=interaction, dm_message=self.dm_message)

    @discord.ui.button(label="活動連絡DMを受け取る打楽器団員", emoji="🥁",row=2)
    async def percussion_callback(self, button, interaction):
        await verify_gas_send_dm(party='percussion', interaction=interaction, dm_message=self.dm_message)

    @discord.ui.button(label="活動連絡DMを受け取る管弦楽団員", emoji="🎼",row=3)
    async def orchestra_callback(self, button, interaction):
        await verify_gas_send_dm(party='orchestra', interaction=interaction, dm_message=self.dm_message)

    @discord.ui.button(label="カスタム列で指定する", emoji="⭐", row=4)
    async def custom_callback(self, button, interaction):
        await verify_gas_send_dm(party='custom', interaction=interaction, dm_message=self.dm_message)

#-------------------------------------------------------------
        
class SelectChannelView(discord.ui.View):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__()
        self.dm_message = dm_message
        self.timeout = None

    @discord.ui.channel_select(placeholder="チャンネルを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        send_list = []
        for channel in select.values:
            if (channel.type == discord.ChannelType.category):
                for channel in channel.channels:
                    send_list.extend(find_member_in_channel(channel))

            send_list.extend(find_member_in_channel(channel))

        self.dm_message.send_list = send_list

        await verify_send_dm_text(
            dm_message=self.dm_message,
            interaction = interaction,
        )

#-------------------------------------------------------------
        
class SelectUsersView(discord.ui.View):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__()
        self.dm_message = dm_message
        self.timeout = None

    @discord.ui.user_select(placeholder="ユーザーを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        send_list = []
        for member in select.values:
            if member.id == bot.application_id:
                continue
            send_list.append(member)
        
        self.dm_message.send_list = send_list

        await verify_send_dm_text(
            dm_message = self.dm_message,
            interaction = interaction, 
            )

#-------------------------------------------------------------
        
class SelectRolesView(discord.ui.View):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__()
        self.dm_message = dm_message

        self.timeout = None

    @discord.ui.role_select(placeholder="ロールを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        send_list = []
        for role in select.values:
            for member in role.members:
                if member.id == bot.application_id:
                    continue
                send_list.append(member)


        self.dm_message.send_list = send_list
        
        await verify_send_dm_text(
            dm_message = self.dm_message,
            interaction = interaction,
            )


#-------------------------------------------------------------        

def find_member_in_channel(channel) -> list:
    if channel.type == discord.ChannelType.voice:
        return channel.members

    if channel.type == discord.ChannelType.text:
        return channel.members
