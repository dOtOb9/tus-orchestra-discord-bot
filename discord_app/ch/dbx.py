import os
import discord
import dropbox

from discord_app.ch.send import ChannelSendButton

DBX_APP_KEY = os.getenv('DBX_APP_KEY')
DBX_APP_SECRET = os.getenv('DBX_APP_SECRET')
DBX_OAUTH2_REFRESH_TOKEN = os.getenv('DBX_OAUTH2_REFRESH_TOKEN')

dbx = dropbox.Dropbox(app_key=DBX_APP_KEY, app_secret=DBX_APP_SECRET, oauth2_refresh_token=DBX_OAUTH2_REFRESH_TOKEN)


class FileRequestModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="ファイルの概要"))
        self.add_item(discord.ui.InputText(label="ファイルの説明", required=False, style=discord.InputTextStyle.long))

    async def callback(self, interaction):
        title = self.children[0].value
        description = self.children[1].value
        folder_metadata = dbx.files_create_folder_v2(path=f'/{title}', autorename=True)

        new_folder_path = folder_metadata.metadata.path_display

        await interaction.response.send_message(view=FileRequestButton(new_folder_path, title, description), ephemeral=True)


class FileRequestButton(discord.ui.View):
    def __init__(self, new_folder_path, title, description, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_folder_path = new_folder_path
        self.title = title
        self.description = description
        
    @discord.ui.button(label="ファイルリクエストを送る", emoji="📁", style=discord.ButtonStyle.primary)
    async def file_request(self, button, interaction):
        shared_link_metadata = dbx.sharing_create_shared_link(self.new_folder_path)

        file_request_url = dbx.file_requests_create(title='テスト', destination=self.new_folder_path).url

        request_embed = discord.Embed(
            title="アップロードはここからできます。",
            url=file_request_url,
            colour=discord.Color.from_rgb(r=0, g=128, b=255), # 明るい青
        )

        shared_embed = discord.Embed(
            title=self.title,
            url=shared_link_metadata.url,
            description=f"{self.description}\n\n[ここ](https://www.dropbox.com/referrals/AAC1BiyJQq4wC-swP7TyqJXdv9-0UVFAiBc?src=global9)からDropboxを始めると、無料で500MB分のストレージが増えます。",
            colour=discord.Color.from_rgb(r=0, g=128, b=255), # 明るい青
        )

        request_embed.set_footer(text="Dropbox", icon_url="https://github.com/dOtOb9/tus-orchestra-discord-bot/blob/main/image/dropbox_tile_logo_icon_168230.png?raw=true")
        shared_embed.set_footer(text="Dropbox", icon_url="https://github.com/dOtOb9/tus-orchestra-discord-bot/blob/main/image/dropbox_tile_logo_icon_168230.png?raw=true")

        shared_embed.set_author(
            name = interaction.user.display_name,
            icon_url = interaction.user.display_avatar, 
            url = interaction.user.jump_url
        )

        await interaction.response.send_message(view=ChannelSendButton(embed=shared_embed), embeds=[request_embed, shared_embed], ephemeral=True)