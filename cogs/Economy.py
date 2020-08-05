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

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command(aliases = ['balance', 'cash', 'bl'])
	async def __balance(self, ctx, member: discord.Member = None):
		if member is None:
			if cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] == 1:
				emb = discord.Embed(title = f'**Баланс {ctx.author.name}**', description = '**Являеться разработчиком бота :white_check_mark:**', colour = discord.Color.purple())
				emb.add_field( name = 'Наличные:', value = f'{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:' )
				emb.add_field( name = 'Банк:', value = f'{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:')
				emb.add_field( name = 'Kindcoins:', value = f'{cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :moneybag:')
				emb.set_thumbnail(url = ctx.author.avatar_url)
				await ctx.send(embed = emb)
			else:
				emb = discord.Embed(title = f'**Баланс {ctx.author.name}**', colour = discord.Color.purple())
				emb.add_field( name = 'Наличные:', value = f'{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:' )
				emb.add_field( name = 'Банк:', value = f'{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:')
				emb.add_field( name = 'Kindcoins:', value = f'{cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :moneybag:')
				emb.set_thumbnail(url = ctx.author.avatar_url)
				await ctx.send(embed = emb)
		else:
			if cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 1:
				emb = discord.Embed(title = f'**Баланс {member.name}!**', description = '**Являеться разработчиком бота :white_check_mark:**', colour = discord.Color.purple())
				emb.add_field( name = 'Наличные:', value = f'{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:' )
				emb.add_field( name = 'Банк:', value = f'{cursor.execute("SELECT bank FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:')
				emb.add_field( name = 'Kindcoins:', value = f'{cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :moneybag:')
				emb.set_thumbnail(url = member.avatar_url)
				await ctx.send(embed = emb)

			else:
				emb = discord.Embed(title = f'**Баланс {member.name}!**', colour = discord.Color.purple())
				emb.add_field( name = 'Наличные:', value = f'{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:' )
				emb.add_field( name = 'Банк:', value = f'{cursor.execute("SELECT bank FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:')
				emb.add_field( name = 'Kindcoins:', value = f'{cursor.execute("SELECT kindcoin FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :moneybag:')
				emb.set_thumbnail(url = member.avatar_url)
				await ctx.send(embed = emb)


	@commands.command()
	async def put(self, ctx, amount: int = None):
		if amount is None:
			await ctx.send('Укажите сумму которую хотите положить на свой банковский счёт!')
		elif amount is None:
			await ctx.send 
		elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send('У вас не достаточно денег на руках!')
		elif amount < 1:
			await ctx.send('Укажите число больше 1!')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			cursor.execute("UPDATE users SET bank = bank + {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Удачно!', description = f'{ctx.author.mention}, вы удачно положили на свой счёт {amount} :leaves:', colour = discord.Color.green())
			await ctx.send(embed = emb)


	@commands.command(aliases = ['with', 'снять'])
	async def __snyat(self, ctx, amount: int = None):
		if amount is None:
			await ctx.send('Укажите сумму котрую хотите снять!')
		elif amount < cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send('У вас не достаточно денег в банке!')
		elif amount < 1:
			await ctx.send('Укажите число больше чем 1!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			cursor.execute("UPDATE users SET bank = bank - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			emb = discord.Embed(title = 'Удачно!', description = f'{ctx.author.mention}, вы удачно сняли со своего счёта {amount} :leaves:', colour = discord.Color.green())
			await ctx.send(embed = emb)



	@commands.command()
	@commands.is_owner()
	async def add_money(self, ctx, member: discord.Member = None, amount: int = None):
		a = random.randint(1, 2)
		
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
		a = random.randint(1, 2)
		
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
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def br(self, ctx, amount: int = None):
		a = random.randint(1, 2)
		
		number = random.randint(1, 100)
		if amount is None:
			await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, укажите сумму!", color=0xc40d11))
			self.br.reset_cooldown(ctx)
		else:
			if amount < 0:
				await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, вы не можете испытать удачу, играя на **0** коинов!", color=0xc40d11))
				self.br.reset_cooldown(ctx)
			elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < amount:
				await ctx.send(embed = discord.Embed(description = f"**{ctx.author.mention}**, на вашем балансе не хватает коинов для ставки!", color=0xc40d11))
				self.br.reset_cooldown(ctx)
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


	@commands.command()
	async def pay(self, ctx, member: discord.Member = None, amount: int = None):
		if member is None:
			await ctx.send('Укажите пользователя!')
		elif ctx.author.id == member.id:
			await ctx.send('Ты не сможешь передать деньги самому себе!')
		elif amount is None:
			await ctx.send('Укажите сумму для передачи!')
		elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send('**У вас нет такой суммы!**')
		elif amount < 1:
			await ctx.send('Укажите число больше чем 1!')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			connection.commit()
			emb = discord.Embed(title = '**Удачно!**', description = f'**Пользователь {ctx.author.mention} передал {amount}:leaves: пользователю {member.mention}**', colour = discord.Color.green())
			await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(Economy(bot))
	print('[COGS] Economy be loaded')