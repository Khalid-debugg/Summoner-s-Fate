import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found in environment variables")

def get_summoner_data(name, tagLine, region):
    formatted_name = name.replace(" ", "%20")
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{formatted_name}/{tagLine}?api_key={API_KEY}"
    return requests.get(url).json()

def get_match_ids(puuid, start, count, region):
    all_match_ids = []
    remaining_count = count
    current_start = start
    
    while remaining_count > 0:
        request_count = min(remaining_count, 100)
        
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={current_start}&count={request_count}&api_key={API_KEY}"
        match_ids = requests.get(url).json()
        
        all_match_ids.extend(match_ids)
        
        remaining_count -= len(match_ids)
        current_start += len(match_ids)
        
        if len(match_ids) < request_count:
            break
            
    return all_match_ids

def get_match_data(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    return requests.get(url).json()
