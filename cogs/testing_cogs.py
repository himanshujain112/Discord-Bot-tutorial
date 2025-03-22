from discord.ext import commands

class Test(commands.Cog): # This is a cog class that inherits from commands.Cog it is used to group commands and events together

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener() # This is a decorator that registers an event
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord! its test cog')
    
    @commands.command() # This is a decorator that registers a command
    async def ping(self, ctx): # This is a command method
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

async def setup(bot): # This is a function that is called when the cog is loaded
    await bot.add_cog(Test(bot)) # This adds the cog to the bot