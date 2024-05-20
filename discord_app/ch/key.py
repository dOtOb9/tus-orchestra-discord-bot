import discord
import datetime as dt


class KeyView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.disable_on_timeout = True
        self.Timeout = 60*60*24*30*3 # 3ヶ月

        self.add_item(KeyButton(style=discord.ButtonStyle.primary, label="借開", row=0))
        self.add_item(KeyButton(style=discord.ButtonStyle.primary, label="閉返", row=0))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="借", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="開", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="閉", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="返", row=1))


class KeyButton(discord.ui.Button):
    def __init__(self, **kwargs) -> None:
        super().__init__(style=kwargs['style'], label=kwargs['label'], row=kwargs['row'])
        self.kwargs = kwargs

    async def callback(self, interaction):
        await interaction.response.send_modal(KeyModal(view=self.view, **self.kwargs))

#================================================================================================================

class KeyModal(discord.ui.Modal):
    def __init__(self, **kwargs) -> None:
        super().__init__(title='部屋開閉連絡')
        self.kwargs = kwargs

        self.add_item(discord.ui.InputText(
            value=self.kwargs['label'],
            label="説明", 
            )
        )

        self.add_item(discord.ui.InputText(
            label="より詳細な説明",
            placeholder="何も書かなくても大丈夫です。",
            style=discord.InputTextStyle.long,
            required=False
            )
        )

    
    async def callback(self, interaction):
        text = self.children[0].value
        description = self.children[1].value

        key_embed = discord.Embed(
            title=text,
            description=description,
            timestamp=dt.datetime.now(),
        )

        key_embed.set_author(
            name=interaction.user.display_name, 
            icon_url=interaction.user.display_avatar,
            url=interaction.user.jump_url,
        )


        self.kwargs['view'].disable_all_items()

        await interaction.response.edit_message(view=discord.ui.View())

        await interaction.channel.send(view=KeyView(), embed=key_embed)