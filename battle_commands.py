import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items
#users
def value_in_list(ls, val): # ls: a list; val: a value
    for test_value in ls:
        if (test_value == val):
            return True
    return False

def gadmin_ck(ctx): # Check if user is a global bot admin
    return value_in_list(bot_admin_discriminators, ctx.author.id)

def Kami_check(ctx):  ##for funsies
    if (ctx.author.id == 256390874848690176) :
        return True
    else:
        return False

def basic_check(ctx):  ##for funsies
    p=ctx.author
    for i in p.roles:
        if i.name=="Staff Access":
            return True
    if (p == ctx.guild.owner) or (p.id == 256390874848690176):
        return True
    else:
        return False




"""CREATE TABLE OCS(ID bIGINT,NAME VARCHAR,HP INT, MAG INT, ATK INT,MONEY INT, BIO VARCHAR, IMAGE VARCHAR)"""


class BattleField(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.start=True
        self.players=dict()
        self.enemies=dict()

    def start_check(self,ctx):
        return self.start

    @commands.group()
    async def battle(self,ctx):
        pass
        
    
    @battle.command(name="start")
    async def start(self,ctx):
        self.start=True

    @battle.command(name="end")
    async def end(self,ctx):
        self.start=False

    @battle.command(name="join")
    @commands.check(start_check)
    async def b_join(self,ctx):
        ex="SELECT NAME, HP FROM OCS WHERE ID ="+ctx.message.author.id
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v=conn.fetch(ex)
        await conn.close()
        if(v[0][0] in self.players):
            await ctx.message.author.send("You have already joined this battle")
            return
        self.players[v[0][0]]="["+str(v[0][1])+"]"
        await ctx.send(v[0][0]+"Has Joined the battle!!")

    @battle.command(name="show")
    @commands.check(start_check)
    async def b_show(self,ctx):
        x=discord.Embed(title="BATTLEGROUND")
        for i,j in players.items():
            x.add_field(name=i, value=j, inline=True)
        x.add_field(name="\nVS\n")
        for i,j in enemies.items():
            x.add_field(name=i, value=j, inline=True)

def setup(bot):
    bot.add_cog(BattleField(bot))
