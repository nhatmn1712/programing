"""The main program to run the online shopping"""
# 1. List all items
# 2. List all info of a specific item (quantity, colors, sizes/dims, specs, descriptions, etc.) (the same as 3,4)
# 3. Search item by name
# 4. Search item by item id
# 5. List all info of a specific customer (name, email address, shipping address, etc.)
# 6. Placing orders (the quantity must be updated when an item is bought)r
from items import available_items, id_list  # import the items and its id
from discount import discount  # import discount function from discount.py

cart = []


def get_from_archive():
    """Update the quantity of each product from a text file"""
    with open('archive.txt', 'r') as archive:
        for line in archive.readlines():
            state = list(line.strip("\n").split(","))
            available_items[state[0]]['quantity'] = int(state[1])
            available_items[state[0]]['state'] = state[2]


def navigate():
    """Guide to navigate around the program"""
    print("""Type the following command to do what you want:
    list: to list all available products
    sch: to search by name or id a specific products, which will also give out details of it
    buy: to enter buy mode, add product to your cart 
    remove: to enter remove mode, remove product in your cart
    here: to know if you've been here before
    mycart: to see what you have buy
    pay: to go to checkout
    false: to report false product for we to exchange
    done: to leave the shopping
    """)


def list_items():
    """List all the items that our online shop currently available"""
    for item in available_items.keys():
        print(item + " " + available_items[item]['state'])


def search():
    """Search for a specific item with name or with id, will
    also show the specs of that item"""
    item_search = "none"
    print("Press 0 to escape")
    while item_search != 0:
        item_search = input("What are you looking for: ")
        if item_search in available_items.keys() or item_search in id_list.keys():
            # if the user search by id, then convert it into the item name
            if item_search in id_list.keys():
                item_search = id_list[item_search]
            # list all specs base on the item name
            for specs in available_items[item_search]:
                print(f"{specs}: {available_items[item_search][specs]}")
        elif item_search == "0":
            return None
        else:
            # if the user search something that our shop doesn't have
            print("Unavailable")


def add_to_cart(cart):
    """Add product to the cart"""
    go_buy = '1'
    print("Here are the product: ")
    print("Press 0 to escape, press 1 at the end to continue")
    while go_buy != "0":
        list_items()  # list all available item
        buy_product = input("Please make a choose: ")
        # if the product is not available that continue the loop
        if buy_product not in available_items.keys():
            print("Unavailable")
            continue
        # add an option to increase quantity only
        quantity = int(input("How many would you like: "))
        # if the wanted quantity is larger than available quantity, print message and continue
        if quantity > available_items[buy_product]['quantity']:
            print("Not meet demand")
            continue
        # Continue the loop if wanted quantity is less than or equal to 0
        elif quantity <= 0:
            print("Please make a clear choose: ")
            continue
        # update the quantity in the product if the cart already has that product,
        # if not then add it to the cart
        for product in cart:
            if buy_product == product[1]:
                quantity += product[0]
                if quantity > available_items[buy_product]['quantity']:
                    print("You have outweighed our supply, we will give you everything we have")
                    quantity = available_items[buy_product]['quantity']
                cart.remove(product)
                break
        cart.append([quantity, buy_product])
        # Ask the customers if they want to continue buying or not
        go_buy = input("Do you want anything else: ")


def rm_from_cart(cart):
    """Remove product from the cart"""
    print("Here is you current order: ")
    my_order(cart)  # display all available items in the current cart
    rm = 1
    print("Press 0 to escape, press 1 at the end to continue")
    while rm != 0:
        # Ask for what product to remove, if the product is not yet in the cart,
        # then continue the loop and ask again
        rm_product = input("what would you like to remove ? ")
        for product in cart:
            if rm_product == product[1]:
                current_quantity = product[0]
                rm_cart = [current_quantity, rm_product]
                break
        else:
            print("You don't have that yet")
            continue
        # Ask for the quantity of the remove product, if the quantity is larger or
        # equal than the current quantity in cart, than remove the whole product
        rm_quantity = input("How many would you like to remove:")
        cart.remove(rm_cart)
        if int(rm_quantity) < current_quantity:
            current_quantity -= int(rm_quantity)
            cart.append([current_quantity, rm_product])
        rm = int(input("Do you want to continue remove"))
    return None


def my_order(cart):
    """Print out what has been added to the current cart"""
    for product in cart:
        print(product)


def payment_management(total_price):  # Feature 1
    """Decide on the method use to pay, will add more fee when use credit card
    base on the total price"""
    waytopay = str(input("how do you want to pay (cash/credit card) "))
    if waytopay == "cash":
        print('here the price of your products: ' + str(total_price))
        return total_price

    elif waytopay == "credit card":
        annualfee = 2
        total_price += annualfee
        return total_price # #


def ship_management():  # Feature 2
    """Choose a shipment method, will ask extra cost for quick shipment"""
    shipping = str(input("please choose your shipment(normal/quick)"))
    if shipping == "normal":
        print("we will deliver your products in 24 hours")
        return 0

    elif shipping == "quick":
        extrafee = 2
        waytopay = 10
        shipping = waytopay + extrafee
        print("we will deliver your products in 2 hours, additional fee is 2$ so price will be " + str(shipping))
        return shipping


def payment(cart):  # Feature 3
    """Print out the total price and a basic receipt in list forms"""
    total_price = 0
    acquaintance, name = here()
    print("Here is your receipt")
    # print receipt
    for product in cart:
        price = available_items[product[1]]['price'] * int(product[0])
        product.append(price)
        total_price += price
        print(f"{product[0]} {product[1]} {product[2]}")
    # Add extra cost for payment and shipment if there are any
    total_price = payment_management(total_price)
    total_price += ship_management()
    print(name)
    total_price *= discount(name, total_price)

    print("Your total price is {0}".format(total_price))

    print("Your total price after using points is {0}".format(total_price))
    # If the customer is first time here, then ask for email and address,
    # if not, then print a message
    if acquaintance == "0":
        email_address = input("Your email addresss")
        shipping_address = input("Where you live")
        with open("customer.txt", "a") as user:
            user.write(name + "," + email_address + "," + shipping_address + "\n")
        return
    print("Welcome back")
    return


def here():
    """Look into the customer.txt file to decide on whether
    the customer is new here or not

    :returns: "1" if the customer used to shop here and vice versa, also return
    the name of the customer"""
    name = input("Please input your name")
    with open("customer.txt", "r") as user:
        for line in user.readlines():
            line = list(line.strip("\n").split(","))
            if line[0] == name:
                present = True
                print(f"Your info:{line[0]},{line[1]},{line[2]}")
                break
        else:
            present = False
    if present is True:
        print("You are our acquaintance here")
        return "1", name
    else:
        print("You are new here")
        return "0", name


def update(available_items, cart):
    """

    :param available_items:
    :param cart:
    :return:
    """
    for product in cart:
        remaining = available_items[product[1]]['quantity'] - \
                    int(product[0])
        if remaining == 0:
            available_items[product[1]]['quantity'] = 0
            available_items[product[1]]['state'] = 'sold out'

            return
        available_items[product[1]]['quantity'] = remaining
        return


def return_shipment():
    """Will replace broken product with new one without extra fee"""
    fault_items = str(input("Is the device not working: "))
    if fault_items == "yes":
        print("We really sorry please ship the device back for us and we will send you the device back,/"
              "all the fees will be covered by us")

    elif fault_items == "no":
        print("Thank you for buying our products")


def update_to_archive():
    """Updating the quantity of each product in the archive.txt file"""
    with open('archive.txt', 'w') as archive:
        for keys in available_items.keys():
            archive.write(keys+","+str(available_items[keys]['quantity'])+","+available_items[keys]['state']+"\n")


def main():
    """The main program than control the flow of all the functions"""
    get_from_archive()
    go_shopping = True
    print("Welcome to our store")
    navigate()
    while go_shopping:
        user_input = input("What do you want: ")
        if user_input == "list":
            list_items()
        elif user_input == "sch":
            search()
        elif user_input == "buy":
            add_to_cart(cart)
        elif user_input == "remove":
            rm_from_cart(cart)
        elif user_input == "mycart":
            my_order(cart)
        elif user_input == "pay":
            payment(cart)
        elif user_input == "here":
            a, b = here()  # to make sure it return something
        elif user_input == 'false':
            return_shipment()
        elif user_input == "done":
            update(available_items, cart)
            update_to_archive()
            go_shopping = False
        else:
            print("I don't know what are you looking for")
    print("Have a nice day")
    print("Your receipt")
    my_order(cart)


if __name__ == '__main__':
    main()
