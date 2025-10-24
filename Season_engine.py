from Hockey_sim_engine import gameplay, ot_gameplay, new_gameplay
import pandas as pd

df = pd.read_excel("NHLplayers.xlsx")
df.to_csv("NHLplayers.csv", index=False)

#####################
#   Lines 1-4 are offensive
#   Lines 5-7 are defensive
#   Lines 8 and 9 are goalies
#   Line 0 is scratched players
#####################

bos_line1 = df[(df["Line"] == 1) & (df["Team"] == "BOS")]
bos_line2 = df[(df["Line"] == 2) & (df["Team"] == "BOS")]
bos_line3 = df[(df["Line"] == 3) & (df["Team"] == "BOS")]
bos_line4 = df[(df["Line"] == 4) & (df["Team"] == "BOS")]
bos_line5 = df[(df["Line"] == 5) & (df["Team"] == "BOS")]
bos_line6 = df[(df["Line"] == 6) & (df["Team"] == "BOS")]
bos_line7 = df[(df["Line"] == 7) & (df["Team"] == "BOS")]
bos_line8 = df[(df["Line"] == 8) & (df["Team"] == "BOS")]
bos_line9 = df[(df["Line"] == 9) & (df["Team"] == "BOS")]
bos = [bos_line1, bos_line2, bos_line3, bos_line4, bos_line5, bos_line6, bos_line7, bos_line8, bos_line9, "Boston", "Bruins"]

tor_line1 = df[(df["Line"] == 1) & (df["Team"] == "TOR")]
tor_line2 = df[(df["Line"] == 2) & (df["Team"] == "TOR")]
tor_line3 = df[(df["Line"] == 3) & (df["Team"] == "TOR")]
tor_line4 = df[(df["Line"] == 4) & (df["Team"] == "TOR")]
tor_line5 = df[(df["Line"] == 5) & (df["Team"] == "TOR")]
tor_line6 = df[(df["Line"] == 6) & (df["Team"] == "TOR")]
tor_line7 = df[(df["Line"] == 7) & (df["Team"] == "TOR")]
tor_line8 = df[(df["Line"] == 8) & (df["Team"] == "TOR")]
tor_line9 = df[(df["Line"] == 9) & (df["Team"] == "TOR")]
tor = [tor_line1, tor_line2, tor_line3, tor_line4, tor_line5, tor_line6, tor_line7, tor_line8, tor_line9, "Toronto", "Maple Leafs"]

ott_line1 = df[(df["Line"] == 1) & (df["Team"] == "OTT")]
ott_line2 = df[(df["Line"] == 2) & (df["Team"] == "OTT")]
ott_line3 = df[(df["Line"] == 3) & (df["Team"] == "OTT")]
ott_line4 = df[(df["Line"] == 4) & (df["Team"] == "OTT")]
ott_line5 = df[(df["Line"] == 5) & (df["Team"] == "OTT")]
ott_line6 = df[(df["Line"] == 6) & (df["Team"] == "OTT")]
ott_line7 = df[(df["Line"] == 7) & (df["Team"] == "OTT")]
ott_line8 = df[(df["Line"] == 8) & (df["Team"] == "OTT")]
ott_line9 = df[(df["Line"] == 9) & (df["Team"] == "OTT")]
ott = [ott_line1, ott_line2, ott_line3, ott_line4, ott_line5, ott_line6, ott_line7, ott_line8, ott_line9, "Ottawa", "Senators"]

buf_line1 = df[(df["Line"] == 1) & (df["Team"] == "BUF")]
buf_line2 = df[(df["Line"] == 2) & (df["Team"] == "BUF")]
buf_line3 = df[(df["Line"] == 3) & (df["Team"] == "BUF")]
buf_line4 = df[(df["Line"] == 4) & (df["Team"] == "BUF")]
buf_line5 = df[(df["Line"] == 5) & (df["Team"] == "BUF")]
buf_line6 = df[(df["Line"] == 6) & (df["Team"] == "BUF")]
buf_line7 = df[(df["Line"] == 7) & (df["Team"] == "BUF")]
buf_line8 = df[(df["Line"] == 8) & (df["Team"] == "BUF")]
buf_line9 = df[(df["Line"] == 9) & (df["Team"] == "BUF")]
buf = [buf_line1, buf_line2, buf_line3, buf_line4, buf_line5, buf_line6, buf_line7, buf_line8, buf_line9, "Buffalo", "Sabres"]





teams = {
    "bos" : bos,
    "tor" : tor,
    "ott" : ott,
    "buf" : buf
}

def single_game(teams: dict, teama: str, teamb: str):
    for key,value in teams.items():
        if teama == key:
            team1 = value
            break
        else:
            continue
    for key,value in teams.items():
        if teamb == key:
            team2 = value
            break
        else:
            continue
    first_line = new_gameplay(team1[0], team1[4], team2[0], team2[4], team1[7], team2[7], 20*60, False)
    second_line = new_gameplay(team1[1], team1[5], team2[1], team2[5], team1[7], team2[7], 17*60, False)
    third_line = new_gameplay(team1[2], team1[6], team2[2], team2[6], team1[7], team2[7], 15*60, False)
    fourth_line_1 = new_gameplay(team1[3], team1[4], team2[3], team2[4], team1[7], team2[7], 4*60, False)
    fourth_line_2 = new_gameplay(team1[3], team1[5], team2[3], team2[5], team1[7], team2[7], 3*60, False)
    fourth_line_3 = new_gameplay(team1[3], team1[6], team2[3], team2[6], team1[7], team2[7], 2*60, False)

    team_1_score = first_line[0]+second_line[0]+third_line[0]+fourth_line_1[0]+fourth_line_2[0]+fourth_line_3[0]
    team_2_score = first_line[1]+second_line[1]+third_line[1]+fourth_line_1[1]+fourth_line_2[1]+fourth_line_3[1]
    team_1_shots = first_line[2]+second_line[2]+third_line[2]+fourth_line_1[2]+fourth_line_2[2]+fourth_line_3[2]
    team_2_shots = first_line[3]+second_line[3]+third_line[3]+fourth_line_1[3]+fourth_line_2[3]+fourth_line_3[3]

    print(f"{team1[9]} scored {team_1_score} on {team_1_shots} shots and {team2[9]} scored {team_2_score} on {team_2_shots} shots at the end of regulation.")
    
    if team_1_score == team_2_score:
        ot_line = new_gameplay(team1[0], team1[4], team2[0], team2[4], team1[7], team2[7], 300, True)
        team_1_score += ot_line[0]
        team_2_score += ot_line[1]
        team_1_shots += ot_line[2]
        team_2_shots += ot_line[3]
        print(f"Overtime elapsed: {ot_line[4]}")
        print(f"{team1[9]} scored {team_1_score} on {team_1_shots} shots and {team2[9]} scored {team_2_score} on {team_2_shots} shots at the end of overtime.")

# single_game(teams, "bos", "buf") ## Test case

single_game(teams, "bos", "tor")