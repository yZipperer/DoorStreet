from time import sleep
import json
import os
import random

master_list = {
    "BSO": {"sector": "energy", "desc": "Bason Oil is a premier oil supplier. With hundreds of thousands of gas stations throughout the world, in addition to hundreds of oil rigs, production of millions of barrels per month is no tough task."},
    "CSC": {"sector": "restaurant", "desc": "Colonel Sawyer's Chicken has pioneered the fast food chicken industry. This chicken giant is popular worldwide and has seen great success through their special 42 herbs and spices recipe plus their 0 tolerance policy."},
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
========================================
Door Street - Stock Market Game
========================================

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
    8. Save
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
            Current: ${"{:.2f}".format(inventory_data["stocks"]["BSO"]["price"])}
    ------------------
    Restaurant Sector:
    ------------------
        $CSC: {inventory_data["portfolio"]["restaurant"]["CSC"]["shares"]} @ ${"{:.2f}".format(inventory_data["portfolio"]["restaurant"]["CSC"]["each"])}
            Current: ${"{:.2f}".format(inventory_data["stocks"]["CSC"]["price"])}
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

        inventory_data["portfolio"][sector][stock]["each"] = ((each * prev_shares) - total) / total_shares
        trading_floor()
    else:
        print("Not enough shares")
        input("Press Enter to continue...")
        trading_floor()

def next_day():
    os.system('cls' if os.name == 'nt' else 'clear')
    inventory_data["time"]["day"] += 1
    
    for stock in inventory_data["stocks"]:
        volatility = inventory_data["stocks"][stock]["volatility"]
        price = inventory_data["stocks"][stock]["price"]
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
            if inventory_data["stocks"][stock]["days effect"] > 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] += change
                inventory_data["stocks"][stock]["days effect"] -= 1
                print(f"{stock} +++ news")
            elif inventory_data["stocks"][stock]["days effect"] <= 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] += change
                for item in inventory_data["active news"]:
                    if item["headline"] == inventory_data["stocks"][stock]["current news"]:
                        index = inventory_data["active news"].index(item)
                removed = inventory_data["active news"].pop(index)
                inventory_data["news"].append(removed)

                inventory_data["stocks"][stock]["days effect"] = 0
                inventory_data["stocks"][stock]["news change"] = 0
                inventory_data["stocks"][stock]["news effect"] = "none"
                inventory_data["stocks"][stock]["current news"] = ""
                print(f"{stock} +++ news")
            else:
                pass
        elif inventory_data["stocks"][stock]["news effect"] == "down":
            if inventory_data["stocks"][stock]["days effect"] > 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] -= change
                inventory_data["stocks"][stock]["days effect"] -= 1
                print(f"{stock} --- news")
            elif inventory_data["stocks"][stock]["days effect"] <= 1:
                change = inventory_data["stocks"][stock]["news change"] * price
                inventory_data["stocks"][stock]["price"] -= change

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
    while i < 3:
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
    Bawson Oil: {master_list["BSO"]["desc"]}
======================
    Restaurant Sector:
----------------------
    Colonel Sawyer's Chicken: {master_list["CSC"]["desc"]}
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

main_screen()