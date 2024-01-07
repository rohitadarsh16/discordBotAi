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

bot.run('MTE5Mjg1MzE4NTk1MDQwMDYxMg.Ga51g4.VpBaJYhDUy9HchH8v64Q8uUmgAXDII6bES-M_s')
