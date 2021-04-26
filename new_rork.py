# Инклюды____________________________________________________________________________________
from random import random, randrange, randint, choice  # стандартная библиотека
import shutil, asyncio, time  # стандартная библиотека
import discord  # надо устанавливать через pip
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import collections

import os

# Переменные________________________________________________________________________________
client = discord.Client()
prefix = 'r'  # Знак который будет перед коммандой, можно изменить
Bot = commands.Bot(command_prefix=prefix)
Bot.remove_command("help")
channels = []
obs = False
nikk_switch = False

# словари___________________________________________________________________________________
smile = {'😊': {'titles': 'Уря', 'urls': 'https://i.imgur.com/k4W7Iiv.png'},
         '✨': {'titles': 'Вжух', 'urls': 'https://i.imgur.com/QRiZFHV.png'},
         '😫': {'titles': 'A-a-a-a-a', 'urls': 'https://i.imgur.com/UAj7798.png'},
         '🤢': {'titles': 'Фе', 'urls': 'https://i.imgur.com/Ake3dlQ.png'},
         '🔫': {'titles': 'Бэнг', 'urls': 'https://i.imgur.com/veQqOkk.png'},
         ':stin1:': {'titles': 'Stin', 'urls': 'https://i.imgur.com/ONrrJ8R.png'},
         ':stin2:': {'titles': 'Stin', 'urls': 'https://i.imgur.com/bmPSiwQ.png'},
         ':stin0:': {'titles': 'Stin', 'urls': 'https://i.imgur.com/CZAvk7l.png'}
         }

d12a = {
    1: 'https://i.imgur.com/vz0Iazn.png',
    2: 'https://i.imgur.com/3shQJ9k.png',
    3: 'https://i.imgur.com/jqY7uj5.png',
    4: 'https://i.imgur.com/iZGNoaN.png',
    5: 'https://i.imgur.com/vt56LdG.png',
    6: 'https://i.imgur.com/vAQdNnw.png',
    7: 'https://i.imgur.com/nuMK8hW.png',
    8: 'https://i.imgur.com/4P2S5VG.png',
    9: 'https://i.imgur.com/nRqlCyq.png',
    10: 'https://i.imgur.com/QhHjGtE.png',
    11: 'https://i.imgur.com/lfY3lpN.png',
    12: 'https://i.imgur.com/krCCE6K.png',
    'Орёл': 'https://i.imgur.com/e2kd5Gv.png',
    'Решка': 'https://i.imgur.com/FCWQLiX.png'
}

dices = {
    'd12': {'rand': [1, 12], 'title': 'Dice 12', 'url': d12a},
    'd': {'rand': [1, 6], 'title': 'Dice 6', 'url': d12a},
    'd2': {'rand': ['Орёл', 'Решка'], 'title': 'Монетка', 'url': d12a}
}


# статические функции
def test_ru_eng(word):
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    ru = ''
    eng = ''
    for i in word:
        if i.lower() in cyrillic:
            ru += i
        else:
            eng += i

    if len(ru) > len(eng):
        return 'ru'
    else:
        return 'eng'


# асинхронные функции______________________________________________________________________
async def smiles(ctx, **kwargs):
    '''
    Смайлики
    '''
    channel = ctx.channel
    user = ctx.author
    embed = discord.Embed(title=kwargs['titles'], description=ctx.system_content, color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.author}', icon_url=str(ctx.author.avatar_url))
    embed.set_image(url=kwargs['urls'])
    await channel.send(embed=embed)


async def roll(ctx, **kwargs):
    '''

    '''
    user = ctx.message.author
    if 'Орёл' in kwargs['rand']:
        dice = choice(kwargs['rand'])
    else:
        dice = randint(*kwargs['rand'])
    embed = discord.Embed(title=kwargs['title'], description='Выпало ' + str(dice), color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    embed.set_image(url=kwargs['url'][dice])
    await ctx.send(embed=embed)


async def voise(member):  # проверка войсов на наличие людей
    channels = member.guild._channels
    voises = [Bot.get_channel(id=i) for i in channels if list(Bot.get_channel(id=i).name)[0] == '🎩']
    channel = [i for i in voises if len(i.members) == 0]
    F = [len(i.members) for i in voises]
    N = sum(F)
    for i in channel:
        await i.delete(reason=None)

    namechannel = '❤ ' + str(N) + ' в войсах ❤'
    numvoise = discord.utils.get(member.guild.voice_channels, id=595105805293060162)
    await asyncio.sleep(360)
    await numvoise.edit(name=namechannel)


async def new_voice(member, before, after):
    member = member
    channels = member.guild._channels
    cat = discord.utils.get(member.guild.voice_channels, name='у костра')
    guild = member.guild
    try:
        if after.channel.id == 590574585917734937:
            namechannel = '🎩 ' + member.name
            await guild.create_voice_channel(name=namechannel, category=cat.category)
            channel = discord.utils.get(member.guild.voice_channels, name=namechannel)
            channel_id = channel.id
            overwrite = discord.PermissionOverwrite()
            overwrite.manage_channels = True
            overwrite.deafen_members = True
            overwrite.move_members = True
            await channel.set_permissions(member, overwrite=overwrite)
            await asyncio.sleep(0.1)
            await member.edit(voice_channel=channel)
            status = True

            while status:
                await asyncio.sleep(0.1)
                channel = Bot.get_channel(channel_id)
                namelist = list(channel.name)
                if namelist[0] != '🎩':
                    namechannel = '🎩 ' + channel.name
                    await channel.edit(name=namechannel)
                if len(channel.members) == 0:
                    status = False

    except:
        pass


# Комманды__________________________________________________________________________________
@commands.has_any_role('Сер Ланселот')
@Bot.command()
async def chnick(ctx, member: discord.Member, *nick):
    global nikk_switch
    if nikk_switch is True:
        nikk_switch = False
    else:
        nikk_switch = True
    while nikk_switch:
        word = ''
        for i in nick:
            word += i
            word += ' '
        await asyncio.sleep(3)
        await member.edit(nick=word)


@Bot.command()
async def vers(ctx):  # Версия на данный момент
    ''' Версия бота
    '''
    global channels
    vers_cnt = "1.010"
    version = discord.Embed(title="Версия на данный момент", description=vers_cnt, colour=0xFFFFFF)
    await ctx.send(embed=version)
    print(channels)


@Bot.command()
async def avatar(ctx, member: discord.Member = None):
    '''
    Вызывает аватар
    '''
    user = ctx.message.author if (member == None) else member
    await ctx.message.delete()
    embed = discord.Embed(title=f'Аватар пользователя {user}',
                          description=f'[Ссылка на изображение]({user.avatar_url})', color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)


@Bot.command()
async def d12(ctx):
    asyncio.ensure_future(roll(ctx, **dices['d12']))
    await ctx.message.delete()


@Bot.command()
async def d(ctx):
    asyncio.ensure_future(roll(ctx, **dices['d']))
    await ctx.message.delete()


@Bot.command()
async def d2(ctx):
    asyncio.ensure_future(roll(ctx, **dices['d2']))
    await ctx.message.delete()


@Bot.command()
async def d3(ctx):
    user = ctx.message.author
    dice = randint(1, 3)
    await ctx.message.delete()
    embed = discord.Embed(title='Dice 3', description='Выпало ' + str(dice), color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    if dice == 1:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609147375969370124/3_Sides_-_Number_1.png')
    elif dice == 2:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609147379488260186/3_Sides_-_Number_2.png')
    elif dice == 3:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609147382856417303/3_Sides_-_Number_3.png')
    await ctx.send(embed=embed)


@Bot.command()
async def d20(ctx):
    user = ctx.message.author
    dice = randint(1, 20)
    await ctx.message.delete()
    embed = discord.Embed(title='Dice 20', description='Выпало ' + str(dice), color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    await ctx.send(embed=embed)


@Bot.command()
async def d4(ctx):
    user = ctx.message.author
    dice = randint(1, 4)
    await ctx.message.delete()
    embed = discord.Embed(title='Dice 4', description='Выпало ' + str(dice), color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    if dice == 1:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609148240306110491/4_Sides_-_Number_1.png')
    elif dice == 2:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609148243091390479/4_Sides_-_Number_2.png')
    elif dice == 3:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609148246790766602/4_Sides_-_Number_3.png')
    elif dice == 4:
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/591257917152296970/609148250100072448/4_Sides_-_Number_4.png')
    await ctx.send(embed=embed)


@Bot.command()
async def c(ctx):
    user = ctx.message.author
    dice = randint(1, 100)
    await ctx.message.delete()
    embed = discord.Embed(title='Стогранник', description='Выпало ' + str(dice), color=user.color)
    embed.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=str(ctx.message.author.avatar_url))
    await ctx.send(embed=embed)


@Bot.command()
async def Dice(ctx):  # Все комманды в кратком объяснении
    ''' первая комманда help
    '''
    D_cnt = prefix + "Dice - показывает это меню \n"
    d_cnt = prefix + "d - шестигранный кубик \n"
    d2_cnt = prefix + "d2 - монетка \n"
    d3_cnt = prefix + "d3 - трёхгранник \n"
    d4_cnt = prefix + "d4 - четырёхгранник \n"
    d12_cnt = prefix + "d12 - двенадцатигранниу \n"
    d20_cnt = prefix + "d20 - двадцати гранник \n"
    c_cnt = prefix + "c - стогранник Чоссера \n"
    helpown = discord.Embed(title="Help",
                            description=D_cnt + d_cnt + d2_cnt + d3_cnt + d4_cnt + d12_cnt + d20_cnt + c_cnt,
                            colour=0xFF0000)
    await ctx.send(embed=helpown)


# ивенты____________________________________________________________________________________
@Bot.event
async def on_ready():
    print("Murk")


# при присоединении на сервер
# discord.on_guild_join( гильдия)

# когда сервер доступен
# discord.on_guild_available( гильдия )

# когда не доступен
# discord.on_guild_unavailable( гильдия ) #доступность сервера

# когда создаётся роль
# discord.on_guild_role_create( роль )

# когда роль удаляется
# discord.on_guild_role_delete( роль )

# когда роль меняется
# discord.on_guild_role_update( до , после )

# когда обновляются смайлики
# discord.on_guild_emojis_update(guild, before, after)¶

# когда кто-то отправил сообщение
@Bot.event
async def on_message(ctx):
    await Bot.wait_until_ready()
    await Bot.process_commands(ctx)
    for i in smile:
        if i in ctx.system_content:
            asyncio.ensure_future(smiles(ctx, **smile[i]))
            await ctx.delete()

        # когда сообщение удалено
        # discord.on_message_delete( сообщение )

        # когда сообщение удалено и его может не быть в кеше
        # discord.on_raw_message_delete( payload )
        '''Вызывается при массовом удалении сообщений. 
        Если ни одно из удаленных сообщений не найдено во 
        внутреннем кэше сообщений, это событие не будет вызываться. 
        Если отдельные сообщения не были найдены во внутреннем 
        кэше сообщений, это событие все равно будет вызываться, 
        но не найденные сообщения не будут включены в список сообщений. 
        Сообщения могут не находиться в кеше, если сообщение слишком 
        старое или клиент участвует в гильдиях с высоким трафиком.'''


# когда сообщение изменилось
# discord.on_message_edit( до , после )

# когда меняются ввойсах(колл-во людей например)
@Bot.event
async def on_voice_state_update(member, before, after):
    asyncio.ensure_future(new_voice(member, before, after))
    asyncio.ensure_future(voise(member))


# когда пользователь присоденился к серверу
# discord.on_member_join( член )

# когда пользователь сервер покинул
# discord.on_member_remove( член )

# изменения пользователя на сервере
# discord.on_member_update( до , после )
'''            status
            activity
            nickname
            roles
            pending'''


# когда пользователь(не на сервере) изменился
# discord.on_user_update( до , после )

# когда кто-то добавил реакцию
# discord.on_raw_reaction_add(payload)

# когда кто-то реакцию снял
@Bot.event
async def on_raw_reaction_add(reaction):
    if str(reaction.emoji) in '🤓':
        s = ''
        slovar = {'`': 'ё', '~': 'Ё', 'q': 'й', 'Q': 'Й',
                  'w': 'ц', 'W': 'Ц', 'e': 'у', 'E': 'У',
                  'r': 'к', 'R': 'К', 't': 'е', 'T': 'Е',
                  'y': 'н', 'Y': 'Н', 'u': 'г', 'U': 'Г',
                  'i': 'ш', 'I': 'Ш', 'o': 'щ', 'O': 'Щ',
                  'p': 'з', 'P': 'З', '[': 'х', '{': 'Х',
                  ']': 'ъ', '}': 'Ъ', 'a': 'ф', 'A': 'Ф',
                  's': 'ы', 'S': 'Ы', 'd': 'в', 'D': 'В',
                  'f': 'а', 'F': 'А', 'g': 'п', 'G': 'П',
                  'h': 'р', 'H': 'Р', 'j': 'о', 'J': 'О',
                  'k': 'л', 'K': 'Л', 'l': 'д', 'L': 'Д',
                  ';': 'ж', ':': 'Ж', "'": 'э', '"': 'Э',
                  "z": 'я', 'Z': 'Я', 'x': 'ч', 'X': 'Ч',
                  'c': 'с', 'C': 'С', 'v': 'м', 'V': 'М',
                  'b': 'и', 'B': 'И', 'n': 'т', 'N': 'Т',
                  'm': 'ь', 'M': 'Ь', ',': 'б', '<': 'Б',
                  '.': 'ю', '>': 'Ю', '/': '.', '?': ',',
                  ' ': ' '
                  }
        slovar2 = {v: k for k, v in slovar.items()}

        guild = discord.utils.get(Bot.guilds, id=reaction.guild_id)
        message = await guild.get_channel(reaction.channel_id).fetch_message(int(reaction.message_id))
        eng_ru = test_ru_eng(message.clean_content)
        if eng_ru == 'ru':
            slovar = slovar2
        else:
            pass
        for i in message.clean_content:
            if i not in slovar:
                s += i
            else:
                s += slovar[i]

        author = "Автор сообщения: " + str(message.author) + "\n"
        clean_content = "Было: \n" + str(message.clean_content) + "\n\n"
        system_content = "Стало: \n" + str(s) + "\n\n"
        created_at = "Созданно: " + str(message.created_at) + "\n"
        symbol = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'F']
        a1 = choice(symbol)
        a2 = choice(symbol)
        b1 = choice(symbol)
        b2 = choice(symbol)
        c1 = choice(symbol)
        c2 = choice(symbol)
        expert = '0x' + a1 + a2 + b1 + b2 + c1 + c2
        cvet = 'Цвет: ' + expert + "\n"
        mess = discord.Embed(
            description=clean_content + system_content,
            colour=int(expert, 16))
        mess.set_footer(text=f'Созданно: {message.author}', icon_url=str(message.author.avatar_url))
        channel = guild.get_channel(reaction.channel_id)
        await channel.send(embed=mess)


# когда удалился приватный канал
# discord.on_private_channel_delete( канал )

# создался приватный канал
# discord.on_private_channel_create( канал )

# изменился приватный канал
# discord.on_private_channel_update( до , после )

# изменение пинов в приватном канале
# discord.on_private_channel_pins_update( канал , last_pin )

#
# discord.on_guild_channel_delete( канал )

#
# discord.on_guild_channel_create( канал )

#
# discord.on_guild_channel_update( до , после )

#
# discord.on_guild_channel_pins_update( канал , last_pin )

#
# discord.on_guild_integrations_update( гильдия )

#
# discord.on_webhooks_update( канал )

#
# on_typing
#    channel ( abc.Messageable) - место, откуда исходил набор текста.
#    user (Union [ User, Member]) - Пользователь, который начал печатать.
#    when ( datetime.datetime) - Когда ввод начался как наивное datetime в UTC.

#
# discord.on_member_ban( гильдия , пользователь user/member)

#
# discord.on_invite_create( пригласить )

#
# discord.on_invite_delete( пригласить )

#
# discord.on_group_join( канал , пользователь )

#
# discord.on_group_remove( канал , пользователь )

#
# discord.on_relationship_add( отношения )

#
# discord.on_relationship_remove( отношения )

#
# discord.on_relationship_update(до после)

# Запуск бота________________________________________________________________________________

# Bot.loop.create_task(my_background_task())

Bot.run('NTkxMjYyOTU5OTg1MDk4NzUz.XQuR5Q.ONT37BmIGyN4Fqnh8AqiTMN2F4w')
