#GUITkinter made by Ebony
#Contributions by Ean Miller, Zachariah Lynch, Jayden Judge 

#This is a tkinter program that allows a user to place an order thru a self ordering system 

#PRESS ESC TO EXIT PROGRAM!!!

import tkinter as tk
from tkinter import ttk
import os

from tkinter import messagebox 

#imports menu items
import Final_menu_items

#imports files for calculations of total
from Bill_Calculations_System import OrderCalculator

#Imports pricing file
from Menu_Prices import menu_prices

#Color pallete 
PALETTE ={
    
    "black_bg" : "#030303",
    "main_bg" : "#f5f7ed",
    "logo_color" : "#f8ad0c",
    "text_dark":"#282316",
    "text_light":"#f5f7ed",
    "menu_bg" : "#833d07",
    "kitchen_button" : "#f35607"
}

# tracking dictionary accessible by the action function
all_menu_spinboxes = {}



# Function to handle order popups
def order_popup():

    calculator = OrderCalculator(menu_prices)
    # Loops through all spinboxes and adds items to the calculator if quantity > 0
    for food_name, spinbox_widget in all_menu_spinboxes.items():

        quantity = int(spinbox_widget.get())

        if quantity > 0:
            calculator.add_item(food_name, quantity)

    if not calculator.order:
        #what displays in pop up when no items are selected
        messagebox.showwarning(
            "Empty Order",
            "No items selected. Please select at least one item!"
        )

    else:
        #Generates and shows the receipt box
        receipt = calculator.generate_receipt(20)
        messagebox.showinfo("Order Sent", receipt)

        #RUNS AUTOMATICALLY THE MOMENT THEY CLICK "OK" clears for the next order
        #Zero out every spinbox widget on the screen
        for spinbox_widget in all_menu_spinboxes.values():
            spinbox_widget.delete(0, tk.END)
            spinbox_widget.insert(0, "0")

        #Direct, safe layout reset for the right panel labels
        order_sum_label.config(
            text="\nSelect the items you wish to order",
            font=("Georgia",18,"bold"),
            #font color after reset
            foreground=PALETTE["text_dark"]
        )
        total_label.config(
            text="Thany you!",
            font=("Georgia",18,"bold"),
            foreground=PALETTE["text_dark"]
        )

# Labels for order summary and total amount
order_sum_label = None
# Label for total amount
total_label = None

# Function to update order selections
def update_order_selections(event=None):
    if order_sum_label is None or total_label is None:
        return

    # calculates ordered items
    calculator = OrderCalculator(menu_prices)
    # Initializes the order summary string
    order_summary = ""

    # Loops through all spinboxes to get the quantity of each item
    for food_name, spinbox_widget in all_menu_spinboxes.items():
        try:
            quantity = int(spinbox_widget.get())
            # Adds the item to the order if quantity is greater than 0
            if quantity > 0:
                calculator.add_item(food_name, quantity)
                order_summary += f"{food_name} x{quantity}\n"
        except ValueError:
            pass
    # Updates the order summary label based on the current order
    if not calculator.order:
        order_sum_label.config(text="Select the items\n you wish to order",
        #settings for selected font                       
        font=("Georgia",18,"bold"),
        foreground=PALETTE["text_dark"])
        return
    order_sum_label.config(text=order_summary)   

    

   
#generates receipt for the order
    try:
        receipt = calculator.generator_receipt(20)
        order_sum_label.config(text=receipt)
    except:
        pass

    try:
        running_total = calculator.get_total()
        total_label.config(text=f"Total: ${running_total:.2f}", foreground=PALETTE["text_dark"])
    except:
        try:
            total_label.config(text=f"Total: ${calculator.total:.2f}", foreground=PALETTE["text_dark"])
        except:
            running_total = sum(menu_prices.get(item, 0) * qty for item, qty in calculator.order.items())
            total_label.config(text=f"Total: ${running_total:.2f}", 
            #controls fg color for the total label once use selcts item
            foreground=PALETTE["text_dark"])

    #calculates ordered items
    calculator = OrderCalculator(menu_prices)
    order_summary = "Your Meal: \n\n"
    # Loops through all spinboxes to get the quantity of each item
    for food_name, spinbox_widget in all_menu_spinboxes.items():
        try:
            quantity = int(spinbox_widget.get())
            if quantity > 0:
                calculator.add_item(food_name, quantity)

                #makes list of items for the  display
                order_summary += f"{food_name} x{quantity}\n"
        except ValueError:
            pass

    #if nothin is selected resets display
    if not calculator.order:
        order_sum_label.config(text="Select the items you wish to order", 
        font=("Georgia",18,"bold"),
        foreground=PALETTE["text_dark"])
        total_label.config(text="Total: $0")
        return

    order_sum_label.config(text=order_summary, foreground=PALETTE["text_dark"])

    # generats receipt total
    try:
        # pulls total text or computing it
        receipt = calculator.generator_receipt(20)

        order_sum_label.config(text=receipt, foreground=PALETTE["text_light"])
    except:
        pass

# Function to handle sending the order to the kitchen
def my_action():
    # Grab the current text string from your live preview label
    current_order = order_sum_label.cget("text")
    #
    if current_order == "Your cart is empty." or current_order == "":
        messagebox.showwarning(
            "Empty Order", 
            "No items selected. Please select at least one item to send to the kitchen!"
        )
    else:
        # Create a small confirmation pop-up window
        popup_message = f"The following items have been sent to the kitchen:\n\n{current_order}"
        messagebox.showinfo("Order Sent", popup_message)



# ***********************
# CLASS 1: THE HEADER VIEW

# This class represents the header section of the application, including the logo and system name
class HeaderView:
    # Initializes the header view with a logo and system name
    def __init__(self, parent_frame,logo_image):
        # Creates header bg section
        self.header_frame = tk.Frame( parent_frame, 
            #bg for header
            background=PALETTE["black_bg"])
        self.header_frame.pack(pady=20, fill=tk.X)

        #display logo
        self.logo_label =  tk.Label(
            self.header_frame,
            image=logo_image,
            #color around border logo
            background=PALETTE["black_bg"]   

        )
        self.logo_label.pack()

        #displays title for our system name
        
        #display settings for system name (smart waiter orderingsystem)
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
# This class represents the main menu section of the application, which contains the tabs for different menu categories

class MainMenuView:
    # Initializes the main menu view with a parent frame
    def __init__(self, parent_frame):
        # Sets up the style for the main menu tabs
        style = ttk.Style()
        style.theme_use('default')
        #main tab container background, border thickness, and tab alignment
        style.configure("TNotebook",
            #color and left boarder behind tabs            
            background=PALETTE["menu_bg"],
            font=("Georgia", 17, "bold"),
            borderwidth=5, tabposition="n")

        # Unselected Tabs view settings
        style.configure("TNotebook.Tab", 
                        
                        #tab unselected bc color         
                        background=PALETTE["menu_bg"], 
                        #tabs word color when unselected
                        foreground=PALETTE["text_light"], 
                        font=("Georgia", 17, "bold"),#tab font controls
                        padding=[15, 15], 
                        borderwidth=0,
                        )

        # Selected tabs
        style.map("TNotebook.Tab",
            background=[
                #background color of selected tabs
                ('selected', PALETTE["logo_color"]),
                #color of tab background when hovering
                ('active', PALETTE["logo_color"]) 
            ],
            foreground=[
                #color of tab font when selected
                ('selected', PALETTE["kitchen_button"]),
                #font color when hovering over tabs
                ('active', PALETTE["kitchen_button"])
            ],
             font=[
                # text settings when hovering over active tabs
                ('active', ("Georgia", 19, "bold")),
                # text setting when tab is actively selected
                ('selected', ("Georgia", 19, "bold"))
            ]
        )        


        
        #***master layout (full page layout inside canvas frame)
        
        columns_container = tk.Frame(parent_frame, 
            #color of gap in center of page                         
            background=PALETTE["logo_color"]) 
        columns_container.pack(fill="both", expand=True, padx=0, pady=0)

        # FORCE 50/50 screen split for left and right columns
        columns_container.columnconfigure(0, weight=1, uniform="half")
        columns_container.columnconfigure(1, weight=1, uniform="half")
        columns_container.rowconfigure(0, weight=1)

        # ***left side (menu)
        menu_notebook = ttk.Notebook(columns_container) # 2. REMOVED width=250
        menu_notebook.grid(row=0, column=0, sticky="nsew", padx=(5, 5))

        # ***right side (selections area)
        right_frame = tk.Frame(columns_container, background=PALETTE["logo_color"]) 
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0)) # 4. CHANGED .pack to .grid

        #Send to kichen button
        button_frame = tk.Frame(right_frame, 
            #background for the button frame
            background=PALETTE["text_light"])
        # add button frame to the bottom of the right frame
        button_frame.pack(side="bottom", fill="x", padx=10, pady=15) # 11. ADDED side="bottom" configuration
        # create the kitchen button within the button frame
        kitchen_button = tk.Button(
            button_frame, 
            font=("Georgia", 20, "bold"), 
            command=order_popup, 
            text="SEND TO KITCHEN!", 
            foreground=PALETTE["text_dark"],
            #color for kitchen button
            background=PALETTE["kitchen_button"])
        kitchen_button.pack(side="bottom", fill="x", pady=5, padx=20)

        #
        global order_sum_label, total_label

        #outter scroll window
        # create a container for the scrollable area
        scroll_container = tk.Frame(right_frame, background=PALETTE["logo_color"])
        scroll_container.pack(fill="both", expand=True, padx=10, pady=10)

        # create the canvas that will hold the scrollable content   
        canvas = tk.Canvas(scroll_container,
        #background for rigth side
            background=PALETTE["logo_color"], highlightthickness=0, width=300)
        canvas.pack(side="left", fill="both", expand=True)

        #Physical slider tracking handle bar
        # Standard tk scrollbar allows direct thickness and color control
        scrollbar = tk.Scrollbar(
            scroll_container, 
            orient="vertical", 
            width=35, # Double width size scrollbar
            bg=PALETTE["black_bg"],           
            activebackground=PALETTE["black_bg"], # Keeps it black when clicked
            command=canvas.yview
        )

        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        #Inner mounting frame that holds the actual text labels
        scrollable_frame = tk.Frame(canvas, 
            #color for top level scrollable frame background behind text                       
            background=PALETTE["logo_color"])
        canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Function to update the scroll region whenever the inner frame changes size
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        # Function to adjust the canvas width to match the scrollable frame width
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_frame_id, width=event.width)
        canvas.bind("<Configure>", configure_canvas_width)


        # Loop that retrieves data from your food dictionary
        for category_name in Final_menu_items.menu_dictionary.keys():
            tab_frame = tk.Frame(menu_notebook, 
                #main menu bg inner color                 
                background=PALETTE["menu_bg"], 
                padx=5, 
                pady=0)
            menu_notebook.add(tab_frame, text=category_name)

            #controls setting for category names in menu
            category_label = tk.Label(
                tab_frame, text=f"{category_name}", 
                font=("Georgia", 25,"bold"),
                #selected tab menu title color inside menu the bg color
                foreground=PALETTE["text_light"], 
                background=PALETTE["menu_bg"] 
            )
            category_label.pack(anchor="w", pady=(15, 5))

            # Loop through each food item in the category
            food_list = Final_menu_items.menu_dictionary[category_name]

            # Loop through each food item in the list for the current category
            for food_item in food_list:
                row = tk.Frame(tab_frame, 
                #bg of space between food name and spinboxes                          
                background=PALETTE["menu_bg"]) 
                row.pack(fill="x", expand=True, anchor="w", padx=(0, 10), pady=2)

                #spin box setting
                spin = tk.Spinbox(
                row, font=("Georgia", 20), from_=0, to=25, increment=1, width=4, 
                #spinbox bg color
                background=PALETTE["main_bg"],
                #spinbox text
                foreground=PALETTE["text_dark"], 
                #color of increment arrow bacground
                buttonbackground=PALETTE["logo_color"], 
                command=update_order_selections

                )   
                # Pack the spinbox to the right side of the row
                spin.pack(side="right", padx=(0, 10))
                # Bind events to update order selections when the spinbox value changes
                spin.bind("<ButtonRelease-1>", update_order_selections)
                spin.bind("<KeyRelease>", update_order_selections)

                all_menu_spinboxes[food_item] = spin

                # Get the price for the current food item
                price = menu_prices.get(food_item, 0.00)
                display_text = f"{food_item} (${price:.2f})"

                #setting for items in menu categories
                item_label = tk.Label(
                    row, 
                    font=("Georgia", 20), text=display_text, 
                    #category list colors
                    foreground=PALETTE["text_light"], 
                    #background of category names
                    background=PALETTE["menu_bg"] 
                )
                # Pack the item label to the left side of the row
                item_label.pack(side="left")

        #
        global order_sum_label, total_label

        # Create labels for order summary and total
        #waht appears before user selects
        order_sum_label = tk.Label(scrollable_frame, 
            text="\nSelect the items you wish to order",
            font=("Georgia", 20, "bold"),
            #color of order text before selection
            foreground=PALETTE["text_dark"], 
            #background color for order sum label text
            background=PALETTE["logo_color"])
        order_sum_label.pack()

        total_label = tk.Label(scrollable_frame, 
            #shows befor and item is selected
            text="Thank you!", 
            font=("Georgia",20, "bold"),
            background=PALETTE["logo_color"], #backgroung color of total_label
            foreground=PALETTE['text_dark']#color of text for total_label
        )
        # Pack the total label below the order summary
        total_label.pack()

#******************
#class 3 FooterView
#Class for the footer view containing images and hover effects

class FooterView:
    # This class handles the footer view, displaying images of menu items with hover effects
    def __init__(self, parent_frame):
        #Create a centered horizontal frame inside the footer bar
        inner_footer = tk.Frame(parent_frame, background="black")
        inner_footer.pack(expand=True)

        #Map your image assets securely
        self.pic1 = rolls_image  
        self.pic2 = wings_image  
        self.pic3 = ribs_image   

        #Image list setup
        footer_items = [
            (self.pic1, "Fresh Rolls"),
            (self.pic2, "Buffalo Wings"),
            (self.pic3, "Baby Back Ribs")
        ]
        # Iterate over each image and its corresponding name to create the footer items
        for img, name in footer_items:
            img_width = img.width()
            img_height = img.height()

            #Create canvas for the food image
            canvas = tk.Canvas(
                inner_footer, 
                width=img_width, 
                height=img_height, 
                background="black", 
                highlightthickness=0
            )
            canvas.pack(side="left", padx=50, pady=10)

            #Draw the background image
            canvas.create_image(img_width // 2, img_height // 2, image=img)

            #Bind mouse hover entry and exit actions
            canvas.bind("<Enter>", lambda e, c=canvas, w=img_width, h=img_height, t=name: self.on_hover(e, c, w, h, t))
            canvas.bind("<Leave>", lambda e, c=canvas: self.on_hover_exit(e, c))

    #Handles hover effect for the footer images
    def on_hover(self, event, canvas, width, height, text_to_show):
        """Fires when mouse enters the image area"""
        #makes semi-transparent dark tint so text reads clearly over food pictures
        canvas.create_rectangle(0, 0, width, height, fill="black", stipple="gray50", tags="hover_ui")
        
        #draw the bright name label directly over the center of the image
        canvas.create_text(
            width // 2, 
            height // 2, 
            text=text_to_show, 
            font=("Georgia", 18, "bold"), 
            fill=PALETTE["logo_color"], 
            tags="hover_ui"
        )
    #Handles hover exit for the footer images
    def on_hover_exit(self, event, canvas):
        """Fires when mouse leaves the image area"""
        # Clear out the text and overlay tint cleanly
        canvas.delete("hover_ui")




# ROOT DESKTOP SYSTEM APPLICATION ENGINE


#create the window and set its properties
root = tk.Tk()
root.attributes  ( "-fullscreen",True) #makes window appear full screen
#how user escapes app by preesing ESC onkeyboard
root.bind("<Escape>", lambda e: root.destroy())
#what appears on the top of the window
root.title("Smart Waiter")
root.attributes("-topmost", True) #makes window stay on top
root.configure(background=PALETTE["main_bg"]) #background color might not show with all page frames covering

#finds and resizes TRH logo
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
Texaslogo = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "Texaslogo.png")).subsample(3, 3)

#finds roll image
rolls_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "rolls.png")).subsample(4,4 )

#finds rib image
ribs_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "ribs.png")).subsample(2, 2)

#finds wings image
wings_image = tk.PhotoImage(file=os.path.join(SCRIPT_DIR, "wings.png")).subsample(4, 4)

#main background color
page_frame = tk.Frame(root, 
    background=PALETTE["logo_color"]) #top and bottom of page title
page_frame.pack(fill=tk.BOTH, expand=True)


#footer settings
footer_frame = tk.Frame(page_frame,
    #footer bg color                     
    background=PALETTE["black_bg"], 
    height=50) 
footer_frame.pack(side="bottom", fill="x")

# Launch the header, main menu, and footer sections
header_section = HeaderView(page_frame,Texaslogo)
menu_section = MainMenuView(page_frame)
footer_section = FooterView(footer_frame)


#
root.mainloop()
