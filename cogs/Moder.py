import discord
from discord.ext import commands
import asyncio
import random
import sqlite3
import datetime

now = datetime.datetime.now()

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect('server.db')
        self.cursor = self.connection.cursor()

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def say(self, ctx, *, arg=None):

        if arg is None:
            await ctx.send(embed=discord.Embed(title="Не бузи!", description=f":x: **{ctx.author.mention}**, укажи **сообщение**, которое хочешь отправить от именни **бота** :x:", color=0xFF0000))
        else:
            await ctx.channel.purge(limit = 1)
            await ctx.send(arg)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount: int = None):

        if amount is None:
            pass

        else:

            amount1 = amount + 1

            await ctx.channel.purge(limit = amount1)
            emb = discord.Embed(title = '**Удаление!**', description = f'**{ctx.author.mention}, удачно удалил сообщения!\nКоличество: {amount}!**', colour = discord.Color.green())
            await ctx.channel.send(embed = emb)
            await asyncio.sleep(2)
            await ctx.channel.purge(limit = 1)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):

        if member is None:
            await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите кикнуть!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину кика!')
        else:
            emb = discord.Embed( title = 'Кик!', description = f'**Администратор: ``{ ctx.author.name }``\nКикнул пользователя: { member.mention },\nПричина: {reason}!**', colour = discord.Color.red())
            await member.send(f'**{member.mention}, вы были кукнуты с сервера: {ctx.guild.name}\nАдминистратор: {ctx.author.name}\nПричина: {reason}**')
            await member.kick( reason = reason )
            await ctx.send( embed = emb )


    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):

        if member is None:
            ctx.send('укажите пользователя которого хотите забанить!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину бана!')
        else:
            emb = discord.Embed( title = '**Бан**', description = f'**Администратор: {ctx.author.mention}\n Забанил пользователя: {member.mention}\nПричина: {reason}**', colour = discord.Color.blue())
            await ctx.channel.purge( limit = 1 )
            await member.send(f'{member.mention}, вы были забанены на всегда!\nСервер: {ctx.guild.name}\nАдминистратор: {ctx.author.name}\nПричина: {reason}')
            await member.ban( reason = reason )
            await ctx.send( embed = emb )



    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member: discord.Member = None, duration: int = None, tm: str = None, *, arg = None):

        try:

            emb = discord.Embed(title='Mute', colour = discord.Color.purple())
            role = discord.utils.get(ctx.guild.roles, name="mute")

            if member is None:
                await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите замутить Пример: /mute @Jhon_San 10 d Оск')
            elif tm is None:
                await ctx.send('Укажите сколько будет действовать мут s = секунд, m = минут, h = час, d = день Пример: /mute @Jhon_San 10 d Оск')
            elif duration < 1:
                await ctx.send(f'{ctx.author.name}, укажите время мута больше чем 1 секунда! Пример: /mute @Jhon_San 10 d Оск')
            elif arg is None:
                await ctx.send(f'{ctx.author.name}, укажите причину мута! Пример: /mute @Jhon_San 10 d Оск')
            else:
                emb.add_field(name="Администратор:", value=f'{ctx.author.mention} **замутил пользователя**: {member.mention} __**на  {duration} {tm}.**__')
                emb.add_field(name="Причина:", value=f'**{arg}**')
                await ctx.send(embed=emb)
                await member.add_roles(role)
                await member.send(f'{member.mention}, на сервере "{ctx.guild.name}", вам был выдан мут на {duration}{tm}\nПричина: {arg}')
                if tm == 's':
                    await asyncio.sleep(duration)
                elif tm == 'm':
                    await asyncio.sleep(duration * 60)
                elif tm == 'h':
                    await asyncio.sleep(duration * 3600)
                elif tm == 'd':
                    await asyncio.sleep(duration * 86400)
                embed = discord.Embed(title = "**Время прошло!**", description = f'**У пользователя {member.mention}, прошло время мута!({duration}{tm})**', colour = discord.Color.green())
                await ctx.send(embed=embed)
                await member.remove_roles(role)
        except:
            role = await ctx.guild.create_role(name="mute")

            await role.edit(name='mute', send_messages=False, send_tts_messages=False, read_messages=True, hoist=True)
            rolee = discord.utils.get(ctx.guild.roles, name = "mute")

            emb.add_field(name="Администратор:", value=f'{ctx.author.mention} **замутил пользователя**: {member.mention} __**на  {duration} {tm}.**__')
            emb.add_field(name="Причина:", value=f'**{arg}**')
            await ctx.send(embed=emb)
            await member.add_roles(role)
            await member.send(f'{member.mention}, на сервере "{ctx.guild.name}", вам был выдан мут на {duration}{tm}\nПричина: {arg}')
            if tm == 's':
                await asyncio.sleep(duration)
            elif tm == 'm':
                await asyncio.sleep(duration * 60)
            elif tm == 'h':
                await asyncio.sleep(duration * 3600)
            elif tm == 'd':
                await asyncio.sleep(duration * 86400)
            embed = discord.Embed(title = "**Время прошло!**", description = f'**У пользователя {member.mention}, прошло время мута!({duration}{tm})**', colour = discord.Color.green())
            await ctx.send(embed=embed)
            await member.remove_roles(role)

            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            for chat in ctx.guild.channels:
                await chat.set_permissions(rolee, overwrite=overwrite)


    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def unwarn(self, ctx, member: discord.Member = None, *, arg = None):

        if member is None:
            ctx.send(f'{ctx.author.mention}, укажите пользователя у которого хотите снять варн!')
            self.unwarn.reset_cooldown(ctx)
        else:
            if arg == "all":
                cursor.execute("UPDATE users SET warn = {} WHERE id = {} AND guild_id = {}".format(0, member.id, ctx.guild.id))
                connection.commit()
                emb = discord.Embed( title = '**Успешно!**', description = f'**У пользователя {member.mention}, были сняты все варн!**', colour = discord.Color.green())
                await ctx.send(embed = emb)
            elif arg is None:
                cursor.execute("UPDATE users SET warn = warn - {} WHERE id = {} AND guild_id = {}".format(1, member.id, ctx.guild.id))
                connection.commit()
                emb = discord.Embed( title = '**Успешно!**', description = f'**У пользователя {member.mention}, был снят варн!\nКол-во варнов: {cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}**', colour = discord.Color.green())
                await ctx.send(embed = emb)


    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: discord.Member = None):

        role = discord.utils.get(ctx.guild.roles, name="mute")
        if member is None:
            await ctx.send(f'{ctx.author.mention}, вы не указали пользователя!')
        else:
            await ctx.send('**Удачно!**')
            await member.remove_roles(role)


    @commands.command()
    async def report(self, ctx, *, arg):

        chanel = chanel = self.bot.get_channel(719146135905894461)
        if arg is None:
            await ctx.send(f'{ctx.author.mention}, вы не указали причину репорта!')
        else:
            emb = discord.Embed(title = '**Успешно!**', description = f'{ctx.author.mention}, вы успешно отправили репорт создателю бота!\nВ скором времени он свяжеться с вами!', colour = discord.Color.green())
            await ctx.send(embed = emb)
            emb1 = discord.Embed(title = '**Репорт!**', description = f'Репорт от: {ctx.author}\nСодержания: {arg}')
            await chanel.send(embed = emb1)



    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def tempban(self, ctx, member: discord.Member = None, amount: int = None, tm: str = None, *, reason = None):

        if member is None:
            await ctx.send(f'{ctx.author.mention}, укажите пользователя которого хотите временно забанить!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину бана!')
        elif amount is None:
            await ctx.send(f'{ctx.author.mention}, укажите время бана!')
        elif tm is None:
            await ctx.send('Укажите сколько будет действовать бан s = секунд, m = минут, h = часов, d = дней')
        else:
            emb = discord.Embed(title = '**Бан!**', description = f'**Администратор: {ctx.author.mention}\nНарушитель:{member.mention}\nПричина: {reason}\nВремя бана:{amount}{tm}!**', colour = discord.Color.blue())
            await member.send(f'{member.mention}, вы были временно забанены на сервере: {ctx.guild.name}\nАдминистратор: {ctx.author.name}\nВремя: {amount}{tm}\nПричина: {reason}')
            await member.ban(reason = reason)
            await ctx.send(embed = emb)
            if tm == 's':
                await asyncio.sleep(amount)
            elif tm == 'm':
                await asyncio.sleep(amount * 60)
            elif tm == 'h':
                await asyncio.sleep(amount * 3600)
            elif tm == 'd':
                await asyncio.sleep(amount * 86400)
            emb1 = discord.Embed(title = '**Разбан!**', description = f'**У {member.mention}, прошло время бана!({amount}{tm})**', colour = discord.Color.green())
            await ctx.guild.unban(member)
            await ctx.send(embed = emb1)



    @commands.command()
    @commands.has_permissions(administrator = True)
    async def give_role(self, ctx, member: discord.Member = None, role: discord.Role = None):

        await ctx.channel.purge(limit = 1)
        if member is None:
            await ctx.send("укажите пользователя!")
        elif ctx.author == member:
            await ctx.send(f'{ctx.author.mention} ты не можешь выдать роль самому себе!')
        elif role is None:
            await ctx.send('Укажите роль!')
        else:
            await member.add_roles(role)
            emb = discord.Embed(title = '**Успешно!**', description = f'**Администратор {ctx.author.mention} выдал роль пользователю {member.mention}\n({role.mention})**', colour = discord.Color.purple())
            await ctx.send(embed = emb)

            print(f'{ctx.author.name} использовал Команду /give_role')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def take_role(self, ctx, member: discord.Member = None, role: discord.Role = None):

        await ctx.channel.purge(limit = 1)
        if not commands.NotOwner:
            await ctx.send("Не доступно!!")
        elif ctx.author == member:
            await ctx.send(f'{ctx.author.mention} ты не можешь снять роль самому себе!')
        elif member is None:
            await ctx.send("укажите пользователя!")
        elif role is None:
            await ctx.send('Укажите роль!')
        else:
            await member.remove_roles(role)
            emb = discord.Embed(title = '**Успешно!**', description = f'**Администратор {ctx.author.mention} забрал роль у пользователю {member.mention}\n ({role.mention})**', colour = discord.Color.purple())
            await ctx.send(embed = emb)

            print(f'{ctx.author.name} использовал Команду /take_role')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, вы не можите использовать эту команду!')
        elif isinstance(error, commands.BadArgument):
            await ctx.send("**Вы не правельно ввели аргументы!**")


    @commands.command(aliases = ['посчитай', 'Посчитай'])
    @commands.has_permissions(administrator = True)
    async def __blyat(self, ctx, lol: int = None):

        if lol is None:
            await ctx.send(f'{ctx.author.mention}, введи число до которого будет считать бот!')
        xd = 1
        while xd <= lol:
            await ctx.send(f'{xd}')
            await asyncio.sleep(1)
            xd = xd + 1


    @commands.command()
    async def say_embed(self, ctx, *, arg):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(description = f'{arg}', colour = discord.Color.purple())
        await ctx.send(embed = emb)


    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def say_channel(self, ctx, chanel: discord.TextChannel = None, *, mesage = None):
        if chanel is None:
            await ctx.send("Введите название канала! на пример #chat")
        elif mesage is None:
            await ctx.send("Введите сообщение!")
        else:
            await ctx.channel.purge(limit = 1)
            await chanel.send(f"{mesage}")
            emb = discord.Embed(title = "**Удачно!**", description = f"**Бот успешно отправил сообщение: '{mesage}' в канал: '{chanel}'**", colour = discord.Color.green())
            await ctx.send(embed = emb)



    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def warn(self, ctx, member: discord.Member = None, reason = None):
        if member is None:
            await ctx.send("Введите пользователя которому хотите выдать варн!")
        elif member.id == 599587609240666123:
            await ctx.send("Вы не можите выполнить это действие с ботом!")
        elif reason is None:
            await ctx.send("Укажите причину!")
        else:
            cursor.execute("UPDATE users SET warn = warn + {} WHERE id = {} AND guild_id = {}".format(1, member.id, ctx.guild.id))
            connection.commit()
            emb = discord.Embed(title = "Удачно!", description = f'**Администратор {ctx.author.mention} выдал warn пользователю {member.mention}\nПричина: {reason}\nКоличество варнов: {cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0]}**', colour = discord.Color.purple())
            await ctx.send(embed = emb)

            if cursor.execute("SELECT warn FROM users WHERE id = {} AND guild_id = {}".format(member.id, ctx.guild.id)).fetchone()[0] >= 3:
                await member.ban(reason = "3/3 warns|kindbot")
                emb1 = discord.Embed(title = "3/3", description = f"**У пользователя {member.mention}, было 3 варна и по этому он был забанен!**", colour = discord.Color.purple())
                await ctx.send(embed = emb1)



def setup(bot):
    bot.add_cog(Moder(bot))
    print('[COGS] Moder be loaded')