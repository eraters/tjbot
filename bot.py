import discord
import os
import asyncio
import random
from discord.ext import commands, tasks
from itertools import cycle

bot = commands.Bot(command_prefix="oc!")

@bot.event
async def on_ready():
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')
    
@bot.command()
async def new(ctx):
    if ctx.message.guild.id == int("638485386376642561"):
      member = ctx.message.author
      server = ctx.message.guild
      createchannel = await server.create_text_channel(f"ticket-{member}")
      embed = discord.Embed(title=f"New ticket created",
                            description=f"Hello {member.mention}, thanks for reaching out to our support team, a member of staff will be with you as soon as possible.", color=0x7289DA)
      embed.set_footer(
          text=f"Request by {ctx.author}", icon_url=member.avatar_url)
      staff = discord.utils.get(ctx.message.author.guild.roles, name="Support")
      guest = discord.utils.get(ctx.message.author.guild.roles, name="member")
      everyone = ctx.message.author.guild.default_role
      disallow = discord.PermissionOverwrite()
      disallow.read_messages = False
      disallow.send_messages = False
      allow = discord.PermissionOverwrite()
      allow.read_messages = True
      allow.send_messages = True
      await createchannel.set_permissions(guest, overwrite=disallow)
      await createchannel.set_permissions(everyone, overwrite=disallow)
      await createchannel.set_permissions(ctx.message.author, overwrite=allow)
      await createchannel.set_permissions(staff, overwrite=allow)
      await createchannel.send(embed=embed)
      channel = bot.get_channel(createchannel)
      await ctx.send("Your ticket has been created!")
      await createchannel.send("<@&618638486996993441795>")
    else:
      await ctx.send(":x: You have to be in the support server to do this!")


@bot.command()
async def close(ctx):
    staff = discord.utils.get(ctx.message.author.guild.roles, name="Support")
    if staff in ctx.author.roles:
        channel = ctx.message.channel
        embed = discord.Embed(
            title="Closing ticket", description="This ticket will be closed in 10 seconds", color=0x7289DA)
        confirmmsg = await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await channel.delete(reason="Ticket closed")
    else:
        await ctx.send(":x: You do not have permission to do that.")
    
@bot.command()
@commands.has_role(638486996993441795)
async def presence(ctx, *, status):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(status))
    await ctx.send("Status Changed!")
    
@bot.command()
@commands.has_role(638486996993441795)
async def offlinemode(ctx):
    await bot.change_presence(status=discord.Status.offline)
    await ctx.send("Status Changed!")

@bot.command()
@commands.has_role(638486996993441795)
async def onlinemode(ctx):
    await bot.change_presence(status=discord.Status.online)
    await ctx.send("Status Changed!")
    
@bot.command()
@commands.has_role(638486996993441795)
async def userpresence(ctx):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"with {len(list(bot.get_all_members()))} users!"))
    await ctx.send("Status Changed!")           
                                                                                  
@bot.command()
@commands.has_role(638486996993441795)
async def serverpresence(ctx):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"in {len(bot.guilds)} servers!"))
    await ctx.send("Status Changed!") 
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='No reason provided.'):
    server = ctx.message.guild
    if member.bot == True:
        await member.ban(reason=reason)
        await ctx.message.delete()
        await ctx.send(f'{member} has been banned.')
    else:
        dm = discord.Embed(title=f"You have been banned from `{server.name}`!", color=0x7289DA)
        dm.add_field(name="Moderator:",
                        value=ctx.message.author.display_name)
        dm.add_field(name="Reason:", value=f"{reason}")
        dm.set_thumbnail(url=member.avatar_url)
        await member.send(embed=dm)  # Send DM
        await member.ban(reason=reason)  # Ban
        await ctx.message.delete()  # Delete The Message
        await ctx.send('Member in this server has been banned.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
        
#kick

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='No reason provided.'):
    server = ctx.message.guild
    if member.bot == True:
        await member.kick(reason=reason)
        await ctx.message.delete()
        await ctx.send(f'{member} has been kicked.')
    else:
        dm = discord.Embed(title=f"You have been kicked from `{server.name}`!", color=0x7289DA)
        dm.set_thumbnail(url=member.avatar_url)
        dm.add_field(name="Reason:", value=f"{reason}")
        dm.add_field(name="Moderator:",
                        value=ctx.message.author.display_name)
        await member.send(embed=dm)  # Send DM
        await member.kick(reason=reason)  # Kick
        await ctx.message.delete()  # Delete The Message
        await ctx.send('member has been kicked.')
 
@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member=None):
    if discord.utils.get(ctx.guild.roles, name="muted") is None:
      guild = ctx.guild
      await guild.create_role(name="muted")
    if not member:
        await ctx.send("Please specify a member.")
        return
    else:
      role = discord.utils.get(ctx.guild.roles, name="muted")
      await member.add_roles(role)
      await ctx.send("Role added!")
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member = None):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not member:
        await ctx.send("Please specify a member.")
        return
    await member.remove_roles(role)
    await ctx.send("Role removed!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clears the amount of messages that you filled in."""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} messages got deleted.")
    
    
@bot.command()
async def ping(ctx):
    embed = discord.Embed(colour=0x00FF00)
    embed.add_field(name="Ping", value=f'🏓 {round(bot.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    
@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(
        title="Overcast Bot", description="Info", color=0x7289DA)

    embed.add_field(name="Bot Owner", value="🎃👻  OvercastGaming  🍬🍭#4086 ")
    
    embed.add_field(name="Bot Developer", value="ImLazyWithAZ#8327")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    embed.add_field(name="User count",
                    value=f"{len(list(bot.get_all_members()))}")

    # give users a link to invite this bot to their server
    embed.add_field(
        name="Invite", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=637036513330331648&scope=bot&permissions=8)")

    embed.set_footer(
        text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def IdleGuild(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Join the Idle Miner guild by Direct Messaging <@293085564171714560>")

@bot.command()
async def hello(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {}!".format(member.mention))
    
@bot.command()
async def ip(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("canada.syte.space:25824")
    
@bot.command()
async def site(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("WIP")
    
@bot.command()
async def overrideenable(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {} your override mode is on!!".format(member.mention))

@bot.command()
async def overridedisable(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {} your override mode is off!!".format(member.mention))

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Overcast bot", description="Commands:", color=0x7289DA)

    embed.set_thumbnail(
        url='https://images.emojiterra.com/twitter/v12/512px/1f3d3.png')
    embed.add_field(name="oc!kick", value="Kicks a member.", inline=False)
    embed.add_field(name="oc!ban", value="Bans a member.", inline=False)
    embed.add_field(name="oc!mute", value="Mutes a member.", inline=False)
    embed.add_field(name="oc!unmute", value="Unmutes a member.", inline=False)
    embed.add_field(name="oc!unban", value="Unbans a user.", inline=False)
    embed.add_field(name="oc!clear", value="Clears the amount of messages that you filled in.", inline=False)
    embed.add_field(name="oc!ping", value="Pings the bot.", inline=False)
    embed.add_field(name="oc!help", value="Gives this message.", inline=False)
    embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error:",
                              description=f"The command `{ctx.invoked_with}` was not found! We suggest you do `help` to see all of the commands",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        roleid = error.missing_role
        embed = discord.Embed(title="Error:",
                              description=f"You don't have permission to execute `{ctx.invoked_with}`, this requires the `{roleid}` role to be executed",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error:",
                              description=f"`{error}`",
                              colour=0xe73c24)
      
bot.run(os.getenv('TOKEN'))


