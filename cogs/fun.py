import voltage
import json
import requests
import aiohttp
import random

from voltage.ext import commands


def setup(client) -> commands.Cog:
    
    fun = commands.Cog("Fun")
    
    @fun.command(
        description="Give someone a headpat!",
        aliases=["headpat", "userpat", "pat"],
    )
    async def pat(ctx, member: voltage.Member):
        if member.id == ctx.author.id:
            async with aiohttp.ClientSession() as session:
                img = await session.get(f"https://some-random-api.ml/animu/pat")
                imgjson = await img.json()
                return await ctx.send(
                    f"{ctx.author.name} pats themself. [Weird...]({imgjson['link']})"
                )
            async with aiohttp.ClientSession() as session:
                img = await session.get(f"https://some-random-api.ml/animu/pat")
                imgjson = await img.json()
                await ctx.send(
                    f"{ctx.author.name} pats {member.name} [How cute.]({imgjson['link']})"
                )
                
    
    @fun.command(
        description="Give someone a hug!",
        aliases=["givehug", "userhug", "hug"],
    )
    async def hug(ctx, member: voltage.Member):
        if member.id == ctx.author.id:
            async with aiohttp.ClientSession() as session:
                img = await session.get(f"https://some-random-api.ml/animu/hug")
                imgjson = await img.json()
                return await ctx.send(
                    f"{ctx.author.name} hugs themself. [Weird...]({imgjson['link']})"
                )
            async with aiohttp.ClientSession() as session:
                img = await session.get(f"https://some-random-api.ml/animu/hug")
                imgjson = await img.json()
                await ctx.send(
                    f"{ctx.author.name} hugs {member.name} [Adorable!]({imgjson['link']})"
                )
                
                
                
    @fun.command(name="8ball", description="Ask the Magic 8 Ball a question!")
    async def _8ball(ctx, *, question):
        responses = [
            "I believe not",
            "I don't think so",
            "No",
            "Maybe",
            "Ask again later",
            "Yes",
            "It is likely",
            "Most definitely",
        ]
        embed = voltage.SendableEmbed(
            title=f"{ctx.author.name}",
            icon_url=ctx.author.avatar.url,
            description=f"""My response is...\n `{random.choice(responses)}`!""",
            colour="#516BF2"
        )
        await ctx.send(content="[]()", embed=embed)
        
        
        
    @fun.command(
        description="Generate a random dog picture!",
        aliases=["dog", "doggo", "woofer", "woof"]
    )
    async def dog(ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/dog")
            dogjson = await request.json()
            request2 = await session.get("https://some-random-api.ml/facts/dog")
            factjson = await request2.json()
            
            embed = voltage.SendableEmbed(
                title="Woof!",
                media=dogjson["link"],
                colour="#516BF2",
                description=factjson["fact"],
            )
            await ctx.send(content="[]()", embed=embed)
            
            
            
    @fun.command(
        description="Generate a random cat picture!",
        aliases=["cat", "meow", "kitty", "kitten"]
    )
    async def cat(ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/cat")
            catjson = await request.json()
            request2 = await session.get("https://some-random-api.ml/facts/cat")
            factjson = await request2.json()
            
            embed = voltage.SendableEmbed(
                title="Meow!",
                media=catjson["link"],
                colour="#516BF2",
                description=factjson["fact"],
            )
            await ctx.send(content="[]()", embed=embed)
            
            
            
    @fun.command(
        description="Generate a random fox picture!",
        aliases=["fox", "floofer", "floof"],
    )
    async def fox(ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get("https://some-random-api.ml/img/fox")
            foxjson = await request.json()
            request2 = await session.get("https://some-random-api.ml/facts/fox")
            factjson = await request2.json()
            
            embed = voltage.SendableEmbed(
                title="Floof!",
                media=foxjson["link"],
                colour="#516BF2",
                description=factjson["fact"],
            )
            await ctx.send(content="[]()", embed=embed)
            
            
            
    return fun