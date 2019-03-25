
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
        ex="INSERT INTO ocs(id,name, HP, MAG, ATK,money,level,exp) VALUES("+str(ctx.message.author.id)+",'"+name.content+"'"+","+"0,0,0,1000,1,0)"
        await conn.execute(ex)
        await conn.close()
        await ctx.send("Welcome to Creata "+ name.content)

    @oc.command(name="show")
    async def oc_show(self, ctx):
        men=ctx.message.author
        if(len(ctx.message.mentions)):
            men=ctx.message.mentions[0]
        ex="SELECT * FROM OCS WHERE( id= "+str(men.id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        await conn.close()
        x= discord.Embed(title=v[0]["name"])
        x.add_field(name="Name", value=v[0]["name"].capitalize,inline=False)
        x.add_field(name="HP", value=v[0]["hp"],inline=True)
        x.add_field(name="INT", value=v[0]["mag"],inline=True)
        x.add_field(name="ATK", value=v[0]["atk"],inline=True)
        x.add_field(name="Bio", value=v[0]["bio"],inline=False)
        x.add_field(name="Current Book", value=v[0]["books"],inline=False)
        x.add_field(name="Level", value=v[0]["level"],inline=False)
        x.add_field(name="Money", value=v[0]["money"],inline=True)
        if (v[0]["image"]):
            x.set_image(url=str(v[0]["image"]))
        await ctx.send(embed=x)

################################################################################
## ADD set of commands
################################################################################

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


####################################################################################################\
##        SIMPLE Add
####################################################################################################


    @add.command(name="img")
    async def oc_add_img(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("UPDATE OCS SET IMAGE ='"+args+"' WHERE ID =" + str(ctx.message.author.id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="bio")
    async def oc_add_bio(self,ctx,args):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("UPDATE OCS SET bio ='"+args+"' WHERE ID =" + str(ctx.message.author.id))
        await conn.close()
        await ctx.send("It is Done")

####################################################################################################\
##        Check Add
####################################################################################################

    @add.command(name="money")
    @commands.check(basic_check)
    async def oc_add_money(self,ctx,args):
        ex="SELECT MONEY FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        await conn.execute("UPDATE OCS SET MONEY ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="book")
    @commands.check(basic_check)
    async def oc_add_book(self,ctx,*,args):
        ex="SELECT BOOK FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=str(args)+"\n" + v[0][0]
        await conn.execute("UPDATE OCS SET ATK ="+str(t)+" WHERE ID =" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")

    @add.command(name="stats")
    @commands.check(basic_check)
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

    @add.command(name="exp")
    @commands.check(basic_check)
    async def oc_add_exp(self,ctx,args):
        ex="SELECT EXP FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        l="SELECT LEVEL FROM OCS WHERE( id= "+str(ctx.message.mentions[0].id)+")"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v= await conn.fetch(ex)
        t=v[0][0]+int(args)
        while(t>50):
            if l==9:
                await conn.execute("UPDATE ocs SET level ="+str(1)+" WHERE id=" + str(ctx.message.mentions[0].id))
                await ctx.message.mentions[0].send("You have COmpleted the book. Gratz!")
                t=0
                break
            else:
                await conn.execute("UPDATE ocs SET level ="+str(l[0][0]+1)+" WHERE id=" + str(ctx.message.mentions[0].id))
            t-=20
            await ctx.message.mentions[0].send("You have leveled up!")
        y=await conn.fetch("UPDATE ocs SET exp ="+ str(t)+" WHERE id=" + str(ctx.message.mentions[0].id))
        await conn.close()
        await ctx.send("It is Done")



def setup(bot):
    bot.add_cog(User_Command(bot))
