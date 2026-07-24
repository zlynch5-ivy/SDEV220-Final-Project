# Author: Ean Miller
# Program: Texas Roadhouse Menu Transfer System
# Purpose: This module reads and translates SteakhousePrices.txt into a usable dictionary
# that can be imported across the entire backend. It safely skips empty lines and divider
# headers, ensuring the billing system can accurately determine item prices.
# --------------------------------------------------------------------------------------------------------------------------------------------

def load_menu_from_file(filename):
    """
    Reads a menu text file and converts it into a dictionary:
        { "Item Name": price_as_float }
    Category headers (--------BURGERS--------) are ignored.
    """
    menu = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip divider lines like --------BURGERS--------
            if line.startswith("--------"):
                continue

            # Parse item lines: Item Name: $Price
            if ":" in line:
                item, price = line.split(":", 1)
                item = item.strip()
                price = price.strip().replace("$", "")

                try:
                    price = float(price)
                    menu[item] = price
                except ValueError:
                    print(f"Warning: Could not parse price for line: {line}")

    return menu


# Load the menu from the text file
MENU_FILE = "SteakhousePrices.txt"
menu = load_menu_from_file(MENU_FILE)

# Optional debugging
if __name__ == "__main__":
    print("Loaded Menu Items:")
    for item, price in menu.items():
        print(f"{item}: ${price:.2f}")