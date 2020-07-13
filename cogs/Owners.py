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



	@commands.command()
	async def ask(self, ctx, *, arg = None):
		channel = channel = self.bot.get_channel(719146135905894461)
		if arg is None:
			await ctx.send(f'{ctx.author.mention}, укажите ваш вопрос!')
		else:
			emb = discord.Embed(title = '**Успешно**', description = f'**{ctx.author.mention}, ваш вопрос был удачно отправлен создателю бота! Скоро он с вами свяжеться!**', colour = discord.Color.green())
			emb1 = discord.Embed(title = '**Новый вопрос!**', description = f'**Жалоба от: {ctx.author}\nСообщение:{arg}**', colour = discord.Color.blue())
			await ctx.send(embed = emb)
			await channel.send(embed = emb1)


	@commands.command()
	@commands.is_owner()
	async def orep(self, ctx, member: discord.Member = None):
		if not commands.NotOwner:
			await ctx.send('**Вам не доступна эта кмд!**')
		elif member is None:
			await ctx.send('**Укажите пользователя!**')
		else:
			cursor.execute("UPDATE users SET rep = rep {}")
			await ctx.send('Успешно!')


	@commands.command()
	@commands.is_owner()
	async def give_rolee(self, ctx, member: discord.Member = None, role: discord.Role = None):
		await ctx.channel.purge(limit = 1)
		if not commands.NotOwner:
			await ctx.send("Не доступно!!")
		elif member is None:
			await ctx.send("укажите пользователя!")
		elif role is None:
			await ctx.send('Укажите роль!')
		else:
			await member.add_roles(role)
			await ctx.send('**Успешно**')
			print(f'{ctx.author.name} использовал Команду /give_role')

	@commands.command()
	@commands.is_owner()
	async def take_rolee(self, ctx, member: discord.Member = None, role: discord.Role = None):
		await ctx.channel.purge(limit = 1)
		if not commands.NotOwner:
			await ctx.send("Не доступно!!")
		elif member is None:
			await ctx.send("укажите пользователя!")
		elif role is None:
			await ctx.send('Укажите роль!')
		else:
			await member.remove_roles(role)
			await ctx.send('**Успешно**')
			print(f'{ctx.author.name} использовал Команду /take_role')


	@commands.command()
	async def read_log(self, ctx):
		f = open(u'./лог.txt', 'r')
		for logs in f:
			await ctx.send(logs)

	@commands.command()
	async def clear_log(self, ctx):
		f = open(u'./лог.txt', 'w')
		f.write('Предыдущии логи были удалены!!\n')
		await ctx.send('Успешно!')

def setup(bot):
	bot.add_cog(Owners(bot))
	print('[COGS] Owners be loaded')