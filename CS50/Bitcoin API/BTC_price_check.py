import json
import requests
import sys

def main():
    #checking if there is only one command line argument (ammount to buy) and catching errors
    try:
        if len(sys.argv) != 2:
            sys.exit("Missing command-line argument")
        else:
            ammount = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")
    price = get_price()
    order_price(ammount, price)


def get_price():
    while True:
        try:
            #getting bitcoin price data
            bitcoin = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
            o = bitcoin.json()
            #returning current $USD value
            return o["bpi"]["USD"]["rate_float"]
        except requests.RequestException:
            continue

def order_price(ammount, price):
    order = ammount * price
    print(f"${order:,.4f}")

if __name__ == "__main__":
    main()
