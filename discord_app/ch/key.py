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

class KeyEmbed(discord.Embed):
    def __init__(self, author: discord.Member, title: str, description: str="", colour: discord.Color=None) -> None:
        super().__init__(
            title=title,
            description=description,
            timestamp=dt.datetime.now(),
            colour=colour
        )

        self.set_author(
            name=author.display_name, 
            icon_url=author.display_avatar,
            url=author.jump_url,
        )

#=================================================================================================================

class KeyButton(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, label: str, row: int) -> None:
        super().__init__(style=style, label=label, row=row)
        self.label = label

    async def callback(self, interaction):
        try:
            await self.view.message.edit(view=discord.ui.View()) # Viewを削除
        except discord.errors.HTTPException: # 既に削除されている場合
            pass

        response_interaction =  await interaction.channel.send(view=KeyView(),embed=KeyEmbed(author=interaction.user, title=self.label))
        await interaction.response.send_message("このメッセージはあなただけに表示されています。\n以下のボタンから、メッセージの編集ができます。", ephemeral=True, view=KeyEditView(response_interaction=response_interaction))

#=================================================================================================================

class KeyEditView(discord.ui.View):
    def __init__(self, response_interaction: discord.Interaction) -> None:
        super().__init__(timeout=None)

        self.message_id = response_interaction.id

        self.add_item(KeyHighlightButton())
        self.add_item(KeyMessageEditButton())
        self.add_item(KeyMessageDeleteButton())

#=================================================================================================================

class KeyMessageDeleteButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(style=discord.ButtonStyle.danger, label="削除")

    async def callback(self, interaction):
        self.view.disable_all_items()

        message = await interaction.channel.fetch_message(self.view.message_id)

        await message.edit(embeds=[])
        await interaction.response.edit_message(view=self.view)


#=================================================================================================================

class KeyMessageEditButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(style=discord.ButtonStyle.primary, label="編集")

    async def callback(self, interaction):

        message = await interaction.channel.fetch_message(self.view.message_id)

        await interaction.response.send_modal(KeyModal(pre_button_label=message.embeds[0].title, message=message))

#=================================================================================================================

class KeyHighlightButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="🌞強調")
        self.state = True

    async def callback(self, interaction):
        message = await interaction.channel.fetch_message(self.view.message_id)
        message.embeds[0].colour = discord.Color.green() if self.state else discord.Color.default()

        self.state = not self.state

        self.label = "🌞強調" if self.state else "🌚非強調"
        self.style = discord.ButtonStyle.success if self.state else discord.ButtonStyle.gray

        await message.edit(embeds=message.embeds)
        await interaction.response.edit_message(view=self.view)

#=================================================================================================================

class KeyModal(discord.ui.Modal):
    def __init__(self, pre_button_label: str, message: discord.Message, title: str = '部屋開閉連絡') -> None:
        super().__init__(title=title)
        self.message = message

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
        self.message.embeds[0].title = self.children[0].value
        self.message.embeds[0].description = self.children[1].value

        await self.message.edit(embeds=self.message.embeds)
        await interaction.response.send_message("メッセージを編集しました。", ephemeral=True)


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