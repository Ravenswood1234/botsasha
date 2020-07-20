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

class Other(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def invite_bot(self, ctx):
		
		emb = discord.Embed( title = 'Ссылка на приглашения бота на свой севрер!', description = 'https://discord.com/oauth2/authorize?client_id=599587609240666123&scope=bot&permissions=2147483647 Перейди по этой ссылки и прегласи бота на севрер!', colour = discord.Color.blue())
		await ctx.send( embed = emb )


	@commands.command()
	async def say_hello(self, ctx, member: discord.Member ):
		
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = '``Привет!``', description = f'Пользователь ``{ ctx.author.name }``, передал привет ``{ member.name }``! ', colour = discord.Color.blue())
		await member.send(f'Привет { member.name }, ты в курсе что { ctx.author.name } передал тебе привет?') 
		await ctx.send( embed = emb )


	@commands.command()
	async def wiki(self, ctx, *, text):
		
		wikipedia.set_lang("ru")
		new_page = wikipedia.page(text)
		summ = wikipedia.summary(text)
		emb = discord.Embed(
			title= new_page.title,
			description= summ,
			color = 0xc582ff)
		await ctx.send(embed=emb)



	@commands.command()
	async def emoji(self, ctx, emoji: discord.Emoji):
		
		await ctx.channel.purge( limit = 1)
		e = discord.Embed(description = f"[Эмодзи]({emoji.url}) сервера {emoji}")
		e.add_field(name = "Имя:", value = f"`{emoji.name}`")
		e.add_field(name = "Автор:", value = f"{(await ctx.guild.fetch_emoji(emoji.id)).user.mention}")
		e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
		e.add_field(name = "Время добавления:", value = f"`{emoji.created_at}`")
		e.add_field(name = "ID эмодзи:", value = f"`{emoji.id}`")
		e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
		e.set_thumbnail(url = f"{emoji.url}")
		await ctx.send(embed = e)


	@commands.command(aliases=['коронавирус'])
	async def cov(self, ctx):
		
		Corona = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/#operational-data'
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

		full_page = requests.get(Corona, headers=headers)
		soup = BeautifulSoup(full_page.content, 'html.parser')

		convert = soup.findAll("div", {"class": "cv-countdown__item-value"})
		hz = soup.find("div",{"class":"cv-banner__description"})

		heads = []
		for i in convert:
			heads.append(i.string)

		emb = discord.Embed(title=f"Данные по короновирусу. {hz.string}", color=708090)
		emb.set_author(name = self.bot.user.name, icon_url = self.bot.user.avatar_url)
		emb.add_field(name="Заболело: ", value=heads[1], inline=False)
		emb.add_field(name="Выздоровело: ", value=heads[3], inline=False)
		emb.add_field(name="Умерло: ", value=heads[4], inline=False)
		emb.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Biohazard_orange.svg/1200px-Biohazard_orange.svg.png')
		await ctx.send(embed=emb)


	@commands.command()
	async def official_server(self, ctx):
		
		emb = discord.Embed( title = '**Официальный сервер бота!**', description = '**Ссылка на официальный сервер бота отправлена тебе в Личные сообщения!**')
		await ctx.send( embed = emb )
		await ctx.author.send( 'Ссылка на официальный сервер бота: https://discord.gg/Vrvypxj, по всем вопросам обращаться туда!' )


	@commands.command(aliases = ['калькулятор', 'calc', 'math'])
	async def kalc(self, ctx, amount: int = None, sho: str = None, amount2: int = None):
		if amount is None:
			await ctx.send('Введите 1 число')
		elif amount2 is None:
			await ctx.send('Введите 2 число')
		elif sho is None:
			await ctx.send('Введите действие: + - /')
		elif sho == '+':
			otv = amount + amount2
			emb1 = discord.Embed(title = '**Ответ!**', description = f'**Пример: {amount} {sho} {amount2}\nОтвет: {otv}**', colour = discord.Color.blue())
			await ctx.send(embed = emb1)
		elif sho == '-':
			otv = amount - amount2
			emb2 = discord.Embed(title = '**Ответ!**', description = f'**Пример: {amount} {sho} {amount2}\nОтвет: {otv}**', colour = discord.Color.blue())
			await ctx.send(embed = emb2)
		elif sho == '/':
			otv = amount / amount2
			emb3 = discord.Embed(title = '**Ответ!**', description = f'**Пример: {amount} {sho} {amount2}\nОтвет: {otv}**', colour = discord.Color.blue())
			await ctx.send(embed = emb3)
		else:
			await ctx.send('Вы ввели не правельный аргумент!')



	@commands.command(aliases = ['уравнение'])
	async def __rovno(self, ctx, amount: int = None, sho: str = None, amount2: int = None):
		if amount is None:
			await ctx.send('Введите 1 число уравнения!')
		elif amount2 is None:
			await ctx.send('Введите 2 число уравнения!')
		else:
			if amount == amount2:
				await ctx.send(f'Уравнение: {amount} {sho} {amount2}\nОтвет: Эти числа равны!')
			else:
				await ctx.send(f'Уравнение: {amount} {sho} {amount2}\nОтвет: Эти числа не равны!')


	@commands.command(aliases = ['сравни'])
	async def __sravni(self, ctx, amount: int = None, amount2: int = None):
		if amount is None:
			await ctx.send('введите 1 число')
		elif amount2 is None:
			await ctx.send('введите 2 число')
		else:
			if amount > amount2:
				skok = amount - amount2
				await ctx.send(f'{amount} больше чем {amount2} на {skok}')
			elif amount < amount2:
				skok = amount2 - amount
				await ctx.send(f'{amount2} больше {amount} на {skok}')
			elif amount == amount2:
				await ctx.send('Они равны!')


def setup(bot):
	bot.add_cog(Other(bot))
	print('[COGS] Other be loaded')