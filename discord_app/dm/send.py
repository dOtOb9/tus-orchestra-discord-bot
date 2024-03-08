import discord
from os import getenv

from discord_app.bot import bot
from discord_app.verify_attend import AttendAuthButton 
from gas.get import can_send_activity_dm   
from gas.post import generate_activity_date


class SendDmButton(discord.ui.View):
    def __init__(self, embed, member_list, name_list_text, send_type, attend_button, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.member_list = member_list
        self.name_list_text = name_list_text
        self.embed = embed
        self.send_type = send_type
        self.name_list = [member.display_name for member in self.member_list]
        self.attend_button = attend_button

        self.disable_on_timeout = True

        if attend_button:
            self.add_item(discord.ui.Button(label="出席認証", row=0, style=discord.ButtonStyle.primary, disabled=True))


    @discord.ui.button(label="送信する", emoji="📧", row=1, style=discord.ButtonStyle.success)
    async def send_callback(self, button, interaction):
        if self.send_type == "Bcc":
            message = "送信先は送信者によって非公開になっています。"
        else:
            message = f"送信先\n{self.name_list_text}"

        button.disabled = True
        button.label = "送信済み"
        await interaction.response.edit_message(view=self)

        if self.attend_button:
            date_value = self.embed.fields[0].value
            date_text = date_value[:date_value.find("(")]
            await generate_activity_date(date_text)

        for member in self.member_list:
            if self.attend_button:
                # 活動日から出欠表の列を生成する
 
                await member.send(message, embed=self.embed, view=AttendAuthButton())
            else:
                await member.send(message, embed=self.embed)


#-------------------------------------------------------------

async def verify_send_dm(member_list, embed, send_type, interaction, attend_button=False):
    for member in member_list:
        if member.bot:
            member_list.remove(member)

    name_list = [member.display_name for member in member_list]
    name_list_text = ','.join([f"`{name}`" for name in name_list])
    message = f"送信先リスト\n{name_list_text}"
    if send_type == "Bcc":
        message += "\n受信者には送信先リストは表示されません。"
    await interaction.user.send(
        message,
        embed = embed,
        view=SendDmButton(embed, member_list, name_list_text, send_type=send_type, attend_button=attend_button),
    )

#---------------------------------------------------------------------------------------------------------------
        
async def verify_send_dm_text(member_list, embed, send_type, interaction):
    await interaction.response.send_message("送信先を確認しています...", ephemeral=True)
    await verify_send_dm(member_list, embed, send_type, interaction)

#----------------------------------------------------------------------------------------------------------------

async def verify_gas_send_dm(mode, embed, send_type, interaction):
    await interaction.response.send_message("送信先を取得しています...", ephemeral=True)
    json_data =  await can_send_activity_dm(mode)

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

    member_id_list = list(json_data['member_list'])

    print(member_id_list)

    member_list = []

    for member in bot.guilds[0].members:
        if str(member.id) in member_id_list:
            member_list.append(member)

    if embed.colour == discord.Colour.from_rgb(0, 255, 0): # 埋め込みテキストの色が緑の場合 → つまり、活動連絡の場合
        attend_button = True
    else:
        attend_button = False

    print(attend_button)

    await verify_send_dm(member_list, embed, send_type, interaction, attend_button)
