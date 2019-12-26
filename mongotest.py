#!/usr/bin/python
from pymongo import MongoClient
client = MongoClient("...")

def pushLoLEntriesToMongoDB(champEntries, idEntries ):
    global client

    db = client.get_database('champions')
    db.drop_collection(db.champion_info)
    db.drop_collection(db.champion_ids)

    db.champion_info.insert_many(champEntries)
    db.champion_ids.insert_many(idEntries)



def pushTftEntriesToMongoDB(tftitemEntries):
    global client
    db = client.get_database('teamfighttactics')
    db.drop_collection(db.tft_items)
    tft_records = db.tft_items
    tft_records.insert_many(tftitemEntries)

def pushTftTierListEntriesToMongoDB(tftTierListEntries):
    global client
    db = client.get_database('teamfighttactics')
    db.drop_collection(db.tft_tierlist)
    db.tft_tierlist.insert_many(tftTierListEntries)

def getTftItemEntriesFromFile():
    tftitemEntries = []
    with open ('tftitems.txt', 'r') as file:
        for line in file:
            lineArray = line.rstrip().split(',')
            tftitem={
                'name':lineArray[0],
                'firstItem':lineArray[1],
                'secondItem':lineArray[2],
                'stats':lineArray[3],
                'description':lineArray[4]
            }
            tftitemEntries.append(tftitem)
    pushTftEntriesToMongoDB(tftitemEntries)

def getTftTierListEntriesFromFile():
    tftTierListEntries = []
    tftTierStrings = ['God', 'Strong', 'Good', 'Average', 'Bellow Average', 'Weak', 'Worst']
    pointer = -1
    with open ('tftTierList.txt', 'r') as file:
        for line in file:
            pointer += 1
            line = line.rstrip()
            tftTier={
                'tier':tftTierStrings[pointer],
                'champions':line,
            }
            tftTierListEntries.append(tftTier)
    pushTftTierListEntriesToMongoDB(tftTierListEntries)


def getLoLEntriesFromFile():
    champEntries = []
    idEntries = []
    with open ('championRunes.txt', 'r') as file1, open('championItems.txt', 'r') as file2, open('championSkillOrder.txt', 'r') as file3:
        for line1, line2, line3 in zip(file1, file2, file3):
            runesArray = line1.rstrip().split('\t')
            itemsArray = line2.rstrip().split('\t')
            skillArray = line3.rstrip().split('\t')

            champInfo = {
                'name': runesArray[0],
                'primary_runes': runesArray[1],
                'secondary_runes': runesArray[2],
                'primary_items': itemsArray[1],
                'skill_order': skillArray[1]
            }
            champEntries.append(champInfo)
    with open ('champions.csv', 'r') as file:
        for line in file:
            champArray = line.rstrip().split('\t')
            champIds={
                'name': champArray[0],
                'id': champArray[1]
            }
            idEntries.append(champIds)

    pushLoLEntriesToMongoDB(champEntries, idEntries)

getLoLEntriesFromFile()
getTftItemEntriesFromFile()
getTftTierListEntriesFromFile()
print('Mongo DB pushes -> OK')
