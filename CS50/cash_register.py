def main():
    total = 0
    while True:
        try:
            #expetcted input as written in menu, case insensitive
            x = input_f()
            y = tab(x)
            if y == 0:
                continue
            else:
                total = total + y
                print(f"Total: ${total:.2f}")
        #continues repetition of main program until "ctrl + d" input
        except EOFError:
            print("")
            break
#formatting input
def input_f():
    x = input("Item: ").lower()
    return x.title()
#getting the price of the selected item or 0 if item does not exist
def tab(x):
    menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
    }
    if x in menu:
        return menu[x]  
    else:
        return 0
    
if __name__ == "__main__":
    main()
