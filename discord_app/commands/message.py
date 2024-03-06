import discord

from discord_app.forward import SelectChannelButtons
from discord_app.bot import bot


@bot.message_command(name="埋め込みテキストを転送する", description="埋め込みテキストがあるメッセージのみ使用できます。")
async def forward(ctx, message: discord.Message):
    if len(message.embeds):
        await ctx.respond(view=SelectChannelButtons(embeds=message.embeds), embeds=message.embeds, ephemeral=True)
    else:
        await ctx.respond("埋め込みテキストがありません。", ephemeral=True)
