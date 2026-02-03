import pandas as pd
import random as rand
import math

def faceoff(off_line_a, off_line_b):
    # Finds centers from each line
    a_center = next((p for p in off_line_a if p["POS"] == "C"), None)
    b_center = next((p for p in off_line_b if p["POS"] == "C"), None)
    
    if a_center is None or b_center is None:
        raise ValueError("Faceoff error: missing center position on one line")
    
    # total skill determines odds
    total = a_center['Faceoff'] + b_center['Faceoff']
    if total <= 0:
        # fallback - random 50/50 if both faceoff stats are zero (should never occur)
        return rand.choice(['A', 'B'])
    
    # probabilistic roll
    return 'A' if rand.random() < (a_center['Faceoff'] / total) else 'B'


def event_roll(off_line_a, off_line_b, def_line_a, def_line_b, event_roll_modifier=1):
    gross_production = off_line_a['O_Rating'].sum() + off_line_b['D_Rating'].sum() + def_line_a['O_Rating'].sum() + def_line_b['D_Rating'].sum()
    a_gross_o_rating = off_line_a['O_Rating'].sum() + def_line_a['O_Rating'].sum()
    roll = rand.randint(0,math.ceil(gross_production))
    return (roll*event_roll_modifier) < a_gross_o_rating

def pick_shooter(off_line, def_line):
    all_players = pd.concat([off_line, def_line], ignore_index=True)
    shooting_sum = all_players['Shooting'].sum()
    shooter_roll = rand.randint(0,math.ceil(shooting_sum))
    shooting_index = 0
    for idx, player in all_players.iterrows():
        shooting_index += player["Shooting"]
        if shooter_roll <= shooting_index:
            return player
        else:
            continue

def get_pos(off_line, def_line, pos):
    all_players = pd.concat([off_line, def_line], ignore_index=True)
    for idx, player in all_players.iterrows():
        if player["POS"]==pos:
            return player

def pass_or_shoot(player):
    if player["PlayerType"] == "SNP":
        shot_threshold = 45
        event_mod = 0.6
        shot_mod = 1.005
    elif player["PlayerType"] == "PLY":
        shot_threshold = 15
        event_mod = 0.35
        shot_mod = 1.11
    elif player["PlayerType"] == "TWF":
        shot_threshold = 35
        event_mod = 0.5
        shot_mod = 1.06
    elif player["PlayerType"] == "PWF":
        shot_threshold = 30
        event_mod = 0.525
        shot_mod = 1.03
    elif player["PlayerType"] == "ENF":
        shot_threshold = 20
        event_mod = 0.55
        shot_mod = 1.01
    elif player["PlayerType"] == "OFD":
        shot_threshold = 25
        event_mod = 0.575
        shot_mod = 1.04
    elif player["PlayerType"] == "TWD":
        shot_threshold = 12
        event_mod = 0.675
        shot_mod = 1.02
    elif player["PlayerType"] == "DFD":
        shot_threshold = 5
        event_mod = 0.7
        shot_mod = 1.005
    shot_chance = rand.randint(0, 50)
    return shot_chance < shot_threshold, event_mod, shot_mod

def shot(player: dict, goalie: dict, shot_mod: float = 1.0) -> bool:
    # Base stats
    shooting = float(player['Shooting'])
    goaltend = float(goalie["Goaltend"])

    adjusted_difficulty = goaltend + (0.1 * shot_mod * shooting)

    roll = rand.random() * adjusted_difficulty
    return roll > goaltend

def rebound_roll(goalie):
    goaltend = float(goalie['Goaltend'])

    rebound_probability = max(0.05, (100-goaltend) / 200)

    return rand.random() < rebound_probability

def make_list(kinda_list):
    newlist = []
    for player in kinda_list:
        player_name = str(player["Name"] + " " + player["Surname"] + ", (" + player["Team"] + ")")
        newlist.append(player_name)
    return newlist

def powerplay(a_team_opp, a_team_dpp, b_team_opk, b_team_dpk, a_team_g, b_team_g, a_team_opp_ref, a_team_dpp_ref, b_team_opk_ref, b_team_dpk_ref, a_shots : list, b_shots : list, shift_time, assists: list, just_scored: bool, my_event_roll_modifier=1, my_shot_mod=1):
    # Will eventually allow for two-minute PPs #
    # Penalties will occur randomly based off of discipline/awareness rating, yet to be added #
    
    pass
    
def shootout(a_team_shooters, b_team_shooters, a_team_g, b_team_g):
    pass

def new_gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, shift_time, overtime: bool, a_city, a_name, b_city, b_name):
    a_team_o_list = a_team_o.to_dict('records')
    b_team_o_list = b_team_o.to_dict('records')
    a_goalie = a_team_g.iloc[0].to_dict()
    b_goalie = b_team_g.iloc[0].to_dict()


    time=0
    a_score = 0
    a_shots = 0
    b_score = 0
    b_shots = 0
    just_stopped = False
    just_scored = False
    opening = False
    assists = []
    just_passed = None
    my_event_roll_modifier = 1
    my_shot_mod = 1
    while time < shift_time:
        if just_scored==True and overtime==True:
            return a_score, b_score, a_shots, b_shots, time
        elif time == 0 or just_stopped == True or just_scored == True:
            # print("Either the time here should be 0, they should have just scored, or the puck was stopped after a shot.")
            just_stopped, just_scored = False, False
            time += 3
            if faceoff(a_team_o_list, b_team_o_list)=='A':
                # print(f"{a_city} wins the faceoff")
                center = get_pos(a_team_o, a_team_d, "C")
                assists = [center]
                o_off, o_def, d_off, d_def, o_g, d_g, o_city, d_city = a_team_o, a_team_d, b_team_o, b_team_d, a_goalie, b_goalie, a_city, b_city
                continue
            else:
                # print(f"{b_city} wins the faceoff")
                center = get_pos(b_team_o, b_team_d, "C")
                assists = [center]
                o_off, o_def, d_off, d_def, o_g, d_g, o_city, d_city = b_team_o, b_team_d, a_team_o, a_team_d, b_goalie, a_goalie, b_city, a_city
        else:
            check_event = event_roll(o_off, d_off, o_def, d_def, my_event_roll_modifier)
            # print(f"{o_city} is looking for a chance...")
            time += rand.randint(5,8)
            if check_event == True:
                # print(f"{o_city} has an opportunity!")
                player = pick_shooter(o_off, o_def)
                if just_passed == None:
                    just_passed = player['PlayerID']
                else:
                    if player['PlayerID'] == just_passed:
                        # print(f"{player['Name']} {player['Surname']} just passed, so in an effort to not pass to himself, the player is being reassigned.")
                        while player['PlayerID'] == just_passed:
                            player = pick_shooter(o_off, o_def)
                    else:
                        pass
                just_passed = player['PlayerID']
                pass_chance = pass_or_shoot(player)
                if pass_chance[0] == True and opening == True:
                    # print(f"{player['Name']} {player['Surname']} gets a look on net")
                    pass
                else:
                    # print(f"{player['Name']} {player['Surname']} chooses to pass")
                    assists.append(player)
                    # print(make_list(assists))
                    if (pass_chance[1]*100 < rand.randint(1, 100)):
                        my_event_roll_modifier, my_shot_mod, opening = my_event_roll_modifier*pass_chance[1], my_shot_mod*pass_chance[2], True
                        continue
                    else:
                        my_event_roll_modifier, my_shot_mod, opening = my_event_roll_modifier*pass_chance[1], my_shot_mod*pass_chance[2], False
                        continue
                opening = False
                shot_chance = shot(player.to_dict(), d_g, my_shot_mod)
                time += rand.randint(1,4)
                if shot_chance == True:
                    print(f'{player["Name"]} {player["Surname"]} ({player["POS"]}, {player["Team"]}, {player["PlayerType"]}, line {player["Line"]}) scores on {d_g["Name"]} {d_g["Surname"]}.')
                    last_two_assists = assists[-2:]
                    if len(last_two_assists) == 2:
                        if last_two_assists[0].equals(last_two_assists[1]):
                            last_two_assists = last_two_assists[-1:]
                    player_ids = [s['PlayerID'] for s in last_two_assists]
                    if player['PlayerID'] in player_ids:
                        idx = player_ids.index(player['PlayerID'])
                        last_two_assists.pop(idx)
                    if len(last_two_assists) == 0:
                        print("UNASSISTED\n")
                    else:
                        print("ASSISTS:")
                        for guy in last_two_assists:
                            print(f'{guy["Name"]} {guy["Surname"]} ({guy["POS"]}, {guy["Team"]})  gets an assist.')
                        print('\n')
                    if player['PlayerID'] in a_team_o['PlayerID'].values or player['PlayerID'] in a_team_d['PlayerID'].values:
                        a_shots+=1
                        a_score+=1
                    elif player['PlayerID'] in b_team_o['PlayerID'].values or player['PlayerID'] in b_team_d['PlayerID'].values:
                        b_shots+=1
                        b_score+=1
                    assists=[]
                    just_scored = True
                    # print(f"TEAM A SCORE: {a_score}    SHOTS {a_shots}")
                    # print(f"TEAM B SCORE: {b_score}    SHOTS {b_shots}")
                    my_event_roll_modifier, my_shot_mod = 1, 1
                    continue
                else:
                    time += rand.randint(3,6)
                    # print(f'{player["Name"]} {player["Surname"]} had a chance to score, but the save was made by {d_g_row["Name"]} {d_g_row["Surname"]}.')
                    rebound_roll_variable = rebound_roll(d_g)
                    my_event_roll_modifier, my_shot_mod = 1, 1
                    if rebound_roll_variable == True:
                        assists.append(player)
                        # print(make_list(assists))
                        # print("Rebound gets loose! Puck is up for grabs")
                        time += rand.randint(5,8)
                        if player['PlayerID'] in a_team_o['PlayerID'].values or player['PlayerID'] in a_team_d['PlayerID'].values:
                            a_shots+=1
                        elif player['PlayerID'] in b_team_o['PlayerID'].values or player['PlayerID'] in b_team_d['PlayerID'].values:
                            b_shots+=1
                        continue
                    else:
                        # print("The puck is stopped and play will resume after a faceoff.")
                        if player['PlayerID'] in a_team_o['PlayerID'].values or player['PlayerID'] in a_team_d['PlayerID'].values:
                            a_shots+=1
                        elif player['PlayerID'] in b_team_o['PlayerID'].values or player['PlayerID'] in b_team_d['PlayerID'].values:
                            b_shots+=1
                        just_stopped = True
                        continue
            elif check_event == False:
                my_event_roll_modifier, my_shot_mod = 1, 1
                # print(f"{d_city} takes the puck away.")
                time += rand.randint(7,10)
                if rand.randint(0,1)==0:
                    ld = get_pos(d_off, d_def, "LD")
                    assists = [ld]
                    o_off, o_def, d_off, d_def, o_g, d_g, o_city, d_city = d_off, d_def, o_off, o_def, d_g, o_g, d_city, o_city
                    continue
                else:
                    rd = get_pos(d_off, d_def, "RD")
                    assists = [rd]
                    o_off, o_def, d_off, d_def, o_g, d_g, o_city, d_city = d_off, d_def, o_off, o_def, d_g, o_g, d_city, o_city
                    continue

    # print(f"Team A scored {a_score} on {a_shots} and Team B scored {b_score} on {b_shots} in this period.\n\n\n")
    return a_score, b_score, a_shots, b_shots, time
                    