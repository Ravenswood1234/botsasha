import discord
from discord.ext import commands
import asyncio
import random
import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

class Moder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect('server.db')
        self.cursor = self.connection.cursor()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send(embed=discord.Embed(title="Не бузи!", description=f":x: **{ctx.author.mention}**, укажи **сообщение**, которое хочешь отправить от именни **бота** :x:", color=0xFF0000))
        else:
            await ctx.channel.purge(limit = 1)
            await ctx.send(arg)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount = None):
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.send(':: Сообщения успешно удалены ::')

    @commands.command()
    @commands.has_permissions( administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        if member is None:
            await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите кикнуть!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину кика!')
        else:
            emb = discord.Embed( title = 'Кик!', description = f'**Администратор: ``{ ctx.author.name }``\n Кикнул пользователя: { member.mention },\nПричина: {reason}!**', colour = discord.Color.red())
            await member.kick( reason = reason )
            await ctx.send( embed = emb )


    @commands.command()
    @commands.has_permissions( administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        if member is None:
            ctx.send('укажите пользователя которого хотите забанить!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину бана!')
        else:
            emb = discord.Embed( title = '**Бан**', description = f'**Администратор: {ctx.author.mention}\n Забанил пользователя: {member.mention}\nПричина: {reason}**', colour = discord.Color.red())
            await ctx.channel.purge( limit = 1 )
            await member.ban( reason = reason )
            await ctx.send( embed = emb )


    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration: int, *, arg = None):
        emb = discord.Embed(title='MUTE')
        role = discord.utils.get(ctx.guild.roles, name="mute")

        if member is None:
            await ctx.send(f'{ctx.author.name}, укажите пользователя которого хотите замутить')
        elif duration < 1:
            await ctx.send(f'{ctx.author.name}, укажите время мута больше чем 1 секунда!')
        elif arg is None:
            await ctx.send(f'{ctx.author.name}, укажите причину мута!')
        else:
            emb.add_field(name="Замутил:", value=f'{ctx.author.mention} __**замутил**__: {member.mention} __**на {duration} секунд.**__')
            emb.add_field(name="Причина:", value=f'__*{arg}*__')
            await ctx.send(embed=emb)
            await member.add_roles(role)
            await asyncio.sleep(duration)
            embed = discord.Embed(description=f'Товарищ {member.mention} успешно прошёл курс оздаровления от мута).', color=discord.Colour.green())
            await ctx.send(embed=embed)
            await member.remove_roles(role)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warn(self, ctx, member: discord.Member = None):
        if ctx.author == member:
            await ctx.send(f'{ctx.author}, ты умный или что то?, зачем себе варн выдаёшь?')
        elif member is None:
            await ctx.send(f'{ctx.author.mention}, обязательно укажите пользователя которому хотите выдать варн!')
        else:
            emb = discord.Embed(title = '**Warn**', description = f'**Администратор: {ctx.author.mention}\n Нарушитель: {member.mention}.\nКоличество Варнов: {cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**')
            cursor.execute("UPDATE users SET warns = warns + {} WHERE id = {}".format(1, member.id))
            connection.commit()
            await ctx.send(embed = emb)


    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unwarn(self, ctx, member: discord.Member = None):
        if member is None:
            ctx.send(f'{ctx.author.mention}, укажите пользователя у которого хотите снять варн!')
        else:
            cursor.execute("UPDATE users SET warns = warns - {} WHERE id = {}".format(1, member.id))
            connection.commit()
            emb = discord.Embed( title = '**Успешно!**', description = f'**У пользователя {member.mention}, был снят варн!\nКол-во варнов: {cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**')
            await ctx.send(embed = emb)



    @commands.command()
    @commands.has_permissions(administrator = True)
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
            await chanel.send(embed = emb)



    @commands.command()
    @commands.has_permissions( administrator = True )
    async def tempban(self, ctx, member: discord.Member = None, reason = None, amount: int = None):
        if member is None:
            await ctx.send(f'{ctx.author.mention}, укажите пользователя которого хотите временно забанить!')
        elif amount is None:
            await ctx.send(f'{ctx.author.mention}, укажите время бана (в секундах)!')
        elif reason is None:
            await ctx.send(f'{ctx.author.mention}, укажите причину бана!')
        else:
            emb = discord.Embed(title = '**Бан!**', description = f'**Администратор: {ctx.author.mention}\nНарушитель:{member.mention}\nПричина: {reason}\nВремя бана:{amount}!**', colour = discord.Color.blue())
            await member.ban(reason = reason)
            await ctx.send(embed = emb)
            await asyncio.sleep(amount)
            emb1 = discord.Embed(title = 'Разбанен!', description = f'Пользователь {member}, был разабанен!', colour = discord.Color.green())
            await ctx.guild.unban(member)
            await ctx.send(embed = emb1)    

        


def setup(bot):
    bot.add_cog(Moder(bot))
    print('[COGS] Moder be loaded')