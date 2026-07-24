# Author: Ean Miller
# Program: Texas Roadhouse Seating and Waiting List Program
# Purpose: This module handles seating customers, managing reservations, tracking waiting lists,
# and maintaining seating availability. It connects to the Order Management System to ensure
# that each seated party can be associated with an active order. This module will be integrated
# into the larger Texas Roadhouse management system and future GUI components.
# --------------------------------------------------------------------------------------------------------------------------------------------

from Texas_Roadhouse_Order_Management_System import OrderManager
from Texas_Roadhouse_Menu_Transfer import menu

order_manager = OrderManager()

available_tables = 15
available_booths = 20
available_date_tables = 10
available_bar_stools = 30

table_list = []
booth_list = []
date_table_list = []
bar_stool_list = []

waiting_list = []
party_lookup = {}


def display_availability():
    print(
        f"\nThere are {available_tables} tables, {available_booths} booths, "
        f"{available_date_tables} date tables, and {available_bar_stools} bar stools available.\n"
    )


def seat_waiting_list():
    global available_tables, available_booths, available_date_tables, available_bar_stools
    global table_list, booth_list, date_table_list, bar_stool_list, waiting_list, party_lookup

    if not waiting_list:
        return

    sorted_waiting = sorted(waiting_list, key=lambda x: (not x[2]))

    for party_name, party_size, is_reservation, reservation_time in sorted_waiting:
        seating_location = None

        if party_size > 4 and available_tables > 0:
            available_tables -= 1
            table_list.append(party_name)
            seating_location = f"Table {len(table_list)}"

        elif party_size > 2 and available_booths > 0:
            available_booths -= 1
            booth_list.append(party_name)
            seating_location = f"Booth {len(booth_list)}"

        elif party_size == 2 and available_date_tables > 0:
            available_date_tables -= 1
            date_table_list.append(party_name)
            seating_location = f"Date Table {len(date_table_list)}"

        elif party_size == 1 and available_bar_stools > 0:
            available_bar_stools -= 1
            bar_stool_list.append(party_name)
            seating_location = f"Bar Stool {len(bar_stool_list)}"

        if seating_location:
            waiting_list.remove((party_name, party_size, is_reservation, reservation_time))
            party_lookup[party_name]["status"] = "seated"
            print(f"{party_name} has been seated at {seating_location}.")

            order_manager.create_order(party_name, seating_location)
            return


def lookup_party():
    name = input("Enter the party name to look up: ")

    if name not in party_lookup:
        print("No party found with that name.")
        return

    info = party_lookup[name]
    print(f"\nParty Name: {name}")
    print(f"Party Size: {info['size']}")
    print(f"Reservation: {'Yes' if info['reservation'] else 'No'}")
    print(f"Reservation Time: {info['time']}")
    print(f"Status: {info['status']}")

    if info["status"] == "waiting":
        for i, entry in enumerate(waiting_list, start=1):
            if entry[0] == name:
                print(f"Waiting List Position: {i}")
                break

    print()


def CustomerSeating():
    global available_tables, available_booths, available_date_tables, available_bar_stools
    global table_list, booth_list, date_table_list, bar_stool_list, waiting_list, party_lookup

    print(
        "\nWelcome to the Texas Roadhouse! Enter 1 to seat a party, 2 to view the waiting list, "
        "3 to remove a party from the waiting list, 4 to free up seating when customers leave, "
        "5 to look up a party, or 0 to exit: "
    )
    choice = int(input())

    if choice == 0:
        print("Thank you for visiting Texas Roadhouse! Have a great day!")
        return False

    elif choice == 2:
        print("Waiting List:")
        for i, (name, size, is_reservation, time) in enumerate(waiting_list, start=1):
            status = "Reservation" if is_reservation else "Walk-in"
            print(f"{i}. {name} ({size} people) - {status} at {time}")
        display_availability()
        return True

    elif choice == 3:
        print("Waiting List:")
        for i, (name, size, is_reservation, time) in enumerate(waiting_list, start=1):
            status = "Reservation" if is_reservation else "Walk-in"
            print(f"{i}. {name} ({size} people) - {status} at {time}")
        try:
            index = int(input("Enter the number of the party you want to remove: ")) - 1
            if 0 <= index < len(waiting_list):
                removed_party = waiting_list.pop(index)
                party_lookup[removed_party[0]]["status"] = "removed"
                print(f"{removed_party[0]} has been removed from the waiting list.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        display_availability()
        return True

    elif choice == 4:
        print("Enter 1 to free a table, 2 for a booth, 3 for a date table, 4 for a bar stool:")
        free_choice = int(input())

        if free_choice == 1 and table_list:
            available_tables += 1
            print(f"{table_list.pop(0)} has left. Table freed.")
        elif free_choice == 2 and booth_list:
            available_booths += 1
            print(f"{booth_list.pop(0)} has left. Booth freed.")
        elif free_choice == 3 and date_table_list:
            available_date_tables += 1
            print(f"{date_table_list.pop(0)} has left. Date table freed.")
        elif free_choice == 4 and bar_stool_list:
            available_bar_stools += 1
            print(f"{bar_stool_list.pop(0)} has left. Bar stool freed.")
        else:
            print("No seating of that type is currently occupied.")

        seat_waiting_list()
        display_availability()
        return True

    elif choice == 5:
        lookup_party()
        return True

    print("Enter the number of people in your party (0 to exit): ")
    party_size = int(input())

    if party_size == 0:
        print("Thank you for visiting Texas Roadhouse! Have a great day!")
        return True

    if party_size > 6:
        print("We cannot seat parties larger than 6.")
        return True

    party_name = input("Please enter the name of your party: ")
    is_reservation = input("Is this a reservation? (Y/N): ").upper() == "Y"
    reservation_time = input("Enter reservation time (HH:MM): ") if is_reservation else "None"

    party_lookup[party_name] = {
        "size": party_size,
        "reservation": is_reservation,
        "time": reservation_time,
        "status": "waiting",
    }

    seating_location = None

    if party_size > 4:
        if available_tables > 0:
            available_tables -= 1
            table_list.append(party_name)
            seating_location = f"Table {len(table_list)}"
    elif party_size > 2:
        if available_booths > 0:
            available_booths -= 1
            booth_list.append(party_name)
            seating_location = f"Booth {len(booth_list)}"
    elif party_size == 2:
        if available_date_tables > 0:
            available_date_tables -= 1
            date_table_list.append(party_name)
            seating_location = f"Date Table {len(date_table_list)}"
    elif party_size == 1:
        if available_bar_stools > 0:
            available_bar_stools -= 1
            bar_stool_list.append(party_name)
            seating_location = f"Bar Stool {len(bar_stool_list)}"

    if seating_location:
        party_lookup[party_name]["status"] = "seated"
        print(f"{party_name} has been seated at {seating_location}.")
        order_manager.create_order(party_name, seating_location)
    else:
        print("No seating available. Added to waiting list.")
        waiting_list.append((party_name, party_size, is_reservation, reservation_time))

    display_availability()
    return True


while True:
    if not CustomerSeating():
        break