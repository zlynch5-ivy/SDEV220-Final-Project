# GUITkinter made by Ebony
# Contributions by Ean Miller, Zachariah Lynch, Jayden Judge

# This is a tkinter program that allows a user to place an order thru a self ordering system
# PRESS ESC TO EXIT PROGRAM!!!

import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox

# imports menu items
import Final_menu_items

# imports files for calculations of total
from Bill_Calculations_System import OrderCalculator

# Imports pricing file
from Menu_Prices import menu_prices

# Color palette
PALETTE = {
    "black_bg": "#030303",
    "main_bg": "#f5f7ed",
    "logo_color": "#f8ad0c",
    "text_dark": "#282316",
    "text_light": "#f5f7ed",
    "menu_bg": "#833d07",
    "kitchen_button": "#f35607"
}

# tracking dictionary accessible by the action function
all_menu_spinboxes = {}

# Labels for order summary and total amount
order_sum_label = None
total_label = None


# Function to handle order popups
def order_popup():
    calculator = OrderCalculator(menu_prices)

    # Loops through all spinboxes and adds items to the calculator if quantity > 0
    for food_name, spinbox_widget in all_menu_spinboxes.items():
        quantity = int(spinbox_widget.get())
        if quantity > 0:
            calculator.add_item(food_name, quantity)

    if not calculator.order:
        messagebox.showwarning("Empty Order", "No items selected. Please select at least one item!")
        return

    # Generates and shows the receipt box
    receipt = calculator.generate_receipt(20)
    messagebox.showinfo("Order Sent", receipt)

    # Reset spinboxes
    for spinbox_widget in all_menu_spinboxes.values():
        spinbox_widget.delete(0, tk.END)
        spinbox_widget.insert(0, "0")

    # Reset right panel labels
    order_sum_label.config(
        text="\nSelect the items you wish to order",
        font=("Georgia", 18, "bold"),
        foreground=PALETTE["text_dark"]
    )
    total_label.config(
        text="Thank you!",
        font=("Georgia", 18, "bold"),
        foreground=PALETTE["text_dark"]
    )


# Function to update order selections
def update_order_selections(event=None):
    if order_sum_label is None or total_label is None:
        return

    calculator = OrderCalculator(menu_prices)
    order_summary = "Your Meal:\n\n"

    # Build order
    for food_name, spinbox_widget in all_menu_spinboxes.items():
        try:
            quantity = int(spinbox_widget.get())
            if quantity > 0:
                calculator.add_item(food_name, quantity)
                order_summary += f"{food_name} x{quantity}\n"
        except ValueError:
            pass

    # If nothing selected
    if not calculator.order:
        order_sum_label.config(
            text="Select the items you wish to order",
            font=("Georgia", 18, "bold"),
            foreground=PALETTE["text_dark"]
        )
        total_label.config(text="Total: $0.00", foreground=PALETTE["text_dark"])
        return

    # Update summary
    order_sum_label.config(text=order_summary, foreground=PALETTE["text_dark"])

    # Update total
    running_total = calculator.calculate_total(20)
    total_label.config(text=f"Total: ${running_total:.2f}", foreground=PALETTE["text_dark"])


# Function to handle sending the order to the kitchen
def my_action():
    current_order = order_sum_label.cget("text")

    if current_order.strip() == "" or current_order == "Your cart is empty.":
        messagebox.showwarning("Empty Order", "No items selected. Please select at least one item!")
        return

    popup_message = f"The following items have been sent to the kitchen:\n\n{current_order}"
    messagebox.showinfo("Order Sent", popup_message)


# ***********************
# CLASS 1: THE HEADER VIEW

class HeaderView:
    def __init__(self, parent_frame, logo_image):
        self.header_frame = tk.Frame(parent_frame, background=PALETTE["black_bg"])
        self.header_frame.pack(pady=20, fill=tk.X)

        self.logo_label = tk.Label(self.header_frame, image=logo_image, background=PALETTE["black_bg"])
        self.logo_label.pack()

        system_name = tk.Label(
            self.header_frame,
            text="[SMART WAITER ORDERING SYSTEM]",
            font=("Rockwell", 25, "italic"),
            background=PALETTE["black_bg"],
            foreground=PALETTE["text_light"]
        )
        system_name.pack()


# **************************
# CLASS 2: THE MAIN MENU VIEW

class MainMenuView:
    def __init__(self, parent_frame):
        style = ttk.Style()
        style.theme_use('default')

        style.configure("TNotebook",
                        background=PALETTE["menu_bg"],
                        font=("Georgia", 17, "bold"),
                        borderwidth=5,
                        tabposition="n")

        style.configure("TNotebook.Tab",
                        background=PALETTE["menu_bg"],
                        foreground=PALETTE["text_light"],
                        font=("Georgia", 17, "bold"),
                        padding=[15, 15],
                        borderwidth=0)

        style.map("TNotebook.Tab",
                  background=[('selected', PALETTE["logo_color"]), ('active', PALETTE["logo_color"])],
                  foreground=[('selected', PALETTE["kitchen_button"]), ('active', PALETTE["kitchen_button"])],
                  font=[('active', ("Georgia", 19, "bold")),
                        ('selected', ("Georgia", 19, "bold"))])

        columns_container = tk.Frame(parent_frame, background=PALETTE["logo_color"])
        columns_container.pack(fill="both", expand=True)

        columns_container.columnconfigure(0, weight=1, uniform="half")
        columns_container.columnconfigure(1, weight=1, uniform="half")
        columns_container.rowconfigure(0, weight=1)

        menu_notebook = ttk.Notebook(columns_container)
        menu_notebook.grid(row=0, column=0, sticky="nsew", padx=(5, 5))

        right_frame = tk.Frame(columns_container, background=PALETTE["logo_color"])
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0))

        button_frame = tk.Frame(right_frame, background=PALETTE["text_light"])
        button_frame.pack(side="bottom", fill="x", padx=10, pady=15)

        kitchen_button = tk.Button(
            button_frame,
            font=("Georgia", 20, "bold"),
            command=order_popup,
            text="SEND TO KITCHEN!",
            foreground=PALETTE["text_dark"],
            background=PALETTE["kitchen_button"]
        )
        kitchen_button.pack(side="bottom", fill="x", pady=5, padx=20)

        global order_sum_label, total_label

        scroll_container = tk.Frame(right_frame, background=PALETTE["logo_color"])
        scroll_container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(scroll_container, background=PALETTE["logo_color"], highlightthickness=0, width=300)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", width=35, bg=PALETTE["black_bg"],
                                 activebackground=PALETTE["black_bg"], command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(canvas, background=PALETTE["logo_color"])
        canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_frame_id, width=e.width))

        # Loop through menu categories
        for category_name in Final_menu_items.menu_dictionary.keys():
            tab_frame = tk.Frame(menu_notebook, background=PALETTE["menu_bg"], padx=5, pady=0)
            menu_notebook.add(tab_frame, text=category_name)

            category_label = tk.Label(
                tab_frame,
                text=f"{category_name}",
                font=("Georgia", 25, "bold"),
                foreground=PALETTE["text_light"],
                background=PALETTE["menu_bg"]
            )
            category_label.pack(anchor="w", pady=(15, 5))

            food_list = Final_menu_items.menu_dictionary[category_name]

            for food_item in food_list:
                row = tk.Frame(tab_frame, background=PALETTE["menu_bg"])
                row.pack(fill="x", expand=True, anchor="w", padx=(0, 10), pady=2)

                spin = tk.Spinbox(
                    row,
                    font=("Georgia", 20),
                    from_=0,
                    to=25,
                    increment=1,
                    width=4,
                    background=PALETTE["main_bg"],
                    foreground=PALETTE["text_dark"],
                    buttonbackground=PALETTE["logo_color"],
                    command=update_order_selections
                )
                spin.pack(side="right", padx=(0, 10))
                spin.bind("<ButtonRelease-1>", update_order_selections)
                spin.bind("<KeyRelease>", update_order_selections)

                all_menu_spinboxes[food_item] = spin

                price = menu_prices.get(food_item, 0.00)
                display_text = f"{food_item} (${price:.2f})"

                item_label = tk.Label(
                    row,
                    font=("Georgia", 20),
                    text=display_text,
                    foreground=PALETTE["text_light"],
                    background=PALETTE["menu_bg"]
                )
                item_label.pack(side="left")

        order_sum_label = tk.Label(
            scrollable_frame,
            text="\nSelect the items you wish to order",
            font=("Georgia", 20, "bold"),
            foreground=PALETTE["text_dark"],
            background=PALETTE["logo_color"]
        )
        order_sum_label.pack()

        total_label = tk.Label(
            scrollable_frame,
            text="Thank you!",
            font=("Georgia", 20, "bold"),
            background=PALETTE["logo_color"],
            foreground=PALETTE["text_dark"]
        )
        total_label.pack()


# ******************
# CLASS 3: FOOTER VIEW

class FooterView:
    def __init__(self, parent_frame):
        inner_footer = tk.Frame(parent_frame, background="black")
        inner_footer.pack(expand=True)

        self.pic1 = rolls_image
        self.pic2 = wings_image
        self.pic3 = ribs_image

        footer_items = [
            (self.pic1, "Fresh Rolls"),
            (self.pic2, "Buffalo Wings"),
            (self.pic3, "Baby Back Ribs")
        ]

        for img, name in footer_items:
            img_width = img.width()
            img_height = img.height()

            canvas = tk.Canvas(inner_footer, width=img_width, height=img_height,
                               background="black", highlightthickness=0)
            canvas.pack(side="left", padx=50, pady=10)

            canvas.create_image(img_width // 2, img_height // 2, image=img)

            canvas.bind("<Enter>", lambda e, c=canvas, w=img_width, h=img_height, t=name:
                        self.on_hover(e, c, w, h, t))
            canvas.bind("<Leave>", lambda e, c=canvas: self.on_hover_exit(e, c))

    def on_hover(self, event, canvas, width, height, text_to_show):
        canvas.create_rectangle(0, 0, width, height, fill="black", stipple="gray50", tags="hover_ui")
        canvas.create_text(width // 2, height // 2, text=text_to_show,
                           font=("Georgia", 18, "bold"), fill=PALETTE["logo_color"], tags="hover_ui")

    def on_hover_exit(self, event, canvas):
        canvas.delete("hover_ui")


# ROOT APPLICATION ENGINE

root = tk.Tk()
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.title("Smart Waiter")
root.attributes("-topmost", True)
root.configure(background=PALETTE["main_bg"])

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
Texaslogo = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "Texaslogo.png")).subsample(3, 3)
rolls_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "rolls.png")).subsample(4, 4)
ribs_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "ribs.png")).subsample(2, 2)
wings_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "wings.png")).subsample(4, 4)

page_frame = tk.Frame(root, background=PALETTE["logo_color"])
page_frame.pack(fill=tk.BOTH, expand=True)

footer_frame = tk.Frame(page_frame, background=PALETTE["black_bg"], height=50)
footer_frame.pack(side="bottom", fill="x")

header_section = HeaderView(page_frame, Texaslogo)
menu_section = MainMenuView(page_frame)
footer_section = FooterView(footer_frame)

root.mainloop()
