# Author: Ean Miller
# Program: Texas Roadhouse Menu Billing and Order Calculator
# Purpose: This module calculates customer bills based on menu items ordered. It retrieves prices
# from a menu collection, supports multiples of the same item, ensures proper money formatting,
# and safeguards against invalid input. It generates an itemized bill showing each charge,
# subtotal, tax, tip, and final total. This module integrates with the Order Management System
# and future GUI components.
# --------------------------------------------------------------------------------------------------------------------------------------------

class OrderCalculator:
    def __init__(self, menu):
        self.menu = menu
        self.order = {}

    def add_item(self, item_name, quantity=1):
        item_name = item_name.strip()

        if item_name not in self.menu:
            print(f"Error: '{item_name}' is not on the menu.")
            return

        if quantity <= 0:
            print("Error: Quantity must be at least 1.")
            return

        self.order[item_name] = self.order.get(item_name, 0) + quantity
        print(f"Added {quantity} x {item_name} to the order.")

    def calculate_subtotal(self):
        return sum(self.menu[item] * qty for item, qty in self.order.items())

    def calculate_tax(self, rate=0.07):
        return self.calculate_subtotal() * rate

    def calculate_tip(self, percentage):
        if percentage < 0:
            print("Error: Tip percentage cannot be negative.")
            return 0
        return (self.calculate_subtotal() + self.calculate_tax()) * (percentage / 100)

    def calculate_total(self, tip_percentage):
        return self.calculate_subtotal() + self.calculate_tax() + self.calculate_tip(tip_percentage)

    def generate_receipt(self, tip_percentage):
        if not self.order:
            return "No items ordered."

        lines = ["----- ITEMIZED RECEIPT -----"]

        for item, qty in self.order.items():
            price = self.menu[item]
            line_total = price * qty
            lines.append(f"{item} x{qty} @ ${price:.2f} = ${line_total:.2f}")

        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        tip = self.calculate_tip(tip_percentage)
        total = self.calculate_total(tip_percentage)

        lines.append("----------------------------")
        lines.append(f"Subtotal: ${subtotal:.2f}")
        lines.append(f"Tax (7%): ${tax:.2f}")
        lines.append(f"Tip ({tip_percentage}%): ${tip:.2f}")
        lines.append(f"TOTAL: ${total:.2f}")
        lines.append("----------------------------")

        return "\n".join(lines)