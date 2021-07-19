import json, os
from os import path

def add_entry(entry):
    file_name = "Pokemon_List.txt"
    if path.exists(file_name):
        f = open(file_name, "a")
    else:
        f = open(file_name, "w")
    f.write(f"{entry}\n")
    f.close()

os.chdir("main")
os.chdir("Gathered Data")

with open("Pokemon_Database.json", "r") as f:
    data = json.load(f)

for entry in data:
    if "\u2640" in entry:
        # entry = f"{entry[0:len(entry) - 1]} [F]"
        entry = entry[0:len(entry) - 1]
    elif "\u2642" in entry:
        # entry = f"{entry[0:len(entry) - 1]} [M]"
        entry = entry[0:len(entry) - 1]

    if "[" in entry and "]" in entry:
        entry = entry[0:len(entry) - 4]
    add_entry(entry)



