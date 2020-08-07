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
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {} AND guild_id = {}".format(1, member.id, ctx.guild.id))
			connection.commit()
			emb = discord.Embed(title = '**Успешно!**', description = f"""У пользователя {member.name} была повышена репутация!\nТекущия репутация: {cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}!""")
			await ctx.send(embed = emb)



	@commands.command(aliases = ['лвл', 'левл', 'уровень', 'lvl'])
	async def __lvl(self, ctx, member: discord.Member = None):

		if member is None:
			emb = discord.Embed(title = f'**Уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0]}**', description = f'Репутация {ctx.author.name}: ``{cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0]}/{cursor.execute("SELECT xpc FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0]}``\nДо следующего уровня: ``{cursor.execute("SELECT xpc FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0] - cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0]}`` репутации!', colour = discord.Color.red())
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(title = f'**Уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(member.id. ctx.guild_id)).fetchone()[0]}**', description = f'Репутация {member.name}: ``{cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}/{cursor.execute("SELECT xpc FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}``\nДо следующего уровня: ``{cursor.execute("SELECT xpc FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0] - cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}`` репутации!', colour = discord.Color.red())
			await ctx.send(embed = emb)



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
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {} AND guild_id = {}".format(countt, member.id, ctx.guild.id))
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
			cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {} AND guild_id = {}".format(countt, member.id, ctx.guild.id))
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
			cursor.execute("UPDATE users SET lvl = {} WHERE id = {} AND guild_id = {}".format(1, member.id, ctx.guild.id))
			connection.commit()
			cursor.execute("UPDATE users SET rep = {} WHERE id = {} AND guild_id = {}".format(0, member.id, ctx.guild.id))
			connection.commit()
			cursor.execute("UPDATE users SET xpc = {} WHERE id = {} AND guild_id = {}".format(30, member.id, ctx.guild.id))
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
			cursor.execute("UPDATE users SET xpc = {} WHERE id = {} AND guild_id = {}".format(countt, member.id, ctx.guild.id))
			connection.commit()
			emb = discord.Embed(title = "Удачно!", description = f"**Создатель бота {ctx.author.mention}, изменил нужное количество exp ({countt}) для нового lvl для пользователя: {member.mention}**", colour = discord.Color.red())
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(Lvl(bot))
	print('[COGS] Lvl be loaded')
