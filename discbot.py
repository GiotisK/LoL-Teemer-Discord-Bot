import discord
import time
import livegame
from pymongo import MongoClient

champions = []

#---------MongoDB Vars---------#...")
db = mongo_client.get_database('champions')
db2 = mongo_client.get_database('teamfighttactics')

champion_records = db.champion_info
champId_records = db.champion_ids
tftitem_records = db2.tft_items
tftTierList_records = db2.tft_tierlist

#---------Discord Vars---------#
TOKEN = '...'
client = discord.Client()


@client.event
async def on_message(message):
    channel = message.channel
    lolPlayersRole = discord.utils.get(message.guild.roles, name='LoL Players')
    
    if message.author == client.user:# we do not want the bot to reply to itself
        return

    if message.content.startswith('!info'):
        info_string = message.content.split(' ', 2)
        region = info_string[1]
        name = info_string[2]
        answer = livegame.getSummonerInfo(region, name)
        embed = createPlayerInfoEmbed(answer)
        await message.channel.send(content = None, embed = embed)
        return

    if message.content.startswith('!live'):
        info_string = message.content.split(' ', 2)
        region = info_string[1]
        name = info_string[2]
        answer = livegame.getSummonerLiveGame(region, name)
        embed = createLiveGameEmbed(answer)
        await message.channel.send(content = None, embed = embed)
        return

    if message.content.startswith('!purge'):
        count = 0
        try:
            num = int(message.content.split(' ')[1])
        except:
            num = 10
        async for msg in channel.history(limit=num+1, before=None, after=None, around=None, oldest_first=None): #+1 cause the !purge commant counts as one aswell
            await msg.delete()
        return

    if message.content.startswith('!del'):
        count = 0
        try:
            num = int(message.content.split(' ')[1])+1
        except:
            num = 11
        async for msg in channel.history(limit=100, before=None, after=None, around=None, oldest_first=None):
            if str(msg.author)=='LoL Teemer#5819' or msg.content.startswith('!'):
                if(count == num):
                    return
                await msg.delete()
                count += 1
        return

    if message.content.startswith('!tft'):
        if message.content == '!tft tierlist':
           embed =  createTftTierListEmbed()
           await message.channel.send(content = None, embed = embed)
           return

        if message.content == '!tft items':
            pass# will add later this function
        elif 'bf sword' in message.content or 'bf' in message.content or 'sword' in message.content or 'ad' in message.content:
            item_name = 'BF Sword'

        elif 'recurve bow' in message.content or 'bow' in message.content or 'recurve' in message.content or 'attack speed' in message.content :
            item_name = 'Recurve Bow'

        elif 'needlessly large rod' in message.content or 'needlessly ord' in message.content or 'large rod' in message.content or 'rod' in message.content or 'ap' in message.content:
            item_name = 'Needlessly Large Rod'

        elif 'tear of the goddess' in message.content or 'tear of goddess' in message.content or 'tear' in message.content or 'mana' in message.content:
            item_name = 'Tear Of The Goddess'

        elif 'chain vest' in message.content or 'vest' in message.content or 'chain' in message.content or 'armor' in message.content:
            item_name = 'Chain Vest'

        elif 'giants belt' in message.content or 'giants' in message.content or 'belt' in message.content or 'hp' in message.content or 'health' in message.content:
            item_name = "Giant's Belt"

        elif 'negatron cloak' in message.content or 'negatron' in message.content or 'cloak' in message.content or 'mr' in message.content :
            item_name = 'Negatron Cloak'

        elif 'spatula' in message.content:
            item_name = 'Spatula'
        else:
            return

        tftitem_records_ = tftitem_records.find( ( {'$or':[ {'firstItem':item_name}, {'secondItem':item_name}]} ) )
        embed = createTftItemEmbed(tftitem_records_, item_name)
        await message.channel.send(content = None, embed = embed)
        return

    if message.content.startswith('!help'):
        embed = createHelpEmbed()
        
        await message.channel.send(content = None, embed = embed)
        return

    elif message.content.startswith('!hello'):
        msg = 'Hello retarded autista {0.author.mention}'.format(message)
        await channel.send(msg)
        return

    elif message.content.startswith('!assemble'):

        msg = ('PLIZ assemble for riot <@&%s>' % (lolPlayersRole.id)).format(message)
        await channel.send(msg)
        return

    elif message.content.startswith('!victory'):
        msg = '{0.author.mention} is doing the victory dance'.format(message)
        embed = discord.Embed(title = '', description = msg)
        embed.set_image(url = 'https://media1.tenor.com/images/26ff317c89f308d16cd5b9c14dd6b584/tenor.gif')
        await message.channel.send(content = None, embed = embed)
        return

    if message.content.startswith('!'):
        token = message.content.split()
        token = token[0].replace('!','').rstrip().lower()

        for champion in champions:
            token = handleShortNames(token)
            if token in champion:
                champion_record = champion_records.find_one({'name': champion})
                try:
                    embed = createChampionEmbed(champion_record)
                    await message.channel.send(content = None, embed = embed)
                except:
                    msg = 'Currently not enough data in champion.gg!'
                    await channel.send(msg)
                return

        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game('Type !help for commands'))

def handleShortNames(token):
    if token == 'j4':
        token = 'jarvan'
    elif token =='mf':
        token = 'missfortune'
    elif token == 'tf':
        token = 'twistedfate'
    return token


def styleTheMessage(record, case):
    if case =='runes':
        combined_runes = ''
        runes = record['primary_runes'].split(',')
        runes[0] = '\n**'+runes[0]+'**' #make the Sorcery, Inspiration etc. bold
        runes[4] = runes[4]+'\t' #split primary runes with secondary
        runes[5] = '\n**'+runes[5]+'**' #same as above ^
        runes[8] = '\n**Stat Runes**\n'+runes[8] #split secondary runes with stat runes
        for rune in runes:
            combined_runes = (combined_runes + rune + '\n')
        msg = ('\n'+combined_runes)

    elif case == 'items':
        combined_items = ''
        items = record['primary_items'].split(',')
        for item in items:
            combined_items = (combined_items + item + '\n')
        msg= ('\n'+combined_items)

    elif case == 'skillorder':
        skillorder = record['skill_order']
        msg = ('\n'+skillorder)

    return msg

def getImageUrl(name):
    if name == 'jarvaniv':
        name = 'JarvanIV'
    elif name == 'reksai':
        name = 'RekSai'
    elif name == 'aurelionsol':
        name = 'AurelionSol'
    elif name == 'drmundo':
        name = 'DrMundo'
    elif name == 'masteryi':
        name = 'MasterYi'
    elif name == 'missfortune':
        name = 'MissFortune'
    elif name == 'tahmkench':
        name = 'TahmKench'
    elif name == 'twistedfate':
        name = 'TwistedFate'
    elif name == 'xinzhao':
        name = 'XinZhao'
    elif name == 'kogmaw':
        name = 'KogMaw'
    elif name == 'leesin':
        name = 'LeeSin'
    else:
        name = name.capitalize()

    img_url = 'http://ddragon.leagueoflegends.com/cdn/9.12.1/img/champion/'+name+'.png'

    return img_url

def createLiveGameEmbed(info):
    if("doesn't exist" in info):
        embed = discord.Embed(
            title = '**Player Info** :mushroom:',
            description = '**ERROR:** '+info,
            colour = discord.Colour.red()
        )
        return embed
    elif('not currently in a game' in info):
        embed = discord.Embed(
            title = '**Player Info** :mushroom:',
            description = '**ERROR:** '+info,
            colour = discord.Colour.red()
        )
        return embed
    else:
        players = info.rstrip().split('\n')
        champs = ''
        ranks = ''
        for p in players:
            pArr = p.split('-')
            summonerName = pArr[0]
            rank = pArr[1]
            champion = champId_records.find_one({'id': pArr[2]})['name']
            champs += ('**%s** (%s)  \n' % (champion.capitalize(), summonerName))
            ranks += ('%s\n' % (rank))

        embed = discord.Embed(
            title = '**LIVE GAME INFO** :mushroom:',
            description = '',
            colour = discord.Colour.green()
        )
        embed.add_field(name='Champions', value=champs, inline=True)
        embed.add_field(name='Divisions', value=ranks, inline=True)
        return embed

def createPlayerInfoEmbed(info):
    print(info)
    if("doesn't exist" in info):
        embed = discord.Embed(
            title = '**Player Info** :mushroom:',
            description = info,
            colour = discord.Colour.red()
        )
        return embed
    else:
        info_string = info.split('-')
        name = info_string[0]
        division = info_string[1]

        embed = discord.Embed(
                title = '**PLAYER INFO** :mushroom:',
                description = '',
                colour = discord.Colour.green()
            )
        embed.add_field(name='Name', value=name, inline=True)
        embed.add_field(name='Division (Solo/Duo Queue)', value=division, inline=True)

        return embed

def createHelpEmbed():
    embed = discord.Embed(
            title = '**COMMANDS** :mushroom:',
            description = '',
            colour = discord.Colour.green()
        )
    embed.add_field(name='`!<champion name>`', value='Shows runes, items, skill order for a champion. Example: `!zyra`.', inline=True)
    embed.add_field(name='`!tft <item>`', value='Shows Teamfight Tactics item recipes with given item . Example: `!tft tear, !tft sword`.', inline=True)
    embed.add_field(name='`!tft tierlist`', value='Shows the best champions currently in Teamfight Tactics.', inline=True)
    embed.add_field(name='`!live <region> <player name>`', value='Live game info of given player in a region (eune, euw).', inline=True)
    embed.add_field(name='`!info <region> <player name>`', value='Ranking info of given player in a region (eune, euw).', inline=True)
    embed.add_field(name='`!del <num>`', value='Delete a total of <num> bot messages/commands, where <num> is a number. Default is 10 messages.', inline=False)
    embed.add_field(name='`!purge <num>`', value='Deletes a total of <num> messages, where <num> is a number. Default is 10 messages.', inline=False)
    embed.add_field(name='`!victory`', value='Does the victory dance ( ͡° ͜ʖ ͡°).', inline=False)
    embed.add_field(name='`!assemble`', value='Mentions LoL Players (must have a role of "LoL Players").', inline=False)
    embed.add_field(name='`!hello`', value=':wave:', inline=True)
    return embed


def createTftItemEmbed(tftitem_records_, item_name):
    embed = discord.Embed(
            title = '**TFT Items** :mushroom:\n',
            description = 'All **%s** recipes' % (item_name),
            colour = discord.Colour.green()
        )
    embed.set_author(name='')
    for item in tftitem_records_:
        embed.add_field(name = '**'+item['name']+'**'+" ("+item['stats']+")", value='**'+item['firstItem']+' + '+item['secondItem']+'**'+'```'+'\n'+item['description']+'```', inline=False)
    return embed

def createChampionEmbed(champion_record):
    runes_msg = styleTheMessage(champion_record,'runes')
    items_msg = styleTheMessage(champion_record, 'items')
    skillOrder_msg = styleTheMessage(champion_record, 'skillorder')
    embed = discord.Embed(
            title = '**'+champion_record['name'].upper()+'** :mushroom: ',
            description = '',
            colour = discord.Colour.green()
        )
    img_url = getImageUrl(champion_record['name'])
    embed.set_thumbnail(url=img_url)
    embed.add_field(name='**RUNES**', value=runes_msg, inline=True)
    embed.add_field(name='**ITEMS**', value=items_msg, inline=True)
    embed.add_field(name='**SKILL ORDER**', value=skillOrder_msg, inline=False)

    return embed

def createTftTierListEmbed():
    embed = discord.Embed(
            title = '**TFT Tier List** :mushroom:',
            colour = discord.Colour.green()
        )
    for tier in tftTierList_records.find({}):
        champions = tier['champions'].split('\t')
        styledString = ''
        for champion in champions:
            styledString += '**'+champion.split(':')[0]+'**'+': '+champion.split(':')[1]+'\n'
        embed.add_field(name = tier['tier'], value=styledString, inline=True)

    return embed


def getChampionsFromCsv():
    global champions

    with open ('champions.csv', 'r') as file:
        for line in file:
            champions.append(line.rstrip().split('\t')[0])

getChampionsFromCsv()
client.run(TOKEN)