from time import sleep
import json
import os
import random

cmd = 'mode 120, 30'
os.system(cmd)

master_list = {
    "BSO": {"sector": "energy", "desc": "Bawson Oil is a premier oil supplier. With hundreds of thousands of gas stations throughout the world, in addition to hundreds of oil rigs, production of millions of barrels per month is no tough task. They are also a large supplier of oil to major airlines throughout the world."},
    "CSC": {"sector": "restaurant", "desc": "Colonel Sawyer's Chicken has pioneered the fast food chicken industry. This chicken giant is popular worldwide and has seen great success through their special 42 herbs and spices recipe plus their 0 tolerance policy. In addition, they have managed to get their trough of chicken to replace existing main holiday courses."},
    "QPS": {"sector": "technology", "desc": "QIPS is a market place where users can purchase shares of computing power that others are not currently using. The same users can also sell their power when they are not using it. QIPS has largely grown due to a large portion of their users using their service for gaming. They have also managed to keep their prices stable, even during day to day fluctuations in computing availability."}
}

def load_data():
    with open('data.json') as json_file:
        return json.load(json_file)

inventory_data = load_data()

def save_data():
    with open('data.json', 'w') as outfile:
        json.dump(inventory_data, outfile)

def main_screen():
    print("""
========================================================================================================================
    Door Street - Stock Market Game
========================================================================================================================
    """)

    input("Press Enter to continue...")
    menu()

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    number = input("""
======================
    1. Trading Floor
    2. News
    3. Next Day
----------------------
    4. Stock Info
    5. Help
    6. Achievements
    7. Statistics
    8. Save/Quit
    9. Settings
======================
    """)
    try:
        number = int(number)
    except:
        return menu()

    if number == 1:
        return trading_floor()
    elif number == 2:
        return news()
    elif number == 3:
        return next_day()
    elif number == 4:
        return stock_info()
    elif number == 5:
        return help_menu()
    elif number == 6:
        return achievements()
    elif number == 7:
        return stats()
    elif number == 8:
        return save_quit()
    elif number == 9:
        return settings()
    else:
        return menu()

def trading_floor():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
======================
    Trading Floor -- Day: {inventory_data["time"]["day"]}
======================
    Money: ${"{:.2f}".format(inventory_data["money"])}
    ------------------
    Energy Sector:
    ------------------
        $BSO: {inventory_data["portfolio"]["energy"]["BSO"]["shares"]} @ ${"{:.2f}".format(inventory_data["portfolio"]["energy"]["BSO"]["each"])}
            Current: {check_color("BSO")}${"{:.2f}".format(inventory_data["stocks"]["BSO"]["price"])}\u001b[37m
    ------------------
    Restaurant Sector:
    ------------------
        $CSC: {inventory_data["portfolio"]["restaurant"]["CSC"]["shares"]} @ ${"{:.2f}".format(inventory_data["portfolio"]["restaurant"]["CSC"]["each"])}
            Current: {check_color("CSC")}${"{:.2f}".format(inventory_data["stocks"]["CSC"]["price"])}\u001b[37m
    ------------------
    Technology Sector:
    ------------------
        $QPS: {inventory_data["portfolio"]["technology"]["QPS"]["shares"]} @ ${"{:.2f}".format(inventory_data["portfolio"]["technology"]["QPS"]["each"])}
            Current: {check_color("QPS")}${"{:.2f}".format(inventory_data["stocks"]["QPS"]["price"])}\u001b[37m
======================
    """)
    string = input("Enter Stock To Trade: ")
    try:
        if str(string) in master_list:
            number = input("""
======================
    1. Buy
    2. Sell
    0. menu
======================
    """)
            try:
                number = int(number)
            except:
                return menu()

            if number == 1:
                return buy_stock(str(string))
            elif number == 2:
                return sell_stock(str(string))
            else:
                return menu()
        elif int(string) == 0:
            menu()
    except:
        return menu()

def check_color(stock):
    if inventory_data["stocks"][stock]["price"] > inventory_data["stocks"][stock]["previous price"]:
        return "\u001b[32m"
    elif inventory_data["stocks"][stock]["price"] < inventory_data["stocks"][stock]["previous price"]: 
        return "\u001b[31m"
    else:
        return "\u001b[37m"

def buy_stock(stock):
    number = input("""
======================
    Enter Shares to Buy: 
======================
    """)
    try:
        number = int(number)
    except:
        return menu()

    stock_price = inventory_data["stocks"][stock]["price"]
    total = stock_price * number
    sector = master_list[stock]["sector"]
    each = inventory_data["portfolio"][sector][stock]["each"]
    prev_shares = inventory_data["portfolio"][sector][stock]["shares"]
    total_shares = inventory_data["portfolio"][sector][stock]["shares"] + number

    if total <= inventory_data["money"]:
        inventory_data["portfolio"][sector][stock]["shares"] += number
        inventory_data["money"] -= total

        inventory_data["portfolio"][sector][stock]["each"] = ((each * prev_shares) + total) / total_shares
        trading_floor()
    else:
        print("Not enough money")
        input("Press Enter to continue...")
        trading_floor()

def sell_stock(stock):
    number = input("""
======================
    Enter Shares Sell: 
======================
    """)
    try:
        number = int(number)
    except:
        return menu()

    stock_price = inventory_data["stocks"][stock]["price"]
    total = stock_price * number
    sector = master_list[stock]["sector"]
    each = inventory_data["portfolio"][sector][stock]["each"]
    prev_shares = inventory_data["portfolio"][sector][stock]["shares"]
    total_shares = inventory_data["portfolio"][sector][stock]["shares"] - number

    if number <= inventory_data["portfolio"][sector][stock]["shares"]:
        inventory_data["portfolio"][sector][stock]["shares"] -= number
        inventory_data["money"] += total

        if inventory_data["portfolio"][sector][stock]["shares"] == 0:
            inventory_data["portfolio"][sector][stock]["each"] = 0
        else:
            inventory_data["portfolio"][sector][stock]["each"] = ((each * prev_shares) - total) / total_shares

        trading_floor()
    else:
        print("Not enough shares")
        input("Press Enter to continue...")
        trading_floor()

def news():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
===================================================================================================
    News -- Day: {inventory_data["time"]["day"]} -- Current Headlines: {len(inventory_data["active news"])}
===================================================================================================
    Energy Sector:
    -----------------------------------------------------------------------------------------------
        $BSO: {has_headline("BSO")}\u001b[37m
    -----------------------------------------------------------------------------------------------
    Restaurant Sector:
    -----------------------------------------------------------------------------------------------
        $CSC: {has_headline("CSC")}\u001b[37m
    -----------------------------------------------------------------------------------------------
    Technology Sector:
    -----------------------------------------------------------------------------------------------
        $QPS: {has_headline("QPS")}\u001b[37m
===================================================================================================
    """)
    input("Press Enter to go back")
    menu()

def has_headline(stock):
    currentNews = inventory_data["active news"]

    for news in currentNews:
        if stock in news["affected stocks"]:
            if inventory_data["stocks"][stock]["days effect"] <= 0:
                return "\u001b[33m" + news["headline"]
            
            if news["effect"] == "up":
                return "\u001b[32m" + news["headline"]
            elif news["effect"] == "down":
                return "\u001b[31m" + news["headline"]
            else:
                return "\u001b[37m" + news["headline"]
    
    return "\u001b[37m None"

def next_day():
    os.system('cls' if os.name == 'nt' else 'clear')
    inventory_data["time"]["day"] += 1
    
    for stock in inventory_data["stocks"]:
        volatility = inventory_data["stocks"][stock]["volatility"]
        price = inventory_data["stocks"][stock]["price"]
        inventory_data["stocks"][stock]["previous price"] = price

        if len(inventory_data["stocks"][stock]["dayta"]) >= 30:
            inventory_data["stocks"][stock]["dayta"].pop(0)
            inventory_data["stocks"][stock]["dayta"].append(price)
        else:
            inventory_data["stocks"][stock]["dayta"].append(price)

        if inventory_data["stocks"][stock]["news effect"] == "none":
            randNum = random.randrange(1, 100, 1)
            if randNum > 50 and randNum <=100:
                change = volatility * price
                inventory_data["stocks"][stock]["price"] -= change
                print(f"{stock} ---")
            elif randNum >=1 and randNum <= 50:
                change = volatility * price
                inventory_data["stocks"][stock]["price"] += change
                print(f"{stock} +++")
            else:
                pass
        elif inventory_data["stocks"][stock]["news effect"] == "up":
            if inventory_data["stocks"][stock]["days effect"] >= 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] += change
                inventory_data["stocks"][stock]["days effect"] -= 1
                print(f"{stock} +++ news")
            elif inventory_data["stocks"][stock]["days effect"] <= 0:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] -= price * inventory_data["stocks"][stock]["stabalize"]\

                for item in inventory_data["active news"]:
                    if item["headline"] == inventory_data["stocks"][stock]["current news"]:
                        index = inventory_data["active news"].index(item)
                removed = inventory_data["active news"].pop(index)
                inventory_data["news"].append(removed)

                inventory_data["stocks"][stock]["days effect"] = 0
                inventory_data["stocks"][stock]["news change"] = 0
                inventory_data["stocks"][stock]["news effect"] = "none"
                inventory_data["stocks"][stock]["current news"] = ""
                inventory_data["stocks"][stock]["stabalize"] = 0
                print(f"{stock} +++ news")
            else:
                pass
        elif inventory_data["stocks"][stock]["news effect"] == "down":
            if inventory_data["stocks"][stock]["days effect"] >= 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] -= change
                inventory_data["stocks"][stock]["days effect"] -= 1
                print(f"{stock} --- news")
            elif inventory_data["stocks"][stock]["days effect"] <= 0:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] += price * inventory_data["stocks"][stock]["stabalize"]

                for item in inventory_data["active news"]:
                    if item["headline"] == inventory_data["stocks"][stock]["current news"]:
                        index = inventory_data["active news"].index(item)
                removed = inventory_data["active news"].pop(index)
                inventory_data["news"].append(removed)

                inventory_data["stocks"][stock]["days effect"] = 0
                inventory_data["stocks"][stock]["news change"] = 0
                inventory_data["stocks"][stock]["news effect"] = "none"
                inventory_data["stocks"][stock]["current news"] = ""
                print(f"{stock} --- news")
            else:
                pass
        else:
            pass
    
    print(f"""
    ========================================================
    {select_news()}
    ========================================================
    """)

    input("A new day has arrived...")
    menu()

def select_news():
    currentNews = inventory_data["active news"]
    
    i = 0
    while i < 2:
        news = random.choice(inventory_data["news"])
        if news not in currentNews:
            affected = news["affected stocks"][0]
            if inventory_data["stocks"][affected]["current news"] == "":
                inventory_data["news"].remove(news)
                inventory_data["active news"].append(news)

                for stock in news["affected stocks"]:
                    inventory_data["stocks"][stock]["current news"] = news["headline"]
                    inventory_data["stocks"][stock]["news change"] = news["change"]
                    inventory_data["stocks"][stock]["news effect"] = news["effect"]
                    inventory_data["stocks"][stock]["days effect"] = news["days"]
                    inventory_data["stocks"][stock]["stabalize"] = news["stabalize"]

                return news["headline"]
            else:
                i+=1
        else:
            i+=1

def achievements():
    print("Achievements")

def stats():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
======================
    Statistics
======================
    Total Money Earned: ${"{:.2f}".format(inventory_data["stats"]["total_money_earned"])}
======================
    """)
    input("Press Enter to continue...")
    menu()

def stock_info():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
======================
    Stock Info
======================
    Energy Sector:
----------------------
    Bawson Oil ($BSO): 
        {master_list["BSO"]["desc"]}
======================
    Restaurant Sector:
----------------------
    Colonel Sawyer's Chicken ($CSC): 
        {master_list["CSC"]["desc"]}
======================
    Technology Sector:
----------------------
    QIPS ($QPS):
        {master_list["QPS"]["desc"]}
    """)
    input("Press Enter to continue...")
    menu()

def help_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
============================================================================
    At any point throughout the game, press '0' to get back to the menu
============================================================================
    """)
    input("Press Enter to continue...")
    
    return menu()

def save_quit():
    save_data()

def settings():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
============================================================================
    Settings: Press Number to toggle true/false
============================================================================
    1. Simplified Trade Menu ({inventory_data["settings"]["simplified trade menu"]})
    """)
    number = input("Enter Setting to Change: ")

    try:
        number = int(number)
    except:
        return menu()

    if number == 1:
        inventory_data["settings"]["simplified trade menu"] = not inventory_data["settings"]["simplified trade menu"]
        settings()
    else:
        return menu()

main_screen()