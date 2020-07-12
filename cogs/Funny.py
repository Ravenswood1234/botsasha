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

class Funny(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command()
	async def game(self, ctx):
		a = random.randint(1, 2)

		if a == 1:
			emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.blue())
			emb.add_field(name = 'Что выпало:', value = '*Вам выпал* __**орёл**__')       
			emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
			await ctx.send(embed = emb)
			emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)

		else:
			emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.red())
			emb.add_field(name = 'Что выпало:', value = '*Вам выпала* __**решка**__')        
			emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
			await ctx.send(embed = emb)
			emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)


	@commands.command()
	async def saper(self, ctx):
		embed = discord.Embed(description = '''
                     	Держи :smile:
	||0️⃣||||0️⃣||||0️⃣||||1️⃣||||1️⃣||||2️⃣||||1️⃣||||2️⃣||||1️⃣||||1️⃣||||
	2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||2️⃣||||💥||||3️⃣||||💥||||1️⃣||||
	💥||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||3️⃣||||💥||||2️⃣||||1️⃣||||
	2️⃣||||2️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||2️⃣||||1️⃣||||1️⃣||||0️⃣||||
	0️⃣||||0️⃣||||0️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||0️⃣||||0️⃣||||0️⃣||||
	1️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||
	💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||💥||||1️⃣||||
	1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||2️⃣||||1️⃣||||
	1️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||💥||||1️⃣||||0️⃣||||0️⃣||||
	💥||||2️⃣||||💥||||1️⃣||||1️⃣||||💥||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||
	1️⃣||||2️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||         
		''', color = discord.Colour.orange())
		await ctx.send(embed=embed)

	@commands.command()
	async def fake_kick(self, ctx, member: discord.Member ):
		emb = discord.Embed( title = 'Кик!', description = f'Администратор: ``{ ctx.author.name }``, кикнул пользователя: { member.mention }!', colour = discord.Color.red())
		await ctx.send( embed = emb )

	@commands.command()
	async def fake_ban(self, ctx, member: discord.Member ):
		emb = discord.Embed( title = 'Ban!', description = f'Администратор: ``{ ctx.author.name }``, забанил пользователя: { member.mention }!', colour = discord.Color.red())
		await ctx.send( embed = emb )

	@commands.command()
	async def fake_mute(self, ctx, member: discord.Member ):
		emb = discord.Embed( title = 'Мут!', description = f'Администратор: ``{ ctx.author.name }``, выдал мут: { member.mention }!', colour = discord.Color.red())
		await ctx.send( embed = emb )

	@commands.command()
	async def kiss(self, ctx, member: discord.Member):
		emb = discord.Embed(title = '💋Поцелуй!💋', description = f'**Пользователь: ``{ctx.author.name}``, поцеловал { member.mention }!💋**', colour = discord.Color.red())
		emb.set_thumbnail(url = 'https://d.radikal.ru/d43/2006/76/fb8f09103a8f.gif')
		await ctx.send( embed = emb )


	@commands.command()
	async def hug(self, ctx, member: discord.Member):
		emb = discord.Embed(title = '**Объятия!**', description = f'**Пользователь: {ctx.author.name}, обнял: {member.mention}!**', colour = discord.Color.blue())
		await ctx.send(embed = emb)


	@commands.command()
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def duel(self, ctx, member: discord.Member = None, amount: int = None ):
		a = random.randint(1, 2)
		if ctx.author == member:
			await ctx.send("С собой то вам зачем сражаться?")
			duel.reset_cooldown(ctx)
			return
		if member is None:
			await ctx.send('укажите пользователя с которым хотите саревноваться')
			duel.reset_cooldown(ctx)
		elif amount is None:
			await ctx.send('Укажите сумму за которую хотите биться!')
			duel.reset_cooldown(ctx)
		elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send(f'У вас не достаточно денег не балансе {PREFIX}cash!')
			duel.reset_cooldown(ctx)
		elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]:
			await ctx.send(f'На балансе вашего противника не хватает денег! {PREFIX}cash!')
			duel.reset_cooldown(ctx)
		else:
			emb = discord.Embed(title = 'Бой', description = f'**Пользователь: {ctx.author.mention}, кинул вызов пользователю: {member.mention}!\n Бой начался!(ожидайте 15 секунд)**')
			await ctx.send(embed = emb)
			await asyncio.sleep(15)


		if a == 1:
			emb1 = discord.Embed(title = '**Итоги!**', description = f'**И так!\nВ этом бою побеждает....\n{ctx.author.mention}!!!!\nПоздравим! Он получает {amount}:leaves:!**')
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, ctx.author.id))
			connection.commit()
			await ctx.send( embed = emb1 )
		else:
			emb2 = discord.Embed(title = '**Итоги!**', description = f'**И так!\nВ этом бою побеждает....\n{member.mention}!!!!\nПоздравим! Он получает {amount}:leaves:!**')
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			connection.commit()
			await ctx.send( embed = emb2 )

	@commands.command()
	async def rpc(self, ctx, *, arg = None):
		sho = random.choice([1, 2, 3])
		if arg is None:
			await ctx.send(f'Выберите чем будите атаковать!(камень, ножницы, бумага!)')
		elif sho == 1:
			await ctx.send(f'Ты выбрал {arg}, а бот Камень')

			if arg == 'камень':
				await ctx.send('Нечья!')
			elif arg == 'бумага':
				await ctx.send('Ты победил!')
			elif arg == 'ножницы':
				await ctx.send('Ты проиграл!')

		elif sho == 2:
			await ctx.send(f'Ты выбрал {arg}, а бот Ножницы')

			if arg == 'ножницы':
				await ctx.send('Нечья')
			elif arg == 'камень':
				await ctx.send('Ты победил')
			elif arg == 'бумага':
				await ctx.send('Ты проиграл')

		elif sho == 3:
			await ctx.send(f'Ты выбрал {arg}, а бот Бумага')

			if arg == 'бумага':
				await ctx.send('Нечья')
			elif arg == 'ножницы':
				await ctx.send('Ты выиграл!')
			elif arg == 'камень':
				await ctx.send('Ты проиграл')


	@commands.command()
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def run(self, ctx, member: discord.Member = None):
		if ctx.author == member:
			await ctx.send('Ты не может соревноваться с сомим собой...')
			run.reset_cooldown(ctx)
		elif member is None:
			await ctx.send('**Укажите пользователя с которым хотите саревноваться!**')
			run.reset_cooldown(ctx)
		else:
			emb = discord.Embed(title = '**Гонка!!**', description = f'Пользователь: {ctx.author.name}, бросил вызов в гонке пользователю: {member.mention}! Гонка началась! Ожидайте 10 секунд', colour = discord.Color.red())
			await ctx.send(embed = emb)
			await asyncio.sleep(10)
			a = random.randint(1, 2)
			embb = discord.Embed(title =  'Итоги!', description = f'**В соревнование:** {ctx.author.mention} и {member.mention}!\n **Побеждает:** {ctx.author.mention}!!\n **Поздравим!**\n **Его счёт пополнен на 1000**:leaves:', colour = discord.Color.blue())
			embbb = discord.Embed(title =  'Итоги!', description = f'**В соревнование:** {ctx.author.mention} и {member.mention}!\n **Побеждает:** {member.mention}!!\n **Поздравим!**\n **Его счёт пополнен на 1000**:leaves:', colour = discord.Color.red())
			if a == 1:
				await ctx.send(embed = embb)
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(1000, ctx.author.id))
				connection.commit()
			else:
				await ctx.send(embed = embbb)
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(1000, member.id))
				connection.commit()


	@commands.command()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def luck(self, ctx):
		number = random.randint(1, 1000)
		number2 = random.randint(1, 1000)
		if number > number2:
			emb = discord.Embed(title = '**Поздравляем!**', description = f'**Поздравляем вы выиграли!\nВаше рандомное число {number}\nРандомное число бота {number2}\nВам было выдано 50 :leaves:!**', colour = discord.Color.green())
			await ctx.send(embed = emb)
		else:
			emb1 = discord.Embed(title = '**Проигрышь**', description = f'{ctx.author.name}, к сожелению вы проиграли!\nВаше рандомное число {number}\nРандомное число бота {number2}!')
			await ctx.send(embed = emb1)


	@commands.command()
	async def giveaway(self, ctx, seconds: int, *, text):
		def time_end_form(seconds):
			h = seconds // 3600
			m = (seconds - h * 3600) // 60
			s = seconds % 60
			if h < 10:
				h = f"0{h}"
			if m < 10:
				m = f"0{m}" 
			if s < 10:
				s = f"0{s}"
			time_reward = f"{h} : {m} : {s}"
			return time_reward
		author = ctx.message.author
		time_end = time_end_form(seconds)
		message = await ctx.send(f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}")
		await message.add_reaction("🎲")
		while seconds > -1:
			time_end = time_end_form(seconds)
			text_message = f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}"
			await message.edit(content=text_message)
			await asyncio.sleep(1)
			seconds -= 1
		channel = message.channel
		message_id = message.id
		message = await channel.fetch_message(message_id)
		reaction = message.reactions[0]
		users = await reaction.users().flatten()
		user = choice(users)
		emb = discord.Embed(title = 'Итоги!', description = f'Ахтунг!\n Победитель розыгрыша - {user.mention}!\n 'f'Напишите {author.mention}, чтобы получить награду' )
		await ctx.send(embed = emb)



def setup(bot):
	bot.add_cog(Funny(bot))
	print('[COGS] Funny be loaded')