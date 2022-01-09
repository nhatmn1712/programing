import json

def register():
    print("What's your name?")
    name = input("Name: ")
    print("How old are you?")
    age = input("Age: ")
    print("What's your phone number?")
    phone = input("Phone number: ")
    print("What's your email?")
    email = input("Email: ")
    print("What's your shipping address")
    address = input("Shipping address: ")
    with open('customer_information.txt') as file:
        customer_info = json.load(file)
    file.close()
    customer_info[name] = {'Age' : age,
                           'Phone number' : phone,
                           'Email' : email,
                           'Shipping address' : address}
    with open('information.txt', 'w') as file:
        file.write(json.dumps(customer_info))
    file.close()
    print("You have successfully registered!")
