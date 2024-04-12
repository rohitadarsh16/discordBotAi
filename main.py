import discord
from discord import File, Embed, Intents
from discord.ext import commands
from discord import app_commands
from easy_pil import Editor, load_image_async,Font
import os
import requests
from io import BytesIO
import time

import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://darakhsharayen9:darakhsha01@cluster0.kpldfgg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)


# Send a ping to confirm a successful connection

db = client.discord
users = db.users
banusers = db.banusers
kickuser = db.kickuser
# mostusedphrases = db.mostusedphrases


intents = discord.Intents.all()
intents.members = True
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)


IMAGE_PATH = "./bg.jpg"

badWordList = ['Motherfucker', 'fuck','Dog']

@bot.event
async def on_message(message):
    if message.author.bot:
        return  
    content_lower = message.content.lower()
    
    for bad_word in badWordList:
        if bad_word.lower() in content_lower:
            await message.channel.set_permissions(message.guild.default_role, send_messages=False)
            embed = discord.Embed(
                title="Inappropriate Language Detected",
                description=f"{message.author.mention}, the use of inappropriate language is not allowed. The text channel has been muted.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)
            banusers.insert({"_id": member.id, "name": member.name, "guild": member.guild.name, 'message': content_lower , 'created_at': currentTime})
            return

    await bot.process_commands(message)  # Continue processing other commands and events


@bot.event
async def on_member_join(member):
    # channel = member.guild.system_channel
    # print(channel)
    # if channel is not None:
    #     await send_welcome_message(channel, member)
    try:
        # Iterate through channels in the guild
        for channel in member.guild.channels:
            # Check if the bot has permission to send messages in the channel
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(member.guild.me).send_messages:
                print(f"Sending welcome message to {member.name} in channel {channel.name}")
                await send_welcome_message(channel, member)
                currentTime = time.time()
                
                users.insert_one({"_id": member.id, "name": member.name, "guild": member.guild.name, 'created_at': currentTime})
                break  # Stop iterating once a channel with permissions is found
        else:
            print("No channel found with permission to send messages.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    

async def send_welcome_message(channel, member):
    member_count = len(member.guild.members)
    background =  Editor("bg.jpg")
    avatar_url = member.display_avatar.url
    profile_image = await load_image_async(str(avatar_url))

    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins_size = 38
    poppins = Font.poppins(size=poppins_size,variant = "bold")

    poppins_small = Font.poppins(size=20,variant = "light")

    background.paste(profile, (50, 40))
    background.ellipse((50,40),150,150, outline= "white", stroke_width=5)


    text_position = (250, 40)  # Shifted towards the top

    background.text(text_position, f"Welcome {member.name}", color="white", font=poppins, align="left")
    text_position = (text_position[0], text_position[1] + poppins_size + 20)  # Adjusted coordinate

    background.text(text_position, f"to {member.guild.name}", color="white", font=poppins, align="left")
    text_position = (text_position[0], text_position[1] + poppins_size + 20)  # Adjusted coordinate

    background.text(text_position, f"You're the {await ordinal(member_count)} user", color="white", font=poppins, align="left")




    file = File(fp=background.image_bytes, filename="welcome.png")
    print(channel)
    await channel.send(f":tada: Hey {member.mention}, you're the {member_count}th member on {member.guild.name} :tada:", file=file)
    


async def ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f"{number}{suffix}"

# @bot.command(name='welcome')
# async def manual_welcome(ctx):
#     print(f"Received manual welcome command f")
#     try:
#         channel = ctx.guild.system_channel
#         if channel is not None:
#             print(f"Sending welcome message to {ctx.author.name}")
#             dummy_member = ctx.author
#             await send_welcome_message(channel, dummy_member)
#     except Exception as e:
#         print(f"An error occurred: {e}")

@bot.command(name='welcome')
async def manual_welcome(ctx):
    print(f"Received manual welcome command")
    try:
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(ctx.guild.me).send_messages:
                print(f"Sending welcome message to {ctx.author.name} in channel {channel.name}")
                dummy_member = ctx.author
                await send_welcome_message(channel, dummy_member)
                break  
        else:
            print("No channel found with permission to send messages.")
    except Exception as e:
        print(f"An error occurred: {e}")
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    await ctx.guild.kick(member)
    embed = discord.Embed(
        title=f'Kicked {member.name}#{member.discriminator}',
        description=f'{member.mention} has kicked by {ctx.author.mention} for {reason}',
        color=discord.Color.red()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)

    await ctx.send(embed=embed)
    
    
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    await ctx.guild.ban(member)
    embed = discord.Embed(
        title=f'Banned {member.name}#{member.discriminator}',
        description=f'{member.mention} has banned by {ctx.author.mention} for {reason}',
        color=discord.Color.red()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)

    await ctx.send(embed=embed)
    
    
@bot.command()
async def mute(ctx: commands.Context, member: discord.Member, *, reason: str = "") -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')

    has_permission = ctx.author.guild_permissions.manage_channels
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')

    is_member_kickable = ctx.author.top_role > member.top_role
    if not is_member_kickable:
        return await ctx.send('You cannot mute this member')

    is_in_voice_channel = member.voice is not None and member.voice.channel is not None
    if not is_in_voice_channel:
        return await ctx.send('This member is not in a voice channel')

    if reason == "":
        reason = "No reason provided"

    await member.edit(mute=True, reason=reason)

    embed = discord.Embed(
        title=f'Mute Report for {member.name}#{member.discriminator}',
        description=f'{member.mention} has been muted by {ctx.author.mention}',
        color=discord.Color.red()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)

    await ctx.send(embed=embed)

@bot.command('unmuteText')
async def unmuteText(ctx, member : discord.Member, *, reason=None):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(
    title=f'Unmute Report for {member.name}#{member.discriminator}',
    description=f'{member.mention} has been unmuted by {ctx.author.mention}',
    color=discord.Color.green()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)

    return await ctx.send(embed=embed)

@bot.command()
async def unmute(ctx: commands.Context, member: discord.Member, *, reason: str = "") -> discord.Message:
    is_in_private_messages = ctx.guild is None and isinstance(ctx.author, discord.User)
   
    if is_in_private_messages:
        return await ctx.send('This command cannot be used in private messages')

    has_permission = ctx.author.guild_permissions.manage_channels
    if not has_permission:
        return await ctx.send('You do not have permission to use this command')

    is_member_kickable = ctx.author.top_role > member.top_role
    if not is_member_kickable:
        return await ctx.send('You cannot unmute this member')

    is_in_voice_channel = member.voice is not None and member.voice.channel is not None
    if not is_in_voice_channel:
        return await ctx.send('This member is not in a voice channel')

    if reason == "":
        reason = "No reason provided"
    await member.edit(mute=False, reason=reason)
    embed = discord.Embed(
        title=f'Unmute Report for {member.name}#{member.discriminator}',
        description=f'{member.mention} has been unmuted by {ctx.author.mention}',
        color=discord.Color.green()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)

    await ctx.send(embed=embed)
    
@bot.command(name='timeout')
async def timeout(ctx, member : discord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    await ctx.guild.timeout(member)
    await ctx.send(f"{member} has been timed out for {reason}")

@bot.command(name='kickk')
async def kickk(ctx, member : discord.Member, *, reason=None):
    if reason == None:
        reason = "No reason provided"
    await ctx.guild.kick(member)
    embed = discord.Embed(
        title=f'Kicked {member.name}#{member.discriminator}',
        description=f'{member.mention} has kicked by {ctx.author.mention} for {reason}',
        color=discord.Color.red()  # You can change the color as per your preference
    )
    embed.add_field(name='Reason', value=reason, inline=False)
    currentTime = time.time()
    kickuser.insert_one({"_id": member.id, "name": member.name, "guild": member.guild.name, 'created_at': currentTime})
    await ctx.send(embed=embed)

@bot.command(name='helpp')
async def helpp(ctx):
    embed = discord.Embed(
        title="Help made by FGITIANS.  darakhsha , chhaya  and shaumya",
        description="List of available commands",
        color=discord.Color.blue()
    )

    embed.add_field(name="!kick", value="Kicks a member from the server", inline=False)
    embed.add_field(name="!ban", value="Bans a member from the server", inline=False)
    embed.add_field(name="!mute", value="Mutes a member", inline=False)
    embed.add_field(name="!unmute", value="Unmutes a member", inline=False)
    embed.add_field(name="!timeout", value="Timeout a member", inline=False)
    embed.add_field(name="!welcome", value="Sends a welcome message to the latest member", inline=False)
    embed.add_field(name="!unmuteText", value="Unmutes a member", inline=False)
    await ctx.send(embed=embed)

bot.run('MTIyMDc4NTcxNTYzMDMwOTQ0Ng.GLyNrl.Lx1S5ebYVVuY0QoL7inXgevYKB8fUg-xPu6n_c')
