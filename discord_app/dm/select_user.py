import discord

from discord_app.bot import bot
from discord_app.dm.send import verify_send_dm_text, verify_gas_send_dm


class SelectUsersButtons(discord.ui.View):
    def __init__(self, embeds, send_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embeds = embeds
        self.send_type = send_type

        self.timeout = None


    @discord.ui.button(label="全員", emoji="👥", style=discord.ButtonStyle.primary)
    async def all_callback(self, button, interaction):
        member_list = []
        for member in bot.guilds[0].members:
            member_list.append(member)

        await verify_send_dm_text(member_list, self.embeds, self.send_type, interaction)

    @discord.ui.button(label="ロールで決める", emoji="👑", style=discord.ButtonStyle.primary)
    async def role_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectRolesMenu(embeds=self.embeds, send_type=self.send_type),
            ephemeral=True
        )

    @discord.ui.button(label="チャンネルで決める", emoji="📢", style=discord.ButtonStyle.primary)
    async def channel_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectChannelMenu(embeds=self.embeds, send_type=self.send_type),
            ephemeral=True
        )
    @discord.ui.button(label="個人で決める", emoji="👤", style=discord.ButtonStyle.primary)
    async def personal_callback(self, button, interaction):
        await interaction.response.send_message(
            view=SelectUsersMenu(embeds=self.embeds, send_type=self.send_type),
            ephemeral=True
        )

    @discord.ui.button(label="活動連絡DMを受け取る弦楽器団員", emoji="🎻",row=1, style=discord.ButtonStyle.primary)
    async def string_callback(self, button, interaction):
        await verify_gas_send_dm(mode='strings', embeds=self.embeds, send_type=self.send_type, interaction=interaction)

    @discord.ui.button(label="活動連絡DMを受け取る金管楽器団員", emoji="🎺",row=2, style=discord.ButtonStyle.primary)
    async def wind_callback(self, button, interaction):
        await verify_gas_send_dm(mode='brass', embeds=self.embeds, send_type=self.send_type, interaction=interaction)

    @discord.ui.button(label="活動連絡DMを受け取る木管楽器団員", emoji="🎹",row=2, style=discord.ButtonStyle.primary)
    async def woodwind_callback(self, button, interaction):
        await verify_gas_send_dm(mode='woodwind', embeds=self.embeds, send_type=self.send_type, interaction=interaction)

    @discord.ui.button(label="活動連絡DMを受け取る打楽器団員", emoji="🥁",row=3, style=discord.ButtonStyle.primary)
    async def percussion_callback(self, button, interaction):
        await verify_gas_send_dm(mode='percussion', embeds=self.embeds, send_type=self.send_type, interaction=interaction)

    @discord.ui.button(label="活動連絡DMを受け取る管弦楽団員", emoji="🎼",row=4, style=discord.ButtonStyle.primary)
    async def orchestra_callback(self, button, interaction):
        await verify_gas_send_dm(mode='orchestra', embeds=self.embeds, send_type=self.send_type, interaction=interaction)

#-------------------------------------------------------------
        
class SelectChannelMenu(discord.ui.View):
    def __init__(self, embeds, send_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.embeds = embeds
        self.send_type = send_type

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
            embeds = self.embeds,
            send_type = self.send_type,
            interaction = interaction
        )

#-------------------------------------------------------------
        
class SelectUsersMenu(discord.ui.View):
    def __init__(self, embeds, send_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.embeds = embeds
        self.send_type = send_type

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
            embeds = self.embeds, 
            send_type = self.send_type, 
            interaction = interaction
            )

#-------------------------------------------------------------
        
class SelectRolesMenu(discord.ui.View):
    def __init__(self, embeds, send_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embeds = embeds
        self.send_type = send_type

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
            embeds = self.embeds, 
            send_type = self.send_type,
            interaction = interaction
            )


#-------------------------------------------------------------        

def find_member_in_channel(channel) -> list:
    if channel.type == discord.ChannelType.voice:
        return channel.members

    if channel.type == discord.ChannelType.text:
        return channel.members
