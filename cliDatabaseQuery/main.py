

def main(): 
    #main menu
    choice = 0
    while choice != '2': 
        print("Choose one of the options below (pressing the number)")
        print("1. Login")
        print("2. Cancel") 
        choice = input()
        if choice == '1': 
            queryMenu()

def queryMenu(): 
    choice = 0
    while choice != '6':
        print("How would you like to look up a patient? (pressing the number)") 
        print("1. Patient ID")
        print("2. First Name")
        print("3. Last name")
        print("4. DoB")
        print("5. Address")
        print("6. Log Out")
        choice = input()



if __name__ =="__main__": 
    main()

