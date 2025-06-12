import requests
import time
import csv
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv('RIOT_API_KEY')
if not API_KEY:
    raise ValueError("RIOT_API_KEY not found in environment variables")

SUMMONER_REGION = "euw1"
MATCH_REGION = "europe"
summoner_name = "MIDKING"
tagLine = "kkkk"
tier = "CHALLENGER"
queue_types_to_include = ["RANKED_SOLO_5x5", "ARAM", "NORMAL"]
HEADERS = {"X-Riot-Token": API_KEY}

os.makedirs("CSVs", exist_ok=True)

def get_summoner_data(name, tagLine):
    url = f"https://{MATCH_REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tagLine}?api_key={API_KEY}"
    res = requests.get(url)
    return res.json()

def get_match_ids(puuid, count=10):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?api_key={API_KEY}&start=0&count={count}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_match_data(match_id):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json()

def extract_match_info(match):
    info = match["info"]
    participants = info["participants"]

    team1_champs, team2_champs = [], []
    team1_win = None

    for p in participants:
        if p["teamId"] == 100:
            team1_champs.append(p["championName"])
            team1_win = p["win"]
        else:
            team2_champs.append(p["championName"])

    winner = 1 if team1_win else 2

    queue_id = info.get("queueId")
    queue_map = {
        420: "RANKED_SOLO_5x5",
        430: "NORMAL",
        440: "RANKED_FLEX_SR",
        450: "ARAM",
    }
    queue_type = queue_map.get(queue_id, "UNKNOWN")

    return team1_champs, team2_champs, winner, queue_type

try:
    summoner = get_summoner_data(summoner_name, tagLine)
    puuid = summoner["puuid"]
    match_ids = get_match_ids(puuid, count=10)
    region = SUMMONER_REGION

    for match_id in match_ids:
        try:
            match = get_match_data(match_id)
            team1, team2, winner, queue_type = extract_match_info(match)

            if queue_types_to_include and queue_type not in queue_types_to_include:
                print(f"Skipping match {match_id} (queueType={queue_type})")
                continue

            file_name = f"{tier}_{region}.csv"
            file_path = os.path.join("CSVs/Europe", file_name)
            file_exists = os.path.isfile(file_path)

            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow([
                        "t1_top", "t1_jg", "t1_mid", "t1_adc", "t1_supp",
                        "t2_top", "t2_jg", "t2_mid", "t2_adc", "t2_supp",
                        "winner", "tier", "region", "queueType"
                    ])

                writer.writerow(team1 + team2 + [winner, tier, region, queue_type])

            print(f"✅ Saved match {match_id} to {file_name}")
            time.sleep(1.2)

        except Exception as e:
            print(f"⚠️ Error with match {match_id}: {e}")

except Exception as e:
    print(f"❌ Failed to start script: {e}")
