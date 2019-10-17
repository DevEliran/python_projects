import discord
import random
import os
import json
from discord.ext import commands,tasks
from discord.ext.commands import CommandNotFound


token=os.getenv('TOKEN')

def get_prefix(bot,message):
    with open ('prefixes.json','r') as f:
        prefixes=json.load(f)

    return [prefixes[str(message.guild.id)]]

bot=commands.Bot(command_prefix=get_prefix)

@bot.event
async def on_guild_join(guild):#add server's prefix from json file
    with open('prefixes.json','r') as f:
        prefixes=json.load(f)

    prefixes[str(guild.id)]='.'

    with open('prefixes.json','w') as f:
        json.dump(prefixes,f,indent=4)

@bot.event
async def on_guild_remove(guild):#remove server's prefix from json file
        with open('prefixes.json','r') as f:
            prefixes=json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json','w') as f:
            json.dump(prefixes,f,indent=4)

@bot.command()
async def change_prefix(ctx,prefix):
    with open('prefixes.json','r') as f:
        prefixes=json.load(f)

    prefixes[str(ctx.guild.id)]=prefix

    with open('prefixes.json','w') as f:
        json.dump(prefixes,f,indent=4)

    await ctx.send(f'Prefix changed to {prefix}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command')
@bot.event
async def on_ready():
    #name of the loop.start
    await bot.change_presence(status=discord.Status.idle , activity=discord.Game('with cogs'))
    print('Bot is online.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('Specify how many messages to clear')
    if isinstance(error,commands.MissingPermissions):
        await ctx.send('NOT')

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

#@tasks.loop(seconds=10) start a loop - name of the loop is the name of the function
#async def

for filename in os.listdir('./cogs'):#iterates through all the files in cogs folder
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(token)
