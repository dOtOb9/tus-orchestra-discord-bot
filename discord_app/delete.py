import discord


#================================================================================================================

class deleteMessageView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(deleteMessageButton())
        self.timeout = 60*60*24*30 # 30日間有効
        self.disable_on_timeout = True

#================================================================================================================

class deleteMessageButton(discord.ui.Button):
    def __init__(self, delete_message=None, row=4, disabled=False) -> None:
        super().__init__(row=row, disabled=disabled)
        self.style = discord.ButtonStyle.danger
        self.label = "削除"
        self.delete_message = delete_message

    async def callback(self, interaction):
        if self.delete_message == None:
            self.delete_message = interaction.message

        await interaction.response.send_modal(VerifydeleteMessageModal(delete_message=self.delete_message))

#----------------------------------------------------------------------------------------------------------------
        
class VerifydeleteMessageModal(discord.ui.Modal):
    def __init__(self, delete_message) -> None:
        super().__init__(title='削除確認フォーム')
        self.delete_message = delete_message

        self.add_item(discord.ui.InputText(label="削除する場合は、`削除`と入力してください。", placeholder="削除"))

    async def callback(self, interaction):
        if self.children[0].value == "削除":
            await self.delete_message.delete()
            await interaction.response.send_message("メッセージを削除しました。", ephemeral=True)
        else:
            await interaction.response.send_message("削除を拒否しました。", ephemeral=True)

#================================================================================================================
        
class viewSendListButton(discord.ui.Button):
    def __init__(self, send_list_embed=None, times=0) -> None:
        super().__init__()
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