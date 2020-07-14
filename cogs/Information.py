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


PREFIX = settings['PREFIX']
owner = settings['OWNER']
data_create = settings['data_create']
NAME = settings['NAME BOT']


class Information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound ):
			await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))
		else:
			raise error


	@commands.command()
	async def profile(self, ctx):
		
		roles = ctx.author.roles
		role_list = ""
		for role in roles:
			role_list += f"<@&{role.id}> "
		emb = discord.Embed(title='Profile', colour = discord.Colour.purple())
		emb.set_thumbnail(url=ctx.author.avatar_url)
		emb.add_field(name='Никнэйм', value=ctx.author.mention)
		emb.add_field(name="Активность", value=ctx.author.activity)
		emb.add_field(name='Роли', value=role_list)

		if 'online' in ctx.author.desktop_status:
			emb.add_field(name="Устройство", value=":computer:Компьютер:computer:")
		elif 'online' in ctx.author.mobile_status:
			emb.add_field(name="Устройство", value=":iphone:Телефон:iphone:")
		elif 'online' in ctx.author.web_status:
			emb.add_field(name="Устройство", value=":globe_with_meridians:Браузер:globe_with_meridians:")
		emb.add_field(name="Статус", value=ctx.author.status)
		emb.add_field(name='Id', value=ctx.author.id)
		await ctx.channel.purge(limit=1)
		await ctx.send(embed = emb )


	@commands.command()
	async def userinfo(self, ctx, member: discord.Member = None):
		
		if member is None:
			await ctx.send(f'{ctx.author.name}, укажите пользователя для вывода информации!')
		roles = member.roles
		role_list = ""
		for role in roles:
			role_list += f"<@&{role.id}> "
			emb = discord.Embed(title=f'Информация о пользователе {member}', colour = 0x179c87)
			emb.set_thumbnail(url=member.avatar_url)
			emb.add_field(name='ID', value=member.id)
			emb.add_field(name='Имя', value=member.name)
			emb.add_field(name='Высшая роль', value=member.top_role)
			emb.add_field(name='Дискриминатор', value=member.discriminator)
			emb.add_field(name='Присоеденился к серверу', value=member.joined_at.strftime('%Y.%m.%d \n %H:%M:%S'))
			emb.add_field(name='Присоеденился к Discord', value=member.created_at.strftime("%Y.%m.%d %H:%M:%S"))
			emb.add_field(name='Роли', value=role_list)
			emb.set_footer(text='Вызвал команду: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
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


	@commands.command()
	async def infobot(self, ctx):
		
		emb = discord.Embed( title = '**Информация о боте:**', color = discord.Color.red())
		emb.add_field(name = 'Моё имя:', value = f'{NAME}')
		emb.add_field(name = 'Я был создан:', value = f'{data_create}')
		emb.add_field(name = 'Я написан на языке программирования:', value = 'Python')
		emb.add_field(name = 'Мой создатель:', value = f'{owner}')

		await ctx.send(embed = emb)


def setup(bot):
	bot.add_cog(Information(bot))
	print('[COGS] Information be loaded')