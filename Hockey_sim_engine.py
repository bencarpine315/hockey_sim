import pandas as pd
import random as rand
import math
import numpy as np

df = pd.read_excel("NHLplayers.xlsx")
df.to_csv("NHLplayers.csv", index=False)

def faceoff(off_line_a, off_line_b):
    a_center = off_line_a[off_line_a["POS"] == 'C']
    b_center = off_line_b[off_line_b["POS"] == 'C']
    a_center_player = a_center.iloc[0]
    b_center_player = b_center.iloc[0]
    faceoff_threshold = a_center_player['Faceoff'] + b_center_player['Faceoff']
    faceoff_roll = rand.randint(0, math.ceil(faceoff_threshold))
    if faceoff_roll < a_center_player['Faceoff']:
        return 'A'
    else:
        return 'B'


def event_roll(off_line_a, off_line_b, def_line_a, def_line_b, event_roll_modifier=1):
    gross_production = off_line_a['O_Rating'].sum() + off_line_b['D_Rating'].sum() + def_line_a['O_Rating'].sum() + def_line_b['D_Rating'].sum()
    a_gross_o_rating = off_line_a['O_Rating'].sum() + def_line_a['O_Rating'].sum()
    roll = rand.randint(0,math.ceil(gross_production))
    return (roll*1.1*event_roll_modifier) < a_gross_o_rating

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
        shot_threshold = 55
        event_mod = 0.9
    elif player["PlayerType"] == "PLY":
        shot_threshold = 25
        event_mod = 0.65
    elif player["PlayerType"] == "TWF":
        shot_threshold = 40
        event_mod = 0.8
    elif player["PlayerType"] == "PWF":
        shot_threshold = 35
        event_mod = 0.825
    elif player["PlayerType"] == "ENF":
        shot_threshold = 25
        event_mod = 0.85
    elif player["PlayerType"] == "OFD":
        shot_threshold = 30
        event_mod = 0.875
    elif player["PlayerType"] == "TWD":
        shot_threshold = 20
        event_mod = 0.975
    elif player["PlayerType"] == "DFD":
        shot_threshold = 5
        event_mod = 1
    shot_chance = rand.randint(0, 100)
    return shot_chance < shot_threshold, event_mod

def shot(player, goalie, shot_mod=1):
    goalie_row = goalie.iloc[0]
    shot_sum = math.ceil(goalie_row["Goaltend"] + (0.04 * shot_mod * player["Shooting"]))
    shot_roll = rand.randint(0, shot_sum)
    if shot_roll < goalie_row["Goaltend"]:
        return False
    else:
        return True
    
def rebound_roll(goalie):
    goalie_row = goalie.iloc[0]
    rebound_chance = rand.randint(0,100)
    goalie_save = goalie_row["Goaltend"]
    return rebound_chance < goalie_save

def make_list(kinda_list):
    newlist = []
    for player in kinda_list:
        player_name = str(player["Name"] + " " + player["Surname"] + ", (" + player["Team"] + ")")
        newlist.append(player_name)
    return newlist

def powerplay(a_team_opp, a_team_dpp, b_team_opk, b_team_dpk, a_team_g, b_team_g, a_team_opp_ref, a_team_dpp_ref, b_team_opk_ref, b_team_dpk_ref, a_shots, b_shots, shift_time, assists: list, just_scored: bool, my_event_roll_modifier=1, my_shot_mod=1):
    # Will eventually allow for two-minute PPs #
    # Penalties will occur randomly based off of discipline/awareness rating, yet to be added #
    
    pass
    

    
def gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, assists: list, just_scored: bool, overtime: bool, my_event_roll_modifier=1, my_shot_mod=1):
    if (time == 0 or just_scored == True) and overtime==True and team_a_score != team_b_score:
        return team_a_score, team_b_score, a_shots, b_shots, time
    elif time == 0 or just_scored == True:
        time += 3
        if faceoff(a_team_o, b_team_o)=='A':
            # print("team A wins faceoff")
            center = get_pos(a_team_o, a_team_d, "C")
            new_assists = [center]
            # print(f'{make_list(new_assists)} is the current assists list. {center["Name"]} {center["Surname"]} was added after the player won the opening faceoff.')
            return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False, overtime)
        else:
            # print("team B wins faceoff")
            center = get_pos(b_team_o, b_team_d, "C")
            new_assists = [center]
            # print(f'{make_list(new_assists)} is the current assists list. {center["Name"]} {center["Surname"]} was added after the player won the opening faceoff.')
            return gameplay(b_team_o, b_team_d, a_team_o, a_team_d, b_team_g, a_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False, overtime)
    elif time != 0 and time > shift_time:
        # print(f"Team A: {team_a_score} | Team B: {team_b_score}")
        # print(f"{time} seconds have elapsed, which should be greater than {shift_time}")
        # print("######################   Period expired   ################################")
        # print(f"Bruins scored {team_a_score}, and Maple Leafs scored {team_b_score}.")
        # print(f'Bruins shot the puck {a_shots} times, and Maple Leafs shot it {b_shots} times.')
        # print(f"The debug values are as follows: team_a_score = {team_a_score}, team_b_score = {team_b_score}, a_shots = {a_shots}, b_shots = {b_shots}, time = {time}")
        # print(team_a_score, team_b_score)
        return team_a_score, team_b_score, a_shots, b_shots, time
    else:
        b_team_g_row = b_team_g.iloc[0]
        check_event = event_roll(a_team_o, b_team_o, a_team_d, b_team_d, my_event_roll_modifier)
        # print("The offense is looking for a chance...")
        time += rand.randint(6,9)
        if check_event == True:
            # print("The offense has an opportunity!")
            player = pick_shooter(a_team_o, a_team_d)
            pass_chance = pass_or_shoot(player)
            if pass_chance[0] == True:
                # print(f"{player['Name']} {player['Surname']} gets a look on net")
                pass
            else:
                # print(f"{player['Name']} {player['Surname']} chooses to pass")
                # print(make_list(assists))
                new_assists = assists + [player]
                # print(f'{make_list(new_assists)} is the current assists list. {player["Name"]} {player["Surname"]} was added after the player chose to pass.')
                return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False,overtime, my_event_roll_modifier*(pass_chance[1]), my_shot_mod*1.05)
            shot_chance = shot(player, b_team_g, my_shot_mod)
            time += rand.randint(3,6)
            if shot_chance == True:
                print(f'{player["Name"]} {player["Surname"]} ({player["POS"]}, {player["Team"]}, {player["PlayerType"]}, line {player["Line"]}) scores on {b_team_g_row["Name"]} {b_team_g_row["Surname"]}.')
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
                    if player['PlayerID'] in a_team_o_ref['PlayerID'].values or player['PlayerID'] in a_team_d_ref['PlayerID'].values:
                        a_shots +=1
                        team_a_score +=1
                    elif player['PlayerID'] in b_team_o_ref['PlayerID'].values or player['PlayerID'] in b_team_d_ref['PlayerID'].values:
                        b_shots +=1
                        team_b_score +=1
                return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, [], True,overtime)
            else:
                time += rand.randint(5,8)
                # print(f'{player["Name"]} {player["Surname"]} had a chance to score, but the save was made by {b_team_g_row["Name"]} {b_team_g_row["Surname"]}.')
                rebound_roll_variable = rebound_roll(b_team_g)
                if rebound_roll_variable == True:
                    # print(make_list(assists))
                    new_assists = assists + [player]
                    # print(f'{make_list(new_assists)} is the current assists list. {player["Name"]} {player["Surname"]} was added after his shot went up for a rebound. The list should only contain his teammates.')
                    # print(make_list(assists))
                    # print("Rebound gets loose! Puck is up for grabs")
                    time += rand.randint(5,8)
                    if player['PlayerID'] in a_team_o_ref['PlayerID'].values or player['PlayerID'] in a_team_d_ref['PlayerID'].values:
                        a_shots += 1
                        # return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, assists, 1)
                    elif player['PlayerID'] in b_team_o_ref['PlayerID'].values or player['PlayerID'] in b_team_d_ref['PlayerID'].values:
                        b_shots += 1
                    return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False,overtime, my_event_roll_modifier*0.9, my_shot_mod*1.11)
                else:
                    # print("The puck is stopped and play will resume after a faceoff.")
                    if player['PlayerID'] in a_team_o_ref['PlayerID'].values or player['PlayerID'] in a_team_d_ref['PlayerID'].values:
                        a_shots+=1
                        # return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots+1, b_shots, shift_time, new_assists, False)
                    elif player['PlayerID'] in b_team_o_ref['PlayerID'].values or player['PlayerID'] in b_team_d_ref['PlayerID'].values:
                        b_shots+=1
                    return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, [], True,overtime)
        elif check_event == False:
            time += rand.randint(7,10)
            if rand.randint(0,1)==0:
                ld = get_pos(b_team_o, b_team_d, "LD")
                new_assists = [ld]
                # print(f'{make_list(new_assists)} is the current assists list. {ld["Name"]} {ld["Surname"]} was added after a takeaway, as he is the defenseman.')
                return gameplay(b_team_o, b_team_d, a_team_o, a_team_d, b_team_g, a_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False,overtime)
            else:
                rd = get_pos(b_team_o, b_team_d, "RD")
                new_assists = [rd]
                # print(f'{make_list(new_assists)} is the current assists list. {rd["Name"]} {rd["Surname"]} was added after a takeaway, as he is the defenseman.')
                return gameplay(b_team_o, b_team_d, a_team_o, a_team_d, b_team_g, a_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, new_assists, False,overtime)
    return team_a_score, team_b_score, a_shots, b_shots, time


                            ########################################
                            # Overtime needs a revamp and overhaul #
                            # In it's current form, OT is too      #
                            # simple and inaccurate. OT has it's   #
                            # own mechanics that are different     #
                            # from traditional gameplay() func.    #
                            ######################################## 


def ot_gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, assists: list, just_scored: bool, overtime: bool):
    return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, assists, just_scored, overtime)
    
    
    # if just_scored == True and team_a_score != team_b_score:
    #     return team_a_score, team_b_score, a_shots, b_shots
    # else:
    #     return gameplay(a_team_o, a_team_d, b_team_o, b_team_d, a_team_g, b_team_g, time, team_a_score, team_b_score, a_team_o_ref, a_team_d_ref, b_team_o_ref, b_team_d_ref, a_team_g_ref, b_team_g_ref, a_shots, b_shots, shift_time, [], False)
