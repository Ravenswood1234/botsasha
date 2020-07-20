import discord
from discord.ext import commands
import bot
import sqlite3
import asyncio
import random
import datetime

now = datetime.datetime.now

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Shop(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect('server.db')
		self.cursor = self.connection.cursor()

	@commands.command()
	async def shop(self, ctx):
		emb = discord.Embed(title = 'Магазин ролей!', )

		for row in  cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
			if ctx.guild.get_role(row[0]) != None:
				emb.add_field(
				name = f"Стоимость {row[1]}",
				value = f"Назвние роли: {ctx.guild.get_role(row[0]).mention}",
				inline = False
				)

		await ctx.send(embed = emb)


	@commands.command()
	@commands.has_permissions( administrator = True )
	async def add_shop(self, ctx, role: discord.Role = None, cost: int = None ):
		
		emb = discord.Embed(title = 'Успешно!', description = 'В магазин была успешно добавлено новая роль!', colour = discord.Color.red())

		if role is None:
			await ctx.send(f'**{ctx.author}**, Укажите роль которую хотите продавать!')
		else:
			if cost is None:
				await ctx.send(f'**{ctx.author}**, Укажите стоимость указанной роли!')
			elif cost < 0:
				await ctx.send(f'**{ctx.author}**, вы указали стоимость меньшe 0. Так нельзя!')
			else:
				cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
				connection.commit()

				await ctx.send(embed = emb)



	@commands.command()
	async def buy_role(self, ctx, role: discord.Role = None):
		
		if role is None:
			await ctx.send(f'**{ctx.author}**, укажите роль которую хотите купить!')
		else:
			if role in ctx.author.roles:
				await ctx.send(f'**{ctx.author}**, данная роль уже присуствует у вас!')
			elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
				await ctx.send(f'**{ctx.author}**, у вас не хватает денег!')
			else:
				await ctx.author.add_roles(role)
				cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				connection.commit()

				emb = discord.Embed(title = 'Успешно!', description = f'**Пользователь {ctx.author.mention}, купил роль: {role}**')
				await ctx.send(embed = emb)
        
        


	@commands.command()
	@commands.has_permissions( administrator = True )
	async def remove_shop(self, ctx, role: discord.Role = None):
		
		emb = discord.Embed( title = 'Роль удалена!', description = f'Пользователь {ctx.author}, удалил роль из магазина!', colour = discord.Color.red())
		if role is None:
			await ctx.send(f'**{ctx.author}**, Укажите роль которую хотите удалить!')

		else:
			cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
			connection.commit()
			await ctx.send( embed = emb )


def setup(bot):
	bot.add_cog(Shop(bot))
	print('[COGS] Shop be loaded')