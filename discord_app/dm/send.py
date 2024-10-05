from os import getenv

import discord

from discord_app.bot import bot
from discord_app.dm.message import DmMessage
from discord_app.dm.ui import viewSendListButton
from discord_app.delete import deleteMessageView
from discord_app.status import UserStatusButton
from gas.get import can_send_activity_dm
from gas.post import generate_activity_date


class SendButton(discord.ui.Button):
    def __init__(self, dm_message: DmMessage, label: str = None, style: discord.ButtonStyle = discord.ButtonStyle.gray, emoji: str = None, row: int = None) -> None:
        super().__init__(label=label, style=style, emoji=emoji, row=row)
        self.dm_message = dm_message

    
    async def callback(self, interaction):
        self.disabled = True
        self.label = "送信済み"
        await interaction.response.edit_message(view=self.view)

        if self.dm_message.activity != None:
            await generate_activity_date(date_text=self.dm_message.activity.time.start.strftime("%Y/%m/%d"), 
                                         time_slots=self.dm_message.activity.time_slots, 
                                         section=self.dm_message.activity.section,
                                         ) # GASと連携

        for member in self.dm_message.send_list: 
            view=self.dm_message.set_view(member)
            await member.send(
                embeds=self.dm_message.embeds, 
                view=view,
            )

#================================================================================================================

class SendDmView(discord.ui.View):
    def __init__(self, dm_message) -> None:
        super().__init__()

        self.timeout = 60*60*24*30 # 30日間有効
        self.disable_on_timeout = True

        self.add_item(viewSendListButton(label="送信先を非表示", row=0, disabled=True))
        self.add_item(SendButton(label="送信する", emoji="📧", row=4, style=discord.ButtonStyle.success, dm_message=dm_message))

        if dm_message.activity != None:
            self.add_item(UserStatusButton(disabled=True, row=1))
        

#================================================================================================================

async def verify_send_dm(interaction: discord.Interaction, dm_message: DmMessage):
    for member in dm_message.send_list:
        if member.bot:
            dm_message.send_list.remove(member)

    await interaction.user.send(
        embeds = dm_message.embeds + [dm_message.generate_send_list_embed()],
        view=SendDmView(dm_message=dm_message),
    )

#================================================================================================================
        
async def verify_send_dm_text(dm_message: DmMessage, interaction: discord.Interaction):
    await interaction.response.send_message("送信先を確認しています...", ephemeral=True)
    await verify_send_dm(dm_message=dm_message, interaction=interaction)

#================================================================================================================

async def verify_gas_send_dm(dm_message: DmMessage, interaction: discord.Interaction):
    await interaction.response.send_message("送信先を取得しています...", ephemeral=True)
    json_data =  await can_send_activity_dm(dm_message.activity.section)

    # 例外処理
    #----------------------------------------------------------------
    if type(json_data) is str:
        embed = discord.Embed(
            title=json_data,
            color=discord.Color.orange(),
        )
        embed.set_author(
            name="出欠表",
            icon_url=getenv("SPREADSHEET_ICON_URL"),
            url=getenv("SPREADSHEET_URL"),  
        )
        await dm_message.interaction.user.send(embed=embed, view=deleteMessageView())
        return
    #----------------------------------------------------------------


    send_id_list = list(json_data['member_list'])

    send_list = []

    for member in bot.guilds[0].members:
        if str(member.id) in send_id_list:
            send_list.append(member)

    dm_message.send_list = send_list
    dm_message.attend_type = dm_message.embeds[0].colour == discord.Colour.from_rgb(0, 255, 0) # 埋め込みテキストの色が緑の場合 → つまり、活動連絡の場合

    await verify_send_dm(interaction=interaction, dm_message=dm_message)
