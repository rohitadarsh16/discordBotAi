import discord
from discord import File, Embed, Intents
from discord.ext import commands
from discord import app_commands
from easy_pil import Editor, load_image_async,Font
import os
import requests
from io import BytesIO


intents = discord.Intents.all()
intents.members = True
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)


IMAGE_PATH = "./bg.jpg"



@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await send_welcome_message(channel, member)

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
    await channel.send(f":tada: Hey {member.mention}, you're the {member_count}th member on {member.guild.name} :tada:", file=file)
    


async def ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f"{number}{suffix}"

@bot.command(name='welcome')
async def manual_welcome(ctx):
    print(f"Received manual welcome command f")
    try:
        channel = ctx.guild.system_channel
        if channel is not None:
            print(f"Sending welcome message to {ctx.author.name}")
            dummy_member = ctx.author
            await send_welcome_message(channel, dummy_member)
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

bot.run('MTE5Mjg1MzE4NTk1MDQwMDYxMg.GRfepO.KcGha4_wZ9iNcK_vvyIFU9albs_i7UOUdCnf2E')
