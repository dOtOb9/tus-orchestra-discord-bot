from os import getenv

import discord

from discord_app.bot import bot
from discord_app.dm.ui import viewSendListButton
from discord_app.delete import deleteMessageView, deleteMessageButton
from discord_app.verify_attend import AttendAuthButton 
from gas.get import can_send_activity_dm
from gas.post import generate_activity_date


class SendDmView(discord.ui.View):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs

        self.timeout = 60*60*24*30 # 30日間有効
        self.disable_on_timeout = True

        self.add_item(viewSendListButton(label="送信先を非表示", disabled=True))
        self.add_item(deleteMessageButton(row=4))

        if kwargs['gas']:
            self.add_item(AttendAuthButton(disabled=True))


    @discord.ui.button(label="送信する", emoji="📧", row=4, style=discord.ButtonStyle.success)
    async def send_callback(self, button, interaction):
        button.disabled = True
        button.label = "送信済み"
        await interaction.response.edit_message(view=self)

        view = discord.ui.View(timeout=60*60*24*30, disable_on_timeout=True) # 30日間有効

        view.add_item(viewSendListButton(self.kwargs['send_list_embed'], times=0, label="送信先を表示", row=0))

        if self.kwargs['gas']:
            # 活動日から出欠表の列を生成する
            date_value = self.kwargs['embeds'][0].fields[0].value # 日付の情報を取得
            date_text = date_value[:date_value.find("(")]
            await generate_activity_date(date_text=date_text, is_tutti=self.kwargs['is_tutti']) # GASと連携
            #----------------------------------------------------------------------------

            view.add_item(AttendAuthButton(row=0))


        for member in self.kwargs['member_list']: 
            await member.send(embeds=self.kwargs['embeds'], 
                              view=view, 
                              )

#================================================================================================================

async def verify_send_dm(**kwargs):
    for member in kwargs['member_list']:
        if member.bot:
            kwargs['member_list'].remove(member)


    # 送信先リストの埋め込みテキストを作成
    #---------------------------------------------------------------------------------------------------------------

    name_list = [member.display_name for member in kwargs['member_list']]
    name_list = sorted(name_list)

    name_list_text = ','.join([f"`{name}`" for name in name_list])

    send_list_embed = discord.Embed(
        title=f"送信先リスト（{len(name_list)}）",
        description=name_list_text,
    )

    if kwargs['send_type'] == "Bcc":
        send_list_embed.title += " (非公開）"

    #---------------------------------------------------------------------------------------------------------------

    await kwargs['interaction'].user.send(
        embeds = kwargs['embeds'] + [send_list_embed],
        view=SendDmView(send_list_embed=send_list_embed, **kwargs),
    )

#================================================================================================================
        
async def verify_send_dm_text(**kwargs):
    kwargs['gas'] = False
    await kwargs['interaction'].response.send_message("送信先を確認しています...", ephemeral=True)
    await verify_send_dm(**kwargs)

#================================================================================================================

async def verify_gas_send_dm(**kwargs):
    await kwargs['interaction'].response.send_message("送信先を取得しています...", ephemeral=True)
    json_data =  await can_send_activity_dm(kwargs['mode'])


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
        await kwargs['interaction'].user.send(embed=embed, view=deleteMessageView())
        return
    #----------------------------------------------------------------


    member_id_list = list(json_data['member_list'])

    member_list = []

    for member in bot.guilds[0].members:
        if str(member.id) in member_id_list:
            member_list.append(member)

    kwargs['gas'] = kwargs['embeds'][0].colour == discord.Colour.from_rgb(0, 255, 0) # 埋め込みテキストの色が緑の場合 → つまり、活動連絡の場合

    await verify_send_dm(member_list=member_list, **kwargs)
