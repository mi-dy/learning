import random

def main():
    level = get_level()
    count = 0
    score = 10
    while True:
        mistakes = 0
        x = generate_integer(level)
        y = generate_integer(level)
        if count < 10:
            try:
                while True:
                    try:
                        i = int(input(f"{x} + {y} = "))
                        z = x + y
                        if i == z:
                            count += 1
                            break
                        else:
                            if mistakes < 2:
                                print("EEE")
                                mistakes += 1
                                continue
                            else:
                                print(f"{x} + {y} = {z}")
                                count += 1
                                score -= 1
                                break
                    except ValueError:
                        continue
            except ValueError:
                continue
        else:
            print(score)
            break

def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if 1 <= level <= 3:
                return level
            else:
                continue
        except ValueError:
            continue

def generate_integer(level):
    if level == 1:
        return random.randrange(0, 10, 1)
    elif level == 2:
        return random.randrange(10, 100, 1)
    else:
        return random.randrange(100, 1000, 1)


if __name__ == "__main__":
    main()
