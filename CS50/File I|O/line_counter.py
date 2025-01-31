import sys

def main():
  #expecting the name of the python file
    if len(sys.argv) != 2:
        sys.exit("Too many argumants")
    elif ".py" not in sys.argv[1]:
        sys.exit("Argument does not end with .py")
    else:
        x = len_checker(sys.argv[1])
    print(f"{x} lines of code")
#checking the number of code lines excluding empty lines and "#" comments
def len_checker(file):
    count = 0
    try:
        with open(file, "r") as text:
            for line in text:
                x = line.lstrip()
                if line.isspace():
                    continue
                elif x[0] != "#":
                    count += 1
            return count
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()
