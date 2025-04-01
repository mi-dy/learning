from tkinter import *

def click(b):
    #If current player 1 print X else print O
    b.config(text="X")

if __name__ == "__main__":
    window = Tk()
    buttons = []

    for n in range(9):
        button = Button(window)
        button.config(command=lambda b=button: click(b))
        row, column = divmod(n, 3)
        button.grid(row=row, column=column)

    window.mainloop()
    #User chooses if he moves first or second. First player is assigned X as button values, second - O
    #If bot goes first, picks middle button.
    #If bot goes second, chooses the best possible option that is determined from previous games, or chooses randomly
    #Checker checks if there are 3 of the same symbols in a row after the third move of the first player and every turn afterwards.
    #If 3 in a row is found, the winner is declared. If not, TIE!
    #The game is saved for bot to use when determening moves in future games