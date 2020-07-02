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

bot = commands.Bot(command_prefix = settings['PREFIX'])
bot.remove_command( 'help' )

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

PREFIX = settings['PREFIX']
owner = settings['OWNER']
data_create = settings['data_create']

@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT,
        warns INT
    )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES('{member}', '{member.id}', 0, 0, 1, 1)")
                
            else:
                pass

    connection.commit()


    print('Бот зашёл в сеть' )
    print('и он готов к работе')
    print(f'Создаель: {owner}.')
    print(f'Создан: {data_create}')
    print(f'Prefix: "{PREFIX}"')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))
    else:
        raise error

@bot.event
async def on_message(message):
    #Чтение лс
    await bot.process_commands(message)
    if message.author != bot.user:
        if not message.guild: # Проверка что это ЛС
            chanel = chanel = bot.get_channel(670926359375118336)
            if message.content == None:
                text = 'Пустое сообщение'
            else:
                text = message.content

            if message.attachments == []:
                file = 'Файла нет'
                filename = 'Файла нет'
            else:
                file = message.attachments[0].url
                filename = message.attachments[0].filename

            embed = discord.Embed(title = message.author.name, description = f'''
    Текст сообщения: {text}
    Название файла: {filename}
    Ccылка на файл: {file}
    '''
    ,color=discord.Colour.green()) 
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            
            await chanel.send(embed = embed)

@bot.event
async def on_guild_role_create(role):
    chanel = bot.get_channel(670926359375118336)
    async for entry in chanel.guild.audit_logs(limit = 1,action=discord.AuditLogAction.role_create):
        e = discord.Embed(colour=0x08dfab)
        e.set_author(name = 'Журнал аудита | создание роли', url = e.Empty, icon_url = 'https://media.discordapp.net/attachments/689879530542071952/711588305506140241/verdict.png?width=407&height=407')
        e.add_field(name = "Роль:", value = f"<@&{entry.target.id}>")
        e.add_field(name = "ID роли:", value = f"{entry.target.id}")
        e.add_field(name = "‎‎‎‎", value = "‎‎‎‎",)
        e.add_field(name = "Создал:", value = f"{entry.user.mention}")
        e.add_field(name = "ID создавшего:", value = f"{entry.user.id}")
        e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
        await chanel.send(embed=e)
        return
@bot.event
async def on_guild_role_delete(role):
    chanel = bot.get_channel(670926359375118336)
    async for entry in chanel.guild.audit_logs(action=discord.AuditLogAction.role_delete):
        e = discord.Embed(colour=0xe84444)
        e.set_author(name = 'Журнал аудита | удаление роли', url = e.Empty, icon_url = 'https://media.discordapp.net/attachments/689879530542071952/711588305506140241/verdict.png?width=407&height=407')
        e.add_field(name = "Роль:", value = f"{role.name}")
        e.add_field(name = "ID роли:", value = f"{entry.target.id}")
        e.add_field(name = "‎‎‎‎", value = "‎‎‎‎",inline=False)
        e.add_field(name = "Удалил:", value = f"{entry.user.mention}")
        e.add_field(name = "ID удалившего:", value = f"{entry.user.id}")
        await chanel.send(embed=e)
        return



# авто выдача роли ага да
@bot.event
async def on_member_join( member ):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES('{member}', '{member.id}', 0, 0, 1, 0)")
        connection.commit()
    else:
        pass




    emb = discord.Embed( title = 'Привет💜', description = f' { member.name } Спасибо  что зашел(зашла), если хочешь ознакомиться с моими командами то пиши `{PREFIX}help`', color = discord.Color.red())
    channel = bot.get_channel( 670921220736155649 )

    role = discord.utils.get( member.guild.roles, id = 719173358838743050 )

    await member.add_roles( role )
    await channel.send( embed = emb )   

# тестовая кмд
@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def test(ctx, arg):  # создаем асинхронную фунцию бота
    await ctx.send(arg)  # отправляем обратно аргумент 


@bot.command()
async def help(ctx):
    emb = discord.Embed( title = f'**Выбирите категорию! Мой префикс: {PREFIX}**', description = f'Категории: ``moderation | funny | other | economy``.    Пример: ``{PREFIX}help_moderation``!', colour = discord.Color.red())
    await ctx.channel.purge( limit = 1)
    await ctx.send( embed = emb )

@bot.command()
async def help_moderation( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = f'**Команды модерации! Мой префикс: {PREFIX}** ', colour = discord.Color.red())
    emb.add_field( name = '`{}clear`'.format( PREFIX ), value = '**очистка чата (для адм)**')
    emb.add_field( name = '`{}kick`'.format( PREFIX ), value = '**Кикнуть пользователя (для адм)**')
    emb.add_field( name = '`{}ban`'.format( PREFIX ), value = '**Забанить пользователя (для адм)**')
    emb.add_field( name = '`{}say`'.format( PREFIX ), value = '**Комманда что бы бот повторил сообщения за тобой **')
    emb.add_field( name = '`{}warn`'.format( PREFIX ), value = '**Выдать варн пользователю**')
    await ctx.send( embed = emb )



@bot.command()
async def help_funny( ctx ):
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

@bot.command()
async def help_other( ctx ):
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


@bot.command()
async def help_economy( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = f'**Список команд экономики! Мой префикс: {PREFIX}**', colour = discord.Color.green())
    emb.add_field( name = '`{}cash`'.format( PREFIX ), value = '**Узнать свой баланс**')
    emb.add_field( name = '`{}luck(число 1 - 1000)`'.format( PREFIX ), value = '**Мини игра в котороый вы должны назвать число которое будет больше чем число бота!**')
    emb.add_field( name = '`{}br`'.format( PREFIX ), value = '**Сделать ставку в казино!**')
    emb.add_field( name = '`{}run`'.format( PREFIX ), value = '**Сыграть в гонку за :leaves:!**')
    emb.add_field( name = '`{}work`'.format( PREFIX ), value = '**Пойти на на работу (заработок: рандомно 10 - 15)**')

    await ctx.send( embed = emb )


@bot.command()
@commands.is_owner()
async def inplay( ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send("Отказано в доступе!")
    else:
        await bot.change_presence(activity=discord.Game(name=arg))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def inwatch( ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send("Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def inlisten (ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send("Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def instream( ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send("Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.streaming))
        await ctx.send( embed = emb )

@bot.command()
async def buy_role( ctx, role: discord.Role = None):
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

            await ctx.send(f'Пользователь {ctx.author}, купил новую роль!')

@bot.command()
async def shop(ctx):
    emb = discord.Embed(title = 'Магазин ролей!', )

    for row in  cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
        if ctx.guild.get_role(row[0]) != None:
            emb.add_field(
                name = f"Стоимость {row[1]}",
                value = f"Назвние роли: {ctx.guild.get_role(row[0]).mention}",
                inline = False
                )

    await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions( administrator = True )
async def remove_shop( ctx, role: discord.Role = None):
    emb = discord.Embed( title = 'Роль удалена!', description = f'Пользователь {ctx.author}, удалил роль из магазина!', colour = discord.Color.red())
    if role is None:
        await ctx.send(f'**{ctx.author}**, Укажите роль которую хотите удалить!')
    else:
        cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
        connection.commit()
        await ctx.send( embed = emb )

@bot.command()
@commands.has_permissions( administrator = True )
async def add_shop( ctx, role: discord.Role = None, cost: int = None ):
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

# кмд привет
@bot.command()
async def hello(ctx):
    await ctx.send( "Приветствую!" )
    
@bot.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    await ctx.channel.send(':: Сообщения успешно удалены ::')

@clear.error
@commands.has_permissions( administrator = True )
async def clear_error(ctx, error):
    if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите количество сообщения для удаления!!')

    
@bot.command()
@commands.has_permissions( administrator = True)
async def kick( ctx, member: discord.Member, *, reason = None):
    if member is None:
        await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите кикнуть!')
    elif reason is None:
        await ctx.send(f'{ctx.author.mention}, укажите причину кика!')
    else:
        emb = discord.Embed( title = 'Кик!', description = f'**Администратор: ``{ ctx.author.name }``\n Кикнул пользователя: { member.mention },\nПричина: {reason}!**', colour = discord.Color.red())
        await member.kick( reason = reason )
        await ctx.send( embed = emb )

@kick.error
async def kick_error(ctx, error):
    if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите кикнуть!!')


@bot.command()
@commands.has_permissions( administrator = True)
async def ban( ctx, member: discord.Member, *, reason = None):
    if member is None:
        ctx.send('укажите пользователя которого хотите забанить!')
    elif reason is None:
        await ctx.send(f'{ctx.author.mention}, укажите причину бана!')
    else:
        emb = discord.Embed( title = '**Бан**', description = f'**Администратор: {ctx.author.mention}\n Забанил пользователя: {member.mention}\nПричина: {reason}**', colour = discord.Color.red())
        await ctx.channel.purge( limit = 1 )
        await member.ban( reason = reason )
        await ctx.send( embed = emb )

@ban.error
async def ban_error(ctx, error):
    if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите забанить!')


# пргласить бота
@bot.command()
async def invite_bot(ctx):
    emb = discord.Embed( title = 'Ссылка на приглашения бота на свой севрер!', description = 'https://discord.com/oauth2/authorize?client_id=599587609240666123&scope=bot&permissions=2147483647 Перейди по этой ссылки и прегласи бота на севрер!',
    colour = discord.Color.blue())
    await ctx.send( embed = emb )


# эмодзи
@bot.command(aliases = ["емодзи", "емоджи", "эмоджи", "эмоция"])
async def emoji(ctx, emoji: discord.Emoji):
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

@bot.command()
async def say_hello( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = '``Привет!``', description = f'Пользователь ``{ ctx.author.name }``, передал привет ``{ member.name }``! ', colour = discord.Color.blue())
    await member.send(f'Привет { member.name }, ты в курсе что { ctx.author.name } передал тебе привет?') 
    await ctx.send( embed = emb )

@bot.command()
async def game(ctx):
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

@bot.command()
async def saper(ctx):
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

@bot.command(aliases=['коронавирус'])
async def cov(ctx):
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
    emb.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
    emb.add_field(name="Заболело: ", value=heads[1], inline=False)
    emb.add_field(name="Выздоровело: ", value=heads[3], inline=False)
    emb.add_field(name="Умерло: ", value=heads[4], inline=False)
    emb.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Biohazard_orange.svg/1200px-Biohazard_orange.svg.png')
    await ctx.send(embed=emb)


@bot.command()
async def ping( ctx ):
    await ctx.send('Pong')

# Profile
@bot.command(pass_context=True)
async def profile(ctx):
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

@bot.command()
async def fake_kick( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Кик!', description = f'Администратор: ``{ ctx.author.name }``, кикнул пользователя: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def fake_ban( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Ban!', description = f'Администратор: ``{ ctx.author.name }``, забанил пользователя: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def fake_mute( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Мут!', description = f'Администратор: ``{ ctx.author.name }``, выдал мут: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def official_server( ctx ):
    emb = discord.Embed( title = '**Официальный сервер бота!**', description = '**Ссылка на официальный сервер бота отправлена тебе в Личные сообщения!**')

    await ctx.send( embed = emb )
    await ctx.author.send( 'Ссылка на официальный сервер бота: https://discord.gg/Vrvypxj, по всем вопросам обращаться туда!' )

@bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ,
        color = 0xc582ff)

    await ctx.send(embed=emb)

@bot.command(aliases = ['balance', 'cash'])
async def __balance( ctx, member: discord.Member = None):
    if member is None:
        await ctx.send( embed = discord.Embed(
            description = f"""Баланс Пользователя **{ctx.author}**: **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves: **"""
        ))

@bot.command()
@commands.has_permissions( administrator = True)
async def add_money( ctx, member: discord.Member = None, amount: int = None):
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
    

@bot.command()
async def take_money( ctx, member: discord.Member = None, amount = None):
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


@bot.command()
@commands.is_owner()
async def game_help(ctx, *, arg):
    emb = discord.Embed(title = 'Успешно!', description = f'Мистер {owner}! Секретная кмд была выполнена!', colour = discord.Color.blue())

    if not commands.NotOwner:
        await ctx.send(f'Прости {ctx.author.name}, но ты не такой классный что бы использовать эту команду(')

    else:
        await bot.change_presence(activity=discord.Game(name="/help"))
        await ctx.send(embeb = emb)

@bot.command()
async def kiss(ctx, member: discord.Member):
    emb = discord.Embed(title = '💋Поцелуй!💋', description = f'**Пользователь: ``{ctx.author.name}``, поцеловал { member.mention }!💋**', colour = discord.Color.red())
    emb.set_thumbnail(url = 'https://d.radikal.ru/d43/2006/76/fb8f09103a8f.gif')
    await ctx.send( embed = emb )


@bot.command()
async def hug(ctx, member: discord.Member):
    emb = discord.Embed(title = '**Объятия!**', description = f'**Пользователь: {ctx.author.name}, обнял: {member.mention}!**', colour = discord.Color.blue())

    await ctx.send(embed = emb)

@bot.command(aliases=['betroll'])
async def br(ctx, amount: int = None):
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

@bot.command()
async def mute(ctx, member: discord.Member, duration: int, *, arg = None):
    emb = discord.Embed(title='MUTE')
    role = discord.utils.get(ctx.guild.roles, name="mute")

    if member is None:
        await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите замутить')
    elif duration < 1:
        await ctx.send(f'{ctx.author.name}, укажите время мута больше чем 1 секунда!')
    elif arg in None:
        await ctx.send(f'{ctx.author.name}, укажите причину мута!')
    else:
        emb.add_field(name="Замутил:",
                    value=f'{ctx.author.mention} __**замутил**__: {member.mention} __**на {duration} секунд.**__')
        emb.add_field(name="Причина:", value=f'__*{arg}*__')
        await ctx.send(embed=emb)
        await member.add_roles(role)
        await asyncio.sleep(duration)
        embed = discord.Embed(description=f'Товарищ {member.mention} успешно прошёл курс оздаровления от мута).',
                            color=discord.Colour.green())
        await ctx.send(embed=embed)
        await member.remove_roles(role)

@mute.error
async def mute_error(ctx, error):
   if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите замутить или же время мута/причину!!')


@bot.command()
async def translate(ctx, lang: str, r: str, *, text):
    t = Translator()
    result = t.translate(text, src = lang, dest = r)
    emb = discord.Embed(title = 'Перевод:', colour = discord.Colour.green())
    emb.add_field(name = 'Перевод', value = result.text)
    await ctx.send(embed = emb)

@bot.command()
async def userinfo(ctx, member: discord.Member):
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

@bot.command()
async def run(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send('**Укажите пользователя с которым хотите саревноваться!**')
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

@bot.command()
async def giveaway(ctx, seconds: int, *, text):
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


@bot.command()
async def serverinfo(ctx):
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

@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=discord.Embed(title="Не бузи!", description=f":x: **{ctx.author.mention}**, укажи **сообщение**, которое хочешь отправить от именни **бота** :x:", color=0xFF0000))
    else:
        await ctx.channel.purge(limit = 1)
        await ctx.send(arg)
        
        print(f'[log Command] Была использована команда - >say. Использовал - Администратор: {ctx.author}\n')

@bot.command()
@commands.has_permissions(administrator = True)
async def warn(ctx, member: discord.Member = None):
    if ctx.author == member:
        await ctx.send(f'{ctx.author}, ты умный или что то?, зачем себе варн выдаёшь?')
    elif member is None:
        await ctx.send(f'{ctx.author.mention}, обязательно укажите пользователя которому хотите выдать варн!')
    else:
        emb = discord.Embed(title = '**Warn**', description = f'**Администратор: {ctx.author.mention}\n Нарушитель: {member.mention}.\nКоличество Варнов: {cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**')

        cursor.execute("UPDATE users SET warns = warns + {} WHERE id = {}".format(1, member.id))
        connection.commit()

        await ctx.send(embed = emb)

@bot.command()
@commands.has_permissions(administrator = True)
async def unwarn(ctx, member: discord.Member = None):
    if member is None:
        ctx.send(f'{ctx.author.mention}, укажите пользователя у которого хотите снять варн!')
    else:
        cursor.execute("UPDATE users SET warns = warns - {} WHERE id = {}".format(1, member.id))
        connection.commit()
        emb = discord.Embed( title = '**Успешно!**', description = f'**У пользователя {member.mention}, был снят варн!\nКол-во варнов: {cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**')
        
        await ctx.send(embed = emb)


@bot.command()
async def work(ctx, member: discord.Member = None):
    a = random.randint(1, 2)
    if a == 1:
        emb = discord.Embed(title = '**Работа!**', description =  f'**Пользователь: {ctx.author.name}, сходил на работу и получил 10:leaves:!**')
        await ctx.send(embed = emb)
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(10, ctx.author.id))
        connection.commit()
    else:
        emb = discord.Embed(title = '**Работа!**', description =  f'**Пользователь: {ctx.author.name}, сходил на работу и получил 15:leaves:!**')
        await ctx.send(embed = emb)
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(15, ctx.author.id))
        connection.commit()



for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded:")
            raise e

@bot.command()
@commands.is_owner()
async def secret_222(ctx, member: discord.Member = None):
    if not commands.NotOwner:
        await ctx.send(f'{ctx.author.mention}, с конечно всё понимаю но тебе нельзя использовать эту кмд!')

    else:
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(1000000, ctx.author.id))
        connection.commit()
        await ctx.channel.purge(limit = 1)
        await ctx.send('Команда была выполнена!')
        print(f'Пользователь {owner}, выполнил Секретную кмд!')

@bot.command()
async def duel(ctx, member: discord.Member = None, amount: int = None ):
    a = random.randint(1, 2)
    if ctx.author == member:
        await ctx.send("С собой то вам зачем сражаться?")
        return
    if member is None:
        await ctx.send('укажите пользователя с которым хотите саревноваться')
    elif amount is None:
        await ctx.send('Укажите сумму за которую хотите биться!')
    elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
        await ctx.send(f'У вас не достаточно денег не балансе {PREFIX}cash!')
    elif amount > cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]:
        await ctx.send(f'На балансе вашего противника не хватает денег! {PREFIX}cash!')
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


@bot.command()
async def luck(ctx, *, amount: int = None):
    number = random.randint(1, 1000)
    if amount is None:
        await ctx.send(f'{ctx.author.mention}, укажите ваше число!(1 - 1000)')
    elif amount > 1000:
        await ctx.send(f'{ctx.author.mention}, вы указали слишком большое число, укажите правильное число(1 - 1000)')
    elif number > amount:
        emb = discord.Embed(title = '**Проигрыш!**', description = f'{ctx.author.mention}, к сожелению вы проиграли!\nЧисло выбраное ботом: {number}\nВаше число:{amount}', colour = discord.Color.red())
        await ctx.send(embed = emb)
    else:
        emb1 = discord.Embed(title = '**Поздравляем!**', description = f'{ctx.author.mention}, Поздравляем вы выиграли!\nВаше число: {amount},\n Число бота: {number}\nНа ваш счёт зачисленно 400:leaves:', colur = discord.Color.green())
        await ctx.send(embed = emb1)
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(400, ctx.author.id))
        connection.commit()

@bot.command()
async def rpc(ctx, *, arg = None):
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

token = os.environ.get(BOT_TOKEN)

bot.run(str(token))
