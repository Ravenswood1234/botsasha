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

#WebHook
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

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
			await ctx.send(f'{ctx.author.mention}, я конечно всё понимаю но тебе нельзя использовать эту кмд!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {} AND guild_id = {}".format(1000000, ctx.author.id, ctx.guild.id))
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
			emb1 = discord.Embed(title = '**Новый вопрос!**', description = f'**Вопрос от: {ctx.author}\nСообщение:{arg}**', colour = discord.Color.blue())
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
	@commands.is_owner()
	async def add_adminstaff(self, ctx, member: discord.Member = None):
		if not commands.NotOwner:
			await ctx.send("Не доступно!!")
		elif member is None:
			await ctx.send('Укажите пользователя!')
		elif cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 1:
			await ctx.send(f'{member.mention}, и так уже являеться администратором бота')
		else:
			cursor.execute("UPDATE users SET adminstaff = {} WHERE id = {}".format(1, member.id))
			connection.commit()
			await ctx.send(f'Успешно!\nПользователь {member.mention} добавлен в админ состав бота!\nПоставил: {ctx.author.mention}')

	@commands.command()
	@commands.is_owner()
	async def remove_adminstaff(self, ctx, member: discord.Member = None):
		if not commands.NotOwner:
			await ctx.send("Не доступно!!")
		elif member is None:
			await ctx.send('Укажите пользователя!')
		elif cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 0:
			await ctx.send(f'{member.mention}, не являеться администратором бота!')
		else:
			cursor.execute("UPDATE users SET adminstaff = {} WHERE id = {}".format(0, member.id))
			connection.commit()
			await ctx.send(f'Успешно!\nПользователь {member.mention} был удалён с админ состава бота!\nСнял: {ctx.author.mention}')




	@commands.command()
	@commands.is_owner()
	async def re_money(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send("Укажите пользователя!")
		else:
			cursor.execute("UPDATE users SET cash = {} WHERE id = {} AND guild_id = {}".format(0, member.id, ctx.guild.id))
			connection.commit()
			cursor.execute("UPDATE users SET bank = {} WHERE id = {} AND guild_id = {}".format(0, member.id, ctx.guild.id))
			connection.commit()
			cursor.execute("UPDATE users SET kindcoin = {} WHERE id = {} AND guild_id = {}".format(0, member.id, ctx.guild.id))
			connection.commit()

			emb = discord.Embed(title = "Удачно!", description = f"**Администратор {ctx.author.mention} полностью обнулил деньги и кинд-коины пользователю {member.mention}!**", colour = discord.Color.purple())
			await ctx.send(embed = emb)


	@commands.command()
	@commands.is_owner()
	async def off_bot(self, ctx):
		if not commands.NotOwner:
			await ctx.send("Ошибка в доступе!")
		else:
			sendd = await ctx.send("Идёт выключение бота.")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "Идёт выключение бота..")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "Идёт выключение бота...")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "Идёт выключение бота....")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "Идёт выключение бота.....")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "Идёт выключение бота.")
			await asyncio.sleep(0.5)
			await sendd.edit(content = "**Удачно!**")
			await self.bot.logout()
			os.system("python 1")


	@commands.command()
	@commands.is_owner()
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def restart_bot(self, ctx):
		if cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] == 0:
			await ctx.send("Вы не можите использовать эту команду - т.к вы не администратор бота!")
			self.restart_bot.reset_cooldown(ctx)
		else:
			await ctx.send("Идёт перезагрузка бота!")
			await asyncio.sleep(2)
			await ctx.send("Успешно ожидайте 5 секунд пока бот прогрузиться!")
			await self.bot.logout()
			os.system("python bot.py")



	@commands.command()
	@commands.is_owner()
	async def create_role(self, ctx, name = None, perm = None):
		if name is None:
			await ctx.send("Укажите название")
		elif perm is None:
			await ctx.send("Укажите сможет ли человек с этой ролью писать сообщения. 1 - да, 0 - нет")
		else:
			role = await ctx.guild.create_role(name = name)

			if perm == "1":
				pass
			elif perm == "0":
				role.edit(send_messages = False, send_tts_messages = False)

			await ctx.send(f"Роль {name}, была удачно создана!")


			overwrite = discord.PermissionOverwrite()
			overwrite.send_messages = False
			for chat in ctx.guild.channels:
				await chat.set_permissions(role, overwrite = overwrite )



	@commands.command()
	async def news(self, ctx, embb = None, *, arg = None):
		if embb is None:
			await ctx.send("Ошибка!")
		elif arg is None:
			await ctx.send("Введите сообщение!")
		elif embb == "1":	
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url('https://discordapp.com/api/webhooks/744203890429263942/XQOaaKC5XOgFbQPcNZ3AumAUPNtGag7oM8Pzi8GC3C5UFqtqmAdoVAw-_775TZ7ePbat', adapter=AsyncWebhookAdapter(session))
				await webhook.send(embed = discord.Embed(description = arg, colour = discord.Color.purple()), username='Новости')
		elif embb == "0":
			async with aiohttp.ClientSession() as session:
				webhook = Webhook.from_url('https://discordapp.com/api/webhooks/744203890429263942/XQOaaKC5XOgFbQPcNZ3AumAUPNtGag7oM8Pzi8GC3C5UFqtqmAdoVAw-_775TZ7ePbat', adapter=AsyncWebhookAdapter(session))
				await webhook.send(arg, username='Новости')

def setup(bot):
	bot.add_cog(Owners(bot))
	print('[COGS] Owners be loaded')