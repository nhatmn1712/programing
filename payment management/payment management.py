def main():
    waytopay = str(input("how do you want to pay (cash/credit card) "))
    payment_management(waytopay)

def payment_management(waytopay):
    if waytopay == "cash":
        print('here the price of your products' + str(itemprice))
        
    elif waytopay == "credit card":
        annualfee = 2
        waytopay = itemprice + annualfee
        print("the price is" + waytopay)
        
main()
