import json
import os
import time
from colorama import Fore, Back, Style

bids_data = []

file_path = 'data.json'

def check_s_b(question):
    while True:
        ans = input(question).strip().upper()
        if ans == "S" or ans == "B":
            return ans
        else:
            print(Fore.RED + "Please enter S or B")
            print(Style.RESET_ALL)


def checkstr(question):
    while True:
        ans = input(question)
        if ans.isalpha():
            return ans
        else:
            print(Fore.RED + "Only input letters")
            print(Style.RESET_ALL)


def checkint(question):
    while True:
        try:
            ans = int(input(question))
            if ans >= 0:
                return ans
        except ValueError:
            print(Fore.RED + "Only input positive numbers")
            print(Style.RESET_ALL)


def seller_menu():
    while True:
        try:
            item_nbr = checkint("How many items do you have (minimum 10): ")
            if item_nbr >= 1:
                pass

            else:
                print("Minimum of 10 items required. Please input again.")
        except ValueError:
            print("Invalid Input. Please input again")

        for i in range(item_nbr):
            item_number = checkint("Item number: ")
            item_description = checkstr("Description: ")
            reserve_price = checkint("Reserve price: ")
            initial_bid = 0

            bids = {
                "Item number": item_number,
                "Item description": item_description,
                "Reserve price": reserve_price,
                "Initial bid": initial_bid
            }

            bids_data.append(bids)
        break

    with open(file_path, "w") as json_file:
        json.dump(bids_data, json_file, indent=4)
    print("Data Saved to file")
    os.system("clear")



def save_auctions(auctions):
    with open(file_path, "w") as json_file:
        json.dump(auctions, json_file, indent=4)
    print("Data Saved to file")


def load_auctions():
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def add_items(buy_id, bid_amount, item_id):
    item_added = {
        "Buyer Id": buy_id,
        "Bid Amount": bid_amount,
        "Item Id": item_id,
    }
    bids_data.append(item_added)


def display_auction(auction):
    print(f"Item Number: {Fore.GREEN}{int(auction['Item number'])}{Style.RESET_ALL}")
    print(f"Item Description: {Fore.GREEN}{auction['Item description']}{Style.RESET_ALL}")
    print(f"Reserve Price: {Fore.GREEN}{auction['Reserve price']}{Style.RESET_ALL}")
    print(f"Current Bid: {Fore.GREEN}{auction['Initial bid']}{Style.RESET_ALL}")



def buyer_menu():
    n = 1
    user_id = n + 1
    available_auctions = load_auctions()
    current_auction = 0
    while True:
        display_auction(available_auctions[current_auction])
        print("N [NEXT AUCTION] / P [PREVIOUS AUCTION] / B [BID] / Q [QUIT]")
        user_choice = checkstr("> ")

        if user_choice.upper() == "N":
            os.system("clear")
            current_auction += 1
        elif user_choice.upper() == "P":
            os.system("clear")
            current_auction -= 1
        elif user_choice.upper() == "Q":
            conclusion()
            break
        elif user_choice.upper() == "B":
            make_bid()


def make_bid():
    auctions = load_auctions()

    while True:
        print("Input the Item Number")
        itm_nbr = checkint("> ")
        selected_item = None

        for item in auctions:
            if item["Item number"] == itm_nbr:
                selected_item = item
                break

        if selected_item is not None:  # checks that the item was found
            print("Input your buyer ID")
            buyer_id = checkint("> ")
            print("Input your bid")
            bid = checkint("> ")

            if bid > selected_item["Initial bid"]:
                print("Bid Accepted")
                selected_item["Initial bid"] = bid
                save_auctions(auctions)
                add_items(buyer_id, bid, itm_nbr)
                os.system("clear")
                # Saved the new bid, now showing the new bid
                print("Information:")
                print("Item Number:", item["Item number"])
                print("Item decription", item["Item description"])
                print("Reserve price", item["Reserve price"])
                print("Your Bid", item["Initial bid"])
                time.sleep(2)
                os.system("clear")
                break
            else:
                print(f"{Back.RED}Bid has to be higher than current bid{Style.RESET_ALL}")

        else:
            print(f"Item {itm_nbr} has not been found")


def conclusion():
    items = load_auctions()
    comission = 0
    sold_item = 0
    unsold = 0
    unbid = 0
    rounded_commission = 0
    for item in items:
        item_number = item["Item number"]
        reserve_price = item["Reserve price"]
        item_price = item["Initial bid"]

        if reserve_price <= item_price:
            print(f"Item {item_number} has been {Fore.GREEN}sold.{Style.RESET_ALL}")
            comission += item_price * 0.1
            rounded_commission = round(comission, 2)
            sold_item += 1
        else:
            print(f"Item {item_number} has {Fore.RED}not been sold.{Style.RESET_ALL}")
            unsold += 1

        if item_price == 0:
            print(f"Item {item_number} has not been {Fore.YELLOW}bid{Style.RESET_ALL}")
            unbid += 1
    time.sleep(2)
    os.system("clear")
    print(f"Total comissions generated during this auction was: {Fore.GREEN}{rounded_commission}{Style.RESET_ALL} CHF")
    print(f"Total Items sold: {Fore.GREEN}{sold_item}{Style.RESET_ALL}")
    print(f"Total Items unsold: {Fore.GREEN}{unsold}{Style.RESET_ALL}")
    print(f"Total bidless items: {Fore.GREEN}{unbid}{Style.RESET_ALL}")
    with open('data.json', 'w') as file:
        file.write('{}')



while True:
    print(f"Are you a {Fore.RED}Seller{Style.RESET_ALL} or {Fore.GREEN}Buyer{Style.RESET_ALL}")
    seller_buyer = check_s_b("> (S/B): ")
    if seller_buyer == "S":
        seller_menu()
    elif seller_buyer == "B":
        buyer_menu()
        break

