# CONFIG
# ---------
token = "OTMwNTUzMzU5MDkyNTY4MDk1.Yd3jWQ.u8IR6GdFrv_Y53KHWU1luUZlt4g" # This is what the bot uses to log into Discord.
prefix = "-" # This will be used at the start of commands.
# ----------

from pickle import FALSE
from discord.ext import commands
from discord.ext.commands import Bot
import discord
import asyncio
from colorama import Fore
import datetime
import random


bot = commands.Bot(command_prefix=prefix)

bot.remove_command("help")


@bot.event
async def on_ready():
    print(Fore.GREEN+"v1.0 up and Ready!")
    activity = discord.Game(name="Avenger Cloud - Gaming is for everyone ➥ https://discord.gg/xu2hG2BBaz", type=3)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)



@bot.command()
@commands.has_permissions(kick_members=True)
async def embed(ctx, color:discord.Color , thumbnailurl, title, *,message):
	embed=discord.Embed(title=f"\n\n{title}", color=color)
	embed.add_field(name=message, value='\u200b', inline=False)
	embed.set_author(name=f"by {ctx.message.author.name}")
	embed.set_thumbnail(url=thumbnailurl)
	await ctx.message.delete()
	await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1,30, commands.BucketType.guild)
async def embedhelp(ctx):
	embed=discord.Embed(title="Embed help menu", description="A guide on how to use the bot's embed functionality", colour=discord.Colour.blue())
	embed.add_field(name="embed", value="Creates an aesthetically pleasing message (admin only)", inline=False)
	embed.add_field(name="PARAMETERS IN ORDER", value=None, inline=False)
	embed.add_field(name="color", value="A color from discord's api's list of colors (plaintext)", inline=False)
	embed.add_field(name="thumbnail url", value="A url for an image that will be used as the thumbnail", inline=False)
	embed.add_field(name="title", value="The embed's title", inline=False)
	embed.add_field(name="message", value="The embed's text content", inline=False)

	await ctx.send(embed=embed)



@bot.event
async def on_message_recieved(ctx,*, message):
  nc = 0
  with open('spamdet.txt','r+') as file:
    for lines in file:
      if lines.strip('\n') == str(message.author.id):
        nc+=1
    file.writelines(f"{str(message.author.id)}\n")
    #this if for the number of messages being send in sucession; you can change it according to your need
    if nc > 5:
      await message.guild.kick(message.author, reason='spam')
      await asyncio.sleep(1)
      await message.guild.unban(message.author)
      await ctx.send(f"Banned {message.author} due to spamming")

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def ping(ctx):
	embed = discord.Embed(title=f"🏓Pong! {round(bot.latency * 1000)}ms", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def tempmute(ctx, member: discord.Member, time, d, reason=None):
	guild = ctx.guild
	role = discord.utils.get(guild.roles, name="Muted")
		
	for channel in guild.channels:
		await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
	await member.add_roles(role)
	embed = discord.Embed(title="Muted!", description=f"{member.mention} has been muted", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	embed.add_field(name="Reason:", value=reason, inline=False)
	embed.add_field(name="Time left for the mute:", value=f"{time}{d}", inline=False)
	await ctx.reply(embed=embed)
	if d == "s":
		await asyncio.sleep(int(time))
	if d == "m":								
		await asyncio.sleep(int(time*60))
	if d == "h":
		await asyncio.sleep(int(time*60*60))
	if d == "d":
		await asyncio.sleep(int(time*60*60*24))
	await member.remove_roles(role)
	embed = discord.Embed(title="Unmuted", description=f"Unmuted {member.mention} ", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	await ctx.reply(embed=embed)

	            
@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def mute(ctx, member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
	embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	embed.add_field(name="Reason:", value=reason, inline=False)
	await ctx.reply(embed=embed)
	await member.add_roles(mutedRole, reason=reason)
	await member.send(f"You have been muted from: {guild.name} Reason: {reason}")


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.remove_roles(mutedRole)
	await member.send(f"You have unmuted from: {ctx.guild.name}")
	embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def kick(ctx, member: discord.Member, reason="No Reason"):
	if member == None:
		embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
		await ctx.reply(embed=embed)

	else:
		guild = ctx.guild
		embed = discord.Embed(title="Kicked!", description=f"{member.mention} has been kicked!!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason: ", value=reason, inline=False)
		await ctx.reply(embed=embed)
		await guild.kick(user=member)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def tempban(ctx, member: discord.Member, time, d, *, reason="No Reason"):
	if member == None:
		embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
		await ctx.reply(embed=embed)
			

	else:
		guild = ctx.guild
		embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason: ", value=reason, inline=False)
		embed.add_field(name="Time left for the ban:", value=f"{time}{d}", inline=False)
		unbanned = discord.Embed(title="Unbanned!", description=f"{member.mention} has been unbanned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		unbanned.add_field(name="Reason: ", value=reason, inline=False)
		unbanned.add_field(name="They had been banned for: ", value=f"{time}{d}", inline=False)


		await ctx.reply(embed=embed)
		await guild.ban(user=member)

		if d == "s":
			await asyncio.sleep(int(time))
			await guild.unban(user=member)
		if d == "m":
			await asyncio.sleep(int(time*60))
			await guild.unban(user=member)
		if d == "h":
			await asyncio.sleep(int(time*60*60))
			await guild.unban(user=member)
		if d == "d":
			await asyncio.sleep(time*60*60*24)
			await guild.unban(int(user=member))
			await ctx.send(embed=unbanned)
			

@bot.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def ban(ctx, member: discord.Member, reason="No Reason"):
	if member == None:
		embed = discord.Embed(f"{ctx.message.author}, utilizator invalid.")
		await ctx.reply(embed=embed)
	else: 
		guild = ctx.guild
		embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
		embed.add_field(name="Reason: ", value=reason, inline=False)
		await ctx.reply(embed=embed)
		await guild.ban(user=member)


@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 30, commands.BucketType.guild)
async def unban(ctx, user: discord.User):
	if user == None:
		embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
		await ctx.reply(embed=embed)

	else:
		guild = ctx.guild
		embed = discord.Embed(title="Unbanned!", description=f"{user.display_name} has been unbanned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
		await ctx.reply(embed=embed)
		await guild.unban(user=user)







@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def help(ctx):
	embed=discord.Embed(title="Help menu", description="A list of all commands available", colour=discord.Colour.blue())
	embed.add_field(name="embed", value="Creates an aesthetically pleasing message (admin only)", inline=False)
	embed.add_field(name="ping", value="Displays the bot's latency", inline=False)
	embed.add_field(name="tempmute", value="Temporarily mutes a user (admin only)", inline=False)
	embed.add_field(name="mute", value="Mutes a user for an undefined amount of time (admin only)", inline=False)
	embed.add_field(name="unmute", value="Unmutes a user (admin only)", inline=False)
	embed.add_field(name="kick", value="Kicks a user (admin only)", inline=False)
	embed.add_field(name="tempban", value="Temporarily bans a user (admin only)", inline=False)
	embed.add_field(name="ban", value="Bans a user (admin only)", inline=False)
	embed.add_field(name="unban", value="Unbans a user (admin only)", inline=False)
	embed.add_field(name="embedhelp", value="Embed creation help wizard", inline=False)
	embed.add_field(name="gcreate", value="Creates a giveaway (only for giveaway hosts)", inline=False)
	embed.add_field(name="greroll `channel` `message id`", value="Picks a new giveaway winner", inline=False)
	await ctx.send(embed=embed)
 

@bot.command()
@commands.has_permissions(kick_members=True)
async def gcreate(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in seconds)?',]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await bot.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}')
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = bot.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')

    # Giveaway embed message
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'{ctx.author.name} is giving away: {prize}!', value = f'React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'Giveaway ends at {end} UTC!')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(embed = winning_announcement)

@bot.command()
@commands.has_permissions(kick_members=True)
async def greroll(ctx, channel: discord.TextChannel, id_ : int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return
    
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'The giveaway was re-rolled by the host!', icon_url = 'https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name = f'🥳 New Winner:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)



bot.run(token)
