def main():
    shipping = str(input("please choose your shipment(normal/quick)"))
    ship_management(shipping)

def ship_management(shipping):
    if shipping == "normal":
        print("we will deliver your products in 24 hours")

    elif shipping == "quick":
        extrafee = 2
        waytopay = 10
        shipping = waytopay + extrafee
        print("we will deliver your products in 2 hours, additional fee is 2$ so price will be " + str(shipping))

main()