#!/usr/bin/python
import requests
import urllib.request
import time

from bs4 import BeautifulSoup
runeNumbers ={
    'precision':'(1)',
    'domination':'(2)',
    'sorcery':'(3)',
    'resolve':'(4)',
    'inspiration':'(5)',
    'press the attack':'(1)',
    'lethal tempo':'(2)',
    'fleet footwork':'(3)',
    'conqueror':'(4)',
    'overheal':'(1)',
    'triumph':'(2)',
    'presence of mind':'(3)',
    'legend: alacrity':'(1)',
    'legend: tenacity':'(2)',
    'legend: bloodline':'(3)',
    'coup de grace':'(1)',
    'cut down':'(2)',
    'last stand':'(3)',
    'electrocute':'(1)',
    'predator':'(2)',
    'dark harvest':'(3)',
    'hail of blades':'(4)',
    'cheap shot':'(1)',
    'taste of blood':'(2)',
    'sudden impact':'(3)',
    'zombie ward':'(1)',
    'ghost poro':'(2)',
    'eyeball collection':'(3)',
    'ravenous hunter':'(1)',
    'ingenious hunter':'(2)',
    'relentless hunter':'(3)',
    'ultimate hunter':'(4)',
    'summon aery':'(1)',
    'arcane comet':'(2)',
    'phase rush':'(3)',
    'nullifying orb':'(1)',
    'manaflow band':'(2)',
    'nimbus cloak':'(3)',
    'transcendence':'(1)',
    'celerity':'(2)',
    'absolute focus':'(3)',
    'scorch':'(1)',
    'waterwalking':'(2)',
    'gathering storm':'(3)',
    'grasp of the undying':'(1)',
    'aftershock':'(2)',
    'guardian':'(3)',
    'demolish':'(1)',
    'font of life':'(2)',
    'shield bash':'(3)',
    'conditioning':'(1)',
    'second wind':'(2)',
    'bone plating':'(3)',
    'overgrowth':'(1)',
    'revitalize':'(2)',
    'unflinching':'(3)',
    'glacial augment':'(1)',
    'kleptomancy':'(2)',
    'unsealed spellbook':'(3)',
    'hextech flashtraption':'(1)',
    'magical footwear':'(2)',
    'perfect timing':'(3)',
    "future's market":'(1)',
    'minion dematerializer':'(2)',
    'biscuit delivery':'(3)',
    'cosmic insight':'(1)',
    'approach velocity':'(2)',
    'time warp tonic':'(3)',
    'adaptive force':'(1)',
    'attack speed':'(2)',
    'scaling cooldown reduction':'(3)',
    'magic resist':'(3)',
    'armor':'(2)',
    'scaling health':'(1)'
}

def writeChampionsListToCsv(soup):
    champions = []
    ids = []
    championDivs = soup.find_all('span', {'class': 'champion-name'})
    championIdDivs = soup.find_all('div', {'class': 'tsm-tooltip'})
    championIdDivs = championIdDivs[30:]
    championDivs = championDivs[34:]

    for div in championIdDivs:
        ids.append(div['data-id'])

    for champDiv in championDivs:
        champName = champDiv.string
        champName = champName.replace("'",'') # replace the ' character for champions like Rek'Sai, Vel'koz with empty character
        champName = champName.replace(' ','') # replace the space character for champions like LeeSin with empty character
        champName = champName.replace('.', '') # replace the dot character for champions like Dr.Mundo with empty character
        if champName == 'Nunu&Willump':
            champName = 'Nunu'
        champions.append(champName)

    with open ('champions.csv', 'w') as file:
            for champName,champID in zip(champions,ids):
                file.write(champName.lower()+'\t'+champID+"\n") #save in lowercase (helps with database)


def writeChampionRunePagesToCsv(champName, primaryTree, secondaryTree):
    with open ('championRunes.txt', 'a') as file:
        file.write(champName+'\t')
        #file.write('\n'+'Primary Runes:\n')
        for elmnt in primaryTree:
            file.write(elmnt+',')
        file.write('\t')
        #file.write('\n'+'Secondary Runes: ')
        for elmnt in secondaryTree:
            file.write(elmnt+',')
        file.write('\n')

def writeChampionItemsToCsv(champName, itemList):
    with open ('championItems.txt', 'a') as file:
        file.write(champName+'\t')
        for elmnt in itemList:
            file.write(elmnt+',')
        file.write('\n')

def writeSkillOrderToCsv(champName, skillOrderList):
     with open ('championSkillOrder.txt', 'a') as file:
        file.write(champName+'\t'+skillOrderList[0]+'>'+skillOrderList[1]+'>'+skillOrderList[2]+'\n')

def writeTftTierListToCsv(tierList):
    with open ('tftTierList.txt', 'a') as file:
        for tier in tierList:
            file.write(tier+'\n')

def getChampionsFromCsv():
    champions = []
    with open ('champions.csv', 'r') as file:
        for line in file:
            champions.append(line.rstrip().split('\t')[0])
    return champions
   


def constructRunePages(champName, soup):
    primaryTree = []
    secondaryTree = []

    primaryKeystoneTitles = soup.find_all('div', {'class': 'KeyStoneSlot__Title-krZhKQ eQgjEC Description__Title-jfHpQH bJtdXG'})

    if(len(primaryKeystoneTitles)<2):#means that there is not enough data
        print(champName+": Not Enough Runes Data for display!!!")
        return
    primaryRunesDivs = soup.find_all('div', {'class': 'Description__Title-jfHpQH bJtdXG'}) #last 3 are stats runes
    secondaryRunesDivs = soup.find_all('div', {'class': 'Description__Title-jfHpQH eOLOWg'})

    primaryTree.append(primaryKeystoneTitles[0].string + runeNumbers[primaryKeystoneTitles[0].string.lower()]) #add primary title eg "Domination"
    secondaryTree.append(primaryKeystoneTitles[1].string + runeNumbers[primaryKeystoneTitles[1].string.lower()])
    for i in range(0, 4):
        primaryTree.append(primaryRunesDivs[i].string + runeNumbers[primaryRunesDivs[i].string.lower()]) #add primary runes
        secondaryTree.append(primaryRunesDivs[i+7].string + runeNumbers[primaryRunesDivs[i+7].string.lower()])
    for i in range (0, 3):
        primaryTree.append(secondaryRunesDivs[i].string + runeNumbers[secondaryRunesDivs[i].string.lower()]) # add secondary runes and secondary title eg "Sorcery"
        secondaryTree.append(secondaryRunesDivs[i+3].string + runeNumbers[secondaryRunesDivs[i+3].string.lower()])
    for i in range (4, 7):
        primaryTree.append(primaryRunesDivs[i].string + runeNumbers[primaryRunesDivs[i].string.lower()]) # add stat runes
        secondaryTree.append(primaryRunesDivs[i+7].string + runeNumbers[primaryRunesDivs[i+7].string.lower()])

    writeChampionRunePagesToCsv(champName, primaryTree, secondaryTree)


def constructItemBuilds(champName, soup):
    itemStrings = []
    try:
        itemDivs = soup.find('div',{'class':'build-wrapper'})
        itemAs = itemDivs.find_all('a')
    except:
        print(champName+": Not Enough Item Data for display!!!")
        return

    for a in itemAs:
        splitArray = a['href'].split('/')
        itemString = splitArray[len(splitArray)-1]
        itemStrings.append(itemString)
    writeChampionItemsToCsv(champName, itemStrings)

def constructSkillOrder(champName, soup):
    try:
        outerDiv = soup.find('div', {'class':'skill-order clearfix'})
        skillDivs = outerDiv.find_all('div', {'class':'skill'})
        del skillDivs[0] #delete first row with numbers
        del skillDivs[3] #delete row of Ulti 

        skillOrder = []
        skillsCounter =[0,0,0]
        q = skillDivs[0].find('div', {'class' : 'skill-selections'}).find_all('div')
        w = skillDivs[1].find('div', {'class' : 'skill-selections'}).find_all('div')
        e = skillDivs[2].find('div', {'class' : 'skill-selections'}).find_all('div')

        for i in range(0, 18):
            if(''.join(q[i]['class']) == 'selected' and skillsCounter[0]<5): #get string of class name using ''.join trick
                skillsCounter[0] += 1
                if(skillsCounter[0]==5):
                    skillsCounter[0] += 1
                    skillOrder.append('Q')

            if(''.join(w[i]['class']) == 'selected' and skillsCounter[1]<5):
                skillsCounter[1] += 1
                if(skillsCounter[1]==5):
                    skillsCounter[1] += 1
                    skillOrder.append('W')
                    

            if(''.join(e[i]['class']) == 'selected' and skillsCounter[2]<5):
                skillsCounter[2] += 1
                if(skillsCounter[2]==5):
                    skillsCounter[2] += 1
                    skillOrder.append('E')
        writeSkillOrderToCsv(champName, skillOrder)
    except:
        print(champName+": Not Enough Skill Order Data for display!!!")
        return



def constructTftTierList(soup):
    tierDivs = soup.find_all('td',{'class':'ChampionTierBG1'})
    tierDescs = ['God', 'Strong', 'Good', 'Average', 'Below Average', 'Weak', 'Worst']
    tierListStrings = []
    count = -1
    for div in tierDivs:
        count += 1
        if count > 6:
            break
        tierStr = ''
        tierListNames = div.find_all('span',{'class':'TierListNames'})
        for tierListName in tierListNames:
            if(tierListName.string != None ):
                if(tierStr!=''):
                    tierStr = tierStr[:-1]+'\t'
                tierStr += tierListName.string+':'
            for types in tierListName.find_all('span',{'class':'type-tierlist-s'}):
                if(types.string != None):
                    tierStr += types.string+','
        tierListStrings.append(tierStr)

    writeTftTierListToCsv(tierListStrings)


def getRequestChampions(): # gather and parse all champions from champion.gg
    url = 'https://champion.gg/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    writeChampionsListToCsv(soup)

def getRequestRunesAndItems():
    champions = getChampionsFromCsv()
    for champName in champions:
        url = 'https://champion.gg/champion/'+champName+'/?league=gold'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        constructRunePages(champName, soup)
        constructItemBuilds(champName, soup)
        constructSkillOrder(champName, soup)
        time.sleep(1)

def getRequestTftTierlist():
    url = 'https://rankedboost.com/league-of-legends/teamfight-tactics/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    constructTftTierList(soup)



    #with open ('out.txt', 'w', encoding = 'utf-8') as file:
    #    file.write(runes)


def truncateFiles():
    runes = open('championRunes.txt', 'w')
    items = open('championItems.txt', 'w')
    skillOrder = open('championSkillOrder.txt', 'w')
    tftTierList = open('tftTierList.txt', 'w')
    runes.truncate()
    items.truncate()
    skillOrder.truncate()
    tftTierList.truncate()

truncateFiles()
getRequestChampions()
print('Champions -> OK')
getRequestRunesAndItems()
print('Runes and Items -> OK')
getRequestTftTierlist()
print('TFT Tier List -> OK')

