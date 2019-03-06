import discord
from discord.ext import commands
import json
import aiohttp
import asyncpg
import os

#items


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


class entity:
    def __init__(self, i,name,hp,mag, atk):
        self.id=i
        self.name=name
        self.hp=hp
        self.mag=mag
        self.atk=atk

    


"""CREATE TABLE OCS(ID bIGINT,NAME VARCHAR,HP INT, MAG INT, ATK INT,MONEY INT, BIO VARCHAR, IMAGE VARCHAR)"""

def start_check(ctx):
    return start

global start
start=False



class BattleField(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        self.players=[]
        self.enemies=[]


    @commands.group()
    async def battle(self,ctx):
        pass
        
    
    @battle.command(name="start")
    @commands.check(basic_check)
    async def start(self,ctx):
        global start
        start=True
        await ctx.send("The Battle has begun. Use ``t battle join`` to join")

    @battle.command(name="end")
    @commands.check(basic_check)
    async def end(self,ctx):
        global start
        start =False
        await ctx.send("The Battle has Ended.")

    @battle.command(name="join")
    @commands.check(start_check)
    async def b_join(self,ctx):
        ex="SELECT ID, NAME, HP,MAG,ATK FROM OCS WHERE ID ="+str(ctx.message.author.id)
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v=await conn.fetch(ex)
        t=v[0]
        await conn.close()
        self.players.append(entity(t[0],t[1],t[2],t[3],t[4]))
        await ctx.send(v[0][1]+" Has Joined the battle!!")

    @battle.command(name="enemy")
    @commands.check(start_check)
    async def b_enemy(self,ctx,*,args):
        ex="SELECT NAME, HP,MAG,ATK FROM creeps WHERE NAME ="+args
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v=await conn.fetch(ex)
        t=v[0]
        await conn.close()
        self.players.append(entity(-1,t[0],t[1],t[2],t[3]))
        await ctx.send(v[0][1]+" Has Joined the battle!!")

    @battle.command(name="show")
    @commands.check(start_check)
    async def b_show(self,ctx):
        x=discord.Embed(title="BATTLEGROUND")
        for i in self.players:
            x.add_field(name=i.name, value="["+str(i.hp)+"]", inline=True)            
        x.add_field(name="\nVS", value="---------------------------",inline=False)
        for i in self.enemies:
            x.add_field(name=i.name, value="["+str(i.hp)+"]", inline=True)         
        await ctx.send(embed=x)



def setup(bot):
    bot.add_cog(BattleField(bot))
