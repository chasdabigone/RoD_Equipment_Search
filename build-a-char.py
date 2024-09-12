import re
import tkinter as tk
from tkinter import ttk
import collections
from collections import OrderedDict
import json

# Create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):
            result.append([line, []])
        else:
            result[-1][1].append(line)

eqDict = {k: "".join(v) for k, v in result}

# define class list
classList = ["none","Augurer","Barbarian","Bladesinger","Cleric","Druid","Fathomer","Mage","Nephandi","Paladin","Ranger","Thief","Vampire","Warrior"]
# define race list
raceList = ["none", "Human", "Dwarf", "Elf", "Halfling", "Pixie", "Half-Elf", "Half-Ogre", "Half-Troll", "Half-Orc", "Gith", "Sea-Elf", "Drow", "Lizardman", "Gnome", "Dragonborn", "Tiefling"]
#define align list
alignList = ["none","evil","neutral","good"]

# Build wearing equipment list
wearLocs = ["light", "finger1", "finger2", "neck1", "neck2", "body1", "body2", "body3", "body4", "body5", "body6", "head", "legs", "feet", "hands1", "hands2", "arms", "about1", "about2", "about3", "about4", "waist", "shield", "hold", "wrist1", "wrist2", "wield1", "wield2", "ears", "eyes", "back", "face", "ankle1", "ankle2"]
charStats = ["hp", "mana", "str", "int", "wis", "dex", "con", "cha", "lck"]
finalDict = collections.defaultdict(list)

classList = ["Augurer", "Barbarian", "Bladesinger", "Cleric", "Druid", "Fathomer", "Mage", "Nephandi", "Paladin", "Ranger", "Thief", "Vampire", "Warrior"]

ignoreList = []

# Load ignore list from file
def load_ignore_list():
    global ignoreList
    try:
        with open("ignoreList.txt", "r", encoding='utf-8') as infile:
            ignoreList = infile.read().strip().split('\n')
            print("Ignore list loaded successfully.")
    except FileNotFoundError:
        print("Ignore list not found. Creating new ignore list.")
        ignoreList = []
load_ignore_list()


# Save ignore list to file
def save_ignore_list_to_file():
    try:
        with open("ignoreList.txt", "w", encoding='utf-8') as outfile:
            outfile.write("\n".join(ignoreList))
            print("Ignore list saved successfully.")
    except Exception as e:
        print(f"Error saving ignore list: {e}")


def open_ignore_list_window():
    def save_ignore_list():
        global ignoreList
        ignoreList = ignore_text.get("1.0", tk.END).strip().split('\n')
        save_ignore_list_to_file()
        ignore_window.destroy()

    ignore_window = tk.Toplevel(char_window)
    ignore_window.title("Ignore List")
    ignore_text = tk.Text(ignore_window, width=40, height=20)
    ignore_text.pack()

    # Populate the ignore_text with existing ignoreList values
    if ignoreList:
        ignore_text.insert(tk.END, "\n".join(ignoreList))

    save_button = tk.Button(ignore_window, text="Save", command=save_ignore_list)
    save_button.pack()

def save_json(entries):
    name = charname.get()
    field1 = list()
    text1 = list()
    for entry in entries:
        field1.append(entry[0])
        text1.append(entry[1].get())
    
    equip = dict(zip(field1, text1))

    with open(name+".char", "w") as f:
        json.dump(equip, f)


def optimize_equipment(stat_to_optimize):
    optimized_equipment = {}
    filled_base_locs = set()
    used_unique_items = set()
    
    selected_class = class_var.get()
    selected_race = race_var.get()
    selected_align = align_var.get()
    
    # Map classes to genres
    class_to_genre = {
        "Augurer": "sorcerer",
        "Barbarian": "fighter",
        "Bladesinger": "rogue",
        "Cleric": "divinity",
        "Druid": "shaman",
        "Fathomer": "rogue",
        "Mage": "sorcerer",
        "Nephandi": "sorcerer",
        "Paladin": "fighter",
        "Ranger": "fighter",
        "Thief": "rogue",
        "Vampire": "aberrant",
        "Warrior": "fighter"
    }
    
    selected_genre = class_to_genre.get(selected_class, "none")
    
    for loc in wearLocs:
        best_item = None
        best_stat_value = -float('inf')
        
        base_loc = ''.join([i for i in loc if not i.isdigit()])
        
        if base_loc in ['body', 'about', 'hands', 'wield'] and base_loc in filled_base_locs:
            continue
        
        items_checked = 0
        items_failed_wear = 0
        items_failed_class = 0
        items_failed_genre = 0
        items_failed_align = 0
        items_failed_race = 0
        items_failed_stat = 0
        
        for key, value in eqDict.items():
            items_checked += 1
            
            if 'unique' in value.lower() and key in used_unique_items:
                continue
            
            if any(ignore_item in key.lower() for ignore_item in ignoreList):
                continue
            
            wear_locations = re.findall(r'Locations it can be worn:\s*(.*)', value)
            if not wear_locations:
                wear_locations = re.findall(r'Locations it can be worn:\s*(.*)', key)
            if not wear_locations and base_loc.lower() == 'light':
                if 'light' in key.lower() or 'light' in value.lower():
                    wear_locations = ['light']
            
            if not wear_locations or not any(base_loc.lower() in wloc.lower() for wloc in wear_locations[0].split()):
                items_failed_wear += 1
                continue
            
            class_allowed = True
            genre_allowed = True
            align_allowed = True
            race_allowed = True
            
            classes = re.findall(r'Classes allowed:\s*(.*)', value)
            if classes and selected_class != "none":
                if selected_class.lower() not in classes[0].lower():
                    items_failed_class += 1
                    continue
            
            genres = re.findall(r'Genres allowed:\s*(.*)', value)
            if genres and selected_genre != "none":
                if selected_genre.lower() not in genres[0].lower():
                    items_failed_genre += 1
                    continue
            
            alignments = re.findall(r'Alignments allowed:\s*(.*)', value)
            if alignments and selected_align != "none":
                if selected_align.lower() not in alignments[0].lower():
                    items_failed_align += 1
                    continue
            
            races = re.findall(r'Races allowed:\s*(.*)', value)
            if races and selected_race != "none":
                if selected_race.lower() not in races[0].lower():
                    items_failed_race += 1
                    continue
            
            # Ignore bonus stats
            value = re.split(r'Bonuses for', value)[0]
            
            stat_value = 0
            stat_matches = re.findall(r'Affects {} by (-?\d+)'.format(stat_to_optimize), value)
            for match in stat_matches:
                stat_value += int(match)
            
            if stat_to_optimize == "damage roll":
                hr_matches = re.findall(r'Affects hit roll by (-?\d+)', value)
                for match in hr_matches:
                    stat_value += int(match)
            elif stat_to_optimize == "hp":
                hp_matches = re.findall(r'Affects hp by (-?\d+)', value)
                for match in hp_matches:
                    stat_value += int(match)
            
            if stat_value == 0:
                items_failed_stat += 1
                continue
            
            if stat_value > best_stat_value:
                best_stat_value = stat_value
                best_item = key
        
        if best_item:
            optimized_equipment[loc] = re.search(r"\'(.*)\'", best_item).group(1)
            filled_base_locs.add(base_loc)
            if 'unique' in eqDict[best_item].lower():
                used_unique_items.add(best_item)
        else:
            print(f"{loc} error: no items matched")
            print(f"  Items checked: {items_checked}")
            print(f"  Items failed wear location: {items_failed_wear}")
            print(f"  Items failed class restriction: {items_failed_class}")
            print(f"  Items failed genre restriction: {items_failed_genre}")
            print(f"  Items failed alignment restriction: {items_failed_align}")
            print(f"  Items failed race restriction: {items_failed_race}")
            print(f"  Items failed {stat_to_optimize} stat: {items_failed_stat}")
    
    return optimized_equipment

def fetch(entries):
    global dic
    dic = OrderedDict()
    dic['hp'] = 0
    dic['mana'] = 0
    dic[' '] = ' '
    dic['damage roll'] = 0
    dic['hit roll'] = 0
    dic['  '] = ' '
    dic['strength'] = 0
    dic['intelligence'] = 0
    dic['wisdom'] = 0
    dic['dexterity'] = 0
    dic['constitution'] = 0
    dic['charisma'] = 0
    dic['luck'] = 0
    dic['   '] = ' '
    
    hp = 0
    mana = 0
    strength = 0
    intelligence = 0
    wisdom = 0
    dexterity = 0
    constitution = 0
    charisma = 0
    luck = 0

    for entry in entries:
        wearingDict = eqDict.copy()
        field = entry[0]
        text = entry[1].get()
        if text != "":
            if field in wearLocs:
                for key, value in list(wearingDict.items()):
                    if text.lower() not in key.lower():
                        del wearingDict[key]

                if len(wearingDict) < 1:
                    print(str(field) + " error: no items matched")
                else:
                    if next(iter(wearingDict)) in finalDict:
                        searchKey = list(wearingDict.keys())[0]
                        searchVal = list(wearingDict.values())[0]
                        finalDict[searchKey] = finalDict[searchKey] + searchVal
                    else:
                        finalDict.update(wearingDict)
            if field in charStats:
                if field == 'hp':
                    hp = text
                if field == 'mana':
                    mana = text
                if field == 'str':
                    strength = text
                if field == 'int':
                    intelligence = text
                if field == 'wis':
                    wisdom = text
                if field == 'dex':
                    dexterity = text
                if field == 'con':
                    constitution = text
                if field == 'cha':
                    charisma = text
                if field == 'lck':
                    luck = text

    armorClassList = []
    affectList = []
    affectList2 = []
    otherAffs = []
    resistList = []
    statAffs = ['hp', 'mana', 'strength', 'intelligence', 'wisdom', 'dexterity', 'constitution', 'charisma', 'luck']
    
    for key, value in list(finalDict.items()):
        armorClassList = armorClassList + re.findall(r'Armor class is (-?[0-9]+) of (-?[0-9]+)', value)
        affectList = affectList + re.findall(r'Affects (.*) by (-?[0-9]+)\.', value)
        affectList2 = affectList2 + re.findall(r'Affects (.*) by (-?[0-9]+) if class is (.*)\.', value)
        otherAffs = otherAffs + re.findall(r'Affects affected_by by (.*)', value)
        resistList = resistList + re.findall(r'Affects resistant:(.*) by (-?[0-9]+)', value)
       
    resDic = {}
    for item in resistList:
        if item[0] in resDic:
            resDic[item[0]] = resDic[item[0]] + int(item[1])
        else:
            resDic[item[0]] = int(item[1])
          
    for item in affectList:
        dic[item[0]] = dic.get(item[0], 0) + int(item[1])
    
    for item in armorClassList:
        dic['Equipment AC'] = dic.get('Equipment AC', 0) + int(item[1])
        
    affectList2Dic = {}
    for item in affectList2:
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], '')) + str(item[1])
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], 0)) + " if " + str(item[2])

    for k in statAffs:
        if k == 'hp':
            dic[k] = dic.get(k, 0) + int(hp)
        if k == 'mana':
            dic[k] = dic.get(k, 0) + int(mana)
        if k == 'strength':
            dic[k] = dic.get(k, 0) + int(strength)
        if k == 'intelligence':
            dic[k] = dic.get(k, 0) + int(intelligence)
        if k == 'wisdom':
            dic[k] = dic.get(k, 0) + int(wisdom)
        if k == 'dexterity':
            dic[k] = dic.get(k, 0) + int(dexterity)
        if k == 'constitution':
            dic[k] = dic.get(k, 0) + int(constitution)
        if k == 'charisma':
            dic[k] = dic.get(k, 0) + int(charisma)
        if k == 'luck':
            dic[k] = dic.get(k, 0) + int(luck)

    identifyWindow.delete('1.0', tk.END)
    
    for x, y in dic.items():
        identifyWindow.insert(tk.END, ''.join(x) + ' ' + str(y))
        identifyWindow.insert(tk.END, '\n')
    
    for x, y in affectList2Dic.items():
        identifyWindow.insert(tk.END, ''.join(x) + ' ' + str(y))
        identifyWindow.insert(tk.END, '\n')
    
    for item in resDic:
        identifyWindow.insert(tk.END, "resist " + ''.join(item) + ' ' + str(resDic[item]) + "%")  
        identifyWindow.insert(tk.END, '\n')

    otherAffs = str(otherAffs).replace(' ', '\n')
    
    for x in otherAffs:
        identifyWindow.insert(tk.END, ''.join(x))

def makeform(char_window, fields, fields2):
    entries = []
    for field in fields:
        row = tk.Frame(char_window)
        lab = tk.Label(row, width=15, text=field, anchor='e')
        ent = tk.Entry(row)
        rows = fields.index(field)
        row.grid(row=rows, column=0, padx=0, pady=0)
        lab.grid(row=rows, column=0)
        ent.grid(row=rows, column=1)
        entries.append((field, ent))
        
    for field in fields2:
        row = tk.Frame(char_window)
        lab = tk.Label(row, width=10, text=field, anchor='e')
        ent = tk.Entry(row, width=3)
        rows2 = fields2.index(field)
        row.grid(row=rows2, column=2, padx=0, pady=0)
        lab.grid(row=rows2, column=2)
        ent.grid(row=rows2, column=3)
        entries.append((field, ent))
    return entries

def load_json():
    name = charname.get()
    o = open(name+".char")
    loaded = json.load(o)

    for key, value in ents:
        value.delete(0, 'end')
        for k, v in loaded.items():
            if v != "":
                if key == k:
                    value.insert(0, v)

    b1.invoke()

def optimize_and_load():
    stat_to_optimize = optimize_var.get()
    optimized_equip = optimize_equipment(stat_to_optimize)
import re
import tkinter as tk
from tkinter import ttk
import collections
from collections import OrderedDict
import json

# Create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):
            result.append([line, []])
        else:
            result[-1][1].append(line)

eqDict = {k: "".join(v) for k, v in result}

# define class list
classList = ["none","Augurer","Barbarian","Bladesinger","Cleric","Druid","Fathomer","Mage","Nephandi","Paladin","Ranger","Thief","Vampire","Warrior"]
# define race list
raceList = ["none", "Human", "Dwarf", "Elf", "Halfling", "Pixie", "Half-Elf", "Half-Ogre", "Half-Troll", "Half-Orc", "Gith", "Sea-Elf", "Drow", "Lizardman", "Gnome", "Dragonborn", "Tiefling"]
#define align list
alignList = ["none","evil","neutral","good"]

# Build wearing equipment list
wearLocs = ["light", "finger1", "finger2", "neck1", "neck2", "body1", "body2", "body3", "body4", "body5", "body6", "head", "legs", "feet", "hands1", "hands2", "arms", "about1", "about2", "about3", "about4", "waist", "shield", "hold", "wrist1", "wrist2", "wield1", "wield2", "ears", "eyes", "back", "face", "ankle1", "ankle2"]
charStats = ["hp", "mana", "str", "int", "wis", "dex", "con", "cha", "lck"]
finalDict = collections.defaultdict(list)

classList = ["Augurer", "Barbarian", "Bladesinger", "Cleric", "Druid", "Fathomer", "Mage", "Nephandi", "Paladin", "Ranger", "Thief", "Vampire", "Warrior"]


def open_ignore_list_window():
    print(ignoreList)
    def save_ignore_list():
        global ignoreList
        ignoreList = ignore_text.get("1.0", tk.END).strip().split('\n')
        

    ignore_window = tk.Toplevel(char_window)
    ignore_window.title("Ignore List")
    ignore_text = tk.Text(ignore_window, width=40, height=20)
    ignore_text.pack()

    # Populate the ignore_text with existing ignoreList values
    if ignoreList:
        ignore_text.insert(tk.END, "\n".join(ignoreList))

    save_button = tk.Button(ignore_window, text="Save", command=save_ignore_list)
    save_button.pack()

def open_ignore_list_window():
    def save_ignore_list():
        global ignoreList
        ignoreList = ignore_text.get("1.0", tk.END).strip().split('\n')
        with open("ignoreList.txt", "w", encoding='utf-8') as outfile:
            outfile.write("\n".join(ignoreList))
            print("Ignore list saved successfully.")
        ignore_window.destroy()

    ignore_window = tk.Toplevel(char_window)
    ignore_window.title("Ignore List")
    ignore_text = tk.Text(ignore_window, width=40, height=20)
    ignore_text.pack()

    # Populate the ignore_text with existing ignoreList values
    if ignoreList:
        ignore_text.insert(tk.END, "\n".join(ignoreList))

    save_button = tk.Button(ignore_window, text="Save", command=save_ignore_list)
    save_button.pack()

def save_json(entries):
    name = charname.get()
    field1 = list()
    text1 = list()
    for entry in entries:
        field1.append(entry[0])
        text1.append(entry[1].get())
    
    equip = dict(zip(field1, text1))

    with open(name+".char", "w") as f:
        json.dump(equip, f)


def optimize_equipment(stat_to_optimize):
    optimized_equipment = {}
    filled_base_locs = set()
    used_unique_items = set()
    
    selected_class = class_var.get()
    selected_race = race_var.get()
    selected_align = align_var.get()
    pk_filter = pk_var.get()  # Get the state of the pk checkbox
    
    # Map classes to genres
    class_to_genre = {
        "Augurer": "sorcerer",
        "Barbarian": "fighter",
        "Bladesinger": "rogue",
        "Cleric": "divinity",
        "Druid": "shaman",
        "Fathomer": "rogue",
        "Mage": "sorcerer",
        "Nephandi": "sorcerer",
        "Paladin": "fighter",
        "Ranger": "fighter",
        "Thief": "rogue",
        "Vampire": "aberrant",
        "Warrior": "fighter"
    }
    
    selected_genre = class_to_genre.get(selected_class, "none")
    
    for loc in wearLocs:
        best_item = None
        best_stat_value = -float('inf')
        
        base_loc = ''.join([i for i in loc if not i.isdigit()])
        
        if base_loc in ['body', 'about', 'hands', 'wield'] and base_loc in filled_base_locs:
            continue
        
        items_checked = 0
        items_failed_wear = 0
        items_failed_class = 0
        items_failed_genre = 0
        items_failed_align = 0
        items_failed_race = 0
        items_failed_stat = 0
        items_failed_pk = 0  # Counter for items failed due to pk filter
        items_failed_two_handed = 0  # Counter for items failed due to two-handed property
        items_failed_magic = 0  # Counter for items failed due to magic property
        
        for key, value in eqDict.items():
            items_checked += 1
            
            if 'unique' in value.lower() and key in used_unique_items:
                continue
            
            if any(ignore_item in key.lower() for ignore_item in ignoreList):
                continue
            
            if not pk_filter and 'pkill' in value.lower():
                items_failed_pk += 1
                continue
            
            if 'two-handed' in value.lower():
                items_failed_two_handed += 1
                continue
            
            if selected_class == "Barbarian" and 'magic' in value.lower():
                items_failed_magic += 1
                continue
            
            wear_locations = re.findall(r'Locations it can be worn:\s*(.*)', value)
            if not wear_locations:
                wear_locations = re.findall(r'Locations it can be worn:\s*(.*)', key)
            if not wear_locations and base_loc.lower() == 'light':
                if 'light' in key.lower() or 'light' in value.lower():
                    wear_locations = ['light']
            
            if not wear_locations or not any(base_loc.lower() in wloc.lower() for wloc in wear_locations[0].split()):
                items_failed_wear += 1
                continue
            
            class_allowed = True
            genre_allowed = True
            align_allowed = True
            race_allowed = True
            
            classes = re.findall(r'Classes allowed:\s*(.*)', value)
            if classes and selected_class != "none":
                if selected_class.lower() not in classes[0].lower():
                    items_failed_class += 1
                    continue
            
            genres = re.findall(r'Genres allowed:\s*(.*)', value)
            if genres and selected_genre != "none":
                if selected_genre.lower() not in genres[0].lower():
                    items_failed_genre += 1
                    continue
            
            alignments = re.findall(r'Alignments allowed:\s*(.*)', value)
            if alignments and selected_align != "none":
                if selected_align.lower() not in alignments[0].lower():
                    items_failed_align += 1
                    continue
            
            races = re.findall(r'Races allowed:\s*(.*)', value)
            if races and selected_race != "none":
                if selected_race.lower() not in races[0].lower():
                    items_failed_race += 1
                    continue
            
            # Ignore bonus stats
            value = re.split(r'Bonuses for', value)[0]
            
            stat_value = 0
            stat_matches = re.findall(r'Affects {} by (-?\d+)'.format(stat_to_optimize), value)
            for match in stat_matches:
                stat_value += int(match)
            
            if stat_to_optimize == "damage roll":
                hr_matches = re.findall(r'Affects hit roll by (-?\d+)', value)
                for match in hr_matches:
                    stat_value += int(match)
            elif stat_to_optimize == "hp":
                hp_matches = re.findall(r'Affects hp by (-?\d+)', value)
                for match in hp_matches:
                    stat_value += int(match)
            
            if stat_value == 0:
                items_failed_stat += 1
                continue
            
            if stat_value > best_stat_value:
                best_stat_value = stat_value
                best_item = key
        
        if best_item:
            optimized_equipment[loc] = re.search(r"\'(.*)\'", best_item).group(1)
            filled_base_locs.add(base_loc)
            if 'unique' in eqDict[best_item].lower():
                used_unique_items.add(best_item)
        else:
            print(f"{loc} error: no items matched")
            print(f"  Items checked: {items_checked}")
            print(f"  Items failed wear location: {items_failed_wear}")
            print(f"  Items failed class restriction: {items_failed_class}")
            print(f"  Items failed genre restriction: {items_failed_genre}")
            print(f"  Items failed alignment restriction: {items_failed_align}")
            print(f"  Items failed race restriction: {items_failed_race}")
            print(f"  Items failed {stat_to_optimize} stat: {items_failed_stat}")
            print(f"  Items failed pk filter: {items_failed_pk}")
            print(f"  Items failed two-handed filter: {items_failed_two_handed}")
            print(f"  Items failed magic property: {items_failed_magic}")
    
    return optimized_equipment

def fetch(entries):
    global dic
    dic = OrderedDict()
    dic['hp'] = 0
    dic['mana'] = 0
    dic[' '] = ' '
    dic['damage roll'] = 0
    dic['hit roll'] = 0
    dic['  '] = ' '
    dic['strength'] = 0
    dic['intelligence'] = 0
    dic['wisdom'] = 0
    dic['dexterity'] = 0
    dic['constitution'] = 0
    dic['charisma'] = 0
    dic['luck'] = 0
    dic['   '] = ' '
    
    hp = 0
    mana = 0
    strength = 0
    intelligence = 0
    wisdom = 0
    dexterity = 0
    constitution = 0
    charisma = 0
    luck = 0

    for entry in entries:
        wearingDict = eqDict.copy()
        field = entry[0]
        text = entry[1].get()
        if text != "":
            if field in wearLocs:
                for key, value in list(wearingDict.items()):
                    if text.lower() not in key.lower():
                        del wearingDict[key]

                if len(wearingDict) < 1:
                    print(str(field) + " error: no items matched")
                else:
                    if next(iter(wearingDict)) in finalDict:
                        searchKey = list(wearingDict.keys())[0]
                        searchVal = list(wearingDict.values())[0]
                        finalDict[searchKey] = finalDict[searchKey] + searchVal
                    else:
                        finalDict.update(wearingDict)
            if field in charStats:
                if field == 'hp':
                    hp = text
                if field == 'mana':
                    mana = text
                if field == 'str':
                    strength = text
                if field == 'int':
                    intelligence = text
                if field == 'wis':
                    wisdom = text
                if field == 'dex':
                    dexterity = text
                if field == 'con':
                    constitution = text
                if field == 'cha':
                    charisma = text
                if field == 'lck':
                    luck = text

    armorClassList = []
    affectList = []
    affectList2 = []
    otherAffs = []
    resistList = []
    statAffs = ['hp', 'mana', 'strength', 'intelligence', 'wisdom', 'dexterity', 'constitution', 'charisma', 'luck']
    
    for key, value in list(finalDict.items()):
        armorClassList = armorClassList + re.findall(r'Armor class is (-?[0-9]+) of (-?[0-9]+)', value)
        affectList = affectList + re.findall(r'Affects (.*) by (-?[0-9]+)\.', value)
        affectList2 = affectList2 + re.findall(r'Affects (.*) by (-?[0-9]+) if class is (.*)\.', value)
        otherAffs = otherAffs + re.findall(r'Affects affected_by by (.*)', value)
        resistList = resistList + re.findall(r'Affects resistant:(.*) by (-?[0-9]+)', value)
       
    resDic = {}
    for item in resistList:
        if item[0] in resDic:
            resDic[item[0]] = resDic[item[0]] + int(item[1])
        else:
            resDic[item[0]] = int(item[1])
          
    for item in affectList:
        dic[item[0]] = dic.get(item[0], 0) + int(item[1])
    
    for item in armorClassList:
        dic['Equipment AC'] = dic.get('Equipment AC', 0) + int(item[1])
        
    affectList2Dic = {}
    for item in affectList2:
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], '')) + str(item[1])
        affectList2Dic[item[0]] = str(affectList2Dic.get(item[0], 0)) + " if " + str(item[2])

    for k in statAffs:
        if k == 'hp':
            dic[k] = dic.get(k, 0) + int(hp)
        if k == 'mana':
            dic[k] = dic.get(k, 0) + int(mana)
        if k == 'strength':
            dic[k] = dic.get(k, 0) + int(strength)
        if k == 'intelligence':
            dic[k] = dic.get(k, 0) + int(intelligence)
        if k == 'wisdom':
            dic[k] = dic.get(k, 0) + int(wisdom)
        if k == 'dexterity':
            dic[k] = dic.get(k, 0) + int(dexterity)
        if k == 'constitution':
            dic[k] = dic.get(k, 0) + int(constitution)
        if k == 'charisma':
            dic[k] = dic.get(k, 0) + int(charisma)
        if k == 'luck':
            dic[k] = dic.get(k, 0) + int(luck)

    identifyWindow.delete('1.0', tk.END)
    
    for x, y in dic.items():
        identifyWindow.insert(tk.END, ''.join(x) + ' ' + str(y))
        identifyWindow.insert(tk.END, '\n')
    
    for x, y in affectList2Dic.items():
        identifyWindow.insert(tk.END, ''.join(x) + ' ' + str(y))
        identifyWindow.insert(tk.END, '\n')
    
    for item in resDic:
        identifyWindow.insert(tk.END, "resist " + ''.join(item) + ' ' + str(resDic[item]) + "%")  
        identifyWindow.insert(tk.END, '\n')

    otherAffs = str(otherAffs).replace(' ', '\n')
    
    for x in otherAffs:
        identifyWindow.insert(tk.END, ''.join(x))

def makeform(char_window, fields, fields2):
    entries = []
    for field in fields:
        row = tk.Frame(char_window)
        lab = tk.Label(row, width=15, text=field, anchor='e')
        ent = tk.Entry(row)
        rows = fields.index(field)
        row.grid(row=rows, column=0, padx=0, pady=0)
        lab.grid(row=rows, column=0)
        ent.grid(row=rows, column=1)
        entries.append((field, ent))
        
    for field in fields2:
        row = tk.Frame(char_window)
        lab = tk.Label(row, width=10, text=field, anchor='e')
        ent = tk.Entry(row, width=3)
        rows2 = fields2.index(field)
        row.grid(row=rows2, column=2, padx=0, pady=0)
        lab.grid(row=rows2, column=2)
        ent.grid(row=rows2, column=3)
        entries.append((field, ent))
    return entries

def load_json():
    name = charname.get()
    o = open(name+".char")
    loaded = json.load(o)

    for key, value in ents:
        value.delete(0, 'end')
        for k, v in loaded.items():
            if v != "":
                if key == k:
                    value.insert(0, v)

    b1.invoke()

def optimize_and_load():
    stat_to_optimize = optimize_var.get()
    optimized_equip = optimize_equipment(stat_to_optimize)
    for key, value in ents:
        value.delete(0, 'end')
        if key in optimized_equip:
            value.insert(0, optimized_equip[key])

    b1.invoke()

if __name__ == '__main__':
    char_window = tk.Tk()
    char_window.title('Character Builder by Moe')
    charname = tk.StringVar(char_window)
    
    identifyWindow = tk.Text(char_window, width=35, height=27)
    identifyWindow.grid(row=7, column=1, columnspan=3, rowspan=27)
    ents = makeform(char_window, wearLocs, charStats)

    char_window.bind('<Return>', (lambda event, e=ents: [finalDict.clear(),fetch(e)]))   
    b1 = tk.Button(char_window, text='Calculate',
                  command=(lambda e=ents: [finalDict.clear(),fetch(e)]))
    b1.grid(row=33, column=1, padx=5, pady=0)

    b3 = tk.Button(char_window, text='Quit', command=char_window.destroy)
    b3.grid(row=33, column=3, padx=5, pady=0)
    name_label = tk.Label(char_window, text = 'Name:')
    name_label.grid(row=32,column=1,padx=5,pady=0)
    name = tk.Entry(char_window, textvariable=charname)
    name.grid(row=32, column=2, padx=5, pady=0)
    b2 = tk.Button(char_window, text='Save',
                   command=(lambda e=ents: [save_json(e)]))
    b2.grid(row=32, column=3, padx=5, pady=0)
    load = tk.Button(char_window, text='Load', command=load_json)
    load.grid(row=33, column=2, padx=5, pady=0)

    # Add horizontal line (separator) on row 34
    separator = ttk.Separator(char_window, orient='horizontal')
    separator.grid(row=34, column=0, columnspan=4, sticky='ew', pady=5)

    # Add Ignore List button on row 34, column 1
    ignore_button = tk.Button(char_window, text='Ignore List', command=open_ignore_list_window)
    ignore_button.grid(row=35, column=1, padx=5, pady=0)

    optimize_var = tk.StringVar(char_window)
    optimize_var.set("hp")  # default value
    optimize_menu = tk.OptionMenu(char_window, optimize_var, "hp", "mana", "damage roll", "hit roll")
    optimize_menu.grid(row=35, column=2, padx=5, pady=0, sticky='e')
    optimize = tk.Button(char_window, text='Optimize', command=optimize_and_load)
    optimize.grid(row=35, column=3, padx=5, pady=0)

    # Move class, race, and alignment selection to the left side
    class_var = tk.StringVar(char_window)
    class_var.set("none")  # default value
    class_menu = tk.OptionMenu(char_window, class_var, *classList)
    class_menu.grid(row=35, column=0, padx=5, pady=0, sticky='w')

    race_var = tk.StringVar(char_window)
    race_var.set("none")  # default value
    race_menu = tk.OptionMenu(char_window, race_var, *raceList)
    race_menu.grid(row=35, column=0, padx=5, pady=0)

    align_var = tk.StringVar(char_window)
    align_var.set("none")  # default value
    align_menu = tk.OptionMenu(char_window, align_var, *alignList)
    align_menu.grid(row=35, column=0, padx=5, pady=0, sticky='e')

    # Add 'pk' checkbox on row 35
    pk_var = tk.BooleanVar()
    pk_checkbox = tk.Checkbutton(char_window, text='pk', variable=pk_var)
    pk_checkbox.grid(row=35, column=2, padx=5, pady=0, sticky='w')

    char_window.mainloop()
