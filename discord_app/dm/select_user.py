import discord

from discord_app.bot import bot
from discord_app.dm.send import verify_send_dm_text, verify_gas_send_dm
from discord_app.dm.message import DmMessage


class SelectSendView(discord.ui.View):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__()
        self.dm_message = dm_message

        self.timeout = None


    @discord.ui.button(label="全員", emoji="👥")
    async def all_callback(self, button, interaction):
        send_list = []
        for member in bot.guilds[0].members:
            send_list.append(member)

        self.dm_message.send_list = send_list

        await verify_send_dm_text(dm_message=self.dm_message, interaction=interaction)

    @discord.ui.button(label="ロールで決める", emoji="👑")
    async def role_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectRolesView(dm_message=self.dm_message),
            ephemeral=True
        )

    @discord.ui.button(label="チャンネルで決める", emoji="📢")
    async def channel_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectChannelView(dm_message=self.dm_message),
            ephemeral=True
        )
    @discord.ui.button(label="個人で決める", emoji="👤")
    async def personal_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectUsersView(dm_message=self.dm_message),
            ephemeral=True
        )

    #------------------------------------------------------

    async def add_activity_members_button(self):
        if (self.dm_message.activity.section == "無し"): 
            return
        
        button = discord.ui.Button(
            label=self.dm_message.activity.section + "の乗り番の団員", 
            emoji="🎼",
            style=discord.ButtonStyle.primary
        )
        button.callback = self.activity_members_callback
        self.add_item(button)

    async def activity_members_callback(self, interaction):
        await verify_gas_send_dm(dm_message=self.dm_message, interaction=interaction)

#--------------------------------------------------------------

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

            try: 
                send_list.extend(find_member_in_channel(channel))

            except TypeError:
                await interaction.response.send_message("メンバーが取得できないチャンネルが含まれています。", ephemeral=True)
                return

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
