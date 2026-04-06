import random
import pandas as pd

off_archetypes = {
    "SNP": {
        "Shooting": (86, 5),
        "Playmaking": (73, 5),
        "Defense": (70, 5),
        "Physicality": (71, 5),
        "Max": "Shooting",
        "Difference": None
    },
    "PLY": {
        "Shooting": (71, 5),
        "Playmaking": (88, 5),
        "Defense": (71, 5),
        "Physicality": (70, 5),
        "Max": "Playmaking",
        "Difference": None
    },
    "TWF": {
        "Shooting": (76, 5),
        "Playmaking": (77, 5),
        "Defense": (74, 5),
        "Physicality": (73, 5),
        "Max": None,
        "Difference": 5
    },
    "ENF": {
        "Shooting": (69, 5),
        "Playmaking": (73, 5),
        "Defense": (73, 5),
        "Physicality": (85, 5),
        "Max": "Physicality",
        "Difference": None
    },
    "PWF": {
        "Shooting": (76, 5),
        "Playmaking": (71, 5),
        "Defense": (72, 5),
        "Physicality": (81, 5),
        "Max": "Physicality",
        "Difference": 5
    }
}

def_archetypes = {
    "OFD": {
        "Shooting": (71, 5),
        "Playmaking": (82, 5),
        "Defense": (76, 5),
        "Physicality": (72, 5),
        "Max": "Playmaking",
        "Difference": None
    },
    "DFD": {
        "Shooting": (67, 5),
        "Playmaking": (67, 5),
        "Defense": (85, 5),
        "Physicality": (81, 5),
        "Max": "Defense",
        "Difference": None
    },
    "TWD": {
        "Shooting": (73, 5),
        "Playmaking": (74, 5),
        "Defense": (77, 5),
        "Physicality": (76, 5),
        "Max": None,
        "Difference": 5
    }
}

def off_def():
    threshold = random.random()
    if threshold >= 0.4:
        return "Offense"
    elif threshold < 0.4:
        return "Defense"

def assign_position(off_or_def):
    threshold = random.random()
    if off_or_def == "Offense":
        if threshold < 1/3:
            return "LW"
        elif 1/3 <= threshold < 2/3:
            return "C"
        elif threshold >= 2/3:
            return "RW"
    elif off_or_def == "Defense":
        if threshold <= 0.5:
            return "LD"
        elif threshold > 0.5:
            return "RD"

def get_off_pos():
    threshold = random.random()
    if threshold < 0.25:
        return "SNP"
    elif 0.25 <= threshold < 0.5:
        return "PLY"
    elif 0.5 <= threshold < 0.8:
        return "TWF"
    elif 0.8 <= threshold < 0.95:
        return "PWF"
    elif threshold >= 0.95:
        return "ENF"
    else:
        return "Error!"

def get_def_pos():
    threshold = random.random()
    if threshold < 0.35:
        return "TWD"
    elif 0.35 <= threshold < 0.7:
        return "DFD"
    elif threshold >= 0.7:
        return "OFD"
    else:
        return "Error!"
    
def get_max(shooting, playmaking, defense, physicality):
        maximum = max(shooting, playmaking, defense, physicality)
        if maximum == shooting:
            return "Shooting"
        elif maximum == playmaking:
            return "Playmaking"
        elif maximum == defense:
            return "Defense"
        elif maximum == physicality:
            return "Physicality"

def get_player_ratings(archetype_dict, archetype):
    while True:
        shooting = min(random.gauss(archetype_dict[archetype]["Shooting"][0], archetype_dict[archetype]["Shooting"][1]),99)
        playmaking = min(random.gauss(archetype_dict[archetype]["Playmaking"][0], archetype_dict[archetype]["Playmaking"][1]),99)
        defense = min(random.gauss(archetype_dict[archetype]["Defense"][0], archetype_dict[archetype]["Defense"][1]),99)
        physicality = min(random.gauss(archetype_dict[archetype]["Physicality"][0], archetype_dict[archetype]["Physicality"][1]),99)

        if archetype_dict[archetype]["Max"] is not None:
            if get_max(shooting, playmaking, defense, physicality) != archetype_dict[archetype]["Max"]:
                continue
            
        if archetype_dict[archetype]["Difference"] is not None:
            if abs(((shooting + playmaking) - (1.3*defense + 0.7*physicality))) > archetype_dict[archetype]["Difference"]:
                continue
            
        return (shooting, playmaking, defense, physicality)


def generate_player_id(counter):
    return f"P{counter:05d}"

def generate_player():
    is_off_def = off_def()
    if is_off_def == "Offense":
        arch = get_off_pos()
        pos = assign_position("Offense")
        player = (get_player_ratings(off_archetypes, arch), arch, pos)
        return player
    elif is_off_def == "Defense":
        arch = get_def_pos()
        pos = assign_position("Defense")
        player = (get_player_ratings(def_archetypes, arch), arch, pos)
        return player

players = []
player_counter = 1

for _ in range(100):
    new_player = generate_player()

    player_id = generate_player_id(player_counter)

    player = {
        "player_id": player_id,
        "pos": new_player[2],
        "arch": new_player[1],
        "shooting": new_player[0][0],
        "playmaking": new_player[0][1],
        "defense": new_player[0][2],
        "physicality": new_player[0][3],
        "drafted_by": None
    }

    players.append(player)
    player_counter += 1

df = pd.DataFrame(players)
