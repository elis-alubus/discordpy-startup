from discord.permissions import PermissionOverwrite
import discord
from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix=".")
token = os.environ["DISCORD_BOT_TOKEN"]


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = "".join(
        traceback.TracebackException.from_exception(orig_error).format()
    )
    await ctx.send(error_msg)


@bot.command()
async def create(ctx):
    roles = ctx.guild.roles
    categories = ctx.guild.categories
    category_names = [c.name for c in categories]
    del roles[0]
    role_names = [i.name for i in roles]
    roles_dic = dict(zip(roles, role_names))
    guild = ctx.guild
    for key, val in roles_dic.items():
        if val not in category_names:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                key: discord.PermissionOverwrite(read_messages=True),
            }
            category = await guild.create_category(val)
            await category.create_text_channel("mtg")
            await category.create_text_channel(name="雑談", overwrites=overwrites)
            await category.create_text_channel(name="反省会", overwrites=overwrites)
            await category.create_voice_channel("会議")



bot.run(token)
