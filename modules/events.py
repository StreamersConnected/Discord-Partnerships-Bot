import discord

class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		bot = self.bot
		game = discord.Game(name="with partners")
		await bot.change_presence(status=discord.Status.idle, game=game)

def setup(bot):
	cog = Events(bot)
	bot.add_cog(cog)