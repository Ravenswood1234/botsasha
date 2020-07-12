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

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Lvl(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()


	@commands.command()
	async def rep(self, ctx, member: discord.Member = None):
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


	@commands.command(aliases = ['лвл', 'левл', 'уровень'])
	async def __lvl(self, ctx, member: discord.Member = None):
		if member is None:
			emb = discord.Embed(title = '**Уровень**', description = f'**{ctx.author.name}, ваш уровень: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb)
		else:
			emb1 = discord.Embed(title = '**Уровень**', description = f'**Уровень участника {member.mention}: {cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb1)


	@commands.command()
	async def getrep(self, ctx, member: discord.Member = None):
		if member is None:
			emb = discord.Embed(title = '**Репутация**', description = f'**{ctx.author.name}, ваша репутация: {cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb)
		else:
			emb1 = discord.Embed(title = '**Репутация**', description = f'**Репутация участника {member.mention}: {cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]}!**', colour = discord.Color.red())
			await ctx.send(embed = emb1)


def setup(bot):
	bot.add_cog(Lvl(bot))
	print('[COGS] Lvl be loaded')