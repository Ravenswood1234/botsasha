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
from Cybernator import Paginator as pag

now = datetime.datetime.now()


PREFIX = settings['PREFIX']
owner = settings['OWNER']
data_create = settings['data_create']
NAME = settings['NAME BOT']

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound ):
			await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))
		else:
			raise error




	@commands.command()
	async def profile(self, ctx, member: discord.Member = None):
		if member is None:
			if cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] == 1:
				emb = discord.Embed(title = f'**Информация о пользователя {ctx.author.name} !**', description = '**Являеться разработчиком бота!:white_check_mark:**', colour = discord.Color.blue())
				emb.set_thumbnail(url = ctx.author.avatar_url)
				emb.add_field(name = '**Никнэйм:**', value = ctx.author.name)
				emb.add_field(name = 'ID:', value = ctx.author.id)
				emb.add_field(name = 'Дискриминатор:', value = ctx.author.discriminator)
				emb.add_field(name = 'Высшая Роль:', value = ctx.author.top_role)
				emb.add_field(name = 'Аккаунт создан:', value = ctx.author.created_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Присоединился к {ctx.guild.name:}', value = ctx.author.joined_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Уровень:', value = cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = 'Exp:', value = cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = "Предупреждений:", value = cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = "Сообщений на этом сервере:", value = cursor.execute("SELECT message_count FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.set_footer(icon_url = ctx.guild.icon_url)
				if 'online' in ctx.author.desktop_status:
					emb.add_field(name = 'Онлайн с :', value = '**Компьютера**')
				elif 'online' in ctx.author.mobile_status:
					emb.add_field(name = 'Онлайн с :', value = '**Телефона**')
				elif 'online' in ctx.author.web_status:
					emb.add_field(name = 'Онлайн с :', value = '**Браузера**')
				await ctx.send(embed = emb)
			else:
				emb = discord.Embed(title = f'**Информация о пользователя {ctx.author.name} !**', colour = discord.Color.blue())
				emb.set_thumbnail(url = ctx.author.avatar_url)
				emb.add_field(name = '**Никнэйм:**', value = ctx.author.name)
				emb.add_field(name = 'ID:', value = ctx.author.id)
				emb.add_field(name = 'Дискриминатор:', value = ctx.author.discriminator)
				emb.add_field(name = 'Высшая Роль:', value = ctx.author.top_role)
				emb.add_field(name = 'Аккаунт создан:', value = ctx.author.created_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Присоединился к {ctx.guild.name}:', value = ctx.author.joined_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Уровень:', value = cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = 'Exp:', value = cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = "Предупреждений:", value = cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(ctx.author.id, ctx.guild.id)).fetchone()[0])
				emb.set_footer(icon_url = ctx.guild.icon_url)
				if 'online' in ctx.author.desktop_status:
					emb.add_field(name = 'Онлайн с :', value = '**Компьютера**')
				elif 'online' in ctx.author.mobile_status:
					emb.add_field(name = 'Онлайн с :', value = '**Телефона**')
				elif 'online' in ctx.author.web_status:
					emb.add_field(name = 'Онлайн с :', value = '**Браузера**')
				await ctx.send(embed = emb)
		else:
			if cursor.execute("SELECT adminstaff FROM users WHERE id = {}".format(member.id)).fetchone()[0] == 1:
				emb = discord.Embed(title = f'**Информация о пользователя {member.name} !**', description = '**Являеться разработчиком бота!:white_check_mark:**',	 colour = discord.Color.blue())
				emb.set_thumbnail(url = member.avatar_url)
				emb.add_field(name = '**Никнэйм:**', value = member.name)
				emb.add_field(name = 'ID:', value = member.id)
				emb.add_field(name = 'Дискриминатор:', value = member.discriminator)
				emb.add_field(name = 'Высшая Роль:', value = member.top_role)
				emb.add_field(name = 'Аккаунт создан:', value = member.created_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Присоединился к {ctx.guild.name}:', value = member.joined_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Уровень:', value = cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = 'Exp:', value = cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = "Предупреждений:", value = cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.set_footer(icon_url = ctx.guild.icon_url)
				if 'online' in member.desktop_status:
					emb.add_field(name = 'Онлайн с:', value = '**Компьютера**')
				elif 'online' in member.mobile_status:
					emb.add_field(name = 'Онлайн с:', value = '**Телефона**')
				elif 'online' in member.web_status:
					emb.add_field(name = 'Онлайн с:', value = '**Браузера**')
				await ctx.send(embed = emb)
			else:
				emb = discord.Embed(title = f'**Информация о пользователя {member.name} !**', colour = discord.Color.blue())
				emb.set_thumbnail(url = member.avatar_url)
				emb.add_field(name = '**Никнэйм:**', value = member.name)
				emb.add_field(name = 'ID:', value = member.id)
				emb.add_field(name = 'Дискриминатор:', value = member.discriminator)
				emb.add_field(name = 'Высшая Роль:', value = member.top_role)
				emb.add_field(name = 'Аккаунт создан:', value = member.created_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Присоединился к {ctx.guild.name}:', value = member.joined_at.strftime('%A, %b %#d %Y'))
				emb.add_field(name = f'Уровень:', value = cursor.execute("SELECT lvl FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = 'Exp:', value = cursor.execute("SELECT rep FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.add_field(name = "Предупреждений:", value = cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0])
				emb.set_footer(icon_url = ctx.guild.icon_url)
				if 'online' in member.desktop_status:
					emb.add_field(name = 'Онлайн с:', value = '**Компьютера**')
				elif 'online' in member.mobile_status:
					emb.add_field(name = 'Онлайн с:', value = '**Телефона**')
				elif 'online' in member.web_status:
					emb.add_field(name = 'Онлайн с:', value = '**Браузера**')
				await ctx.send(embed = emb)




	@commands.command()
	async def serverinfo(self, ctx):

		members = ctx.guild.members
		online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
		offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
		idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
		dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
		allchannels = len(ctx.guild.channels)
		allvoice = len(ctx.guild.voice_channels)
		alltext = len(ctx.guild.text_channels)
		allroles = len(ctx.guild.roles)
		embed = discord.Embed(title=f"{ctx.guild.name}", color=discord.Color.blue(), timestamp=ctx.message.created_at)
		embed.description=(
			f":timer: Время создания севрера: **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
			f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
			f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
			f":green_circle: Онлайн: **{online}**\n\n" f":black_circle: Оффлайн: **{offline}**\n\n" f":yellow_circle: Отошли: **{idle}**\n\n"
			f":red_circle: Не трогать: **{dnd}**\n\n"
			f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
			f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
			f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
			f":keyboard: Текстовых каналов: **{alltext}**\n\n"
			f":briefcase: Всего ролей: **{allroles}**\n\n"
			f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"

		)

		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text=f"ID: {ctx.guild.id}")
		embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
		await ctx.send(embed=embed)


	@commands.command(aliases = ['инфобот', 'infobot', 'botinfo'])
	async def __infobot(self, ctx):

		emb = discord.Embed( title = '**Информация о боте:**',  color = discord.Color.purple())
		emb.description = (
			'**Меня завут:\n'
			'```Kind Bot```\n'
			'Меня создал:\n'
			'```Jhon_San.py#9232```\n'
			'Я написан на:\n'
			'```Языке Python 3.8.3```\n'
			'**Дата создания:\n'
			'```15.05.2020```\n'
			'Я состою на:**\n'
			f'```{len(self.bot.guilds)} серверах```'
			)
		await ctx.send(embed = emb)


	@commands.command()
	async def update(self, ctx):
		emb = discord.Embed(title = '**1.0**', description = '**Был добавлена команда временного бана!\nУлучшены отстальные команды модераторов!**', colour = discord.Color.red())
		emb1 = discord.Embed(title = '**1.2**', description = '**Теперь когда вы наказываете пользователя ему приходит об этом уведомления!**', colour = discord.Color.purple())
		emb2 = discord.Embed(title = '**1.5**', description = '**Обновлена команда /cash\nТеперь можно работать с банком (ложить и снимать деньги с банковского счёта)!\n /help economy**', colour = discord.Color.purple())
		emb3 = discord.Embed(title = '**2.0**', description = '**Теперь в боте есть система kindcoin\nВы сможите покупать/продавать эти коины. Их цена всегда будет меняться. Когда то падать, когда подниматься по этому успейте купить их по низкой цене а продать за дорого! Вся информация в /help kindcoin**')

		embeds = [emb, emb1, emb2, emb3]

		message = await ctx.send(embed = emb)

		page = pag(self.bot, message, only = ctx.author, use_more = False, embeds = embeds)
		await page.start()


def setup(bot):
	bot.add_cog(Information(bot))
	print('[COGS] Information be loaded')
