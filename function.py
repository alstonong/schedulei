import json
import dearpygui.dearpygui as dpg
import winsound

datafile = "alldata.json"

ingredients = [] # List of dictionaries
vegetables = [] # List of dictionaries
noduplicatevegetablenames = []
vegetablerowexistinchecklist = set()

rowtags = []
sortoptions = [
    {"key": "vegetableid", "name": "Vegetable ID"},
    {"key": "name", "name": "Name"}, 
    {"key": "cost", "name": "Cost"}, 
    {"key": "sale", "name": "Sale"}, 
    {"key": "profit", "name": "Profit"}, 
]
usersortchoice = sortoptions[0]
reverse = False

pgrcost = 30.0 
yieldoptions = [
    {"key": "ty", "name": "Tent Yield", "value": 8.0},
    {"key": "tpy", "name": "Tent PGR Yield", "value": 12.0},
    {"key": "py", "name": "Pot Yield", "value": 12.0},
    {"key": "ppy", "name": "Pot PGR Yield", "value": 16.0}
]
useryieldchoice = yieldoptions[0] 

errortext = "Error --- "

# Load and save data


def loadalldata():
    global ingredients, vegetables, noduplicatevegetablenames
    data = {} 

    with open(datafile) as file:
        data = json.load(file)
        ingredients = data.get("ingredients")
        vegetables = data.get("vegetables")
    
    noduplicatevegetablenames = sorted({i["name"] for i in vegetables})


def savealldata():
    global ingredients, vegetables
    data = {"ingredients": ingredients, "vegetables": vegetables}

    with open(datafile, "w") as file:
        json.dump(data, file, indent=4)


# -----UI-----


def menuwindow():
    with dpg.window(label="Menu", tag="menuwindow", no_close=True, no_collapse=True, width=1400, height=10):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False, width=200):
                dpg.add_button(label="Add New Vegetable", callback=toggleaddnewvegetablewindow)
                dpg.add_button(label="Add Duplicate Vegetable", callback=toggleaddduplicatevegetablewindow)

            with dpg.group(horizontal=False, width=100):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Ingredients", callback=toggleingredientswindow)
                    dpg.add_text("Ingredients count:")
                    dpg.add_text("0", tag="ingredientscount")
                
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Vegetables", callback=togglevegetableswindow)
                    dpg.add_text("Vegetables count:")
                    dpg.add_text("0", tag="vegetablescount")

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Checklist", callback=togglechecklistwindow)
                    dpg.add_text("Checklist completion:")
                    dpg.add_text("0", tag="checklistcompletionpercentage")
                    dpg.add_text("%")

            with dpg.group(horizontal=False):
                dpg.add_text("| Error: ---", tag="errortext")


def toggleaddnewvegetablewindow():
    if not dpg.is_item_shown("addnewvegetablewindow"):
        dpg.configure_item("addnewvegetablewindow", pos=((dpg.get_viewport_width() - 400) // 2, (dpg.get_viewport_height() - 200) // 2))
        dpg.configure_item("addnewvegetablewindow", show=True)


def toggleaddduplicatevegetablewindow():
    if not dpg.is_item_shown("addduplicatevegetablewindow"):
        dpg.configure_item("addduplicatevegetablewindow", pos=((dpg.get_viewport_width() - 400) // 2, (dpg.get_viewport_height() - 200) // 2))
        dpg.configure_item("addduplicatevegetablewindow", show=True)


def toggleingredientswindow():
    if dpg.is_item_shown("ingredientswindow"):
        dpg.hide_item("ingredientswindow")
    else:
        dpg.show_item("ingredientswindow")


def togglevegetableswindow():
    if dpg.is_item_shown("vegetableswindow"):
        dpg.hide_item("vegetableswindow")
    else:
        dpg.show_item("vegetableswindow")


def togglechecklistwindow():
    if dpg.is_item_shown("checklistwindow"):
        dpg.hide_item("checklistwindow")
    else:
        dpg.show_item("checklistwindow")


def triggererror(text=None):
    global errortext
    if text is None: 
        text = "UNKNOWN ERROR"

    errortext += text + " --- "
    dpg.set_value("errortext", errortext)  
    winsound.MessageBeep(winsound.MB_ICONHAND)   


# Add new vegetable window


def addnewvegetablewindow():
    global ingredients, vegetables, noduplicatevegetablenames

    with dpg.window(
        label="Ingredients", 
        tag="addnewvegetablewindow", 
        modal=True, 
        no_close=True, 
        width=400, 
        height=200
    ):
        dpg.add_input_text(label=": Name", tag="newvegetablename")

        dpg.add_combo(
            label=": Ingredient", 
            tag="newvegetableingredient",
            items=[i["name"] for i in ingredients],
            default_value=""
        )

        dpg.add_combo(
            label=": Vegetable", 
            tag="newvegetablevegetable",
            items=noduplicatevegetablenames,
            default_value=""
        )

        dpg.add_input_float(label=": Sale", tag="newvegetablesale", format="%.2f")
        dpg.add_button(label="Submit", callback=submitaddnewvegetable)
        dpg.add_button(label="Cancel", callback=clearaddnewvegetable)

    dpg.configure_item("addnewvegetablewindow", show=False)


def submitaddnewvegetable():    
    name = dpg.get_value("newvegetablename")
    ingredient = dpg.get_value("newvegetableingredient")
    vegetable = dpg.get_value("newvegetablevegetable")

    try: 
        sale = float(dpg.get_value("newvegetablesale"))
    except:
        triggererror("Can't cast sale from string to float")
        return

    if name == "" or ingredient == "" or vegetable == "" or sale == 0.0:
        triggererror("Entry error")
        return

    processaddvegetable(name, ingredient, vegetable, sale)

    clearaddnewvegetable()


def clearaddnewvegetable():
    dpg.set_value("newvegetablename", "")
    dpg.set_value("newvegetableingredient", "")
    dpg.set_value("newvegetablevegetable", "")
    dpg.set_value("newvegetablesale", 0.0)

    dpg.configure_item("addnewvegetablewindow", show=False)


def addduplicatevegetablewindow():
    global ingredients, vegetables, noduplicatevegetablenames

    with dpg.window(
        label="Ingredients", 
        tag="addduplicatevegetablewindow", 
        modal=True, 
        no_close=True, 
        width=400, 
        height=200
    ):
        dpg.add_combo(
            label=": Name", 
            tag="duplicatevegetablename",
            callback=onduplicatevegetablenamechange,
            items=noduplicatevegetablenames,
            default_value=""
        )

        dpg.add_combo(
            label=": Ingredient", 
            tag="duplicatevegetableingredient",
            items=[i["name"] for i in ingredients],
            default_value=""
        )

        with dpg.group(horizontal=True, width=400):
            dpg.add_text("---", tag="duplicatevegetablevegetable")
            dpg.add_text(": Vegetable")

        with dpg.group(horizontal=True, width=400):
            dpg.add_text("---", tag="duplicatevegetablesale")
            dpg.add_text(": Sale")

        dpg.add_button(label="Submit", callback=submitaddduplicatevegetable)
        dpg.add_button(label="Cancel", callback=clearaddduplicatevegetable)

    dpg.configure_item("addduplicatevegetablewindow", show=False)


def onduplicatevegetablenamechange(sender, app_data):
    global vegetables
    dpg.set_value("duplicatevegetablevegetable", app_data)

    for i in vegetables: 
        if app_data == i["name"]:
            dpg.set_value("duplicatevegetablesale", i["sale"])
            break


def submitaddduplicatevegetable():
    name = dpg.get_value("duplicatevegetablename")
    ingredient = dpg.get_value("duplicatevegetableingredient")
    vegetable = dpg.get_value("duplicatevegetablevegetable")
    
    try: 
        sale = float(dpg.get_value("duplicatevegetablesale"))
    except:
        triggererror("Can't cast sale from string to float")
        return

    if name == "" or ingredient == "":
        triggererror("Empty name / ingredient")
        return
    
    if sale == 0.0:
        triggererror("Existing sale as 0.0")
        return

    processaddvegetable(name, ingredient, vegetable, sale)

    dpg.configure_item("duplicatevegetablename", items=[i["name"] for i in vegetables])

    clearaddduplicatevegetable()


def clearaddduplicatevegetable():
    dpg.set_value("duplicatevegetablename", "")
    dpg.set_value("duplicatevegetableingredient", "")
    dpg.set_value("duplicatevegetablevegetable", "")
    dpg.set_value("duplicatevegetablesale", 0.0)

    dpg.configure_item("addduplicatevegetablewindow", show=False)


def processaddvegetable(name, ingredient, vegetable, sale):
    global ingredients, vegetables, yieldoptions
    dependencies = []

    dependencies.append(next((i["ingredientid"] for i in ingredients if i["name"] == ingredient), -1))
    dependencies.append(-2 if name == vegetable else next((i["vegetableid"] for i in vegetables if i["name"] == vegetable), -1))
    
    for i in vegetables:
        if i["name"] == name and i["dependencies"] == dependencies:
            triggererror("Doppleganger vegetable")
            return 
        
    unavailablevegetableids = {i["vegetableid"] for i in vegetables}
    currentvegetableid = 10
    while currentvegetableid in unavailablevegetableids: 
        currentvegetableid += 1


    # Profit calc
    costandprofit = [
        {"name": "costty", "value": None},
        {"name": "costtpy", "value": None},
        {"name": "costpy", "value": None},
        {"name": "costppy", "value": None},
        {"name": "profitty", "value": None},
        {"name": "profittpy", "value": None},
        {"name": "profitpy", "value": None},
        {"name": "profitppy", "value": None}
    ]

    if dependencies[0] == -1 or dependencies[1] == -1:
        triggererror("Non existing dependency")
        return

    # Costs
    for i in ingredients: 
        if i["ingredientid"] == dependencies[0]:
            for j in costandprofit:
                # Sets initial values for costs
                if j["name"].startswith("cost"):
                    j["value"] = i["cost"]

    def applycostsfromvegetable(vegetable):
        for j in costandprofit:
            if not j["name"].startswith("cost"):
                continue

            field = j["name"]
            value = vegetable.get(field)

            if value is None:
                triggererror(f"{field} is None")
                return False

            if j["value"] is None:
                triggererror(f"{j['name']} is None")
                return False

            j["value"] += value
        return True

    if dependencies[1] == -2:
        lowestcostid = None
        lowestcostvalue = None

        for i in vegetables:
            if i["name"] == name:
                if lowestcostid is None or (i["costty"] is not None and i["costty"] < lowestcostvalue):
                    lowestcostid = i["vegetableid"]
                    lowestcostvalue = i["costty"]

        for i in vegetables:
            if i["vegetableid"] == lowestcostid:
                if not applycostsfromvegetable(i):
                    return
    else:
        for i in vegetables:
            if i["vegetableid"] == dependencies[1]:
                if not applycostsfromvegetable(i):
                    return

    # Profit
    for i in costandprofit:
        if i["name"].startswith("profit"):
            costfield = "cost" + i["name"][6:]
            totalcost = next((j for j in costandprofit if j["name"] == costfield), None)

            if totalcost is None or  totalcost["value"] is None:
                triggererror(f"{costfield} is None")
                return

            i["value"] = sale - totalcost["value"]

    for i in costandprofit:
        if i["value"] is None: 
            triggererror(f"{i['name']} is None")

    newvegetable = {
        "vegetableid": currentvegetableid, 
        "name": name, 
        "dependencies": dependencies, 
        "sale": sale, 
        "costty": costandprofit[0]["value"], 
        "costtpy": costandprofit[1]["value"], 
        "costpy": costandprofit[2]["value"], 
        "costppy": costandprofit[3]["value"], 
        "profitty": costandprofit[4]["value"], 
        "profittpy": costandprofit[5]["value"], 
        "profitpy": costandprofit[6]["value"], 
        "profitppy": costandprofit[7]["value"] 
    }

    vegetables.append(newvegetable)
    
    localcount = 0

    if name not in vegetablerowexistinchecklist:
        with dpg.table_row(parent="checklisttable"):
            dpg.add_text(name)
            for i in ingredients:
                tag = f"{i['name']}{name}cell"
                dpg.add_text("", tag=tag)

                localcount +=1
    
    ocount = int(dpg.get_value("ocount")) + localcount
    dpg.set_value("ocount", ocount )

    tag = f"{ingredient}{vegetable}cell"

    if dpg.does_item_exist(tag):
        if dpg.get_value(tag) == "":
            dpg.set_value(tag, "X")
            xcount = int(dpg.get_value("xcount")) + 1
            dpg.set_value("xcount", xcount)
            pfilledvalue = round(xcount * 100 / ocount, 2)
            dpg.set_value("pfilled", pfilledvalue)
        elif dpg.get_value(tag) == "X":
            dpg.set_value(tag, "2")
        elif dpg.get_value(tag) == "2":
            dpg.set_value(tag, "3")

    onvegetablesuccessfullyadded()
    savealldata()
    

def onvegetablesuccessfullyadded():
    global vegetables, noduplicatevegetablenames

    noduplicatevegetablenames = sorted({i["name"] for i in vegetables})
    dpg.configure_item("newvegetablevegetable", items=noduplicatevegetablenames)
    dpg.configure_item("duplicatevegetablename", items=noduplicatevegetablenames)


# Ingredients window


def ingredientswindow():
    global ingredients
    count = 0

    with dpg.window(label="Ingredients", tag="ingredientswindow", width=180, height=400):
        with dpg.table(header_row=True, tag="ingredientstable"):
            dpg.add_table_column(label="UID", init_width_or_weight=0.2)
            dpg.add_table_column(label="Name", init_width_or_weight=0.6)
            dpg.add_table_column(label="Cost", init_width_or_weight=0.2)
        
    for i in ingredients: 
        with dpg.table_row(parent="ingredientstable"):
            dpg.add_text(i["ingredientid"])
            dpg.add_text(i["name"])
            dpg.add_text(i["cost"])
        
        count += 1
        
    dpg.set_value("ingredientscount", str(count))
    dpg.hide_item("ingredientswindow")
    

# Vegetables window


def vegetableswindow():
    global yieldoptions, sortoptions
    yieldoptionsname = [i["name"] for i in yieldoptions]
    sortoptionsname = [i["name"] for i in sortoptions]

    with dpg.window(label="Vegetables", tag="vegetableswindow", width=500, height=500):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False, width=125):
                dpg.add_combo(
                    label=": Sort", 
                    tag="usersortchoice", 
                    callback=setusersortchoice, 
                    items=sortoptionsname, 
                    default_value=usersortchoice["name"]
                )

                dpg.add_checkbox(label="Ascending", callback=setascendingcheckbox)
                dpg.add_button(label="Populate", callback=populatevegetableswindow, width=100)

            with dpg.group(horizontal=False, width=125):
                dpg.add_combo(
                    label=": Yield", 
                    tag="useryieldchoice", 
                    callback=setuseryieldchoice, 
                    items=yieldoptionsname, 
                    default_value=useryieldchoice["name"]
                )

        with dpg.child_window(width=-1, height=-1, autosize_x=False, autosize_y=False, horizontal_scrollbar=True):
            with dpg.table(header_row=True, tag="vegetablestable"):
                dpg.add_table_column(label="UID", init_width_or_weight=0.05)
                dpg.add_table_column(label="Name", init_width_or_weight=0.3)
                dpg.add_table_column(label="Dependencies", init_width_or_weight=0.5)
                dpg.add_table_column(label="Cost", init_width_or_weight=0.05)
                dpg.add_table_column(label="Sale", init_width_or_weight=0.05)
                dpg.add_table_column(label="Profit", init_width_or_weight=0.05)

    populatevegetableswindow()
    dpg.hide_item("vegetableswindow")


def setusersortchoice(sender, app_data):
    global usersortchoice, sortoptions
    for i in sortoptions:
        if i["name"] == app_data:
            usersortchoice = i
            break


def setascendingcheckbox(sender, app_data):
    global reverse
    if app_data: 
        dpg.set_item_label(sender, "Descending")
        reverse = True
    else:
        dpg.set_item_label(sender, "Ascending")
        reverse = False


def setuseryieldchoice(sender, app_data):
    global useryieldchoice, yieldoptions
    for i in yieldoptions:
        if i["name"] == app_data:
            useryieldchoice = i
            break


def populatevegetableswindow():
    global vegetables, usersortchoice, useryieldchoice, reverse
    count = 0

    localvegetables = vegetables
    localusersortchoice = (
        usersortchoice["key"] + useryieldchoice["key"]
        if usersortchoice["key"] in ("cost", "profit")
        else usersortchoice["key"]
    )

    for i, j in enumerate(localvegetables):
        if localusersortchoice not in j:
            print(f"[WARNING] Missing key '{localusersortchoice}' in item at index {i}: {j}")

    localvegetables.sort(key=lambda x: x.get(localusersortchoice, 0), reverse=reverse)

    for i in rowtags:
        if dpg.does_item_exist(i):
            dpg.delete_item(i)

    rowtags.clear()

    for i in localvegetables:
        rowtag = f"vegetablesrow{i}"
        rowtags.append(rowtag)
        with dpg.table_row(parent="vegetablestable", tag=rowtag):
            dpg.add_text(i["vegetableid"])
            dpg.add_text(i["name"])

            dpg.add_text(", ".join(
                [j["name"] for j in ingredients if j["ingredientid"] == i["dependencies"][0]] +
                (
                    [i["name"]] if i["dependencies"][1] == -2 else
                    [j["name"] for j in vegetables if j["vegetableid"] == i["dependencies"][1]]
                    if i["dependencies"][1] not in [-1, -2] else []
                )
            ))

            dpg.add_text(i["cost" + useryieldchoice["key"]])
            dpg.add_text(i["sale"])
            dpg.add_text(i["profit" + useryieldchoice["key"]])

        count +=1
        
    dpg.set_value("vegetablescount", str(count))

# Checklist window

def checklistwindow():
    global ingredients, vegetables
    xcount = 0
    ocount = 0

    with dpg.window(label="Checklist", tag="checklistwindow", width=500, height=600):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Populated count:")
                dpg.add_text("0", tag="xcount")
                dpg.add_text("|")

            with dpg.group(horizontal=True):
                dpg.add_text("Total cell count:")
                dpg.add_text("0", tag="ocount")
                dpg.add_text("|")

            with dpg.group(horizontal=True):
                dpg.add_text("Percentage filled:")
                dpg.add_text("0", tag="pfilled")
                dpg.add_text("%")

        with dpg.child_window(width=-1, height=-1, autosize_x=False, autosize_y=False, horizontal_scrollbar=True):
            with dpg.table(
                header_row=True, 
                tag="checklisttable", 
                resizable=True, 
                borders_innerH=True, 
                borders_innerV=True, 
                policy=dpg.mvTable_SizingStretchProp
            ):
                dpg.add_table_column(label="Vegetable", init_width_or_weight=0.4)

                for i in ingredients:
                    dpg.add_table_column(label=i["name"], init_width_or_weight=0.05)

            for i in vegetables:
                vegetablename = i["name"]
                if vegetablename in vegetablerowexistinchecklist:
                    continue

                with dpg.table_row(parent="checklisttable"):
                    dpg.add_text(vegetablename)
                    for j in ingredients: 
                        tag = f"{j['name']}{vegetablename}cell"
                        dpg.add_text("", tag=tag)

                        ocount += 1
                
                vegetablerowexistinchecklist.add(vegetablename)

            dpg.set_value("ocount", ocount)

    # Populate checklist
    for i in vegetables:
        if i["vegetableid"] < 10: 
            continue

        tag = ""

        for j in ingredients:
            if j["ingredientid"] == i["dependencies"][0]:
                tag += j["name"]
                break
        
        vegetabledependency = i["dependencies"][1]
        if vegetabledependency == -1:
            pass 
        elif vegetabledependency == -2:
            tag += i["name"]
        else:
            for j in vegetables:
                if j["vegetableid"] == vegetabledependency:
                    tag += j["name"]
                    break

        tag += "cell"

        if dpg.does_item_exist(tag):
            if dpg.get_value(tag) == "":
                dpg.set_value(tag, "X")
                xcount += 1
            elif dpg.get_value(tag) == "X":
                dpg.set_value(tag, "2")
            elif dpg.get_value(tag) == "2":
                dpg.set_value(tag, "3")

    dpg.set_value("xcount", xcount)
    pfilledvalue = round(xcount * 100 / ocount, 2)
    dpg.set_value("pfilled", pfilledvalue)
    dpg.set_value("checklistcompletionpercentage", pfilledvalue)

    dpg.hide_item("checklistwindow")