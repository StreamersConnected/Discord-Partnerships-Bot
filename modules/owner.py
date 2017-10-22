"""
Read LICENSE file
"""

import discord
from discord.ext import commands
import datetime
from collections import Counter
import io

class Owner:

	def __init__(self, bot):
		self.bot = bot

	def cleanup_code(self, content):
		if content.startswith('```') and content.endswith('```'):
			return '\n'.join(content.split('\n')[1:-1])
		return content.strip('` \n')

	def get_syntax_error(self, e):
		if e.text is None:
			return f'```py\n{e.__class__.__name__}: {e}\n```'
		return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

	@commands.is_owner()
	@commands.command()
	async def reload(self, ctx, module):
		print(module)
		try:
			self.bot.unload_extension(module)
			self.bot.load_extension(module)
		except Exception as e:
			await ctx.send(f"An error occurred while reloading {module}\n``{e}``")
		else:
			await ctx.send(f"Module {module} reloaded successfully")

	@commands.is_owner()
	@commands.command()
	async def load(self, ctx, module):
		try:
			self.bot.load_extension(module)
		except Exception as e:
			return await ctx.send(f"An error occurred while loading {module}\n{e}")
		return await ctx.send(f"Module {module} loaded successfully")

	@commands.is_owner()
	@commands.command()
	async def unload(self, ctx, module):
		try:
			self.bot.unload_extension(module)
		except Exception as e:
			return await ctx.send(f"An error occurred while loading {module}\n{e}")
		return await ctx.send(f"Module {module} loaded successfully")

	@commands.is_owner()
	@commands.command()
	async def about(self, ctx):
		embed = discord.Embed()
		embed.color = discord.Colour.blue()
		embed.add_field(name="Discord.py version", value=discord.__version__)
		embed.add_field(name="Author", value="[JustMaffie](https://github.com/JustMaffie)")
		embed.add_field(name="Bot link", value="[github.com/JustMaffie/Discord-Partnerships-Bot](https://github.com/JustMaffie/Discord-Partnerships-Bot)")

		return await ctx.send(embed=embed)

	# Thanks danny
	@commands.command(name='eval')
	@commands.is_owner()
	async def _eval(self, ctx, *, body: str):
		env = {
			'bot': self.bot,
			'ctx': ctx,
			'channel': ctx.channel,
			'author': ctx.author,
			'guild': ctx.guild,
			'message': ctx.message,
		}

		env.update(globals())

		body = self.cleanup_code(body)
		stdout = io.StringIO()

		to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
		else:
			value = stdout.getvalue()
			try:
				await ctx.message.add_reaction('\u2705')
			except:
				pass

			if ret is None:
				if value:
					await ctx.send(f'```py\n{value}\n```')
			else:
				self._last_result = ret
				await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
	cog = Owner(bot)
	bot.add_cog(cog)