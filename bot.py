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

da = True

bot = commands.Bot(command_prefix = settings['PREFIX'])
bot.remove_command( 'help' )

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

PREFIX = settings['PREFIX']
owner = settings['OWNER']
data_create = settings['data_create']
NAME = settings['NAME BOT']


cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT,
        warns INT,
        bank BIGINT,
        kindcoin BIGINT,
        adminstaff INT,
        cost_kindcoin BIGINT,
        old_kindcoin BIGINT,
        message_count BIGINT
    )""")
    
cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS rp(
        hp INT,
        patrone BIGINT,
        member_id
    )""")


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name=f'/help'))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name=f'{len(bot.guilds)} серверов', type=discord.ActivityType.watching))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name=f'/update'))
        await asyncio.sleep(30)

@bot.event
async def on_ready():

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES({member.id}, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0)")
                
            else:
                pass

    connection.commit()


    print('Бот зашёл в сеть' )
    print('и он готов к работе')
    print(f'Создаель: {owner}.')
    print(f'Создан: {data_create}')
    print(f'Prefix: "{PREFIX}"')

    bot.loop.create_task(status_task())

    #await bot.change_presence(activity=discord.Game(name=f'/help | {len(bot.guilds)} серверов | /update'))

    while da is True:
        costt = random.randint(1, 10000)

        chanel = chanel = bot.get_channel(732189531402403841)

        old_costt = cursor.execute("SELECT cost_kindcoin FROM users WHERE id = {}".format(558235304138637332)).fetchone()[0]

        cursor.execute("UPDATE users SET old_kindcoin =  {} WHERE id = {}".format(old_costt, 558235304138637332))
        connection.commit()

        cursor.execute("UPDATE users SET cost_kindcoin =  {} WHERE id = {}".format(costt, 558235304138637332))
        connection.commit()
        await chanel.send(f"Стоимость KindCoins была изменена! Стоимость: {costt}")
        print(f"Стоимость KindCoins была изменена! Стоимость: {costt}")
        await asyncio.sleep(7200)

@bot.event
async def on_message(message):

    chanel = chanel = bot.get_channel(message.channel.id)

    cursor.execute("UPDATE users SET message_count = message_count + {} WHERE id = {}".format(1, message.author.id))
    connection.commit()

    cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, message.author.id))
    connection.commit()

    rep = cursor.execute("SELECT rep FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]

    if rep % 20 == 0:
        if message.author.id == 719135635272761375:
            pass
        else:
            cursor.execute("UPDATE users SET lvl = lvl + {} WHERE id = {}".format(1, message.author.id))
            connection.commit()
            new_lvl = cursor.execute("SELECT lvl FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]

            emb = discord.Embed(title = "**Lvl Up!**", description = f"**У пользователя: {message.author.name} новый уровень! ({new_lvl})**", colour = discord.Color.purple())

            await chanel.send(embed = emb)
        


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))
    elif isinstance(error, commands.CommandOnCooldown ):
        await ctx.send(f'Ошибка! Вы сможите использовать эту команду через: {round(error.retry_after)} секунд')
    else:
        raise error


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

# кмд привет
@bot.command()
async def hello(ctx):
    await ctx.send( "Приветствую!" )

@bot.command()
async def ping( ctx ):
    await ctx.send('Pong')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.environ.get('BOT_TOKEN')

bot.run(token)
