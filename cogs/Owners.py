import discord
from discord.ext import commands
import bot
import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Owners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command()
	@commands.is_owner()
	async def inplay(self, ctx, *, arg):
		emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")

		else:
			await self.bot.change_presence(activity=discord.Game(name=arg))
			await ctx.send( embed = emb )


	@commands.command()
	@commands.is_owner()
	async def inwatch(self, ctx, *, arg):
		emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")

		else:
			await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
			await ctx.send( embed = emb )


	@commands.command()
	@commands.is_owner()
	async def inlisten (self, ctx, *, arg):
		emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")

		else:
			await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
			await ctx.send( embed = emb )


	@commands.command()
	@commands.is_owner()
	async def instream(self, ctx, *, arg):
		emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")
		else:
			await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.streaming))
			await ctx.send( embed = emb )


	@commands.command()
	@commands.is_owner()
	async def secret_222(self, ctx, member: discord.Member = None):
		if not commands.NotOwner:
			await ctx.send(f'{ctx.author.mention}, с конечно всё понимаю но тебе нельзя использовать эту кмд!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(1000000, ctx.author.id))
			connection.commit()
			await ctx.channel.purge(limit = 1)
			await ctx.send('Команда была выполнена!')
			print(f'Пользователь {owner}, выполнил Секретную кмд!')



def setup(bot):
	bot.add_cog(Owners(bot))
	print('[COGS] Owners be loaded')