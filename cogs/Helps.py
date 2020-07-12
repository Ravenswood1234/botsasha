import discord
from discord.ext import commands
from config import settings

PREFIX = settings['PREFIX']

class Helps(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx):
		emb = discord.Embed( title = f'**Выбирите категорию! Мой префикс: {PREFIX}**', description = f'Категории: ``moderation | funny | other | economy | lvl``.    Пример: ``{PREFIX}funny``!', colour = discord.Color.red())
		await ctx.channel.purge( limit = 1)
		await ctx.send( embed = emb )


	@commands.command()
	async def moderation(self, ctx ):
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Команды модерации! Мой префикс: {PREFIX}** ', colour = discord.Color.red())
		emb.add_field( name = '`{}clear`'.format( PREFIX ), value = '**очистка чата (для адм)**')
		emb.add_field( name = '`{}kick`'.format( PREFIX ), value = '**Кикнуть пользователя (для адм)**')
		emb.add_field( name = '`{}ban `'.format( PREFIX ), value = '**Забанить пользователя (для адм)**')
		emb.add_field( name = '`{}say`'.format( PREFIX ), value = '**Комманда что бы бот повторил сообщения за тобой **')
		emb.add_field( name = '`{}warn`'.format( PREFIX ), value = '**Выдать варн пользователю**')
		emb.add_field( name = '`{}mute (@пользовател) (время) (s/m/h/d) (причина)`'.format( PREFIX ), value = '**Замутить пользователя**')
		emb.add_field( name = '`{}report`'.format( PREFIX ), value = '**Отправить репорт создателю сервера!**')
		emb.add_field( name = '`{}unmute`'.format( PREFIX ), value = '**Размутить пользователя**')
		emb.add_field( name = '`{}tempban (@пользователь) (причина) (время) (s/m/h/d)`'.format( PREFIX ), value = '**Временно Забанить пользователя (для адм)**')
		await ctx.send( embed = emb )


	@commands.command()
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


	@commands.command()
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

		await ctx.send( embed = emb )


	@commands.command()
	async def economy(self, ctx ):
		await ctx.channel.purge( limit = 1 )
		emb = discord.Embed( title = f'**Список команд экономики! Мой префикс: {PREFIX}**', colour = discord.Color.green())
		emb.add_field( name = '`{}cash`'.format( PREFIX ), value = '**Узнать свой баланс**')
		emb.add_field( name = '`{}luck`'.format( PREFIX ), value = '**Мини игра в которой ваше рандомное число должно быть больше чем число бота!**')
		emb.add_field( name = '`{}br`'.format( PREFIX ), value = '**Сделать ставку в казино!**')
		emb.add_field( name = '`{}run`'.format( PREFIX ), value = '**Сыграть в гонку за :leaves:!**')
		emb.add_field( name = '`{}work`'.format( PREFIX ), value = '**Пойти на на работу (заработок: рандомно 10 - 15)**')

		await ctx.send( embed = emb )


	@commands.command()
	async def lvl(self, ctx):
		await ctx.channel.purge(limit = 1)
		emb = discord.Embed(title = f'**Список команд экономики! Мой префикс: {PREFIX}**', colour = discord.Color.blue())
		emb.add_field( name = '`{}getrep`'.format( PREFIX ), value = '**Узнать сколько у вас репутации! Если указать пользователя то вы сможите узнать его репутацию!**')
		emb.add_field( name = '`{}уровень`'.format( PREFIX ), value = '**Узнать какой у вас уровень! Если указать пользователя то вы сможите узнать его лвл!**')
		emb.add_field( name = '`{}rep`'.format( PREFIX ), value = '**Повысить репутацию участнику!**')

		await ctx.send(embed = emb)



def setup(bot):
	bot.add_cog(Helps(bot))
	print('[COGS] Helps be loaded')