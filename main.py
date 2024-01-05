import discord
from discord import File, Embed, Intents
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.messages = True 
bot = commands.Bot(command_prefix='!', intents=intents)

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
    file = File("./bg.jpg", filename="bg.jpg")  # replace with your image file
    # embed.set_thumbnail(url="attachment://bg.jpg")

     # Get the member count after the new member joins
    member_count = len(member.guild.members)

    # Create a circular avatar with a banner background
    avatar_url = member.avatar
    banner_image_url ="attachment://bg.jpg"  # Replace with your banner image URL

    embed = Embed(description=f":tada: Hey {member.mention}, you're the {member_count}th member  :tada:", color=0x00ff00)

    # Set the circular profile image in the left corner
    embed.set_thumbnail(url=avatar_url)

    # Set the banner image as the main background
    embed.set_image(url=banner_image_url)

    # Add a custom message
    embed.add_field(name="Welcome to our channel!", value="We're glad to have you here.")

    await channel.send(embed=embed)

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

bot.run('MTE5Mjg1MzE4NTk1MDQwMDYxMg.GyFlb5.kfMNEunTXUv1K8rj2VTWHOZsZ41gp14yziLpcE')
