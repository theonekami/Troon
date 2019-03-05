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

async def dice(args):
    'Rolls a dice. Formatted as  <no of dice>d<no of sides> eg. 3d10'
    y = str(args).replace(' ', '')
    x = ''
    for i in y:
        if i in ('+', '-', '*', '/'):
            break
        x += i
    z = x.split('d')
    no = int(z[0])
    limit = int(z[1])
    rolls = list()
    for i in range(no):
        rolls.append(random.randint(1, limit))

    s = str(sum(rolls))
    y = y.replace(x, s)

    return int(res)


class entity:
    def __init__(self, i,name,hp,mag, atk):
        self.id=i
        self.name=name
        self.hp=hp
        self.mag=mag
        self.atk=atk

    async def accroll(self,v, x):
        acc=dice("1d20")
        if acc<= 1:
            x.add_field(name="ACCURACY ROLL", value=v+" Crtically fails (rolled a one or less)")
        elif acc<=4:
            x.add_field(name="ACCURACY ROLL", value=v+" Fails")
        elif acc<=18:
            x.add_field(name="ACCURACY ROLL", value=v+" Hits the target(s) successfully")
        else:
            x.add_field(name="ACCURACY ROLL", value=v+" Suceeds Critically")
        return x,acc

    
    async def Effect(self,ctx):
        x=discord.Embed(title="Results")
        v="The Effect"
        x,r=accroll(v,x)
        return x

    async def Magic(self,ctx):
        x=discord.Embed(title="Results")
        v="The Effect"
        x,r=accroll(v,x)
        if r<=4:
            return x
        elif r<=18:
            rol="1d"+str(self.mag//2+1)+"+"+str(self.mag//2+1)
        else:
            rol="1d"+str(self.mag//2+1)+"+"+str(self.mag//2+1)+"*1.5"
        rol=dice(rol)
        x.add_field(name="DAMAGE ROLL",value="You deal " +str(rol) +" INT dmg")
        return x

    async def Attack(self,ctx):
        x=discord.Embed(title="Results")
        v="The Effect"
        x,r=accroll(v,x)
        if r<=4:
            return x
        elif r<=18:
            rol="1d"+str(self.atk//2+1)+"+"+str(self.atk//2+1)
        else:
            rol="1d"+str(self.mag//2+1)+"+"+str(self.mag//2+1)+"*1.5"
        rol=dice(rol)
        x.add_field(name="DAMAGE ROLL",value="You deal " +str(rol) +" ATK dmg")
        return x

    


"""CREATE TABLE OCS(ID bIGINT,NAME VARCHAR,HP INT, MAG INT, ATK INT,MONEY INT, BIO VARCHAR, IMAGE VARCHAR)"""

def start_check(ctx):
    return start

global start
start=False



class BattleField(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

        self.players=[]
        self.pl_no=0
        self.enemies=[]
        self.en_no=0
        self.turn=""


    @commands.group()
    async def battle(self,ctx):
        pass
        
    
    @battle.command(name="start")
    @commands.check(basic_check)
    async def start(self,ctx):
        global start
        start=True
        x=dice("1d2")
        if(x==1):
            self.turn="ALL!!!"
        else:
            self.turn="ENEMY!!!"
        await ctx.send("The Battle has begun. Use ``t battle join`` to join")

    @battle.command(name="end")
    @commands.check(basic_check)
    async def end(self,ctx):
        global start
        start =False
        self.players=[]
        self.pl_no=0
        self.enemies=[]
        self.en_no=0
        await ctx.send("The Battle has Ended.")

    @battle.command(name="join")
    @commands.check(start_check)
    async def b_join(self,ctx):
        ex="SELECT ID, NAME, HP,MAG,ATK FROM OCS WHERE ID ="+str(ctx.message.author.id)
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v=await conn.fetch(ex)
        await conn.close()
        t=v[0]
        self.pl_no+=1
        for i in self.players:
            if i.id==t[0]:
                await ctx.message.author.send("You are already a part of this battle")
                return
        self.players.append(entity(t[0],t[1],t[2],t[3],t[4]))
        await ctx.send(v[0][1]+" Has Joined the battle!!")

    @battle.command(name="creep")
    @commands.check(start_check)
    @commands.check(basic_check)
    async def b_creep(self,ctx,*,args):
        ex="SELECT NAME, HP,MAG,ATK FROM creeps WHERE NAME ='"+args+"'"
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = await asyncpg.connect(DATABASE_URL)
        v=await conn.fetch(ex)
        t=v[0]
        self.en_no+=1
        await conn.close()
        self.enemies.append(entity(-1,t[0]+str(self.en_no),t[1],t[2],t[3]))
        await ctx.send(v[0][0]+" Has Joined the battle!!")

    @battle.command(name="show")
    @commands.check(start_check)
    async def b_show(self,ctx):
        x=discord.Embed(title="BATTLEGROUND")
        for i in self.players:
            x.add_field(name=i.name, value="["+str(i.hp)+"]", inline=True)            
        x.add_field(name="\nVS", value="---------------------------",inline=False)
        for i in self.enemies:
            x.add_field(name=i.name, value="["+str(i.hp)+"]", inline=True)
        x.add_field(name="Turn", value=self.turn,inline=False)
        await ctx.send(embed=x)

    @battle.command(name="switch")
    @commands.check(start_check)
    @commands.check(basic_check)
    async def b_toggle(self,ctx):
        if(self.turn=="ENEMY!!!"):
            self.turn="ALL!!!"
        else:
            self.turn="ENEMY!!!"
        x=discord.Embed(title=self.turn)
        await ctx.send(embed=x)

    @battle.group()
    @commands.check(start_check)
    async def action(self, ctx):
        pass

    @roll.command(name="ATK")
    async def b_roll_atk(self, ctx,*,args=None):
        if not(kami_check()):
            for i in players:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Attack(ctx))
                else:
                    await ctx.message.author.send("You are not in the battle.")
        else:
            for i in enemy:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Attack(ctx))
                else:
                    await ctx.message.author.send("Enemy not in the battle.")
            

    @roll.command(name="MAG")
    async def b_roll_atk(self, ctx,*,args=None):
        if not(kami_check()):
            for i in players:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Magic(ctx))
                else:
                    await ctx.message.author.send("You are not in the battle.")
        else:
            for i in enemy:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Magic(ctx))
                else:
                    await ctx.message.author.send("Enemy not in the battle.")
            
    @roll.command(name="effect")
    async def b_roll_atk(self, ctx,*,args=None):
        if not(kami_check()):
            for i in players:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Effect(ctx))
                else:
                    await ctx.message.author.send("You are not in the battle.")
        else:
            for i in enemy:
                if(i.id==ctx.message.author.id):
                    await ctx.send(embed=i.Effect(ctx))
                else:
                    await ctx.message.author.send("Enemy not in the battle.")
            


def setup(bot):
    bot.add_cog(BattleField(bot))
