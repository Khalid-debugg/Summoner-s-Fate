from champ_roles import champ_to_role

tier_encoding = {
    "IRON": 1,
    "BRONZE": 2,
    "SILVER": 3,
    "GOLD": 4,
    "PLATINUM": 5,
    "EMERALD": 6,
    "DIAMOND": 7,
    "MASTER": 8,
    "GRANDMASTER": 9,
    "CHALLENGER": 10
}

region_encoding = {
    "europe": 1,
    "americas": 2,
    "asia": 3
}

queue_encoding = {
    "NORMAL": 1,
    "RANKED_SOLO_5x5": 2,
    "RANKED_FLEX_SR": 3,
    "DRAFT_PICK": 4
}

def extract_match_info(match):
    info = match["info"]
    participants = info["participants"]
    
    champ_presence = {champ: 0 for champ in champ_to_role.keys()}
    
    for p in participants:
        champ = p["championName"].strip()
        if p["teamId"] == 100:
            champ_presence[champ] = 1
        else:
            champ_presence[champ] = 2
    
    queue_map = {
        400: "DRAFT_PICK",  
        420: "RANKED_SOLO_5x5",
        430: "NORMAL",  
        440: "RANKED_FLEX_SR"  
    }
    
    queue_type = queue_map.get(info.get("queueId"))
    
    if not queue_type or queue_type not in queue_encoding:
        return None
    
    winner = 1 if any(p["teamId"] == 100 and p["win"] for p in participants) else 2
    
    champ_values = [champ_presence[champ] for champ in champ_to_role.keys()]
    
    return champ_values, winner, queue_encoding[queue_type]

