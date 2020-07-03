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

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command(aliases = ['balance', 'cash'])
	async def __balance(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send( embed = discord.Embed(description = f"""Баланс Пользователя **{ctx.author}**: **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves: **"""))
		else:
			emb = discord.Embed(title = f'**Баланс: {member.name}**', description = f"""У Пользователя: {member.name}, {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}:leaves:""")
			await ctx.send(embed = emb)



	@commands.command()
	@commands.is_owner()
	async def add_money(self, ctx, member: discord.Member = None, amount: int = None):
		if member is None:
			await ctx.send(f"**{ctx.author}**, укажите пользователя которому хотите выдать деньги!")
		else:
			if amount is None:
				await ctx.send(f"**{ctx.author}**, укажите сумму которую хотите выдать!")
			elif amount < 1:
				await ctx.send(f"**{ctx.author}**, укажите сумму больше одного :leaves:!") 
			else:
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
				connection.commit()
				await ctx.send(f'Пользователю: {member.mention}, были выданы деньги!')


	@commands.command()
	@commands.is_owner()
	async def take_money(self, ctx, member: discord.Member = None, amount = None):
		if member is None:
			await ctx.send(f"**{ctx.author}**, укажите пользователя у которого хотите забрать деньги!")
		else:
			if amount is None:
				await ctx.send(f'**{ctx.author}**, укажите сумму которую хотите забрать!')
			elif amount == 'all':
				cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
				connection.commit()
				await ctx.send(f"У Пользователю: {member.mention}, были зобраны все деньги!")
			elif int(amount) < 1:
				await ctx.send(f"**{ctx.author}**, укажите сумму больше одного :leaves:!") 
			else:
				cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
				connection.commit()
				await ctx.send(f'У Пользователю: {member.mention}, были зобраны деньги!')


	@commands.command(aliases=['betroll'])
	async def br(self, ctx, amount: int = None):
		number = random.randint(1, 100)
		if amount is None:
			await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, укажите сумму!", color=0xc40d11))
		else:
			if amount < 0:
				await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, вы не можете испытать удачу, играя на **0** коинов!", color=0xc40d11))
			elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
				await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, на вашем балансе не хватает коинов для ставки!", color=0xc40d11))
			else:
				cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
				connection.commit()
				if number > 60:
					cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount *2), ctx.author.id))
					connection.commit()
					await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, выпало число **{number}**! Ты выйграл **{amount *2}** коинов!", color=0x179c87))
				else:
					await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, выпало число **{number}**! Ты проиграл **{amount}** коинов!", color=0xc40d11))


	@commands.command()
	@commands.cooldown(1, 7200, commands.BucketType.user)
	async def work(self, ctx, member: discord.Member = None):
		a = random.randint(1, 2)
		if a == 1:
			emb = discord.Embed(title = '**Работа!**', description =  f'**Пользователь: {ctx.author.name}, сходил на работу и получил 2000:leaves:!(Следующий рабочий день через 2 часа!)**')
			await ctx.send(embed = emb)
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(2000, ctx.author.id))
			connection.commit()
		else:
			emb = discord.Embed(title = '**Работа!**', description =  f'**Пользователь: {ctx.author.name}, сходил на работу и получил 2000:leaves:!(Следующий рабочий день через 2 часа!)**')
			await ctx.send(embed = emb)
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(2000, ctx.author.id))
			connection.commit()

def setup(bot):
	bot.add_cog(Economy(bot))
	print('[COGS] Economy be loaded')