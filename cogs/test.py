import discord
from discord.ext import commands

'''Cog for testing cog functionality'''


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["experiment"], invoke_without_command=True)
    async def test(self, ctx, *, msg):
        await ctx.send(str(msg))

    @test.command(pass_context=True)
    async def buh(self, ctx):
        await ctx.send("heuhueue")


def setup(bot):
    bot.add_cog(Test(bot))
