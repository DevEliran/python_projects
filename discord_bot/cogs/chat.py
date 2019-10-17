import discord
import random
import sys
from discord.ext import commands

class chat(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,ctx):
        id=ctx.guild.id
        guild=self.bot.get_guild(id)
        if "community_report"==ctx.content.lower():
            online,idle,offline=0,0,0
            for i in guild.members:
                if str(i.status)=='online':
                    online+=1
                elif str(i.status)=='offline':
                    offline+=1
                else:
                    idle+=1
            await ctx.channel.send(f"```Online : {online}\nIdle : {idle}\nOffline : {offline} ```")

        if "go out bot"==ctx.content.lower():
            self.bot.close()
            sys.exit()

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'Pong! {round(self.bot.latency*1000)} ms')#Bot sends a message

    @commands.command(aliases=['ask1'])# all of the strings in this array can invoke the ask function
    async def ask(self,ctx,*,question):
        res=['combining the two. It’s really not as bad as it sounds.',
                'Friday; otherwise, he would have not passed the class.',
                'to spend two weeks there next year.',
                'movie alone.',
                'kite in the middle of the night and ended up sunburnt.',
                'Please wait outside of the house.',
                'Wednesday is hump day, but has anyone asked the camel if he’s happy about it?',
                'This is the last random sentence I will be writing and I am going to stop mid-sent',
                'Sixty-Four comes asking for bread.',
                'I checked to make sure that he was still alive.',
                'I love eating toasted cheese and tuna sandwiches.']
        await ctx.send(random.choice(res))

def setup(bot):
    bot.add_cog(chat(bot))
