import voltage
import asyncio
import time
import json
import datetime

from datetime import timedelta
from voltage.ext import commands


def setup(client) -> commands.Cog:
    
    mod = commands.Cog("Moderation")
    
    
    @mod.command(description="Purge a select amount of messages")
    @commands.has_perms(manage_messages=True)
    async def purge(ctx, amount: int) -> None:
        starttime = time.time()
        await ctx.channel.purge(amount)
        embed = voltage.SendableEmbed(
            description=f"Purged {amount} messages in {round(time.time() - starttime, 2)}s!",
            color="#00FF00",
        )
        await ctx.send(content=ctx.author.mention, embed=embed)
        
        
    @mod.command(
        description="Set a custom prefix for the server!",
        aliases=["setprefix", "prefix", "serverprefix", "p", "sp"],
    )
    @commands.has_perms(manage_server=True)
    async def sp(ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        with open("prefixes.json", "w") as f:
            prefixes[str(ctx.server.id)] = prefix
            json.dump(prefixes, f, indent=2)
            embed = voltage.SendableEmbed(
                title="Prefix set!",
                description=f"Set this server's prefix to `{prefix}`!",
                colour="#516BF2",
            )
        return await ctx.send(content=ctx.author.mention, embed=embed)
    
    
    @mod.command(description="Ban a user from the server!")
    @commands.has_perms(ban_members=True)
    async def ban(ctx, member: voltage.Member):
        if ctx.author.roles[0] > len(member.roles):
            return await ctx.send("That user is above your top role. I'm unable to ban them.")
        elif ctx.author.permissions.ban_members:
            return await ctx.send(f"Attempting to ban {member.mention}...")
        elif member.id == ctx.author.id:
            return await ctx.send("You cannot ban yourself.")
        elif member.id == "01H2YMK1VSZM0X4GJAAC7X48TN":
            return await ctx.send("If you want to ban me so bad, just ban me through the client. Not from my own commands..")
        elif member.permissions.ban_members:
            return await ctx.send("This user is an admin. I'm unable to ban them.")
        try:
            await member.ban()
            embed = voltage.SendableEmbed(
                title="Banned!",
                description="{member} is now banned.",
            )
            await ctx.send(content=ctx.author.mention, embed=embed)
        except Exception as e:
            await ctx.send(f"I was unable to ban {member}\n```{e}\n```")
            
            
    @mod.command(description="Kick a user from the server!")
    async def kick(ctx, member: voltage.Member):
        if not ctx.author.permissions.kick_members:
            return await ctx.send("You do not have the required permissions to send this command.")
        elif ctx.author.roles[0] > member.roles[0]:
            return await ctx.send("That user is above your top role. I'm unable to kick them.")
        elif member.roles[0] < client.roles[0]:
            return await ctx.send("I was unable to kick the member because I do not have a high enough role.")
        elif ctx.author.permissions.ban_members:
            return await ctx.send(f"Attempting to kick {member.name}..")
        elif member.id == ctx.author.id:
            return await ctx.send("You cannot kick yourself.")
        elif member.id == "01H2YMK1VSZM0X4GJAAC7X48TN":
            return await ctx.send("If you want to kick me so bad, just do it from the client. Not my own commands..")
        elif member.permissions.ban_members:
            return await ctx.send("This user is an admin. I'm unable to kick them.")
        try:
            await member.kick()
            embed = voltage.SendableEmbed(
                title="Kicked!",
                description=f"{member} is now kicked from the server.",
            )
            await ctx.send(content=ctx.author.mention, embed=embed)
        except Exception as e:
            await ctx.send(f"I was unable to kick {member}\n```{e}\n```")
            
    
    return mod