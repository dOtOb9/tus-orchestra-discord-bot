import discord
import datetime as dt


class KeyView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.disable_on_timeout = True
        self.timeout = 60*60*24*30*3 # 3ヶ月

        self.add_item(KeyButton(style=discord.ButtonStyle.primary, label="借開", row=0))
        self.add_item(KeyButton(style=discord.ButtonStyle.primary, label="閉返", row=0))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="借", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="開", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="閉", row=1))
        self.add_item(KeyButton(style=discord.ButtonStyle.secondary, label="返", row=1))


    def create_buttons_for_notice_key_place(self, places: list[str]):

        for place in places:
            self.add_item(KeyPlaceButton(label=place, row=2))

        self.add_item(KeyPlaceButton(label="その他", is_place=False, row=2))


#================================================================================================================


class KeyButton(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, label: str, row: int) -> None:
        super().__init__(style=style, label=label, row=row)
        self.label = label

    async def callback(self, interaction):
        await interaction.response.send_modal(KeyModal(pre_button_label=self.label, pre_view=self.view))


class KeyModal(discord.ui.Modal):
    def __init__(self, pre_button_label: str, pre_view: discord.ui.View, title: str = '部屋開閉連絡') -> None:
        super().__init__(title=title)
        self.pre_view = pre_view


        self.add_item(discord.ui.InputText(
            value=pre_button_label,
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


        await interaction.response.edit_message(view=discord.ui.View()) # Viewを削除

        await interaction.channel.send(view=self.pre_view, embed=key_embed)


#================================================================================================================

class KeyPlaceButton(discord.ui.Button):
    def __init__(self, label: str, row: int, is_place: bool = True) -> None:
        super().__init__(style=discord.ButtonStyle.green, label=label, row=row)
        self.label = label
        self.is_place = is_place

    async def callback(self, interaction):
        await interaction.response.send_modal(WhereIsKeyModal(pre_button_label=self.label, pre_view=self.view, is_place=self.is_place))


class WhereIsKeyModal(KeyModal):
    def __init__(self, pre_button_label: str, pre_view: discord.ui.View, is_place: bool = True) -> None:
        super().__init__(title="鍵の場所連絡", pre_button_label=pre_button_label, pre_view=pre_view)

        if not is_place:
            self.children[0].value = ""


    async def callback(self, interaction: discord.Interaction):
        text = f"鍵の場所：　{self.children[0].value}"
        description = self.children[1].value

        key_embed = discord.Embed(
            title=text,
            description=description,
            timestamp=dt.datetime.now(),
            colour=discord.Colour.green(),
        )

        key_embed.set_author(
            name=interaction.user.display_name, 
            icon_url=interaction.user.display_avatar,
            url=interaction.user.jump_url,
        )

        await interaction.response.edit_message(view=discord.ui.View()) # Viewを削除

        await interaction.channel.send(view=self.pre_view, embed=key_embed)