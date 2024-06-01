import discord


class viewSendListButton(discord.ui.Button):
    def __init__(self, label="送信先を表示", disabled=False, send_list_embed=None, covered=True) -> None:
        super().__init__(label=label, disabled=disabled)
        self.covered = covered
        self.send_list_embed = send_list_embed

    async def callback(self, interaction):
        new_embeds = self.view.message.embeds.copy()
        if self.covered:
            self.label = "送信先を非表示"
            new_embeds.append(self.send_list_embed)

            await interaction.response.edit_message(embeds=new_embeds, view=self.view)
        else:
            self.label = "送信先を表示"

            await interaction.response.edit_message(embeds=new_embeds, view=self.view)

        self.covered = not self.covered