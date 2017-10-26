import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
import traceback

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

	@commands.command()
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
		for question in questions:
			if first:
				await ctx.send(f"Hello, welcome to this partnerships prompt. {question['question']}")
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
		embed.color = discord.Color.blue()
		embed.add_field(name="User info:", value=f"**User ID: **{ctx.message.author.id}\n**Username: **{ctx.message.author.name}")
		await self.output.send(embed=embed)
		await ctx.send("Thanks for your application, it will be reviewed asap.")

def setup(bot):
	cog = Partnerships(bot)
	bot.add_cog(cog)