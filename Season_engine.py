from Hockey_sim_engine import gameplay, ot_gameplay
import pandas as pd

df = pd.read_csv("C:\\users\\benca\\Desktop\\Personal Projects\\My own python stuff\\Hockey Sim\\NHL team.csv")

#####################
#   Lines 1-4 are offensive
#   Lines 5-7 are defensive
#   Lines 8 and beyond are goalies
#   Line 0 is scratched players
#####################

bos = "bos"
tor = "tor"
ott = "ott"

bos_line1 = df[(df["Line"] == 1) & (df["Team"] == "BOS")]
bos_line2 = df[(df["Line"] == 2) & (df["Team"] == "BOS")]
bos_line3 = df[(df["Line"] == 3) & (df["Team"] == "BOS")]
bos_line4 = df[(df["Line"] == 4) & (df["Team"] == "BOS")]
bos_line5 = df[(df["Line"] == 5) & (df["Team"] == "BOS")]
bos_line6 = df[(df["Line"] == 6) & (df["Team"] == "BOS")]
bos_line7 = df[(df["Line"] == 7) & (df["Team"] == "BOS")]
bos_line8 = df[(df["Line"] == 8) & (df["Team"] == "BOS")]
bos_line9 = df[(df["Line"] == 9) & (df["Team"] == "BOS")]

tor_line1 = df[(df["Line"] == 1) & (df["Team"] == "TOR")]
tor_line2 = df[(df["Line"] == 2) & (df["Team"] == "TOR")]
tor_line3 = df[(df["Line"] == 3) & (df["Team"] == "TOR")]
tor_line4 = df[(df["Line"] == 4) & (df["Team"] == "TOR")]
tor_line5 = df[(df["Line"] == 5) & (df["Team"] == "TOR")]
tor_line6 = df[(df["Line"] == 6) & (df["Team"] == "TOR")]
tor_line7 = df[(df["Line"] == 7) & (df["Team"] == "TOR")]
tor_line8 = df[(df["Line"] == 8) & (df["Team"] == "TOR")]
tor_line9 = df[(df["Line"] == 9) & (df["Team"] == "TOR")]

ott_line1 = df[(df["Line"] == 1) & (df["Team"] == "OTT")]
ott_line2 = df[(df["Line"] == 2) & (df["Team"] == "OTT")]
ott_line3 = df[(df["Line"] == 3) & (df["Team"] == "OTT")]
ott_line4 = df[(df["Line"] == 4) & (df["Team"] == "OTT")]
ott_line5 = df[(df["Line"] == 5) & (df["Team"] == "OTT")]
ott_line6 = df[(df["Line"] == 6) & (df["Team"] == "OTT")]
ott_line7 = df[(df["Line"] == 7) & (df["Team"] == "OTT")]
ott_line8 = df[(df["Line"] == 8) & (df["Team"] == "OTT")]
ott_line9 = df[(df["Line"] == 9) & (df["Team"] == "OTT")]



first_line = gameplay(bos_line1, bos_line5, tor_line1, tor_line5, bos_line8, tor_line8, 0, 0, 0, bos_line1, bos_line5, tor_line1, tor_line5, bos_line8, tor_line8, 0, 0, 20*60, [], False, False)
second_line = gameplay(bos_line2, bos_line6, tor_line2, tor_line6, bos_line8, tor_line8, 0, 0, 0, bos_line2, bos_line6, tor_line2, tor_line6, bos_line8, tor_line8, 0, 0, 17*60, [], False, False)
third_line = gameplay(bos_line3, bos_line7, tor_line3, tor_line7, bos_line8, tor_line8, 0, 0, 0, bos_line3, bos_line7, tor_line3, tor_line7, bos_line8, tor_line8, 0, 0, 15*60, [], False, False)
fourth_line_1 = gameplay(bos_line4, bos_line5, tor_line4, tor_line5, bos_line8, tor_line8, 0, 0, 0, bos_line4, bos_line5, tor_line4, tor_line5, bos_line8, tor_line8, 0, 0, 4*60, [], False, False)
fourth_line_2 = gameplay(bos_line4, bos_line6, tor_line4, tor_line6, bos_line8, tor_line8, 0, 0, 0, bos_line4, bos_line6, tor_line4, tor_line6, bos_line8, tor_line8, 0, 0, 3*60, [], False, False)
fourth_line_3 = gameplay(bos_line4, bos_line7, tor_line4, tor_line7, bos_line8, tor_line8, 0, 0, 0, bos_line4, bos_line7, tor_line4, tor_line7, bos_line8, tor_line8, 0, 0, 2*60, [], False, False)


bos_score = first_line[0]+second_line[0]+third_line[0]+fourth_line_1[0]+fourth_line_2[0]+fourth_line_3[0]
tor_score = first_line[1]+second_line[1]+third_line[1]+fourth_line_1[1]+fourth_line_2[1]+fourth_line_3[1]
bos_shots = first_line[2]+second_line[2]+third_line[2]+fourth_line_1[2]+fourth_line_2[2]+fourth_line_3[2]
tor_shots = first_line[3]+second_line[3]+third_line[3]+fourth_line_1[3]+fourth_line_2[3]+fourth_line_3[3]
print(f"Bruins scored {bos_score} on {bos_shots} shots and Maple Leafs scored {tor_score} on {tor_shots} shots at the end of regulation.")


if bos_score == tor_score:
    ot_line = ot_gameplay(bos_line1, bos_line5, tor_line1, tor_line5, bos_line8, tor_line8, 0, 0, 0, bos_line1, bos_line5, tor_line1, tor_line5, bos_line8, tor_line8, 0, 0, 300, [], False, True)
    bos_score += ot_line[0]
    tor_score += ot_line[1]
    bos_shots += ot_line[2]
    tor_shots += ot_line[3]
    print(f"Overtime elapsed: {ot_line[4]}")
    print(f"Bruins scored {bos_score} on {bos_shots} shots and Maple Leafs scored {tor_score} on {tor_shots} shots at the end of overtime.")

