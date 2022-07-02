import re
import tkinter as tk
import collections
from collections import OrderedDict
import json



#create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):             #Check if line starts with 'Object'
            result.append([line, []])        #Create new list with format --> [key, [list of corresponding text]]
        else:
            result[-1][1].append(line)       #Append text to previously found key. 

eqDict ={k: "".join(v) for k, v in result}   #Form required dictionary.

#build wearing equipment list

wearLocs = ["light","finger1","finger2","neck1","neck2","body1","body2","body3","body4","body5","body6","head","legs","feet","hands1","hands2","arms","about1","about2","about3","about4","waist","shield","hold","wrist1","wrist2","wield1","wield2","ears","eyes","back","face","ankle1","ankle2"]
charStats = ["hp","mana","str","int","wis","dex","con","cha","lck"]
finalDict = collections.defaultdict(list)



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
        text  = entry[1].get()
        if text != "":
            if field in wearLocs:

                for key, value in list(wearingDict.items()):
                    if text not in key.lower():
                        del wearingDict[key]

                if len(wearingDict) < 1:
                    print (str(field) + " error: no items matched")
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

                
                
    armorClassList = [] # to tally equip armor class
    affectList = [] # affects by number
    affectList2 = [] # affects with class restrict
    otherAffs = [] # word affects
    resistList = [] # list of resists
    statAffs = ['hp','mana','strength','intelligence','wisdom','dexterity','constitution','charisma','luck'] #affects from stats and base
    
    for key, value in list(finalDict.items()):
        
        armorClassList = armorClassList + re.findall(r'Armor class is (-?[0-9]+) of (-?[0-9]+)', value)
        affectList = affectList + re.findall(r'Affects (.*) by (-?[0-9]+)\.', value)
        affectList2 = affectList2 + re.findall(r'Affects (.*) by (-?[0-9]+) if class is (.*)\.', value)
        otherAffs = otherAffs + re.findall(r'Affects affected_by by (.*)', value)
        resistList = resistList + re.findall(r'Affects resistant:(.*) by (-?[0-9]+)', value)
       
    # create dictionary of resists
    resDic = {}
    # combine like items
    for item in resistList:
        if item[0] in resDic:
            resDic[item[0]] = resDic[item[0]] + int(item[1])
        else:
            resDic[item[0]] = int(item[1])
          
    for item in affectList:
        
        dic[item[0]] = dic.get(item[0], 0) + int(item[1])
    
    for item in armorClassList:

        dic['Equipment AC'] = dic.get('Equipment AC', 0) + int(item[1])
        
    
    # new dictionary for affectList2
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
    
    # print affectList2Dic to identifyWindow   
    for x, y in affectList2Dic.items():
        identifyWindow.insert(tk.END, ''.join(x) + ' ' + str(y))
        identifyWindow.insert(tk.END, '\n')
    
    # print resDic to identifyWindow
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
                
        



if __name__ == '__main__':
    char_window = tk.Tk()
    char_window.title('Character Builder by Moe')
    charname = tk.StringVar(char_window)
    
    identifyWindow = tk.Text(char_window, width=35, height=27)
    identifyWindow.grid(row=8, column=1, columnspan=3, rowspan=27)
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

    char_window.mainloop()
