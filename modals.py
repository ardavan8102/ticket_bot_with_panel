import discord
from discord.ext import commands
from discord.utils import get
from discord import TextStyle, Embed, Interaction, Intents, Webhook, Colour, ButtonStyle
from discord.ui import TextInput, Modal, Button, View
from datetime import datetime
from aiohttp import ClientSession

bot = commands.Bot(
    command_prefix = "s!",
    intents = Intents.all()
)

class SubmitTicketModal(Modal, title = "Ticket Bot By Ardavan"):
    
    
    problem = TextInput(
        label = "موضوع", 
        style = TextStyle.short,
        placeholder = "موضوع تیکت خود را وارد کنید",
        required = True,
        max_length = 100,
        min_length = 2,
    )
    
    async def on_submit(self, interaction : Interaction):
            
        name = f'ticket-{interaction.user.name}'
        category = discord.utils.get(interaction.guild.categories, name='Tickets')


        # create ticket channel
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await interaction.guild.create_text_channel(name, category=category, overwrites=overwrites)

        # send initial message
        if self.problem != None:
            embed = discord.Embed(
                title = "Ticket Bot",
                description="Developed By Ardavan",
                colour = 0x54FFF2
            )
            embed.add_field(name = "Ticket's For :", value = interaction.user, inline=False)
            embed.add_field(name = "Ticket's Subject :",value = self.problem)
            embed.set_footer(text = "React ❌ To Close The Ticket")
            
            await channel.send(f'{interaction.user.mention}')
            msg = await channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = "Ticket Bot",
                description="Developed By Ardavan",
                colour = 0x54FFF2
            )
            embed.add_field(name = "Ticket's For :", value = interaction.user, inline=False)
            embed.set_footer(text = "React ❌ To Close The Ticket")
            
            await channel.send(f'{interaction.user.mention}')
            msg = await channel.send(embed = embed)

        # add ticket emoji reaction to message
        emoji = '❌'
        await msg.add_reaction(emoji)
        
        await interaction.response.send_message(
            f"Ticket Created: {channel.mention}",
            ephemeral=True,
            delete_after=30.0
        )