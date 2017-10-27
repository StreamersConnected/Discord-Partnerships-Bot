import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import traceback
import json

def get_applycmdname():
	with open("data/config.json") as f:
		ff = json.load(f)
		return ff.get("apply_command_name", "apply")

class Partnerships:
	def __init__(self, bot):
		self.f = ["Thanks! ", "Alright! ", "Very well. "]
		self.bot = bot
		self.questions = bot.config.get("questions")
		self.output = self.getOutput(bot.config.get("output"))
		self.timeout = 60

	async def on_ready(self):
		self.output = self.getOutput(self.bot.config.get("output"))

	def getOutput(self, id):
		output = self.bot.get_channel(id=id)
		return output

	@commands.command(name=get_applycmdname())
	@commands.cooldown(1, 60*10, type=BucketType.user)
	async def apply(self, ctx):
		"""Start the interactive partner application prompt."""
		if self.bot.config.get("dm_only"):
			if not isinstance(ctx.message.channel, discord.DMChannel):
				return
		questions = self.questions
		first = True
		def check(m):
			return m.author.id == ctx.message.author.id and m.channel.id == ctx.message.channel.id
		embed = discord.Embed()
		embed.color = discord.Color.blue()
		embed.add_field(name="User info:", value=f"**User ID: **{ctx.message.author.id}\n**Username: **{ctx.message.author.name}")
		embed.set_thumbnail(ctx.message.author.avatar_url)
		for question in questions:
			if first:
				await ctx.send(f"{self.bot.config.get('welcome_message')} {question['question']}")
				try:
					msg = await self.bot.wait_for("message", check=check, timeout=self.timeout)
					embed.add_field(name=question['embed_title'], value=msg.content)
				except asyncio.TimeoutError:
					return await ctx.send("Well, then not :wave:")
				except:
					self.bot.logger.exception(traceback.format_exc())
					return await ctx.send("Something went wrong... Please try again later.")
				first = False
			else:
				await ctx.send(random.choice(self.f) + question['question'])
				try:
					msg = await self.bot.wait_for("message", check=check, timeout=self.timeout)
					embed.add_field(name=question['embed_title'], value=msg.content)
				except asyncio.TimeoutError:
					return await ctx.send("Well, then not :wave:")
				except:
					self.bot.logger.exception(traceback.format_exc())
					return await ctx.send("Something went wrong... Please try again later.")	
		await self.output.send(embed=embed)
		await ctx.send("Thanks for your application, it will be reviewed asap.")

def setup(bot):
	cog = Partnerships(bot)
	bot.add_cog(cog)