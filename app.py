from discord.ext import commands
from config import DISCORD_TOKEN
import discord
import os
from discord import app_commands 

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all()) # This creates a new bot instance with the command prefix '!' and all intents enabled
bot.intents.members = True # This is required to access member information 

# -------------------------------------- Core Event methods ------------------------------------------------------------------#

@bot.event # This is a decorator that registers an event
async def on_connect(): # This event is called when the bot connects to Discord but not yet ready to receive commands
    print(f'{bot.user.name} has not yet connected to Discord!')
@bot.event
async def on_ready(): # This event is called when the bot is ready to receive commands
    await bot.tree.sync() #we need to sync all slash commands on bot ready beforeq we can use them
    print(f'{bot.user.name} has connected to Discord!')
@bot.event
async def on_disconnect(): # This event is called when the bot disconnects from Discord
    print(f'{bot.user.name} has disconnected from Discord!')
@bot.event
async def on_resumed(): # This event is called when the bot resumes connection to Discord
    print(f'{bot.user.name} has resumed connection to Discord!')

# -------------------------------------- Guild (Server) Event methods ------------------------------------------------------------------#

@bot.event
async def on_guild_join(guild): # This event is called when the bot joins a guild
    channel = guild.text_channels[0] # This gets the first text channel in the guild
    await channel.send('Hello, I am here!')

@bot.event
async def on_guild_remove(guild): # This event is called when the bot leaves a guild
    channel = guild.text_channels[0]
    await channel.send('Goodbye, I am leaving!')

@bot.event
async def on_guild_update(before, after): # This event is called when a guild is updated
    channel = before.text_channels[0]
    await channel.send('I have been updated!')

@bot.event
async def on_guild_channel_create(channel): # This event is called when a channel is created in a guild
    await channel.send('I have been created!')

@bot.event
async def on_guild_channel_delete(channel): # This event is called when a channel is deleted in a guild
    await channel.send('I have been deleted!')

@bot.event
async def on_guild_available(guild): # This event is called when a guild becomes available
    channel = guild.text_channels[0]
    await channel.send('I am available!')

@bot.event
async def on_guild_unavailable(guild): # This event is called when a guild becomes unavailable
    channel = guild.text_channels[0]
    await channel.send('I am unavailable!')

# -------------------------------------- Member Event methods ------------------------------------------------------------------#

@bot.event
async def on_member_join(member): # This event is called when a member joins a guild
    channel = member.guild.text_channels[0]
    await channel.send(f'Welcome, {member.mention}!')

@bot.event
async def on_member_remove(member): # This event is called when a member leaves a guild
    channel = member.guild.text_channels[0]
    await channel.send(f'Goodbye, {member.mention}!')

@bot.event
async def on_member_update(before, after): # User changes roles, nickname, or avatar.
    channel = before.guild.text_channels[0]
    await channel.send(f'{before.mention} has been updated!')

@bot.event
async def on_user_update(before, after): # User changes global username/avatar.
    channel = before.guild.text_channels[0]
    await channel.send(f'{before.mention} has been updated!')

# -------------------------------------- Message Event methods ------------------------------------------------------------------#

@bot.event
async def on_message(message): # This event is called when a message is sent in a channel
    if message.author == bot.user:
        return
    if message.content == 'hello':
        await message.channel.send('Hello!' + message.author.mention)
    await bot.process_commands(message)  # FIXED: Allow commands to be processed
@bot.event
async def on_message_edit(before, after): # This event is called when a message is edited
    channel = before.channel
    await channel.send(f'{before.author.mention} has edited a message!')

@bot.event
async def on_message_delete(message): # This event is called when a message is deleted
    channel = message.channel
    await channel.send(f'{message.author.mention} has deleted a message!')

@bot.event
async def on_bulk_message_delete(messages): # This event is called when multiple messages are deleted
    channel = messages[0].channel
    await channel.send(f'{messages[0].author.mention} has deleted multiple messages!')

# -------------------------------------- Reaction Event methods ------------------------------------------------------------------#

@bot.event
async def on_reaction_add(reaction, user): # This event is called when a reaction is added to a message
    channel = reaction.message.channel
    await channel.add_reaction(reaction.emoji)

@bot.event
async def on_reaction_remove(reaction, user): # This event is called when a reaction is removed from a message
    channel = reaction.message.channel
    await channel.remove_reaction(reaction.emoji)

@bot.event
async def on_reaction_clear(message, reactions): # This event is called when all reactions are removed from a message
    channel = message.channel
    await channel.send('All reactions have been removed!')

@bot.event
async def on_raw_reaction_add(payload): # This event is called when a reaction is added to a message
    channel = bot.get_channel(payload.channel_id)
    await channel.send('A reaction has been added!')

@bot.event
async def on_raw_reaction_remove(payload): # This event is called when a reaction is removed from a message
    channel = bot.get_channel(payload.channel_id)
    await channel.send('A reaction has been removed!')

# -------------------------------------- Voice Event methods ------------------------------------------------------------------#

@bot.event
async def on_voice_state_update(member, before, after): # This event is called when a member joins/leaves a voice channel
    channel = member.guild.text_channels[0]
    await channel.send(f'{member.mention} has joined a voice channel!')
    
# -------------------------------------- Miscellenous Events ------------------------------------------------------------------#

@bot.event
async def on_typing(channel, user, when): # A user starts typing in a channel.
    await channel.send(f'{user.mention} is typing!')

@bot.event
async def on_raw_typing(channel, user, when): #Raw typing event (no API call).
    channel = bot.get_channel(channel)
    await channel.send(f'{user.mention} is typing!')

@bot.event
async def on_error(event, *args, **kwargs): # Global error handler for events.
    channel = bot.guilds[0].text_channels[0]
    await channel.send('An error has occurred!')

# -------------------------------------- Prefix Command methods ------------------------------------------------------------------#

@bot.command(name="pika", help="Pikachu says pika!") # This is a decorator that registers a command
async def pika(ctx):
    await ctx.send('pika.. pikachu!')

# -------------------------------------- Slash Command methods ------------------------------------------------------------------#

@bot.tree.command(name='ask', description='Make an API call to Gemini') # This is a decorator that registers a slash command
@app_commands.describe(msg='The message to ask!')
async def ask(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message('I will make an API call to Gemini!' + " " +msg)

# -------------------------------------- Hybrid Command methods ------------------------------------------------------------------#

#@commands.has_role('Admin') # This is a decorator that checks if the user has the 'Admin' role
#@commands.has_permissions(manage_messages=True) # This is a decorator that checks if the user has the 'manage_messages' permission
@commands.hybrid_command(
    name="hello", 
    description="Greet a user", 
    help="Usage: !hello <user> or /hello <user>"
)
async def hello(ctx, member: discord.Member):
    await ctx.send(f"Hello {member.mention}! 👋")

# -------------------------------------- Context menu Command methods ------------------------------------------------------------------#
# Context menus let users interact with messages or users via right-click.
    
    #1. User context menu
@bot.tree.context_menu(name="Get User Info")
async def get_user_info(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"{user.name}'s Info")
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"))
    await interaction.response.send_message(embed=embed, ephemeral=True)

    #2. Message context menu
@bot.tree.context_menu(name="Get Message Info")
async def report_message(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(f"Message content: {message.content}", ephemeral=True)

# -------------------------------------- Interactive Components ------------------------------------------------------------------#


# -------------------------------------- Core utility ------------------------------------------------------------------#

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")
                continue
async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

#bot.run(DISCORD_TOKEN)
import asyncio
asyncio.run(main())