import discord
from discord import File, Embed, Intents
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
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
    # Create a circular avatar with a banner background
    # avatar_url = member.avatar
    # embed = Embed(title="Welcome to our server!", description=f"Hello {member.mention}, welcome to our Discord server!", color=0x00ff00)
    # embed.set_image(url=avatar_url)

    # Use a banner image as a background
    # file = File("./welcome_image.png", filename="welcome_image.png")  # replace with your image file
    # embed.set_thumbnail(url="attachment://bg.jpg")

     # Get the member count after the new member joins
    member_count = len(member.guild.members)
    welcome_image_path = await generate_welcome_image(member.display_name, member_count, member.avatar)
    # Create a circular avatar with a banner background
    avatar_url = member.avatar
    banner_image_url ="attachment://"+welcome_image_path  # Replace with your banner image URL

    embed = Embed(description=f":tada: Hey {member.mention}, you're the {member_count}th member  :tada:", color=0x00ff00)

    # Set the circular profile image in the left corner
    embed.set_thumbnail(url=avatar_url)

    # Set the banner image as the main background
    embed.set_image(url=banner_image_url)

    # Add a custom message
    embed.add_field(name="Welcome to our channel!", value="We're glad to have you here.")

    await channel.send(embed=embed)

def generate_welcome_image(username, member_count, avatar_url):
    # Open the background image
    background_image = Image.open(IMAGE_PATH)
    
    # Use the default font
    font = DEFAULT_FONT_PATH

    # Create a drawing object
    draw = ImageDraw.Draw(background_image)

    # Draw the circular profile image in the left corner
    
    response = requests.get(avatar_url)
    print(avatar_url)
    profile_image = Image.open(BytesIO(response.content))

    # Remove alpha channel before resizing
    profile_image = profile_image.convert("RGB").resize((100, 100), Image.LANCZOS)

    # Add alpha channel back
    profile_image.putalpha(255)

    background_image.paste(profile_image, (50, 50), profile_image)

    # Draw welcome text in the center
    welcome_text = f"Welcome to our server, {username}!\nYou are the {ordinal(member_count)} member."
    text_width, text_height = draw.textsize(welcome_text, font)
    text_position = ((background_image.width - text_width) // 2, (background_image.height - text_height) // 2)
    draw.text(text_position, welcome_text, font=font, fill=TEXT_COLOR)

    # Save the dynamically generated image
    welcome_image_path = "welcome_image.png"
    background_image.save(welcome_image_path)

    return welcome_image_path

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
