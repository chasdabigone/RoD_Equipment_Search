import re
from tkinter import *
import webbrowser



#create dictionary from database file
result = []
with open("Equip_DB.txt", "r", encoding='utf-8') as infile:
    for line in infile:
        if line.startswith("Object"):             #Check if line starts with 'Object'
            result.append([line, []])        #Create new list with format --> [key, [list of corresponding text]]
        else:
            result[-1][1].append(line)       #Append text to previously found key. 

eqDict ={k: "".join(v) for k, v in result}   #Form required dictionary.

#define class list
classList = ["none","Augurer","Barbarian","Bladesinger","Cleric","Druid","Fathomer","Mage","Nephandi","Paladin","Ranger","Thief","Vampire","Warrior"]
#define wearlocs list
wearList = ["none","wield","light","finger","neck","head","legs","feet","hands","arms","eyes","ears","body","about","shield","hold","wrist","waist","face","ankle","back"]
#define align list
alignList = ["none","evil","neut","good"]
#define stat list
statList = ["str","int","wis","dex","cha","con","lck"]
#define search variables
genreSearch = None
classSearch = None
raceSearch = None
alignSearch = None
levelSearch = None
hpSearch = None
drSearch = None
hrSearch = None
manaSearch = None
strSearch = None
dexSearch = None
wisSearch = None
intSearch = None
conSearch = None
chaSearch = None
lckSearch = None
wearSearch = "none"
wearEntry = None
acSearch = None
searchResult = []
searchDict = eqDict.copy()



#GUI setup
root = Tk()
root.title('Realms of Despair Equipment Search by Moe')
root.geometry("500x700")


#dropdown class select

def searcheq():

    #erase variables
    genreSearch = None
    classSearch = None
    raceSearch = None
    alignSearch = None
    levelSearch = None
    hpSearch = None
    drSearch = None
    hrSearch = None
    manaSearch = None
    strSearch = None
    dexSearch = None
    wisSearch = None
    intSearch = None
    conSearch = None
    chaSearch = None
    lckSearch = None
    wearSearch = "none"
    statSearch = None
    acSearch = None
    keywordSearch = None
    searchResult = []
    searchDict = eqDict.copy()

    #set selected variables from GUI
    if hpEntry.get() != "":
        if hpEntry.get() != "0":
            hpSearch = int(hpEntry.get())
    if wearclick is not None:
        if wearclick.get() != "none":
            wearSearch = wearclick.get()
    if keywordEntry is not None:
        if keywordEntry.get() != "":
            keywordSearch = keywordEntry.get().lower()
    if alignclick is not None:
        if alignclick.get() != "none":
            alignSearch = alignclick.get()
    if levelEntry.get() != "":
        if levelEntry.get() < "50":
            levelSearch = int(levelEntry.get())
    if acEntry.get() != "":
        if acEntry.get() != "0":
            acSearch = int(acEntry.get())
    if statEntry.get() != "":
        if statEntry.get() != "0":
            statSearch = int(statEntry.get())
            statType = statclick.get()
    if manaEntry.get() != "":
        if manaEntry.get() != "0":
            manaSearch = int(manaEntry.get())
    if drEntry.get() != "":
        if drEntry.get() != "0":
            drSearch = int(drEntry.get())
    
    #class selection variables defined
    if classclick.get() != "none":
        if classclick.get() == "Augurer":
            classSearch = "Augurer"
            genreSearch = "sorcerer"
        if classclick.get() == "Barbarian":
            classSearch = "Barbarian"
            genreSearch = "fighter"
        if classclick.get() == "Bladesinger":
            classSearch = "Bladesinger"
            genreSearch = "rogue"
        if classclick.get() == "Cleric":
            classSearch = "Cleric"
            genreSearch = "divinity"
        if classclick.get() == "Druid":
            classSearch = "Druid"
            genreSearch = "shaman"
        if classclick.get() == "Fathomer":
            classSearch = "Fathomer"
            genreSearch = "rogue"
        if classclick.get() == "Mage":
            classSearch = "Mage"
            genreSearch = "sorcerer"
        if classclick.get() == "Nephandi":
            classSearch = "Nephandi"
            genreSearch = "sorcerer"
        if classclick.get() == "Paladin":
            classSearch = "Paladin"
            genreSearch = "fighter"
        if classclick.get() == "Ranger":
            classSearch = "Ranger"
            genreSearch = "fighter"
        if classclick.get() == "Thief":
            classSearch = "Thief"
            genreSearch = "rogue"
        if classclick.get() == "Vampire":
            classSearch = "Vampire"
            genreSearch = "aberrant"
        if classclick.get() == "Warrior":
            classSearch = "Warrior"
            genreSearch = "fighter"
    

    
    #search and prune for genre+class
    if genreSearch is not None and classSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search('Genres allowed\: (.*)', value)
            f = re.search('Classes allowed\: (.*)', value)
            g = re.search(r'Special properties\: (.*)', value)
            if e is not None:
                e = re.search('Genres allowed\: (.*)', value).group(1)
            if f is not None:
                f = re.search('Classes allowed\: (.*)', value).group(1)
            if classSearch == "Barbarian":
                if g is not None:
                    g = re.search(r'Special properties\: (.*)', value).group(1)
                    if "magic" in g or e is not None or f is not None:
                        if e is None:
                            e = "nil"
                        if f is None:
                            f = "nil"
                        del searchDict[key]
            else:
                if e is not None or f is not None:
                    if e is None:
                        e = "nil"
                    if f is None:
                        f = "nil"
                    if e != "nil" and f != "nil":
                        if genreSearch not in e and classSearch not in f:
                            del searchDict[key]
                

    #search for align and prune
    if alignSearch is not None:
        if alignSearch != "none":
            for key, value in list(searchDict.items()):
                e = re.search('Alignments allowed\: (.*)', value)
                if e is not None:
                    e = re.search('Alignments allowed\: (.*)', value).group(1)
                    if alignSearch not in e:
                        del searchDict[key]

    #search for keyword and prune
    if keywordSearch is not None:
        if keywordSearch != "":
            for key, value in list(searchDict.items()):
                if keywordSearch not in key.lower() and keywordSearch not in value.lower():
                    del searchDict[key]

    #search and prune for max level
    if levelSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'It is a level (\d+)', value)
            if e is not None:
                e = re.search(r'It is a level (\d+)', value).group(1)
                if levelSearch <= int(e):
                    del searchDict[key]

    #search and prune for pkill items
    if pkillCheck.get() == 0:
        for key, value in list(searchDict.items()):
            e = re.search(r'Special properties\: (.*)', value)
            if e is not None:
                e = re.search(r'Special properties\: (.*)', value).group(1)
                if "pkill" in e:
                    del searchDict[key]
                    
    #search for wearloc and prune
    if wearSearch is not None:
        if wearSearch != "":
            if wearSearch != "none":
                if wearSearch != "light":
                    for key, value in list(searchDict.items()):
                        e = re.search(r'Locations it can be worn\: (.*)', value)
                        if e is not None:
                            e = re.search(r'Locations it can be worn\: (.*)', value).group(1)
                            if wearSearch not in e:
                                del searchDict[key]
                        if e is None:
                            del searchDict[key]
                if wearSearch == "light":
                        for key, value in list(searchDict.items()):
                            e = re.search(r'It is a level (\d+) (.*)\,', value)
                            if e is not None:
                                e = re.search(r'It is a level (\d+) (.*)\,', value).group(2)
                                if e != "light":
                                    del searchDict[key]
                                
    #search and prune old style wearlocs
    if wearSearch is not None:
        if wearSearch != "":
            for key, value in list(searchDict.items()):
                e = re.search(r'with wear location\: (.*)', key)
                if e is not None:
                    e = re.search(r'with wear location\: (.*)', key).group(1)
                    if wearSearch not in e:
                        del searchDict[key]

    #search for races and prune
    if raceSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search('Races allowed\: (.*)', value)
            if e is not None:
                e = re.search('Races allowed\: (.*)', value).group(1)
                if raceSearch not in e:
                    del searchDict[key]
                                        
    #search for hp and prune
    if hpSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'Affects hp by (\d+)', value)
            if e is None:
                del searchDict[key]
            else:
                e = re.search(r'Affects hp by (\d+)', value).group(1)
                if int(e) < hpSearch:
                    del searchDict[key]

    #search for mana and prune
    if manaSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'Affects mana by (\d+)', value)
            if e is None:
                del searchDict[key]
            else:
                e = re.search(r'Affects mana by (\d+)', value).group(1)
                if int(e) < manaSearch:
                    del searchDict[key]

    #search for AC and prune
    if acSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'Armor class is (\d+) of (\d+)', value)
            if e is None:
                del searchDict[key]
            else:
                e = re.search(r'Armor class is (\d+) of (\d+)', value).group(2)
                if int(e) < acSearch:
                    del searchDict[key]
                
    #search for DR and prune
    if drSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'Affects damage roll by (\d+)', value)
            if e is None:
                del searchDict[key]
            else:
                e = re.search(r'Affects damage roll by (\d+)', value).group(1)
                if int(e) < drSearch:
                    del searchDict[key]

    #search for HR and prune
    if hrSearch is not None:
        for key, value in list(searchDict.items()):
            e = re.search(r'Affects hit roll by (\d+)', value)
            if e is None:
                del searchDict[key]
            else:
                e = re.search(r'Affects hit roll by (\d+)', value).group(1)
                if int(e) < hrSearch:
                    del searchDict[key]
    
    #search for STR and prune
    if statSearch is not None:
        if statType == "str":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects strength by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects strength by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #search for DEX and prune
    if statSearch is not None:
        if statType == "dex":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects dexterity by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects dexterity by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #search for WIS and prune
    if statSearch is not None:
        if statType == "wis":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects wisdom by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects wisdom by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]
    
    #search for INT and prune
    if statSearch is not None:
        if statType == "int":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects intelligence by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects intelligence by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #search for CON and prune
    if statSearch is not None:
        if statType == "con":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects constitution by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects constitution by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #search for CHA and prune
    if statSearch is not None:
        if statType == "cha":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects charisma by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects charisma by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #search for LCK and prune
    if statSearch is not None:
        if statType == "lck":
            for key, value in list(searchDict.items()):
                e = re.search(r'Affects luck by (\d+)', value)
                if e is None:
                    del searchDict[key]
                else:
                    e = re.search(r'Affects luck by (\d+)', value).group(1)
                    if int(e) < statSearch:
                        del searchDict[key]

    #parse searchDict to display results
       
    searchList = searchDict.keys()
    for value in searchList:
        e = re.search(r"Object \'(.*)\' is", value)
        if e is not None:
            e = re.search(r"Object \'(.*)\' is", value).group(1)            
            searchResult.append(e)

    #clean up parsed search and turn into list for tkinter
    searchResult = str(searchResult)
    searchResult = searchResult.strip(']')
    searchResult = searchResult.strip('[')
    searchResult = searchResult.replace('"',"'")
    searchResult = searchResult[1:-1]
    searchResult = searchResult.split("', '")

    #populate listbox window
    searchList1 = StringVar()
    searchList1.set(searchResult)
    resultWindow = Listbox(root, width=60, height=15, listvariable=searchList1)
    resultWindow.grid(row=12, column=1, columnspan=4)

    #make items clickable
    resultWindow.bind("<<ListboxSelect>>", listclick)
    resultWindow.bind('<3>', lambda e: context_menu(e, menu))

#set up empty results display   
identifyWindow = Text(root, width=60, height=15)
identifyWindow.grid(row=13, column=1, columnspan=4)
resultWindow = Listbox(root, width=60, height=15)
resultWindow.grid(row=12, column=1, columnspan=4)

#define listclick function for resultWindow to print identify when clicked
def listclick(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        global itemName
        itemName = event.widget.get(index)
        itemDisp = [val for key, val in eqDict.items() if "\'" + itemName in key.replace('"',"'")]
        identifyWindow.delete('1.0', END)
        identifyWindow.insert(END, (', '.join(itemDisp)))

#class selection button    
classText = StringVar()
classText.set("Class")
classDir = Label(root, textvariable=classText, height = 1)
classDir.grid(row=1, column=1, sticky=E)
classclick = StringVar()
classclick.set("")
classSelect = OptionMenu(root, classclick, *classList)
classSelect.grid(row=1, column=2, sticky=W)

#wearloc selection button
wearText = StringVar()
wearText.set("Wear Loc")
wearDir = Label(root, textvariable=wearText, height = 1)
wearDir.grid(row=2, column=1, sticky=E)
wearclick = StringVar()
wearclick.set("")
wearSelect = OptionMenu(root, wearclick, *wearList)
wearSelect.grid(row=2, column=2, sticky=W)

#align selection button
alignText = StringVar()
alignText.set("Align")
alignDir = Label(root, textvariable=alignText, height = 1)
alignDir.grid(row=3, column=1, sticky=E)
alignclick = StringVar()
alignclick.set("")
alignSelect = OptionMenu(root, alignclick, *alignList)
alignSelect.grid(row=3, column=2, sticky=W)

#wildcard keyword search
keywordText = StringVar()
keywordText.set("Keyword")
keywordDir = Label(root, textvariable=keywordText, height=1)
keywordDir.grid(row=4, column=1, sticky=E)
keywordEntry = Entry(root, width=15)
keywordEntry.grid(row=4, column=2, sticky=W)

#pkill item checkbox
pkillText = StringVar()
pkillText.set("Include Pkill?")
pkillDir = Label(root, textvariable=pkillText, height=1)
pkillDir.grid(row=5, column=1, sticky=E)
pkillCheck = IntVar()
pkBox = Checkbutton(root, text='', variable=pkillCheck, onvalue=1, offvalue=0)
pkBox.grid(row=5, column=2, sticky=W)
    
#level entry box
levelText = StringVar()
levelText.set("Max Level")
levelDir = Label(root, textvariable=levelText, height = 1)
levelDir.grid(row=1, column=3, sticky=E)
levelEntry = Entry(root, width=3)
levelEntry.grid(row=1, column=4, sticky=W)

#AC entry box
acText = StringVar()
acText.set("Armor AC")
acDir = Label(root, textvariable=acText, height = 1)
acDir.grid(row=2, column=3, sticky=E)
acEntry = Entry(root, width=3)
acEntry.grid(row=2, column=4, sticky=W)

#hp entry box
hpText = StringVar()
hpText.set("Hitpoints")
hpDir = Label(root, textvariable=hpText, height = 1)
hpDir.grid(row=3, column=3, sticky=E)
hpEntry = Entry(root, width=3)
hpEntry.grid(row=3, column=4, sticky=W)

#mana entry box
manaText = StringVar()
manaText.set("Mana")
manaDir = Label(root, textvariable=manaText, height = 1)
manaDir.grid(row=4,column=3, sticky=E)
manaEntry= Entry(root, width=3)
manaEntry.grid(row=4,column=4, sticky=W)

#stat selection button #1
statclick = StringVar()
statclick.set("str")
statSelect = OptionMenu(root, statclick, *statList)
statSelect.grid(row=6, column=3, sticky=E)
statEntry = Entry(root, width=3)
statEntry.grid(row=6, column=4, sticky=W)

#DR entry box
drText = StringVar()
drText.set("DamRoll")
drDir = Label(root, textvariable=drText, height = 1)
drDir.grid(row=5,column=3, sticky=E)
drEntry= Entry(root, width=3)
drEntry.grid(row=5,column=4, sticky=W)

#display number of items in DB
itemNum = StringVar()
itemNum.set("Searching " + str(len(eqDict)) + " items")
itemDir = Label(root, textvariable=itemNum, height = 1)
itemDir.grid(row=11,column=1, sticky=E)

#search button
searchButton = Button(root, text="Search", command=searcheq).grid(row=11, column=4, sticky=E)

#right click on results to go to web page
#aqua = root.tk.call('tk', 'windowingsystem') == 'aqua'
def wiki_open():
    global wikiLink
    first, rest = itemName.split(None, 1)
    if first in {'A', 'An', 'The'}:
        wikiLink = rest + ', ' + first
        wikiLink = wikiLink.replace(" ","_")
    else: wikiLink = itemName
    webbrowser.open_new_tab('http://rodpedia.realmsofdespair.info/wiki/' + wikiLink)

menu = Menu(tearoff=0)
menu.add_command(label=u'View on Wiki', command=wiki_open)

def context_menu(event, menu):
    menuwidget = event.widget
    menuindex = menuwidget.nearest(event.y)
    _, yoffset, _, height = menuwidget.bbox(menuindex)
    if event.y > height + yoffset + 5: # XXX 5 is a niceness factor :)
        # Outside of widget.
        return
    menuitem = menuwidget.get(menuindex)
    menu.post(event.x_root, event.y_root)





root.mainloop()

