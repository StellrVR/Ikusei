import voltage
import asyncio
import random
import time
import aiohttp
import json
import re
import datetime
import random

from datetime import timedelta
from voltage.ext import commands

starttime = time.time()
version = "0.1"

def setup(client) -> commands.Cog:
    
    util = commands.Cog("Utility")
    
    @util.command(description="Get information of a server!")
    async def serverinfo(ctx):
        with open("json/servers.json", "r") as f:
            data = json.load(f)
        if ctx.server.id not in data:
            try:
                with open("json/servers.json", "w") as f:
                    data[ctx.server.id] = {
                        "name": ctx.server.name,
                        "members": str(len(ctx.server.members)),
                        "owner": ctx.server.owner.id,
                        "ownername": ctx.server.owner.name,
                        "banner": ctx.server.banner.url,
                        "icon": ctx.server.icon.url,
                    }
                    json.dump(data, f, indent=2)
                    embed = voltage.SendableEmbed(
                        description="Your server is now registered into our database!"
                    )
                    return await ctx.send(content="[]()", embed=embed)
            except Exception as e:
                return await ctx.send(e)
        elif ctx.server.owner.name != data[ctx.server.id]["ownername"]:
            with open("json/servers.json", "w") as f:
                data[ctx.server.id] = {
                    "name": ctx.server.name,
                    "members": str(len(ctx.server.members)),
                    "owner": ctx.server.owner.id,
                    "ownername": ctx.server.owner.name,
                    "banner": ctx.server.banner.url,
                    "icon": ctx.server.icon.url,
                }
                json.dump(data, f, indent=2)
                embed = voltage.SendableEmbed(
                    description="Your server wasnt registered in our database, but it is now!",
                    color="#00FF00",
                )
                return await ctx.send(content="[]()", embed=embed)
        else:
            info = data[ctx.server.id]
            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description=f"**Information on {info['name']}**\n**Server Owner:**\n> `{info['ownername']}`\n",
                media=info["banner"]
            )
            await ctx.send(content="[]()", embed=embed)
            
            
    @util.command(description="Generate a random color!")
    async def color(ctx):
        chosen = "#%06x" % random.randint(0, 0xFFFFFF)
        print(chosen)
        await ctx.send(f"[](https://some-random-api.ml/canvas/colorviewer?hex={chosen})")
        
    
    @util.command(description="Generate a random hex color code as an image!")
    async def getcolor(ctx, hex):
        embed = voltage.SendableEmbed(
            title="Here's your color:",
            description="{hex}",
        )
        await ctx.send(
            content=f"[](https://some-random-api.ml/canvas/colorviewer?hex={hex})",
            embed=embed
        )
        
        
    @util.command(description="See how long Ikusei has been online for!")
    async def uptime(ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - starttime))))
        embed = voltage.SendableEmbed(
            title="Ikusei's Uptime:",
            description=f"`{uptime}",
        )
        await ctx.send(content=ctx.author.mention, embed=embed)
        
        
    @util.command(description="See Ikusei's bot statistics!")
    async def stats(ctx):
        embed = voltage.SendableEmbed(
            title="Ikusei's Statistics:",
            description=f"**Servers:**\n`{len(client.cache.servers)}`\n**Members:**\n`{len(client.members)}`\n**Version:**\n*{version}*\n",
        )
        await ctx.send(content="[]()", embed=embed)
        
    
    @util.command(description="Ping Ikusei!")
    async def ping(ctx):
        embed = voltage.SendableEmbed(
            title="Pong!",
            description=f"**Ping:**\n*Pinging...*\n",
        )
        embed2 = voltage.SendableEmbed(
            title="Pong!",
            description=f"**Ping:**\n{random.randint(1, 1000) / 10}ms\n",
        )
        msg = await ctx.send(content=ctx.author.mention, embed=embed)
        await msg.edit(content=ctx.author.mention, embed=embed2)
        
        
    @util.command(description="Get information on a user!")
    async def userinfo(ctx, user: voltage.User):
        if user.bot is False:
            embed = voltage.SendableEmbed(
                title=user.display_name,
                media=user.profile.background,
                icon_url=user.display_avatar.url,
                description=f"""
# {user.name}'s Info:
---
`{user.name.capitalize()}'s User ID:`
> {user.id}

`{user.name.capitalize()}'s Avatar:`
> [Avatar Link]({user.avatar.url})
---
# {user.name.capitalize()}'s Revolt Profile:
---
`{user.name.capitalize()}'s Status:`
> {user.status.text}

`{user.name.capitalize()}'s Badges:`
> {user.badges}

`{user.name.capitalize()}'s Banner:`
> {user.profile.background}

`{user.name.capitalize()}'s Bio:`
> {user.profile.content}
    """,
            )
            return await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            return await ctx.send("Profiles coming the future!")
    
    
    return util