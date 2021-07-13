from bs4 import BeautifulSoup
import requests
import os, json

# NU Leavers
# Ubers + Teammates, OU, UU
# If % in title
# If teammates

main_website = requests.get("https://www.smogon.com/smog/archive")

column_informations_desk = {}
tiers_look = ["NU", "OU", "UU", "Uber"]

tier_dict = {}

output = {}
poke_list = []

os.chdir("main")
os.chdir("Gathered Data")

f = open("Pokemon_List.txt", "r")
all_poke = f.readlines()
f.close()

for poke in all_poke:
    poke_list.append(poke.strip())

for tier in range(len(tiers_look)):
    tier_dict[tiers_look[tier]] = []

def isnum(string_num):
    try:
        int(string_num)
        return True
    except ValueError:
        return False

def remove_puncs(word):
    puncs = [",", ".", "!", "'", ":", ";", '/', "&", "|", "\\", "(", ")", "*"]
    if word[len(word) - 1] in puncs:
        word = word[0:len(word) - 1]
    return word

def try_remove_extra(word):
    word2 = ""
    prev_useful = False
    for index in range(len(word) - 1, -1, -1):
        puncs_used = ["-", ".", "—", "%", "–"]
        if isnum(word[index]) or word[index] in puncs_used:
            if prev_useful:
                word2 += " "
            else:
                word2 += ""
            prev_useful = False
        else:
            word2 += word[index]
            prev_useful = True
    return word2[::-1]

def try_remove_extra_2(word):
    if word[0].isalpha() == False:
        for i in range(len(word) - 1):
            if word[i].isalpha():
                word = word[i:len(word)]
                break

    word2 = ""
    prev_useful = False
    for index in range(len(word) - 1, -1, -1):
        puncs_used = ["(", ")", ","]
        if word[index] in puncs_used:
            word2 += ""
        else:
            word2 += word[index]
    word2 = word2[::-1]
    for i in range(len(word) - 1):
        if word2[i] == " ":
            word2[i] == word2[i + 1: len(word2)]
        else:
            break
    return word2

def extract_2nd_part(first_part, full_text):
    second_part = ""
    tryu = full_text[len(first_part) - 1: len(full_text)]

    if len(tryu) == 1:
        if isnum(tryu[0]):
            second_part = tryu[0:len(tryu)]
    else:
        for ia in range(len(tryu) - 1):
            if isnum(tryu[ia]):
                second_part = tryu[ia:len(tryu)]
                break

    return second_part

def separate_percentage_name(text):
    name = ""
    usage = ""
    if len(text.split()) == 1:
        possible = try_remove_extra(text).split()
        if len(possible) == 1:
            if possible[0] in poke_list:
                name = possible[0]
                usage = extract_2nd_part(name, text)
        else:
            for i in range(len(possible) - 1):
                if possible[i] in poke_list:
                    name = possible[i]
                    usage = extract_2nd_part(name, text)
    else:
        for word in text.split():
            if word in poke_list:
                name = word
                usage = extract_2nd_part(name, text)
    
    return (name, usage)

def remove_after_percent(word):
    word = word[::-1]
    for i in range(len(word) - 1):
        if word[i] == "%":
            word = word[i:len(word)]
            break

    return word[::-1]

src = main_website.content

soup = BeautifulSoup(src, "lxml")

article_row = soup.find_all("tr")

for article in article_row:
    column_info = article.find_all("td")
    article_a_tagged = article.find_all("a")
    
    if len(article_a_tagged) == 0:
        continue
    else:
        article_name = article_a_tagged[0].text

    td_place = 0
    for info in column_info:
        column_informations_desk[td_place] = info
        td_place += 1

    if ("Metagame" in article_name and "Analysis" in article_name) and column_informations_desk[4].text == "Metagame":
        for tier in range(len(tiers_look)):
            if tiers_look[tier] in article_name:
                tier_dict[tiers_look[tier]].append(article_a_tagged[0].attrs["href"])

for tier in tier_dict:
    output[tier] = {}
    for article in tier_dict[tier]:
        print (article)
        article_website = requests.get(f"https://www.smogon.com{article}")
        article_contents = article_website.content

        article_soup = BeautifulSoup(article_contents, "lxml")

        if tier == "NU":
            all_paragraphs = article_soup.find_all("p")
            output[tier] = {}
            output[tier]["NU leavers"] = []
            for paragraph in all_paragraphs:
                if "leave the NU" in paragraph.text:
                    for word in paragraph.text.split():
                        word = remove_puncs(word)
                        if word in poke_list:
                            output[tier]["NU leavers"].append(word)
        else:
            for header_type in range(1, 7, 1):
                all_headers = article_soup.find_all(f"h{header_type}")
                for header in all_headers:
                    name, usage = separate_percentage_name(header.text)
                
                    if len(name) != 0:
                        output[tier][name] = {}
                        output[tier][name]["Usage"] = remove_after_percent(usage)
                        output[tier][name]["Teammates"] = {}

                    if name != "":
                        next_element = header.find_next_sibling()
                        if "Teammate" in next_element.text:
                            possible_team = next_element.find_next_sibling().text.split()
                            if len(possible_team) < 5:
                                print (possible_team)
                                for i in range(len(possible_team) - 1):
                                    pos_team = try_remove_extra_2(possible_team[i])
                                    if pos_team in poke_list:
                                        pos_usage = try_remove_extra_2(possible_team[i + 1])
                                        output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                        elif next_element.name == "img":
                            if next_element.find_next_sibling().name == "dl":
                                for data in next_element.find_next_sibling():
                                    try:
                                        pos_list = try_remove_extra_2(data.text).split()
                                        for word in pos_list:
                                            if word in poke_list:
                                                pos_team = word
                                                pos_usage = extract_2nd_part(pos_team, data.text)
                                                break
                                        output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                                    except AttributeError:
                                        if len(data) != 0:
                                            pos_list = try_remove_extra_2(data).split()
                                            for word in pos_list:
                                                if word in poke_list:
                                                    pos_team = word
                                                    pos_usage = extract_2nd_part(pos_team, data)
                                                    break
                                            output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                            else:
                                if "Teammate" in next_element.find_next_sibling().text:
                                    possible_team = next_element.find_next_sibling().text.split()
                                    for i in range(len(possible_team) - 1):
                                        pos_team = try_remove_extra_2(possible_team[i])
                                        if pos_team in poke_list:
                                            pos_usage = try_remove_extra_2(possible_team[i + 1])
                                            output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                        else:
                            if next_element.find_next_sibling().name == "dl":
                                for data in next_element.find_next_sibling():
                                    try:
                                        pos_list = try_remove_extra_2(data.text).split()
                                        for word in pos_list:
                                            if word in poke_list:
                                                pos_team = word
                                                pos_usage = extract_2nd_part(pos_team, data.text)
                                                break
                                        output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                                    except AttributeError:
                                        if len(data) != 0:
                                            pos_list = try_remove_extra_2(data).split()
                                            for word in pos_list:
                                                if word in poke_list:
                                                    pos_team = word
                                                    pos_usage = extract_2nd_part(pos_team, data)
                                                    break
                                            output[tier][name]["Teammates"][pos_team] = remove_after_percent(pos_usage)
                    
with open('Extracted_Data.json', 'w') as database:
    json.dump(output, database)

