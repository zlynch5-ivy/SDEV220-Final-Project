# Texas Roadhouse Billing & Order Calculator
# Author: Ean Miller
# Purpose:
#   - Calculates customer bills based on menu items ordered
#   - Retrieves prices from a menu dictionary
#   - Supports multiple quantities of each item
#   - Ensures proper money formatting
#   - Generates an itemized receipt including subtotal, tax, tip, and total
#   - Integrates with the Smart Waiter GUI ordering system

# ---------------------------------------------------------------------------

class OrderCalculator:
    def __init__(self, menu):
        """Initialize the calculator with a menu price dictionary."""
        self.menu = menu
        self.order = {}

    # -----------------------------------------------------------------------
    # ORDER MANAGEMENT
    # -----------------------------------------------------------------------

    def add_item(self, item_name, quantity=1):
        """Add an item and quantity to the order."""
        item_name = item_name.strip()

        if item_name not in self.menu:
            print(f"Error: '{item_name}' is not on the menu.")
            return

        if quantity <= 0:
            print("Error: Quantity must be at least 1.")
            return

        self.order[item_name] = self.order.get(item_name, 0) + quantity
        print(f"Added {quantity} x {item_name} to the order.")

    # -----------------------------------------------------------------------
    # CALCULATIONS
    # -----------------------------------------------------------------------

    def calculate_subtotal(self):
        """Return the subtotal cost of all ordered items."""
        return sum(self.menu[item] * qty for item, qty in self.order.items())

    def calculate_tax(self, rate=0.07):
        """Return the tax amount based on the subtotal."""
        return self.calculate_subtotal() * rate

    def calculate_tip(self, percentage):
        """Return the tip amount based on subtotal + tax."""
        if percentage < 0:
            print("Error: Tip percentage cannot be negative.")
            return 0
        return (self.calculate_subtotal() + self.calculate_tax()) * (percentage / 100)

    def calculate_total(self, tip_percentage):
        """Return the final total including subtotal, tax, and tip."""
        return (
            self.calculate_subtotal()
            + self.calculate_tax()
            + self.calculate_tip(tip_percentage)
        )

    # -----------------------------------------------------------------------
    # RECEIPT GENERATION
    # -----------------------------------------------------------------------

    def generate_receipt(self, tip_percentage):
        """Generate a formatted itemized receipt."""
        if not self.order:
            return "No items ordered."

        lines = ["----- ITEMIZED RECEIPT -----"]

        # Itemized list
        for item, qty in self.order.items():
            price = self.menu[item]
            line_total = price * qty
            lines.append(f"{item} x{qty} @ ${price:.2f} = ${line_total:.2f}")

        # Totals
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
