import pandas as pd
import json, os
from os import path

os.chdir("main")
os.chdir("Gathered Data")

f = open("Extracted_Data.json", "r")
data = json.load(f)
f.close()

f = open("Pokemon_Database.json", "r")
info = json.load(f)
f.close()

os.chdir("..")
os.chdir("Analyses")

NU_leavers_types = {
    "Normal": 0,
    "Fire": 0,
    "Fighting": 0,
    "Water": 0,
    "Flying": 0,
    "Grass": 0,
    "Poison": 0,
    "Electric": 0,
    "Ground": 0,
    "Psychic": 0,
    "Rock": 0,
    "Ice": 0,
    "Bug": 0,
    "Dragon": 0,
    "Ghost": 0,
    "Dark": 0,
    "Steel": 0,
    "Fairy": 0
}

def num_type(poke_type):
    if "/" in poke_type:
        return "Multitype"
    else:
        return "Monotype"

def first_type(pokemon_type):
    if num_type(pokemon_type) == "Multitype":
        for i in range(len(pokemon_type) - 1):
            if pokemon_type[i] == "/":
                type_1 = pokemon_type[0:i]
    else:
        type_1 = pokemon_type

    return type_1

def second_type(pokemon_type):
    if num_type(pokemon_type) == "Multitype":
        for i in range(len(pokemon_type) - 1):
            if pokemon_type[i] == "/":
                type_2 = pokemon_type[i + 1: len(pokemon_type)]
    else:
        type_2 = ""

    return type_2

def remove_percent_to_int(number):
    if number != "":
        number = number[0:len(number) - 1]
        number = float(number)
    else:
        number = 0
    return number

def to_percent(number):
    number = 100 - number
    number = float(number)
    number = f"{number}%"
    return number

for tier in data:
    if path.exists(f"{tier} Metagame Analyses") == False:
        os.mkdir(f"{tier} Metagame Analyses")
    os.chdir(f"{tier} Metagame Analyses")

    if tier == "NU":
        in_data_1 = []
        in_data_2 = []
        column_1 = ["Name", "Dex Entry", "Type"]
        column_2 = ["Types", "Number"]
        types = []

        for leaver in data[tier]["NU leavers"]:
            in_data_1.append([leaver, info[leaver]["Dex Entry"], info[leaver]["Type"]])
            types.append(first_type(info[leaver]["Type"]))
            if second_type(info[leaver]["Type"]) != "":
                types.append(second_type(info[leaver]["Type"]))

        for poke_type in types:
            NU_leavers_types[poke_type] += 1

        for poke_type in NU_leavers_types:
            in_data_2.append([poke_type, NU_leavers_types[poke_type]])

        enter_1 = pd.DataFrame(in_data_1, columns=column_1)
        enter_2 = pd.DataFrame(in_data_2, columns=column_2)

        enter_1.to_csv('NU_leavers.csv', index = False)
        enter_2.to_csv('NU_leavers_Types_Frequency.csv', index = False)      
    
    else:
        total_percent = 0.0
        general_data = []
        general_column = ["Name", "Overall Usage"]

        for pokemon in data[tier]:
            general_data.append([pokemon, data[tier][pokemon]["Usage"]])  #na_rep = "No value!"

            total_percent += remove_percent_to_int(data[tier][pokemon]["Usage"])

            if len(data[tier][pokemon]["Teammates"]) != 0:
                total_percent_team = 0.0

                if path.exists(f"{tier} Teammates Analyses") == False:
                    os.mkdir(f"{tier} Teammates Analyses")
                os.chdir(f"{tier} Teammates Analyses")

                team_file = f"{pokemon} Teammates Frequency.csv"
                team_data = []
                team_header = ["Teammate", "Overall Usage"]

                for teammate in data[tier][pokemon]["Teammates"]:
                    team_data.append([teammate, data[tier][pokemon]["Teammates"][teammate]])

                    total_percent_team += remove_percent_to_int(data[tier][pokemon]["Teammates"][teammate])

                # team_data.append(["Others", to_percent(total_percent_team)])

                team_data_frame = pd.DataFrame(team_data, columns=team_header)
                team_data_frame.to_csv(team_file, index = False)

                os.chdir("..")

        # general_data.append(["Others", to_percent(total_percent)])

        general_data_frame = pd.DataFrame(general_data, columns=general_column)
        general_data_frame.to_csv(f"{tier} Frequency Usage.csv", index = False)

    os.chdir("..")



