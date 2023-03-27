import discord
from discord import app_commands, ButtonStyle
from discord.ui import Button, View 
from asyncio import sleep
from discord.ext import commands
from modals import *

bot = commands.Bot(
    command_prefix='!', 
    description='Ticket bot for Discord', 
    intents=discord.Intents.all()
)

panel = discord.Embed(
    title = "Create Tickets",
    description = "Developed By Ardavan",
    colour = 0x9F2B68
)


@bot.event
async def on_ready():
    # Changing Presences
    await bot.change_presence(
        status = discord.Status.dnd,
        activity = discord.Activity(type = discord.ActivityType.watching, name = '| Matrix Rain 💚')
    )
    
    # Sync Slash Commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} Commands")
    except Exception as e:
        print(e)
        
    # Send Panel When Running
    openTicketButton = Button(
        style = ButtonStyle.green,
        custom_id="openTicket",
        label = " Open Ticket",
        emoji = "📝",
        row = 0
    )
    
    
    
    async def openTicketCallback(interaction):
        
        global user_id
        user_id = int(interaction.user.id)
        await interaction.response.send_modal(SubmitTicketModal())
        
    openTicketButton.callback = openTicketCallback
        
    view = View()
    view.add_item(openTicketButton)
    
    channel = discord.utils.get(bot.get_all_channels(), name = "ticket")
    await channel.purge(limit = 1)
    await channel.send(embed = panel, view = view)
        

@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        emoji = payload.emoji.name
        channel = bot.get_channel(payload.channel_id)
        guild = bot.get_guild(payload.guild_id)

        if emoji == '❌' and channel.name.startswith('ticket'):

            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(guild.members, id=payload.user_id)

            if int(user.id) == user_id:
                countdown = await channel.send(f'Ticket will be closed in 10s')
                
                for i in range(9, -1, -1):
                    await countdown.edit(content = f'Ticket will be closed in {i}s')
                    await sleep(1)
                
                await channel.delete()


bot.run('BOTTOKEN')
