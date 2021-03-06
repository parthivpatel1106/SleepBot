import discord
import sqlite3
import random
import Util
import asyncio
from discord.ext import commands

class Point(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name = 'give_coins', aliases = ['give_points'])
	@commands.has_role('SleepBot Admin')
	async def give_coins(self, ctx, target: discord.Member = None, amount = 0):
		await Util.command_log(self.client, ctx, "give_points")
		if target == None:
			return
		if target.id in Util.POINT:
			Util.POINT[target.id] += amount
		else:
			Util.POINT[target.id] = amount
		await ctx.send(f'Gave {target} {amount} coins')
	
	@commands.command(name='coins', 
		aliases=['point', 'points', 'all_points', 'coin', 'all_coins'], 
		help="Shows the Coins that the mentioned user has. If no one is mentioned then shows the Top 20 users.")
	@Util.is_point_cmd_chnl()
	async def coins(self, ctx, target: discord.Member = None):
		await Util.command_log(self.client, ctx, "points")
		total_point = dict(Util.POINT)
		for user in Util.DB_POINT:
			if user[0] in total_point:
				total_point[user[0]] += user[1]
			else:
				total_point[user[0]] = user[1]
		if target != None :
			if not (target.id in total_point):
				total_point[target.id] = 0
			embed = discord.Embed(title = "User {}'s Coins".format(target.name),
				description = "{} has {} coins since reset.".format(target.name,total_point[target.id]),
				colour = random.randint(0,0xffffff)
				)
			await ctx.send(embed = embed)
			return
	
		top_20 = 1
		total_point = sorted(total_point.items(), key = lambda kv: kv[1])
		total_point.reverse()
		embed = discord.Embed(title = "Coins Leaderboard",
			description = "Top Coins Since Last Reset.",
			colour = random.randint(0,0xffffff)
			)
		for user in total_point:
			embed.add_field(name = "{} : {}".format(top_20,ctx.guild.get_member(int(user[0]))), value = user[1])
			top_20 += 1
			if top_20 == 21:
				break
		await ctx.send(embed = embed)
	@coins.error
	async def coins_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send("Points command can only be used in <#{}> channel!".format(Util.POINTCMD))



def setup(client):
	client.add_cog(Point(client))
