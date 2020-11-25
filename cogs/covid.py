<<<<<<< HEAD
import discord
from discord.ext import commands
import requests
from bot import get_abb, STATES
import time

start_time = time.time()

class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command(description='Bots current ping', brief='Bots ping')
    async def ping(self, ctx): await ctx.send(embed=discord.Embed(description=f'Pong. Bot latency: {round(self.client.latency * 1000)}ms', color=0xffffff))


    @commands.command(brief='Current state stats', description='Current state stats')
    async def costats(self, ctx, state='US'):

        if state != 'US': # Specified a state
            global STATES
            state.lower()
            state_abb, state_name = get_abb(state)

            if state_abb != None:
                costats_state = requests.get(f'https://api.covidtracking.com/v1/states/{state_abb}/current.json')
                costats_state.raise_for_status()
                data = costats_state.json()
                pos, neg = data.get('positive'), data.get('negative')
                death, rec = data.get('death'), data.get('recovered')

                costats = discord.Embed(title=f'Covid-19 Stats ({state_name.capitalize()})')
                costats.set_thumbnail(url='https://raw.githubusercontent.com/Bakon-Bots/CoStats/main/covidpic.png')
                costats.add_field(name='Positive Cases', value=pos)
                costats.add_field(name='Negative Cases', value=neg)
                costats.add_field(name='Deaths', value=death)
                costats.add_field(name='Recovered', value=rec)
                await ctx.send(embed=costats)

            else: await ctx.send('Invalid state passed. Please use the full state name.')
        else:
            # For the US.
            costats_US = requests.get(url='https://api.covidtracking.com/v1/us/current.json')
            costats_US.raise_for_status()
            data = costats_US.json()
            pos, neg = data[0].get('positive'), data[0].get('negative')
            death, rec = data[0].get('death'), data[0].get('recovered')

            costats = discord.Embed(title='Covid-19 Stats (US)')
            costats.set_thumbnail(url='https://raw.githubusercontent.com/Bakon-Bots/CoStats/main/covidpic.png')
            costats.add_field(name='Positive Cases', value=pos)
            costats.add_field(name='Negative Cases', value=neg)
            costats.add_field(name='Deaths', value=death)
            costats.add_field(name='Recovered', value=rec)
            await ctx.send(embed=costats)


    @commands.command(brief='Gets the postal code', description='Gets the postal code')
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


def setup(client):
    client.add_cog(Covid(client))
