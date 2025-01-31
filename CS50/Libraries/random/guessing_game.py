import random
import sys

def main():
    #getting a number to determine range of possible number to guess
    while True:
        try:
            n = int(input("Level: "))
            if n < 1:
                continue
            else:
                break
        except ValueError:
            continue
    rnd = (generate_random(n))
    guess(rnd)
#generating random number in the range 1 to n
def generate_random(n):
    return int(random.randrange(1, n+1, 1))

def guess(rnd):
    while True:
        try:
            n = int(input("Guess: "))
            if n >= 1:
                if n > rnd:
                    print("Too large!")
                elif n < rnd:
                    print("Too small!")
                else:
                    print("Just right!")
                    sys.exit()
            else:
                continue
        except ValueError:
            continue

main()
