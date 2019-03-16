
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




"""CREATE TABLE OCS(ID bIGINT,NAME VARCHAR,HP INT, MAG INT, ATK INT,MONEY INT,EXP INT,LEVEL INT BIO VARCHAR, IMAGE VARCHAR)"""


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
        def person(a):
            return a.author==ctx.author

        def accept(a):
            t=a.content.lower()
            y=["y","yes","n","no"]
            return ((t in y) and (person(a)))

        name=await self.bot.wait_for("message",timeout=120,check=person)
        await ctx.send("Is " + name.content + " your Desired name?")
        t= await self.bot.wait_for("message",timeout=120,check=accept)
        while(t.content.lower()=="n" or t.content.lower()=="no"):
            await ctx.send("What is your name child?")
            name=await self.bot.wait_for("message",timeout=120,check=person)
            await ctx.send("Is " + name.content + " your Desired name?")
            t= await self.bot.wait_for("message",timeout=120,check=accept)
        ex="INSERT INTO ocs(id,name, HP, MAG, ATK) VALUES("+str(ctx.message.author.id)+",'"+name.content+"'"+","+"0,0,0)"
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Welcome to Creata "+ name.content)

    @oc.command(name="show")
    async def oc_show(self, ctx):
        ex="SELECT * FROM OCS WHERE( id= "+str(ctx.message.author.id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title="Info")
        for i,j in v[0].items():
            if( i=="id"):
                continue
            elif(i=="image" and j ):
                x.set_img(url=i)
                continue
            elif(i=="name" and j):
                x.add_field(name=i.capitalize(),value=str(j).capitalize(), inline=False)
                continue
            x.add_field(name=i.capitalize(),value=str(j).capitalize(), inline=True)
        await ctx.send(embed=x)

    @oc.group()
    async def add(self, ctx):
        pass

    @add.command(name="hp")
    @commands.check(basic_check)
    async def oc_add_hp(self,ctx,args):
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
    async def oc_add_int(self,ctx,args):
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
    async def oc_add_atk(self,ctx,args):
        ex="SELECT ATK FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        await conn.execute("UPDATE OCS SET ATK ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="img")
    async def oc_add_img(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("UPDATE OCS SET IMAGE ='"+args+"' WHERE ID =" + str(ctx.message.author.id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="stats")
    async def oc_add_stats(self,ctx,args):
        ex="SELECT HP,MAG,ATK FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        args=args.split(",")
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=[]
        for i in range(0,len(v[0])):
            t.append(v[0][i]+int(args[i]))
        await conn.execute("UPDATE OCS SET HP="+str(t[0])+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.execute("UPDATE OCS SET MAG="+str(t[1])+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.execute("UPDATE OCS SET ATK="+str(t[2])+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")        


def setup(bot):
    bot.add_cog(User_Command(bot))
