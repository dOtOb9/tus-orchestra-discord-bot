from os import getenv

import discord

from discord_app.bot import bot
from discord_app.verify_attend import AttendAuthButton 
from gas.get import can_send_activity_dm   
from gas.post import generate_activity_date


class SendDmButton(discord.ui.View):
    def __init__(self, embeds, member_list, send_type, attend_button, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.member_list = member_list
        self.embeds = embeds
        self.send_type = send_type
        self.attend_button = attend_button

        self.disable_on_timeout = True

        self.add_item(viewSendListButton(label="送信先を非表示", disabled=True))

        if attend_button:
            self.add_item(AttendAuthButton(disabled=True))


    @discord.ui.button(label="送信する", emoji="📧", row=4, style=discord.ButtonStyle.success)
    async def send_callback(self, button, interaction):

        button.disabled = True
        button.label = "送信済み"
        await interaction.response.edit_message(view=self)

        view = discord.ui.View(timeout=60*60*24*30, disable_on_timeout=True) # 30日間有効

        view.add_item(viewSendListButton(self.embeds[-1], times=0, label="送信先を表示"))

        self.embeds.pop(-1) # 送信先リストの埋め込みを削除
        
        if self.attend_button:
            # 活動日から出欠表の列を生成する
            date_value = self.embeds[0].fields[0].value # 日付の情報を取得
            date_text = date_value[:date_value.find("(")]
            await generate_activity_date(date_text) # GASと連携
            #----------------------------------------------------------------------------

            view.add_item(AttendAuthButton(row=0))


        for member in self.member_list: 
            await member.send(embeds=self.embeds, view=view)


#================================================================================================================
                

class viewSendListButton(discord.ui.Button):
    def __init__(self, send_list_embed=None, times=0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.times = times
        self.send_list_embed = send_list_embed

    async def callback(self, interaction):
        new_embeds = self.view.message.embeds.copy()
        if self.times % 2 == 0:
            self.label = "送信先を非表示"
            new_embeds.append(self.send_list_embed)

            await interaction.response.edit_message(embeds=new_embeds, view=self.view)
        else:
            self.label = "送信先を表示"

            await interaction.response.edit_message(embeds=new_embeds, view=self.view)

        self.times += 1

#================================================================================================================

async def verify_send_dm(member_list, embeds, send_type, interaction, attend_button=False):
    for member in member_list:
        if member.bot:
            member_list.remove(member)


    # 送信先リストの埋め込みテキストを作成
    #---------------------------------------------------------------------------------------------------------------
    new_embeds = embeds.copy()

    name_list = [member.display_name for member in member_list]
    name_list_text = ','.join([f"`{name}`" for name in name_list])

    send_list_embed = discord.Embed(
        title="送信先リスト",
        description=name_list_text,
    )

    if send_type == "Bcc":
        send_list_embed.title += " (非公開）"

    new_embeds.append(send_list_embed)

    #---------------------------------------------------------------------------------------------------------------

    await interaction.user.send(
        embeds = new_embeds,
        view=SendDmButton(new_embeds, member_list, send_type=send_type, attend_button=attend_button),
    )

#================================================================================================================
        
async def verify_send_dm_text(member_list, embeds, send_type, interaction):
    await interaction.response.send_message("送信先を確認しています...", ephemeral=True)
    await verify_send_dm(member_list, embeds, send_type, interaction)

#================================================================================================================

async def verify_gas_send_dm(mode, embeds, send_type, interaction):
    await interaction.response.send_message("送信先を取得しています...", ephemeral=True)
    json_data =  await can_send_activity_dm(mode)


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
        await interaction.user.send(embed=embed, ephemeral=True)
        return
    #----------------------------------------------------------------


    member_id_list = list(json_data['member_list'])

    member_list = []

    for member in bot.guilds[0].members:
        if str(member.id) in member_id_list:
            member_list.append(member)

    if embeds[0].colour == discord.Colour.from_rgb(0, 255, 0): # 埋め込みテキストの色が緑の場合 → つまり、活動連絡の場合
        attend_button = True
    else:
        attend_button = False

    await verify_send_dm(member_list, embeds, send_type, interaction, attend_button)
