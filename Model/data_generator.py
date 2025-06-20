import os
import csv
import time
from riot_api import get_summoner_data, get_match_ids, get_match_data
from match_utils import extract_match_info, tier_encoding, region_encoding
from champ_roles import champ_to_role
from summoners import summoners

def generate_data(queue_types_to_include=None, max_rows_per_tier=2000):
    if queue_types_to_include is None:
        queue_types_to_include = ["RANKED_SOLO_5x5", "NORMAL", "RANKED_FLEX_SR"]
    
    for summoner_group in summoners:
        summoner_names = summoner_group["summoner_names"]
        tagLines = summoner_group["tagLines"]
        tier = summoner_group["tier"]
        region = summoner_group["region"]
        output_dir = os.path.join(os.path.dirname(__file__), f"CSVs")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{region}.csv")
        
        rows_written = 0
        
        try:
            for summoner_name, tagLine in zip(summoner_names, tagLines):
                if rows_written >= max_rows_per_tier:
                    print(f"✅ Reached maximum of {max_rows_per_tier} rows for tier {tier}")
                    break
                    
                summoner = get_summoner_data(summoner_name, tagLine, region)
                puuid = summoner["puuid"]
                match_ids = get_match_ids(puuid, 0 , 250, region)

                for match_id in match_ids:
                    if rows_written >= max_rows_per_tier:
                        break
                        
                    try:
                        match = get_match_data(match_id, region)
                        result = extract_match_info(match)
                        if result is None:
                            print(f"⏩ Skipping {match_id} (invalid queue type)")
                            continue
                        
                        champ_values, winner, queue_type = result

                        file_exists = os.path.isfile(file_path)
                        with open(file_path, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            if not file_exists:
                                header = list(champ_to_role.keys()) + ["winner", "tier", "region"]
                                writer.writerow(header)
                        
                            writer.writerow(champ_values + [
                                winner,
                                tier_encoding[tier],
                                region_encoding[region], 
                            ])
                            rows_written += 1

                        print(f"✅ Saved {match_id} (Row {rows_written}/{max_rows_per_tier})")
                        time.sleep(1.2)

                    except Exception as e:
                        print(f"⚠️ Error in {match_id}: {summoner_name}")

        except Exception as e:
            print(f"❌ Failed to run script for summoner group: {e}") 