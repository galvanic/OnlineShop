# coding: utf-8
# python3

"""
Script to automate who owes what for our online shopping.
Input:  A .txt file generated by copying the confirmation email content
        into a text file
        Asks who ordered which item
Output: Calculates who owes who and how much ?

Future improvements:
- Yahoo Mail API ?
- Makes guesses on whose item it is based on previous shop assignments
"""
import sys
import os
from ask import ask # my function from other file
import re
from collections import namedtuple
import csv

SHOP_DIRECTORY="shops/"


# make the ShopItem class (= a named tuple)
ShopItem = namedtuple("ShopItem", "name, price, whose")

def powerset(lst): # is this the fastest way to make a powerset ? Does it matter ? :p
    return reduce(lambda result, x: result +[subset +[x]for subset in result], lst,[[]])

flatmates = ["Justine", "Emily", "Ben", "Helena"]

flatmates = {person: 0.0 for person in flatmates}
flatmate_names = sorted(flatmates.keys(), key=len)  # bit repetitive, but in case I change things in the future
flatmate_initials = [name[0] for name in flatmate_names]
flatmate_diminutives = flatmate_names + flatmate_initials + ["Ben", "Em"]   # add diminutives in a more thorough manner

# groups = [", ".join(people) for people in powerset(flatmate_names)[1:]]
# groups = sorted(groups, key=len)

def whoIs(diminutive):
    for name in flatmate_names:
        match = re.search(r"^%s"%diminutive.lower(), name.lower())
        if match:
            return name 
    else:
        raise ValueError

##############################

def getLatestFile(filetype):
    """
    Returns a string with the name of the last modified file in
    the current folder.
    """
    filelist = [fn for fn in os.listdir(SHOP_DIRECTORY) if fn[-3:] == filetype]
    newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
    return SHOP_DIRECTORY + newest

def chooseFile():
    filelist = [fn for fn in os.listdir(SHOP_DIRECTORY) if fn[-3:] in ["txt", "csv"]]
    for i, filename in enumerate(filelist, 1):
        print(i, filename)
    f = ask("Which file do you want to open ?", range(1, len(filelist)+1))
    if not f:   # this doesn't work for the moment, can't figure out how to make it accept a None value
        filename = getLatestFile("csv")
    filename = filelist[int(f)-1]
    return SHOP_DIRECTORY + filename

def findShopItems(filename, write2file=True):
    """
    Finds all the shop items with regular expressions in the
    confirmation email.
    Returns a list of ShopItems, unassigned.
    Writes them to file by calling other function.
    """
    with open(filename, "rU") as f:
        ifile = f.read()
        items = re.findall(r'(^\d\d?) (.+?) £(\d\d?\.\d\d)', ifile, re.MULTILINE)
        other_info = re.search(r'^Delivery date\s([\w\d ]+).+?Delivery\s*£(\d\d?\.\d\d)\n^Voucher Saving\s*£(-?\d\d?.\d\d)', ifile, re.MULTILINE | re.DOTALL) # should make this one verbose

    delivery_date = other_info.group(1)
    delivery = float(other_info.group(2))
    voucher  = float(other_info.group(3))

    shop_items = []
    shop_items.append(ShopItem("Delivery costs", delivery, "".join(flatmate_initials)))
    if voucher:
        shop_items.append(ShopItem("Voucher savings", voucher, "".join(flatmate_initials)))

    shop_items += [ShopItem(name, float(price)/float(amount), "") for amount, name, price in items for i in range(int(amount))]
    # need to make function to reformat floated price into a £price

    subtotal = sum([float(item.price) for item in shop_items])
    total = subtotal + voucher + delivery

    # 1st checkpoint: check that subtotal and total correspond to the text file

    if write2file:
        writeShop2File(shop_items, "Ocado Shop %s.csv"%(delivery_date))

    return shop_items

def writeShop2File(shop_items, ofilename="temp_shop.csv", verbose=False):
    with open(ofilename, "w") as ofile:
        writer = csv.writer(ofile, dialect='excel')

        # title row
        writer.writerow(["#", "Name", "Price"] + flatmate_names)

        for i, item in enumerate(shop_items):
            who_ordered = []
            # this assumes whose is ordered
            for initial in item.whose:
                if initial != " ":
                    who_ordered.append("yes")
                else:
                    who_ordered.append("")
            writer.writerow([i, item.name, item.price] + who_ordered)
    if verbose:
        print("\nWritten to file %s.\n"%(ofilename))
    return

def getShopItems(filename):
    """
    From a csv file,
    Returns an (ordered) list of ShopItems.
    """
    if filename[-3:] == "txt":
        return findShopItems(filename)

    shop_items = list()
    with open(filename, "rU") as f:
        csv_reader = csv.reader(f)
        for i, row in enumerate(csv_reader):
            number, itemname, price, *flatmate_headers = row
            if i == 0:
                continue    # skips header
            whose = ""
            for j, name in enumerate(flatmate_headers):
                if name:
                    whose += flatmate_initials[j]
                else:
                    whose += " "
            s = ShopItem(itemname, float(price), whose)
            shop_items.append(s)
    return shop_items

def displayShop(itemlist, item_range=None):
    """
    Displays the shop in the terminal.
    Can decide what range of items to include.
    """
    start = item_range[0] if item_range else 0
    end = item_range[1] if item_range else len(itemlist)
    for i, item in enumerate(itemlist):
        if i < start:
            continue
        if i > end:
            break
        print("{:<4}{:_<60}".format(i, item.name), end=" ")
        for j, name in enumerate(item.whose):
            if name != " ":
                print(name, end=" ")
            else:
                print("_", end=" ")
        print()
    print()
    return


def askWhose(shop_items, start_line=1):
    """
    Since I can't read and write a function at the same time,
    this function will take the list of items, write in a 2nd file,
    delete 1st file and rename 2nd file to 1st filename.
    (for the moment i'm just making it overwrite because annoying
    otherwise)

    Returns a modified shop_items list.
    """
    modified_shopitems = list()
    end = None
    for i, item in enumerate(shop_items):
        if i < start_line:
            modified_shopitems.append(item)
            continue

        who = ask("Who bought - {} - {:<10}".format(item.name, "?"), None, "Enter a flatmate name or a value between 0 and 14.")
        # the formatting thing isn't working

        if not who:
            end = i
            break

        # turn string into one of the groups
        if who.lower() in ["everyone", "ev", "all"]:
            who = "".join(flatmate_initials)
        # else:
            # who = filter(None, re.findall(r"\w*", who)) ??

        # try splitting who by comma, and spaces
        # if no difference, either it's the initials joint together
        # of it's just one name
        # check it against names and diminutives
        # otherwise divide it by characters

        who = "".join(whoIs(person)[0] for person in who)
        who = who.upper()

        whose = ""
        for j, person in enumerate(flatmate_initials):
            if person in who:
                whose += flatmate_initials[j]
            else: whose += " "

        modified_shopitems.append(ShopItem(item.name, item.price, whose))
    
    if end:
        for i, item in enumerate(shop_items):
            if i > end:
                modified_shopitems.append(item)

    return modified_shopitems   # problem here, too easy to lose items


def isEveryItemAssigned(shop_items):
    for i, item in enumerate(shop_items):
        for char in item.whose:
            if char.upper() not in string.ascii_uppercase:
                return False
    return True

def calculateMoneyOwed(shop_items):
    """"""
    # check every item is assigned otherwise, division by zero next
    if not isEveryItemAssigned:
        "Not every item is assigned, so we cannot calculate total."
        return # make this into raising an exception?

    for i, item in enumerate(shop_items):
        amount_people = len([char for char in item.whose if char!= " "])
        for j, person in enumerate(item.whose):
            if person != " ":
                flatmates[flatmate_names[j]] += item.price/float(amount_people)

    print("\nEach person's total:\n")
    for person, total in flatmates.items():
        print("%s\t£%.2f"%(person, total))

    print("\nTotal paid by flatmates is £%.2f"%sum(flatmates.values()))
    print("Total paid for all items is £%.2f\n"%sum(item.price for item in shop_items))

    # # calculating who owes what to who
    # who_payed = ask("\nWho payed the shop ?", [name.lower() for name in flatmate_diminutives], "Enter the name of someone living in this flat.")
    # # easy, it's just the final total of each person
    # # actual difficulty will be in Excel, how to reduce the amount of transactions
    # who_payed = whoIs(who_payed)

    # for person in [name for name in flatmate_names if name != who_payed]:
    #   print("\n%s owes %s £%.2f."%(person, who_payed, flatmates[person]))

    return


def main():
    shopfile = chooseFile()
    shop_items = getShopItems(shopfile)
    displayShop(shop_items)
    line_start = ask("Which line do you want to start at ?", range(len(shop_items)))
    shop_items = askWhose(shop_items, int(line_start))
    writeShop2File(shop_items, verbose=True)
    displayShop(shop_items)
    calculateMoneyOwed(shop_items)
    return

if __name__ == '__main__':
    main()

"""
Different scenarios of how I'll use this script:

I input the confirmation email. I have a bit of time so I fill
in the first few items. Quit the script, I come back. It automatically
loads the latest shop. It loads the previously sorted items, and I
can either continue or change the previous ones.
When all are filled in, it calculates everyone's shop.
Ideally, you'd want the script to look at previous shop assignments,
and see who is more likely to have bought an item, and pre-assign
the items so that we just need to check.

At start, the script should load the latest shop assignment (offers
to load other shops). I can mark it as paid back. I can then choose
to load a new shop. It would be ideal if the program could then
automatically sign in to Yahoo and download latest email, but it
seems too complicated. I'll therefore assume that I've already
downloaded the email and saved it to a text file. The script chooses
the latest file.
The script should then go through everything and automatically create
the csv file. I'd been thinking of saving the amount of time it goes
through the item list by asking at that moment and calculating there
and then, but it's not worth the hassle since these lists are quite
small.
The script then asks me if I want to assign. If yes, I decide which
line to start assigning from and I can assign by name/number/wtv. I
can stop whenever.
When I've assigned the last item in the list, the programs goes
through the list calculating the money owed, but breaks if there is
an unassigned item. If not, it displays the money owed.

# I should have some sort of parameter file


"""


















