import discord
from discord import File, Embed, Intents
from discord.ext import commands
from easy_pil import Editor, load_image_async,Font
import os
import requests
from io import BytesIO


intents = discord.Intents.all()
intents.members = True
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# Constants for image generation
IMAGE_PATH = "./bg.jpg"
DEFAULT_FONT_PATH = ImageFont.load_default()  # Use the default font
FONT_SIZE = 20  # Manually specify the font size
TEXT_COLOR = (255, 255, 255)  # White color


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await send_welcome_message(channel, member)

async def send_welcome_message(channel, member):
    member_count = len(member.guild.members)
    background =  Editor("bg.jpg")
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()
    poppins = Font.poppins(size=50,variant = "bold")
    poppins_small = Font.poppins(size=20,variant = "light")
    background.paste(profile, (325, 90))
    background.ell


    embed = Embed(description=f":tada: Hey {member.mention}, you're the {member_count}th member  :tada:", color=0x00ff00)

    # Set the circular profile image in the left corner
    embed.set_thumbnail(url=avatar_url)

    # Set the banner image as the main background
    embed.set_image(url=banner_image_url)

    # Add a custom message
    embed.add_field(name="Welcome to our channel!", value="We're glad to have you here.")

    await channel.send(embed=embed)


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

bot.run('MTE5Mjg1MzE4NTk1MDQwMDYxMg.GFlNyO.5x1ei2NSkVv0mJhCW6ywXRCHDW1yhyR9Ab24qE')
