"""
Read LICENSE file
"""

import discord
from discord.ext import commands

class Owner:

	def __init__(self, bot):
		self.bot = bot

def setup(bot):
	cog = Owner(bot)
	bot.add_cog(cog)