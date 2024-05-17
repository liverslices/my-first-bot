'''
Based heavily on:
	https://raspberrytips.com/make-a-discord-bot-on-pi/
	https://medium.com/@tonite/finding-the-invite-code-a-user-used-to-join-your-discord-server-using-discord-py-5e3734b8f21f

'''

import discord
from discord.ext import commands

with open('token.txt') as f:
	token = f.read()

bot = commands.Bot(command_prefix='+', intents=discord.Intents.all())

invites = {}

@bot.event
async def on_ready():
	for g in bot.guilds:
		invites[g.id] = await g.invites()

def find_invite_by_code(invite_list, code):
	for i in invite_list:
		if i.code == code:
			return i

@bot.event
async def on_member_join(member):
	invites_before_join = invites[member.guild.id]
	invites_after_join = await member.guild.invites()
	for ibj in invites_before_join:
		if ibj.uses < find_invite_by_code(invites_after_join, ibj.code).uses:
			print(f"Member {member.name} joined, invited by {invite.inviter} (code: {invite.code})")
			invites[member.guild.id] = invites_after_join
			return

@bot.event
async def on_member_remove(member):
	invites[member.guild.id] = await member.guild.invites()

@bot.command()
async def ping(ctx):
	await ctx.send('pong')

@bot.command()
async def gambit(ctx):
	await ctx.send('sucks')

bot.run(token)
