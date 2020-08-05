import discord
from discord.ext import commands
import random
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from config import settings
import wikipedia
from googletrans import Translator
import asyncio
import os
import json
import datetime

now = datetime.datetime.now()

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Lvl(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()


	@commands.command(aliases = ['благодарить', '+rep'])
	async def __rep(self, ctx, member: discord.Member = None):
		
		if member is None:
			await ctx.send(f'{ctx.author.mention}, вы не указали пользователя!')
		elif ctx.author == member:
			await ctx.send(f'{ctx.author.mention}, ты конечно извени но себе ты не сможешь дать репу!')
		else:
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
			connection.commit()
			emb = discord.Embed(title = '**Успешно!**', description = f"""У пользователя {member.name} была повышена репутация!\nТекущия репутация: {cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}!""")
			await ctx.send(embed = emb)

			if cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 20:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 30:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 40:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 50:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 60:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 70:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 80:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 90:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')

			elif cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 100:
				cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, member.id))
				connection.commit()
				await ctx.send(f'У пользователя {member.mention}, повыселcя уровень! Новый уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')


	@commands.command(aliases = ['лвл', 'левл', 'уровень', 'lvl'])
	async def __lvl(self, ctx, member: discord.Member = None):

		if member is None:
			emb = discord.Embed(title = f'**Уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**', description = f'Репутация {ctx.author.name}: ``{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}/{cursor.execute("SELECT xpc FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}``\nДо следующего уровня: ``{cursor.execute("SELECT xpc FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] - cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}`` репутации!', colour = discord.Color.red())
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(title = f'**Уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**', description = f'Репутация {member.name}: ``{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}/{cursor.execute("SELECT xpc FROM users WHERE id = {}".format(member.id)).fetchone()[0]}``\nДо следующего уровня: ``{cursor.execute("SELECT xpc FROM users WHERE id = {}".format(member.id)).fetchone()[0] - cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}`` репутации!', colour = discord.Color.red())
			await ctx.send(embed = emb)


	@commands.command(aliases = ['опыт', 'репутация', 'myrep'])
	async def __myrep(self, ctx, member: discord.Member = None):
		if member is None:
			emb = discord.Embed(title = '**Репутация:**', description = f'**{ctx.author.name}, ваша репутация: {cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb)
		else:
			emb1 = discord.Embed(title = '**Репутация**', description = f'**Репутация участника {member.mention}: {cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb1)


	@commands.command()
	@commands.is_owner()
	async def add_exp(self, ctx, member: discord.Member = None, countt: int = None):
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")
		elif member is None:
			await ctx.send("Введите пользователя которому хотите выдать exp!")
		elif countt is None:
			await ctx.send("Введите число exp которое хотите выдать!")
		else:
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(countt, member.id))
			connection.commit()
			emb = discord.Embed(title = "Удачно!", description = f"**Администратор {ctx.author.mention} выдал ``{countt}`` exp пользователю {member.mention}**", colour = discord.Color.purple())
			await ctx.send(embed = emb)

	
	@commands.command()
	@commands.is_owner()
	async def add_lvl(self, ctx, member: discord.Member = None, countt: int = None):
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")
		elif member is None:
			await ctx.send("Введите пользователя которому хотите выдать lvl!")
		elif countt is None:
			await ctx.send("Введите какой lvl хотите выдать!")
		else:
			cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(countt, member.id))
			connection.commit()
			emb = discord.Embed(title = "Удачно!", description = f"**Администратор {ctx.author.mention} выдал ``{countt}`` lvl пользователю {member.mention}**", colour = discord.Color.purple())
			await ctx.send(embed = emb)


	@commands.command()
	@commands.is_owner()
	async def re_lvl(self, ctx, member: discord.Member = None):
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")
		elif member is None:
			await ctx.send("Введите пользователя у которого хотите обнулить уровень!")
		else:
			cursor.execute("UPDATE users SET lvl = {} WHERE id = {}".format(1, member.id))
			connection.commit()
			cursor.execute("UPDATE users SET rep = {} WHERE id = {}".format(0, member.id))
			connection.commit()
			cursor.execute("UPDATE users SET xpc = {} WHERE id = {}".format(30, member.id))
			connection.commit()
			emb = discord.Embed(title = "Удачно!", description = f"**Создатель бота {ctx.author.mention}, польностью обнулил статистику пользователю: {member.mention}**", colour = discord.Color.red())
			await ctx.send(embed = emb)

	@commands.command()
	@commands.is_owner()
	async def set_expc(self, ctx, member: discord.Member = None, countt: int = None):
		if not commands.NotOwner:
			await ctx.send("Отказано в доступе!")
		elif member is None:
			await ctx.send("Укажите пользователя!")
		elif countt is None:
			await ctx.send("Укажите число (можно использовать минус)")
		else:
			cursor.execute("UPDATE users SET xpc = {} WHERE id = {}".format(countt, member.id))
			connection.commit()
			emb = discord.Embed(title = "Удачно!", description = f"**Создатель бота {ctx.author.mention}, изменил нужное количество exp ({countt}) для нового lvl для пользователя: {member.mention}**", colour = discord.Color.red())
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(Lvl(bot))
	print('[COGS] Lvl be loaded')