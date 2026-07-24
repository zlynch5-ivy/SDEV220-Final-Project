# Author: Ean Miller
# Program: Texas Roadhouse Order Management System
# Purpose: This module connects the seating system with the billing system. It associates each
# seated party with an order, tracks order status, and uses the OrderCalculator to generate
# itemized receipts. This module ensures that orders are linked to seated parties and provides
# status updates for kitchen and serving staff. It acts as the bridge between the seating
# subsystem and the billing subsystem within the Texas Roadhouse Restaurant Management Backend.
# --------------------------------------------------------------------------------------------------------------------------------------------

from Texas_Roadhouse_Menu_Transfer import menu
from Texas_Roadhouse_Bill_Calculation_System import OrderCalculator


class Order:
    """
    Represents a single party's order.
    Stores:
        - party name
        - seating location (Table 3, Booth 2, etc.)
        - OrderCalculator instance
        - order status (Pending → In Progress → Ready → Served → Paid)
    """

    def __init__(self, party_name, seating_location):
        self.party_name = party_name
        self.seating_location = seating_location
        self.calculator = OrderCalculator(menu)
        self.status = "Pending"  # Default status when order is created

    def add_item(self, item_name, quantity=1):
        """Adds an item to the order."""
        self.calculator.add_item(item_name, quantity)

    def update_status(self, new_status):
        """Updates the order's workflow status."""
        self.status = new_status

    def get_receipt(self, tip_percentage):
        """Generates an itemized receipt using the billing system."""
        return self.calculator.generate_receipt(tip_percentage)


class OrderManager:
    """
    Manages all active orders in the restaurant.
    Provides:
        - order creation
        - item addition
        - status updates
        - receipt retrieval
    """

    def __init__(self):
        self.orders = {}  # Maps party_name → Order object

    def create_order(self, party_name, seating_location):
        """Creates a new order for a seated party."""
        if party_name in self.orders:
            print("Order already exists for this party.")
            return

        self.orders[party_name] = Order(party_name, seating_location)
        print(f"Order created for {party_name} at {seating_location}.")

    def add_item_to_order(self, party_name, item_name, quantity=1):
        """Adds an item to an existing order."""
        if party_name not in self.orders:
            print("No order found for this party.")
            return

        self.orders[party_name].add_item(item_name, quantity)

    def update_order_status(self, party_name, new_status):
        """Updates the workflow status of an order."""
        if party_name not in self.orders:
            print("No order found for this party.")
            return

        self.orders[party_name].update_status(new_status)
        print(f"Order status for {party_name} updated to {new_status}.")

    def get_order_status(self, party_name):
        """Returns the current status of a party's order."""
        if party_name not in self.orders:
            return "No order found."
        return self.orders[party_name].status

    def get_receipt(self, party_name, tip_percentage):
        """Returns the final receipt for a party."""
        if party_name not in self.orders:
            return "No order found."
        return self.orders[party_name].get_receipt(tip_percentage)
