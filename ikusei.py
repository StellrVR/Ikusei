import voltage
import json
import asyncio
import os
import random
from voltage.ext import commands
from voltage import CommandNotFound, NotEnoughArgs, NotEnoughPerms, NotBotOwner, NotFoundException

async def get_prefix(message, client):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    if message.server is None:
        return "ik."
    elif str(message.server.id) not in prefixes:
        with open("prefixes.json", "w") as f:
            prefixes[str(message.server.id)] = "ik."
            json.dump(prefixes, f, indent=2)
        return "m!"
    else:
        return prefixes.get(str(message.server.id), "ik.")
    
    
class HelpCommand(commands.HelpCommand):
    async def send_help(self, ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title="Help",
            description=f"Use `{ctx.prefix}help <command>` to get help for a command.",
            colour="#516BF2",
            icon_url=ctx.author.display_avatar.url
        )
        text = "\n### **No Category**\n"
        for command in self.client.commands.values():
            if command.cog is None:
                text += f"> {command.name}\n"
        for i in self.client.cogs.values():
            text += f"\n### **{i.name}**\n{i.description}\n"
            for j in i.commands:
                text += f"\n> {j.name}"
        if embed.description:
            embed.description += text
        return await ctx.reply(f"[]({ctx.author.id})", embed=embed)
    
    
bot = commands.CommandsClient(get_prefix, help_command=HelpCommand)

async def status():
    for i in range(1, 10000):
        statuses = [
            f"Playing with {len(bot.cache.servers)} servers and {len(bot.members)} users!",
            f"Watching {len(bot.members)} users!",
            f"To Nurture | {len(bot.cache.servers)} servers",
            f"Do you think we're alone in this universe? | {len(bot.cache.servers)} servers"
        ]
        status = random.choice(statuses)
        await bot.set_status(status, voltage.PresenceType.online)
        await asyncio.sleep(10)
        
        
@bot.listen("message")
async def on_message(message):
    with open("prefixes.json", "r") as g:
        prefixes = json.load(g)
    if message.server.id not in prefixes:
        with open("prefixes.json", "w") as g:
            prefixes[message.server.id] = "ik."
            json.dump(prefixes, g, indent=2)
    with open("json/users.json", "r") as f:
        data = json.load(f)
    if message.author.id in data:
        pass
    elif message.server.id in prefixes:
        pass
    else:
        if message.author.id not in data:
            with open("json/users.json", "w") as f:
                data[message.author.id] = {
                    "username": message.author.name,
                    "id": message.author.id,
                    "bio": "User has no bio set!",
                    "beta": "False",
                    "ff": "False",
                    "notifications": [],
                }
                json.dump(data, f, indent=2)
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        prefix = prefixes.get(str(message.server.id))
    if message.content == "<@01H2YMK1VSZM0X4GJAAC7X48TN>":
        await message.channel.send(
            f"Pong, {message.author.mention}! My prefix for this server is `{prefix}`"
        )
    elif message.content.startswith(prefix) is True:
        if message.author.bot is False:
            pass
        else:
            with open("json/users.json", "r") as f:
                data = json.load(f)
            if message.author.id in data:
                with open("json/users.json", "w") as f:
                    data[message.author.id] = {
                        "username": message.author.name,
                        "id": message.author.id,
                        "bio": "User has no bio set!",
                        "beta": "False",
                        "ff": "False",
                        "notifications": [],
                    }
                json.dump(data, f, indent=2)
            return
    await bot.handle_commands(message)
    
    
@bot.command()
async def reload(ctx):
    if str(ctx.author.id) == "01H213M511VS2W8HMAHHVCSBPT":
        await ctx.send("Reloading all cogs!")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    bot.reload_extension(f"cogs.{filename[:-3]}")
                    print(f"Just reloaded {filename}")
                    await ctx.send(f"Reloaded {filename}")
                except Exception as e:
                    print(e)
    else:
        await ctx.send("You're not the Ikusei's owner.")
        
        
@bot.listen("ready")
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.add_extension(f'cogs.{filename[:-3]}',)
                print(f"Just loaded {filename}")
            except Exception as e:
                print(e)
    await status()
    
    
@bot.command(description="Get support for Ikusei!")
async def support(ctx):
    embed = voltage.SendableEmbed(
        title="Did you find a bug, need help understanding Ikusei, want to suggest a feature?",
        description="Join the support server, [Lunar Cafe](https://rvlt.gg/Xg2H4j7j)!",
        colour="#516BF2",
    )
    await ctx.send(content=ctx.author.mention, embed=embed)
    
    
    
@bot.command(description="Get a user's avatar!")
async def avatar(ctx, member: voltage.Member):
    embed = voltage.SendableEmbed(
        title=f"{member.display_name}'s avatar",
        media=member.display_avatar.url,
        colour="#516BF2",
    )
    await ctx.send(content=ctx.author.mention, embed=embed)
    
    
    
@bot.error("message")
async def on_message_error(error: Exception, message):
    if isinstance(error, CommandNotFound):
        errormsg = [
            "And error has occurred...",
            "Something went wrong!",
            "Stinky 404!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="That command doesn't exist!",
            colour="#516BF2",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotEnoughArgs):
        errormsg = [
            "And error has occurred...",
            "Something went wrong!",
            "Stinky 404!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="You're missing args, you dingus!",
            colour="#516BF2",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotFoundException):
        errormsg = [
            "And error has occurred...",
            "Something went wrong!",
            "Stinky 404!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description=error,
            colour="#516BF2",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotEnoughPerms):
        errormsg = [
            "And error has occurred...",
            "Something went wrong!",
            "Stinky 404!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description=error,
            colour="#516BF2",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotBotOwner):
        errormsg = [
            "And error has occurred...",
            "Something went wrong!",
            "Stinky 404!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="You're not the owner of Ikusei!",
            colour="#516BF2",
        )
        return await message.reply(message.author.mention, embed=embed)
    
    
    
bot.run("TOKEN")
