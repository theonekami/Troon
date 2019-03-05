
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




"""CREATE TABLE CREEPS(NAME VARCHAR,DISC VARCHAR, HP INT, MAG INT, ATK INT)"""


class Creep_command(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.group()
    async def creep(self,ctx):
        pass

    @creep.command(name="create")
    @commands.check(basic_check)
    async def creep_create(self, ctx):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)

        def person(a):
            return a.author==ctx.author

        def accept(a):
            t=a.content.lower()
            y=["y","yes","n","no"]
            return (t in y and person(a))
        
        await ctx.send("What is the name of your Creature is it?")
        name=await self.bot.wait_for("message",timeout=120,check=person)
        
        await ctx.send("Describe the Creature")
        disc=await self.bot.wait_for("message",timeout=120,check=person)
        
        await ctx.send("Stats?")
        stats=await self.bot.wait_for("message",timeout=120,check=person)
        stats=stats.content.split("|")
        
        await ctx.send("Are you sure?")
        t= await self.bot.wait_for("message",timeout=120,check=accept)
        while(t.content.lower()=="n" or t.content.lower()=="no"):
            await ctx.send("What is the name of your Creature is it?")
            name=await self.bot.wait_for("message",timeout=120,check=person)
            
            await ctx.send("Describe the Creature")
            disc=await self.bot.wait_for("message",timeout=120,check=person)
            
            await ctx.send("Stats?")
            stats=await self.bot.wait_for("message",timeout=120,check=person)
            stats=stats.content.split("|")
            t= await self.bot.wait_for("message",timeout=120,check=accept)
            
        y=await conn.fetch("SELECT * FROM CREEPS WHERE NAME='" +name.content.strip()+"'")
        if(y):
            await ctx.send("Such a creature already exsits")
            await conn.close()
            return
        
        ex="INSERT INTO creeps(name, disc,HP, MAG, ATK) VALUES('"+name.content.strip().replace("'","''")+"'"+",'"+disc.content.replace("'","''")+"',"+str(stats[0]) +","+str(stats[1]) +","+str(stats[2])+")"

        await conn.execute(ex)
        await conn.close()
        await ctx.send(name.content+ " Has been added as a creep")

    @creep.command(name="show")
    async def creep_show(self, ctx,args):
        ex="SELECT * FROM CREEPS WHERE( name= '"+str(args).strip()+"')"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title="Info")
        for i,j in v[0].items():
            if(i=="name" and j):
                x.add_field(name=i.capitalize(),value=str(j).capitalize(), inline=False)
                continue
            if(i=="disc" and j):
                x.add_field(name=i.capitalize(),value=str(j).capitalize(), inline=False)
                continue
            x.add_field(name=i.capitalize(),value=str(j).capitalize(), inline=True)
        await ctx.send(embed=x)

    @creep.group()
    async def add(self, ctx):
        pass

    @add.command(name="hp")
    @commands.check(basic_check)
    async def creep_add_hp(self,ctx,args):
        ex="SELECT HP FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        await conn.execute("UPDATE OCS SET HP ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="int")
    @commands.check(basic_check)
    async def creep_add_int(self,ctx,args):
        ex="SELECT MAG FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        await conn.execute("UPDATE OCS SET MAG ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="atk")
    @commands.check(basic_check)
    async def creep_add_atk(self,ctx,args):
        ex="SELECT ATK FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        await conn.execute("UPDATE OCS SET ATK ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")


def setup(bot):
    bot.add_cog(Creep_command(bot))
