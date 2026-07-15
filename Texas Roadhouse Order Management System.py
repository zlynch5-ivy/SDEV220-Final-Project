# Author: Ean Miller
# Program: Texas Roadhouse Order Management System
# Purpose: This module connects the seating system with the billing system. It associates each
# seated party with an order, tracks order status, and uses the OrderCalculator to generate
# itemized receipts. This module ensures that orders are linked to seated parties and provides
# status updates for kitchen and serving staff.
# --------------------------------------------------------------------------------------------------------------------------------------------

from order_calculator import OrderCalculator

class Order:
    def __init__(self, party_name, seating_location, menu):
        self.party_name = party_name
        self.seating_location = seating_location
        self.calculator = OrderCalculator(menu)
        self.status = "Pending"

    def add_item(self, item_name, quantity=1):
        self.calculator.add_item(item_name, quantity)

    def update_status(self, new_status):
        self.status = new_status

    def get_receipt(self, tip_percentage):
        return self.calculator.generate_receipt(tip_percentage)


class OrderManager:
    def __init__(self):
        self.orders = {}

    def create_order(self, party_name, seating_location, menu):
        if party_name in self.orders:
            print("Order already exists for this party.")
            return

        self.orders[party_name] = Order(party_name, seating_location, menu)
        print(f"Order created for {party_name} at {seating_location}.")

    def add_item_to_order(self, party_name, item_name, quantity=1):
        if party_name not in self.orders:
            print("No order found for this party.")
            return

        self.orders[party_name].add_item(item_name, quantity)

    def update_order_status(self, party_name, new_status):
        if party_name not in self.orders:
            print("No order found for this party.")
            return

        self.orders[party_name].update_status(new_status)
        print(f"Order status for {party_name} updated to {new_status}.")

    def get_order_status(self, party_name):
        if party_name not in self.orders:
            return "No order found."
        return self.orders[party_name].status

    def get_receipt(self, party_name, tip_percentage):
        if party_name not in self.orders:
            return "No order found."
        return self.orders[party_name].get_receipt(tip_percentage)