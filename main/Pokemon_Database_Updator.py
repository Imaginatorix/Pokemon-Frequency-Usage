import json, os, requests
from bs4 import BeautifulSoup
import time    

def replace_key_3args(dict, key, new_key, a, b, c):
    prev_a = dict[key][a]
    prev_b = dict[key][b]
    prev_c = dict[key][c]
    del dict[key]
    dict[new_key] = {}
    dict[new_key][a] = prev_a
    dict[new_key][b] = prev_b
    dict[new_key][c] = prev_c

def add_entry(dict, key, a, b, c):
    data[name] = {}
    data[name]["Dex Entry"] = a
    data[name]["Type"] = b
    data[name]["Generation"] = c

data_website = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
web_data = data_website.content

soup = BeautifulSoup(web_data, "lxml")

data = {}
repeat = {}

titles = soup.find_all("h3")

for title in titles:
    if "Generation" in title.text:
        generation = title.text
        main_table = title.find_next_sibling("table")
        
        first_time = True
        for all_td in main_table:
            try:
                tester = all_td.text
                has_text = True
            except AttributeError:
                has_text = False

            if has_text and not first_time:
                first_td = True
                td_num = 1
                for sub_td in all_td.find_all("td"):
                    if first_td:
                        first_td = False
                    else:
                        text = sub_td.text[1:len(sub_td.text)]
                        if td_num == 1:
                            entry_num = text.strip()
                            td_num += 1
                        elif td_num == 2:
                            name = text.strip()
                            td_num += 1
                        else:
                            if text[len(text) - 1] != "\n":
                                double_type = True
                                first_type = text
                            else:
                                if td_num == 4:
                                    second_type = text
                                    poke_type = f"{first_type[0:len(first_type) - 1]}/{second_type.strip()}"
                                    coming_up = True
                                else:
                                    double_type = False
                                    poke_type = text.strip()
                                    coming_up = True
                            if double_type:
                                td_num += 1
                if coming_up:
                    # print (f"Name: {name}\tEntry: {entry_num}\tType: {poke_type}\tGeneration: {generation}")
                    coming_up = False
                    if name in repeat:
                        orig_name = name
                        name = f"{name} [{repeat[name]}]"
                        repeat[orig_name] += 1 
                    if name in data:
                        # gen_before_7 = ["Generation I", "Generation II", "Generation III", "Generation IV", "Generation V", "Generation VI"]
                        # if data[name]["Generation"] in gen_before_7:
                        #     generation_tbs = generation
                        #     name = "Alolan " + name
                        #     add_entry(data, name, entry_num, poke_type, generation_tbs)
                        # else:
                        orig_name = name
                        new_name = f"{name} [1]"
                        replace_key_3args(data, name, new_name, "Dex Entry", "Type", "Generation")
                        name = f"{name} [2]"
                        add_entry(data, name, entry_num, poke_type, generation)
                        repeat[orig_name] = 3
                    else:
                        add_entry(data, name, entry_num, poke_type, generation)

            elif has_text and first_time:
                first_time = False

# for pokemon in data:
#     print (pokemon)

os.chdir("main")
os.chdir("Gathered Data")

with open('Pokemon_Database.json', 'w') as database:
    json.dump(data, database)

