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

old_cost = 0
now_cost = 10

class Kindcoin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command()
	async def kindcoin(self, ctx):
		emb = discord.Embed(title = '**Информация о kindcoin!**', description = f'**Сдесь вы сможите узнать старую и настоящию стоимость kindcoin`ов\nСтарая стоимость: {old_cost}\nНастоящия: {now_cost}**', colour = discord.Color.purple())
		emb.set_footer(text = 'Что бы купить киндоины введите /buy_kindcoin (кол-во kindcoins)')
		await ctx.send(embed = emb)


	@commands.command()
	async def buy_kindcoin(self, ctx, amount: int = None):
		cost = now_cost * amount
		if amount is None:
			await ctx.send('Введите число kindcoin которые хотите купить')
		elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < now_cost:
			await ctx.send(f'У вас не достаточно денег! Стоимость kindcoin {now_cost}')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(cost, ctx.author.id))
			connection.commit()
			cursor.execute("UPDATE users SET kindcoin = kindcoin + {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Успешно!', description = f'Пользователь {ctx.author.mention}, купил {amount}', colour = discord.Color.green())
			await ctx.send(embed = emb)


	@commands.command()
	async def sell_kindcoin(self, ctx, amount: int = None):
		cost = now_cost * amount
		if amount is None:
			await ctx.send('Введите число kindcoin которые хотите продать')
		elif cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
			await ctx.send(f'У вас не достаточно kindcoin, у вас {cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} kindcoin, а вы пытаетесь продать {amount}')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(cost, ctx.author.id))
			connection.commit()
			cursor.execute("UPDATE users SET kindcoin = kindcoin - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Успешно!', description = f'Пользователь {ctx.author.mention}, продал {amount} kindcoin', colour = discord.Color.green())
			await ctx.send(embed = emb)


	@commands.command()
	@commands.has_permissions(administrator = True)
	async def add_kindcoin(self, ctx, member: discord.Member = None, amount: int = None):
		if member is None:
			await ctx.send('Введите Пользователя которому хотите выдать kindcoins')
		elif amount is None:
			await ctx.send('Введите число kindcoin которые хотите выдать')
		elif amount > 10000:
			await ctx.send(f'{ctx.author.mention}, вы не можите выдать больше 10000 за раз!')
		else:
			cursor.execute("UPDATE users SET kindcoin = kindcoin + {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Успешно', description = f'**Администратор {ctx.author.mention}, выдал {amount} kindcoins пользователю {member.mention}**', colour = discord.Color.green())
			await ctx.send(embed = emb)


	@commands.command()
	async def take_kindcoin(self, ctx, member: discord.Member = None, amount: int = None):
		if member is None:
			await ctx.send('Введите Пользователя у которому хотите забрать kindcoins')
		elif amount is None:
			await ctx.send('Введите число kindcoin которые хотите забрать')
		elif cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] <= 0:
			await ctx.send(f'У {member}, и так осталось всево-лишь {cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} kindcoin, куда ещё то забирать??')
		else:
			cursor.execute("UPDATE users SET kindcoin = kindcoin - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Успешно', description = f'**Администратор {ctx.author.mention}, забрал {amount} kindcoins у Пользователя {member.mention}**', colour = discord.Color.green())
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(Kindcoin(bot))
	print('[COGS] kindcoin be loaded')