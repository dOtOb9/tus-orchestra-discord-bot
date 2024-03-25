import discord

from discord_app.bot import bot

#================================================================================================

class campasSelectView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = 60 * 60 * 24 * 30
        self.disable_on_timeout = True

    @discord.ui.select(placeholder="キャンパスを選択してください。",
                       max_values=1,
                       min_values=1,
                       options=[discord.SelectOption(label=campas, value=campas) for campas in ["神楽坂", "葛飾", "野田"]]
                       )
    async def callback(self, select, interaction):
        select.disabled = True

        for member in bot.guilds[0].members:
            if member.id == interaction.user.id:
                for role in bot.guilds[0].roles:
                    if role.name == interaction.data["values"][0]:
                        await member.add_roles(role)

        campas = interaction.data["values"][0]

        success_embed = discord.Embed(
            title="🥳 設定が完了しました！",
            description="練習連絡を受信したい方は、更に`/set activity_dm types:受信する`と入力してください！", 
            color=discord.Color.gold(),
        )

        await interaction.response.send_message(f"所属：{campas}", embeds=[success_embed], ephemeral=True)

#===============================================================================================

class gradeSelectView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = 60 * 60 * 24 * 30

    @discord.ui.select(placeholder="学年を選択してください。",
                       max_values=1,
                       min_values=1,
                       options=[discord.SelectOption(label=str(grade)+"年", value=str(grade)+"年") for grade in range(1, 5)]
                       )
    async def callback(self, select, interaction):
        select.disabled = True

        for member in bot.guilds[0].members:
            if member.id == interaction.user.id:
                for role in bot.guilds[0].roles:
                    if role.name == interaction.data["values"][0]:
                        await member.add_roles(role)


        grade = interaction.data["values"][0]
        await interaction.response.send_message(f"学年：{grade}", view=campasSelectView(), ephemeral=True)

#===============================================================================================
        

class partSelectView(discord.ui.View):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.timeout = 60 * 60 * 24 * 30 # 30日間
        self.disable_on_timeout = True

    part_list = ['Vn', 'Va', 'Vc', 'Cb', 'Trb', 'Ob', 'Hr', 'Fl', 'Fg', 'Cl', 'Perc']
    @discord.ui.select(placeholder="パートを選択してください。", 
                       max_values=1,
                       min_values=1,
                       options=[discord.SelectOption(label=part, value=part) for part in part_list]
                       )
    async def callback(self, select, interaction):
        select.disabled = True

        part = interaction.data["values"][0]

        for member in bot.guilds[0].members:
            if member.id == interaction.user.id:
                nick = part + "." + self.name                
                #await member.edit(nick=nick)

        await interaction.response.send_message(f"氏名：{self.name}\nパート：{part}\nで設定しました。", view=gradeSelectView(), ephemeral=True)

#===============================================================================================

class nameModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="氏名", placeholder="氏名を入力してください。"))

    async def callback(self, interaction):
        name = self.children[0].value

        await interaction.response.send_message(f"氏名：{name}",view=partSelectView(name), ephemeral=True)

#===============================================================================================

class setProfileView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeout = 60 * 60 * 24 * 30 # 30日間
        self.disable_on_timeout = True


    @discord.ui.button(label="サーバー内プロフィールを設定する", emoji="👤", style=discord.ButtonStyle.primary)
    async def callback(self, button, interaction):
        await interaction.response.send_modal(nameModal(title="氏名入力フォーム"))
        self.stop()
