import discord

from discord_app.bot import bot
from discord_app.dm.send import verify_send_dm_text, verify_gas_send_dm


class SelectSendView(discord.ui.View):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs

        self.timeout = None


    @discord.ui.button(label="全員", emoji="👥", style=discord.ButtonStyle.primary)
    async def all_callback(self, button, interaction):
        member_list = []
        for member in bot.guilds[0].members:
            member_list.append(member)

        await verify_send_dm_text(member_list=member_list, interaction=interaction, **self.kwargs)

    @discord.ui.button(label="ロールで決める", emoji="👑", style=discord.ButtonStyle.primary)
    async def role_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectRolesView(**self.kwargs),
            ephemeral=True
        )

    @discord.ui.button(label="チャンネルで決める", emoji="📢", style=discord.ButtonStyle.primary)
    async def channel_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectChannelView(**self.kwargs),
            ephemeral=True
        )
    @discord.ui.button(label="個人で決める", emoji="👤", style=discord.ButtonStyle.primary)
    async def personal_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectUsersView(**self.kwargs),
            ephemeral=True
        )

    @discord.ui.button(label="活動連絡DMを受け取る弦楽器団員", emoji="🎻",row=1)
    async def string_callback(self, button, interaction):
        await verify_gas_send_dm(mode='strings', interaction=interaction, **self.kwargs)

    @discord.ui.button(label="活動連絡DMを受け取る金管楽器団員", emoji="🎺",row=2)
    async def wind_callback(self, button, interaction):
        await verify_gas_send_dm(mode='brass', interaction=interaction, **self.kwargs)

    @discord.ui.button(label="活動連絡DMを受け取る木管楽器団員", emoji="🎹",row=2)
    async def woodwind_callback(self, button, interaction):
        await verify_gas_send_dm(mode='woodwind', interaction=interaction, **self.kwargs)

    @discord.ui.button(label="活動連絡DMを受け取る打楽器団員", emoji="🥁",row=2)
    async def percussion_callback(self, button, interaction):
        await verify_gas_send_dm(mode='percussion', interaction=interaction, kwargs=self.kwargs)

    @discord.ui.button(label="活動連絡DMを受け取る管弦楽団員", emoji="🎼",row=3)
    async def orchestra_callback(self, button, interaction):
        await verify_gas_send_dm(mode='orchestra', interaction=interaction, **self.kwargs)

    @discord.ui.button(label="カスタム列で指定する", emoji="⭐", row=4)
    async def custom_callback(self, button, interaction):
        await verify_gas_send_dm(mode='custom', interaction=interaction, **self.kwargs)

#-------------------------------------------------------------
        
class SelectChannelView(discord.ui.View):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs
        self.timeout = None

    @discord.ui.channel_select(placeholder="チャンネルを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        member_list = []
        for channel in select.values:
            if (channel.type == discord.ChannelType.category):
                for channel in channel.channels:
                    member_list.extend(find_member_in_channel(channel))

            member_list.extend(find_member_in_channel(channel))

        await verify_send_dm_text(
            member_list = list(set(member_list)), 
            interaction = interaction,
            **self.kwargs,
        )

#-------------------------------------------------------------
        
class SelectUsersView(discord.ui.View):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs
        self.timeout = None

    @discord.ui.user_select(placeholder="ユーザーを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        member_list = []
        for member in select.values:
            if member.id == bot.application_id:
                continue
            member_list.append(member)
        
        await verify_send_dm_text(
            member_list = list(set(member_list)), 
            interaction = interaction, 
            **self.kwargs, 
            )

#-------------------------------------------------------------
        
class SelectRolesView(discord.ui.View):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs

        self.timeout = None

    @discord.ui.role_select(placeholder="ロールを選択", min_values=1, max_values=25)
    async def select_callback(self, select, interaction):
        member_list = []
        for role in select.values:
            for member in role.members:
                if member.id == bot.application_id:
                    continue
                member_list.append(member)
        
        await verify_send_dm_text(
            member_list = list(set(member_list)), 
            interaction = interaction,
            **self.kwargs
            )


#-------------------------------------------------------------        

def find_member_in_channel(channel) -> list:
    if channel.type == discord.ChannelType.voice:
        return channel.members

    if channel.type == discord.ChannelType.text:
        return channel.members
