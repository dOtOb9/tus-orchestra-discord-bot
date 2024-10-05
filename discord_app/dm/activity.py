import discord

from discord_app.dm.message import DmMessage
from discord_app.dm.select_user import SelectSendView
from discord_app.dm.send import verify_gas_send_dm


class ActivityModal(discord.ui.Modal):
    def __init__(self, dm_message: DmMessage) -> None:
        super().__init__(title="活動連絡フォーム")
        self.dm_message = dm_message


        self.add_item(discord.ui.InputText(label='タイトル', placeholder="練習内容を入力", value=dm_message.activity.title))
        self.add_item(discord.ui.InputText(label="会場", placeholder="GoogleMapで検索できるワードを推奨", value=dm_message.activity.place))
        self.add_item(discord.ui.InputText(label="詳細", style = discord.InputTextStyle.long, required=False, 
                                           value=f"- 部屋\n\n\n- 練習内容\n__１コマ目(10:00~11:20)__：{dm_message.activity.time_slots.first}\n__２コマ目(11:35~12:55)__：{dm_message.activity.time_slots.second}\n__３コマ目(13:35~14:55)__：{dm_message.activity.time_slots.third}\n__４コマ目(15:10~16:30)__：{dm_message.activity.time_slots.forth}"))


    async def callback(self, interaction: discord.Interaction):
        

        self.dm_message.activity.title = self.children[0].value
        self.dm_message.activity.place = self.children[1].value
        self.dm_message.activity.description = self.children[2].value

        self.dm_message.embeds = self.dm_message.activity.set_all_embeds(interaction.user)

        select_send_view = SelectSendView(dm_message=self.dm_message)

        await select_send_view.add_activity_members_button()

        if self.dm_message.activity.section == 'tutti':
            await verify_gas_send_dm(section='tutti', dm_message=self.dm_message, interaction=interaction)
        else:
            await interaction.response.send_message(
                "送信先を選んでください。",
                view=select_send_view,
                ephemeral=True,
                embeds=self.dm_message.embeds,
                )
