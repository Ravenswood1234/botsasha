import discord
from discord.ext import commands
from config import settings
import datetime
from Cybernator import Paginator as pag

now = datetime.datetime.now()

PREFIX = settings['PREFIX']

class Helps(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	async def help(self, ctx):
		
		if ctx.invoked_subcommand is None:
			emb = discord.Embed(title = '**Команды!**', description = f'**Я предоставляю тебе список групп команд\nДля выбора определённой группы:\nВведи "{PREFIX}help moderation"!\nСписок групп:**', colour = discord.Color.purple())
			emb.set_thumbnail(url = "https://image.flaticon.com/icons/png/512/16/16686.png")
			emb.add_field(name = '**`moderation`**', value = '**Команды администрации сервера.\n `ban, kick` [...]**')
			emb.add_field(name = '**`funny`**', value = '**Команды для развлечения.\n`rpc, saper` [...]**')
			emb.add_field(name = '**`other`**', value = '**Прочии команды.\n`emoji, profile` [...]**')
			emb.add_field(name = '**`economy`**', value = '**Команды эканомики\n`work, shop` [...]**')
			emb.add_field(name = '**`lvl`**', value = '**Команды системы уровней.\n`myrep, lvl` [...]**')
			emb.add_field(name = '**`kindcoin`**', value = '**Команды системы kindcoin\n`kindcoin, buy_kindcoin` [...]**')
			
			await ctx.send(embed = emb)
		


	@help.command()
	async def moderation(self, ctx ):
		
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Команды модерации! Мой префикс: {PREFIX}** ', colour = discord.Color.red())
		emb.add_field( name = '`{}clear`'.format( PREFIX ), value = '**очистка чата (для адм)**')
		emb.add_field( name = '`{}kick`'.format( PREFIX ), value = '**Кикнуть пользователя (для адм)**\n')
		emb.add_field( name = '`{}ban `'.format( PREFIX ), value = '**Забанить пользователя (для адм)**\n')
		emb.add_field( name = '`{}say`'.format( PREFIX ), value = '**Комманда что бы бот повторил сообщения за тобой **\n')
		emb.add_field( name = '`{}warn`'.format( PREFIX ), value = '**Выдать варн пользователю**\n')
		emb.add_field( name = '`{}mute (@пользовател) (время) (s/m/h/d) (причина)`'.format( PREFIX ), value = '**Замутить пользователя**\n')
		emb.add_field( name = '`{}report`'.format( PREFIX ), value = '**Отправить репорт создателю сервера!**\n')
		emb.add_field( name = '`{}unmute`'.format( PREFIX ), value = '**Размутить пользователя**\n')
		emb.add_field( name = '`{}tempban (@пользователь) (причина) (время) (s/m/h/d)`'.format( PREFIX ), value = '**Временно Забанить пользователя (для адм)**\n')
		await ctx.send( embed = emb )


	@help.command()
	async def funny(self, ctx ):
		
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Список "Фан" команд! Мой префикс: {PREFIX}**', colour = discord.Color.blue())
		emb.add_field( name = '`{}game`'.format( PREFIX ), value = '**Игра в орл и решку**')
		emb.add_field( name = '`{}saper`'.format( PREFIX ), value = '**Игра в сапера**')
		emb.add_field( name = '`{}hello`'.format( PREFIX ), value = '**Поздороваться с ботом**')
		emb.add_field( name = '`{}fake_kick`'.format( PREFIX ), value = '**Фэйк Кик!**')
		emb.add_field( name = '`{}fake_ban`'.format( PREFIX ), value = '**Фэйк Бан!**')
		emb.add_field( name = '`{}fake_mute`'.format( PREFIX ), value = '**Фэйк Мут!**')
		emb.add_field( name = '`{}prc(камень, ножницы, бумага)`'.format( PREFIX ), value = '**Игра в камень, ножницы, бумага!**')
		emb.add_field( name = '`{}hug(@пользователь)`'.format( PREFIX ), value = '**Обнять пользователя**')
		emb.add_field( name = '`{}kiss(@пользователь)`'.format( PREFIX ), value = '**Поцеловать пользователя!**')
		emb.add_field( name = '`{}duel (@пользователя) (сумма)`'.format( PREFIX ), value = '**Играть в дуель на виртуальную вылюту (:leaves:)**')

		await ctx.send( embed = emb )


	@help.command()
	async def other(self, ctx ):
		
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Список прочих команд! Мой префикс: {PREFIX}**', colour = discord.Color.red())
		emb.add_field( name = '`{}invite_bot`'.format( PREFIX ), value = '**Получить ссылку на бота для подключения на свой сервер!**')
		emb.add_field( name = '`{}emoji (сам эмодзи)`'.format( PREFIX ), value = '**Узнать информацию о эмодзи добавленый на этот сервер**')
		emb.add_field( name = '`{}say_hello`'.format( PREFIX ), value = '**При вводе этой комманды и упоменания человека которому хотите передать привет бот будет писать ему привет ( в личные сообщения )!**')
		emb.add_field( name = '`{}cov`'.format( PREFIX ), value = '**Статистика короновируса в России**')
		emb.add_field( name = '`{}profile`'.format( PREFIX ), value = '**Информация о вашем аккаунте!**')
		emb.add_field( name = '`{}userinfo`'.format( PREFIX ), value = '**Информация о пользователе!**')
		emb.add_field( name = '`{}serverinfo`'.format( PREFIX ), value = '**Информация о сервере!**')
		emb.add_field( name = f'`{PREFIX}update`', value = '**Просмотреть историю обновлений!**')
		emb.add_field( name = '`{}math (1 число) (действие) (2 число)`'.format( PREFIX ), value = '**Простой калькулятор умеющий складывать вычитать и делить**')

		await ctx.send( embed = emb )


	@help.command()
	async def economy(self, ctx ):
		
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Список команд экономики! Мой префикс: {PREFIX}**', colour = discord.Color.green())
		emb.add_field( name = '`{}cash`'.format( PREFIX ), value = '**Узнать свой баланс**')
		emb.add_field( name = '`{}luck`'.format( PREFIX ), value = '**Мини игра в которой ваше рандомное число должно быть больше чем число бота!**')
		emb.add_field( name = '`{}br`'.format( PREFIX ), value = '**Сделать ставку в казино!**')
		emb.add_field( name = '`{}run`'.format( PREFIX ), value = '**Сыграть в гонку за :leaves:!**')
		emb.add_field( name = '`{}work`'.format( PREFIX ), value = '**Пойти на на работу (заработок: рандомно 10 - 15)**')
		emb.add_field( name = '`{}put`'.format(PREFIX), value = '**Положить деньги в банк**' )
		emb.add_field( name = '`{}with`'. format(PREFIX), value = '**Снять деньги с банка!**' )

		await ctx.send( embed = emb )


	@help.command()
	async def lvl(self, ctx):
		
		await ctx.channel.purge(limit = 1)
		emb = discord.Embed(title = f'**Список команд экономики! Мой префикс: {PREFIX}**', colour = discord.Color.blue())
		emb.add_field( name = '`{}myrep/опыт`'.format( PREFIX ), value = '**Узнать сколько у вас репутации! Если указать пользователя то вы сможите узнать его репутацию!**')
		emb.add_field( name = '`{}lvl/лвл`'.format( PREFIX ), value = '**Узнать какой у вас уровень! Если указать пользователя то вы сможите узнать его лвл!**')
		emb.add_field( name = '`{}+rep`'.format( PREFIX ), value = '**Повысить репутацию участнику!**')

		await ctx.send(embed = emb)


	@help.command()
	async def kindcoin(self, ctx):
		await ctx.channel.purge(limit = 1)
		emb = discord.Embed(ttile = f'**Список команд kindcoins! Мой префикс: {PREFIX}**', colour = discord.Color.purple())
		emb.add_field( name = f'`{PREFIX}kindcoin`', value = '**Узнать информацию о kindcoin**')
		emb.add_field( name = f'`{PREFIX}buy_kindcoin`', value = '**Купить kindcoin**')
		emb.add_field( name = f'`{PREFIX}sell_kindcoin`', value = '**Продать kindcoin**')
		emb.add_field( name = f'`{PREFIX}add_kindcoin`', value = '**Выдать kindcoin пользователю (для адм)**')
		emb.add_field( name = f'`{PREFIX}add_kindcoin`', value = '**Забрать kindcoin у пользователя (для адм)**')
		await ctx.send(embed = emb)


	@commands.command()
	async def cybernator(self, ctx):
		emb1 = discord.Embed(title = '1', description = '1 страница')
		emb2 = discord.Embed(title = '2', description = '2 страница')
		emb3 = discord.Embed(title = '3', description = '3 страница')

		embs = [emb1, emb2, emb3]

		message = await ctx.send(embed = emb1)

		page = pag(self.bot, message, only = ctx.author, use_more = False, embeds = embs)
		await page.start()


def setup(bot):
	bot.add_cog(Helps(bot))
	print('[COGS] Helps be loaded')