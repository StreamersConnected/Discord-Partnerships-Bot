import discord

class Events:
	def __init__(self, bot):
		self.bot = bot

	async def on_ready(self):
		bot = self.bot
		game = discord.Game(name="with partners")
		await bot.change_presence(status=discord.Status.idle, game=game)

	async def on_ready(self):
		info = ["\n", str(self.bot.user), f"Discord.py version: {discord.__version__}", f'Shards: {self.bot.shard_count}', f'Guilds: {len(self.bot.guilds)}',
			f'Users: {len(set([m for m in self.bot.get_all_members()]))}', f'{len(self.bot.cogs)} modules with {len(self.bot.commands)} commands']
		self.bot.logger.info("\n".join(info))

def setup(bot):
	cog = Events(bot)
	bot.add_cog(cog)