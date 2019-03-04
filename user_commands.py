
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

def accept(a):
    a=a.content.lower()
    y=["y","yes","n","no"]
    return a in y


"""CREATE TABLE OCS(ID bIGINT,NAME VARCHAR,HP INT, MAG INT, ATK INT,MONEY INT, BIO VARCHAR, IMAGE VARCHAR)"""


class User_Command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.group()
    async def oc(self,ctx):
        pass

    @oc.command(name="create")
    async def oc_create(self, ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        y=await conn.fetch("SELECT * FROM OCS WHERE ID=" +str(ctx.message.author.id))
        if(len(y)):
            await ctx.send("You..You Already have an oc right? INSOLENCE")
            await conn.close()
            return
        await ctx.send("What is your name child?")
        name=await self.bot.wait_for("message",timeout=120)
        await ctx.send("Is " + name.content + " your Desired name?")
        t= await self.bot.wait_for("message",timeout=120,check=accept)
        while(t.content.lower()=="n" or t.content.lower()=="NO"):
            await ctx.send("What is your name child?")
            name=await self.bot.wait_for("message",timeout=120)
            await ctx.send("Is " + rew.content + " your Desired name?")
            t= await self.bot.wait_for("message",timeout=120,check=accept)
        ex="INSERT INTO ocs(id,name, HP, MAG, ATK) VALUES("+str(ctx.message.author.id)+"'"+name+"'"+","+"0,0,0)"
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Welcome to Creata "+ name)

    @oc.command(name="show")
    async def oc_show(self, ctx):
        ex="SELECT * FROM OCS WHERE( id= "+str(ctx.message.author.id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title="Info")
        for i,j in v[0].items():
            if(not(j)):
                continue
            x.add_field(name=i,value=str(j), inline=False)
        await ctx.send(embed=x)
  
        
def setup(bot):
    bot.add_cog(User_Command(bot))
