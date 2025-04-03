from tkinter import *

def choose_sequence():

    window.title("Tic-Tac-Toe Choose!")

    label = Label(window,
                  text="Choose to go first or second?",
                  font=("Arial",20,"bold"),
                  relief=SUNKEN,
                  bd=5,
                  padx=5,
                  pady=5)
    label.pack()

    button_first = Button(window,text="First!",command=lambda: game(window, "X"))
    button_first.pack()

    button_second = Button(window,text="Second!",command=lambda: game(window, "O"))
    button_second.pack()


def game(window, player):
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Tic-Tac-Toe Play!")

    for n in range(9):
        button = Button(window)
        button.config(command=lambda b=button: click(b, player))
        row, column = divmod(n, 3)
        button.grid(row=row, column=column)

def click(b, player):
    b.config(text=player)


if __name__ == "__main__":
    window = Tk()
    window.geometry("400x400")

    choose_sequence()
    
    window.mainloop()
    #User chooses if he moves first or second. First player is assigned X as button values, second - O
    #If bot goes first, picks middle button.
    #If bot goes second, chooses the best possible option that is determined from previous games, or chooses randomly
    #Checker checks if there are 3 of the same symbols in a row after the third move of the first player and every turn afterwards.
    #If 3 in a row is found, the winner is declared. If not, TIE!
    #The game is saved for bot to use when determening moves in future games