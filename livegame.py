import requests

api_key = '...'
regions = {
    'eun1':'eun1',
    'eune':'eun1',
    'EUNE':'eun1',
    'east':'eun1',
    'EAST':'eun1',
    'euw1':'euw1',
    'euw':'euw1',
    'EUW':'euw1',
    'west':'euw1',
    'WEST':'euw1'
}

def getSummonerId(region, summoner_name):
    
    url = 'https://'+region+'.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+summoner_name+'?api_key='+api_key
    summoner_json = requests.get(url).json()
    try:
        summoner_id = summoner_json['id']
        return summoner_id
    except:
        return ('not exists')

def getSummonerInfo(region, summoner_name):
    region = regions[region]
    summoner_id = getSummonerId(region, summoner_name)

    if(summoner_id == 'not exists'):
        return ('Summoner name "**'+summoner_name+'**"'+" doesn't exist")

    url = 'https://'+region+'.api.riotgames.com/lol/league/v4/entries/by-summoner/'+summoner_id+'?api_key='+api_key

    summoner_json = requests.get(url).json()
    print(summoner_json)
    if(summoner_json == []):
        return (summoner_name+'-unranked') #case 1
    if len(summoner_json) >= 2: #case 2
        if(summoner_json[0]['queueType'] == 'RANKED_SOLO_5x5'):
            summoner_json = summoner_json[0]
        elif(summoner_json[1]['queueType'] == 'RANKED_SOLO_5x5'):
            summoner_json = summoner_json[1]

    else: #case 3
        if(summoner_json[0]['queueType'] == 'RANKED_SOLO_5x5'):
            summoner_json = summoner_json[0]
        else:
            return(summoner_name+'-unranked')
        
    summoner_tier = summoner_json['tier']
    summoner_rank = summoner_json['rank']

    return(summoner_name+'-'+summoner_tier+' '+summoner_rank)

def getSummonerLiveGame(region, summoner_name):
    region = regions[region]
    summoner_id = getSummonerId(region, summoner_name)
    if(summoner_id =='not exists'):
        return ('Summoner name "**'+summoner_name+'**"'+" doesn't exist") 
    url = 'https://'+region+'.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'+summoner_id+'?api_key='+api_key
    livegame_json = requests.get(url).json()
   
    answer = ''
    try:
        for player in livegame_json['participants']:
            answer += getSummonerInfo(region, player['summonerName'])+'-'+str(player['championId'])+'\n'
    except Exception as e:
        print(e)
        answer = 'Summoner '+'**"'+summoner_name+'**"'+' is not currently in a game'
    return answer

