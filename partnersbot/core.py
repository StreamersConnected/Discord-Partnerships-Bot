"""
Read LICENSE file
"""

from discord.ext import commands
import discord
from .config import initConfig

class Bot(commands.AutoShardedBot):
	def __init__(self, *args, **kwargs):
		self.config = initConfig()
		super(Bot, self).__init__(command_prefix=self.config.get('command_prefix'), *args, **kwargs)
		self.description = "An instance of JustMaffie's Partnerships Discord Bot"

	def load_extension(self, name):
		print(f'LOADING EXTENSION {name}')
		if not name.startswith("core.modules."):
			name = f"modules.{name}"
		return super().load_extension(name)

	def unload_extension(self, name):
		print(f'UNLOADING EXTENSION {name}')
		if not name.startswith("core.modules."):
			name = f"modules.{name}"
		return super().unload_extension(name)

	def run(self):
		super().run(self.config.get("token"))

def make_bot(*args, **kwargs):
	bot = Bot(*args, **kwargs)
	for module in ['owner']:
		bot.load_extension(module)

	return bot
