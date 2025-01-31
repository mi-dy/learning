#expecting fraction of current fuel tank output(as in x/y)
def main():
        i = input("Fraction: ")
        print(gauge(convert(i)))

def convert(fraction):
  #checking if fraction is numbers and not other symbols
        a, b = fraction.split("/")
        if a.isdigit() == False or b.isdigit() == False:
            raise ValueError("Value Error")
        elif int(a) > int(b):
            raise ValueError("Value Error")
        elif b == "0":
             raise ZeroDivisionError("Zero Division")
        else:
             a = int(a)
             b = int(b)
        x = a / b * 100
        return x
#converting fraction to percentage, with exceptions when the tank is Full or Empty
def gauge(percentage):
    if 0 <= percentage <= 1:
        return("E")
    elif  99 <= percentage <= 100:
        return("F")
    else:
        return(f"{percentage:.0f}%")

if __name__ == "__main__":
    main()
