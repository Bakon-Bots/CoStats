import discord
from discord.ext import commands
import requests
from bot import get_abb, STATES


class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    # For the US.
    costats_US = requests.get(url='https://api.covidtracking.com/v1/us/current.json')
    costats_US.raise_for_status()
    data = costats_US.json()


    @commands.command(aliases=['costats'], brief='Current US Covid Stats', description='Current US Covid Stats.')
    async def coUS(self, ctx):
        pos, neg = self.data[0]['positive'], self.data[0]['negative']
        death, rec = self.data[0]['death'], self.data[0]['recovered']

        costats = discord.Embed(title='Covid-19 Stats (US)')
        costats.set_thumbnail(url='https://raw.githubusercontent.com/Bakon-Bots/CoStats/main/covidpic.png')
        costats.add_field(name='Positive Cases', value=pos)
        costats.add_field(name='Negative Cases', value=neg)
        costats.add_field(name='Deaths', value=death)
        costats.add_field(name='Recovered', value=rec)
        await ctx.send(embed=costats)


    @commands.command(brief='Current state stats')
    async def statestats(self, ctx, state):
        global STATES
        state.lower()
        state_abb = get_abb(state)

        costats_state = requests.get(f'https://api.covidtracking.com/v1/states/{state_abb}/current.json')
        data = costats_state.json()
        pos, neg = data['positive'], data['negative']
        death, rec = data['death'], data['recovered']

        costats = discord.Embed(title=f'Covid-19 Stats ({state.capitalize()})')
        costats.set_thumbnail(url='https://raw.githubusercontent.com/Bakon-Bots/CoStats/main/covidpic.png')
        costats.add_field(name='Positive Cases', value=pos)
        costats.add_field(name='Negative Cases', value=neg)
        costats.add_field(name='Deaths', value=death)
        costats.add_field(name='Recovered', value=rec)
        await ctx.send(embed=costats)


    @commands.command(brief='Gets the postal code')
    async def getcode(self, ctx, state=None):
        if state == None:
            form = ''
            for state, abb in STATES.items():
                form += f'**{state}** - *{abb}*\n\n'
            await ctx.send(form)
        else:
            if state.capitalize() in STATES.keys():
                await ctx.send(f'**{STATES[state.capitalize()]}**')
                return STATES[state.capitalize()]
            else: await ctx.send(f'```Could not find state {state}. Check your spelling.```')

  
    @commands.command(name='help', description='The help command!')
    async def help_command(self, ctx, cog='all'):
        help_embed = discord.Embed(
            title='Help',
            color=0xffffff
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=self.client.user.avatar_url
        )

        # Get a list of all cogs
        cogs = [c for c in self.client.cogs.keys()]

        if cog == 'all':
            for cog in cogs:

                cog_commands = self.client.get_cog(cog).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - *{comm.description}*\n'

                    # Add the cog's details to the embed.
                    help_embed.add_field(
                    name=cog,
                    value=commands_list,
                    inline=False
                    )
                pass
        else:
            # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:
                commands_list = self.client.get_cog_commands(cogs[ lower_cogs.index(cog.lower()) ])
                help_text=''
                
                # Format
                for command in commands_list:
                    help_text += f'```{command.name}```\n' \
                    f'**{command.description}**\n\n'
                    
                    if len(command.aliases) > 0: help_text += f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n'
                    else: help_text += '\n'

                    help_text += f'Format: `@{self.client.user.name}#{self.client.user.discriminator}' \
                    f' {command.name} {command.usage if command.usage is not None else ""}`\n\n'

                help_embed.description = help_text
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('Invalid cog specified.\nUse `help` command to list all cogs.')

        await ctx.send(embed=help_embed)


def setup(client):
    client.add_cog(Covid(client))
