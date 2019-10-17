import discord
from discord.ext import commands

class MemberHandler(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def kick(self,ctx,member:discord.Member,*,reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self,ctx,member:discord.Member,*,reason=None):
        await member.ban(reason=reason)

    @commands.command()
    async def unban(self,ctx ,*, member):
        banned_users= await ctx.guild.bans()
        member_name , member_num =member.split('#')
        for banned in banned_users:
            user=banned.user
            if (user.name,user.discriminator)==(member_name,member_num):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} Unbanned')
                return

    @commands.Cog.listener()
    async def on_member_join(self,member):
        print(f'{member} has joined the server')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f'{member} has left the server')




def setup(bot):
    bot.add_cog(MemberHandler(bot))
