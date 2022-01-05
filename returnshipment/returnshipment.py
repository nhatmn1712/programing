def main():
    faultItems = str(input("Is the device not working  "))
    return_shipment(faultItems)

def return_shipment(faultItems):
    if faultItems == "yes":
        print ("We really sorry please ship the device back for us and we will send you the device back, all the fees will be covered by us")

    elif faultItems == "no":
        print ("Thank you for buying our products")

main()
    
    
