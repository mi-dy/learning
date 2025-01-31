import sys
import csv

def main():
    try:
      #expecting 2 arguments in command line, first for file to convert, second for output
        if len(sys.argv) != 3:
            sys.exit("Argument count is not 2")
        else:
            file_check(sys.argv[1])
            converter(sys.argv[1], sys.argv[2])
    except FileNotFoundError:
        sys.exit("File not found")
#checking if expected lines are in the files fieldnames
def file_check(x):
    with open(x, "r") as file:
        reader = csv.DictReader(file)
        if "name" not in reader.fieldnames or"house" not in reader.fieldnames:
            sys.exit("Wrong file format")
#adding aditional fieldname. Instead of Name, now we have First and Last names
def converter(a, b):
    with open(a, "r") as file1, open(b, "w") as file2:
        csv.writer(file2).writerow(["first","last","house"])
        reader = csv.DictReader(file1)
        writer = csv.DictWriter(file2, fieldnames=["first", "last", "house"])
        for row in reader:
            last, first = row["name"].split(", ")
            writer.writerow({"first": first, "last": last, "house": row["house"]})

if __name__ == "__main__":
    main()
