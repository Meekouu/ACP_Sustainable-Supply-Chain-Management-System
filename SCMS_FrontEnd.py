"""
    FrontEnd
    OOP-DBMS Joint Collaboration Final Project
    Advanced Computer Programming Final Project
    *****, Mico
    BSIT - 2102/2104        | BATSTATEU-The National Engineering University


        since this is open to the public, i will try to describe
        every part of this code.
                                                    - C0mi (Mico)
"""
# import modules required to run
# import necessary gui libs.
import ttkbootstrap as ttkbs
from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox  # under ttkbs, messagebox pop up
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk

import matplotlib.pyplot as plt

import cv2
from pyzbar.pyzbar import decode
import time
import threading

# BackEnd import
import SCMS_BackEnd  # import the backend code.


# class for the whole application
class LOGISYNC:
    logi_sync = None
    current_profile_picture = None

    def __init__(self, root):
        self.root = root
        self.root.title("LogiSync Login")
        self.root.iconphoto(False, (ttkbs.PhotoImage(file="images/supply_icon.png")))
        self.root.iconbitmap(default='images/supply_icon.ico')
        self.login_window()

    def login_window(self):
        self.ttkbs_style = ttkbs.Style()
        self.ttkbs_style.load_user_themes(file='themes/dark_green.json')
        self.ttkbs_style.theme_use('dark_green')
        self.ttkbs_style.configure('TLabel', foreground="#FFFFFF", background="#191A19")

        self.ttkbs_style.configure('TOutlineButton', foreground="#4E9F3D", background="white")

        logo1 = ttkbs.Image.open(fp="images/login_page.png")
        self.new_logo = ImageTk.PhotoImage(logo1.resize((180, 430)))
        logo_label = ttkbs.Label(self.root, image=self.new_logo, background="#191A19")
        logo_label.place(x=0, y=0)
        user_img = ctk.CTkImage(ttkbs.Image.open(fp='images/enter.png'), size=(15, 15))
        ttkbs.Label(self.root, text="LogiSync:\nSupply-Chain\nManagement System", font=('Helvetica', 17, 'bold'),
                    foreground="#FFFFFF", background="#191A19", justify="left").place(x=200, y=30)

        window_width = 500
        window_height = 430
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(False, False)

        # log in credentials
        ttkbs.Label(self.root, text="USERNAME", foreground="#FFFFFF").place(x=231,
                                                                            y=167,
                                                                            anchor="center")
        self.username_underline = Frame(self.root)
        self.username_underline.config(background="#4E9F3D", height=2, width=220)
        self.username_underline.place(x=200, y=200)
        self.username_entry = Entry(self.root, width=30)
        self.username_entry.configure(highlightthickness=0, bg="#191A19", fg="white", font=('Arial', 10),
                                      selectbackground="#4E9F3D")
        self.username_entry.place(x=200, y=180)
        self.username_entry.insert(0, "")

        ttkbs.Label(self.root, text="PASSWORD", foreground="#FFFFFF").place(x=231,
                                                                            y=250,
                                                                            anchor="center")
        self.password_underline = Frame(self.root)
        self.password_underline.config(background="#4E9F3D", height=2, width=220)
        self.password_underline.place(x=200, y=290)
        self.password_entry = Entry(self.root, show="*", width=30)
        self.password_entry.config(highlightthickness=0, bg="#191A19", fg="white", font=('Arial', 10),
                                   selectbackground="#4E9F3D")
        self.password_entry.place(x=200, y=270)
        self.password_entry.insert(0, "")

        self.login_button = ctk.CTkButton(self.root, text="Login", command=self.login_button_click, image=user_img,
                                          fg_color='#4e9f3d', hover_color='#1E5128')
        self.login_button.configure(width=20)
        self.login_button.place(x=280, y=330)

        ttkbs.Label(self.root, text="Don't have an account?").place(x=220, y=365)
        self.register_button = ctk.CTkButton(self.root, text="Sign up", command=self.register_window,
                                             font=('Helvetica', 12, 'underline'), fg_color='transparent',
                                             hover_color='#191A19', text_color='#4e9f3d', anchor='n')
        self.register_button.configure(width=8)
        self.register_button.place(x=345, y=363)

        self.inv_frame = Frame(self.root)
        self.inv_frame.place(x=100, y=175)

    def login_button_click(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if SCMS_BackEnd.authenticate_user(username, password):
            Messagebox.show_info("Authentication Successful. Access Granted to the application", "Login Successful"
                                 , parent=self.inv_frame)
            self.current_user = username
            self.root.withdraw()
            create_main_window(self.root, self.current_user)
        elif username == "" and password == "":
            Messagebox.show_error("Username/Password cannot be empty!", "Login Error!"
                                  , parent=self.inv_frame)
        else:
            Messagebox.show_error("Authentication Failed. Access Denied", "Login Failed"
                                  , parent=self.inv_frame)

        for widget in self.root.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, "end")

    def register_window(self):
        self.register_window = ttkbs.Toplevel(self.root)
        self.register_window.title("Register")
        self.inv_frame1 = Frame(self.register_window)
        self.inv_frame1.place(x=100, y=50)

        ttkbs.Label(self.register_window, text="LogiSync:\nRegistration",
                    font=('Helvetica', 14, 'bold'),
                    foreground="#FFFFFF", background="#191A19", justify="left").place(x=50, y=12)

        # registration form
        ttkbs.Label(self.register_window, text="Username:", foreground="white").grid(row=0, column=0, padx=10,
                                                                                     pady=(75, 5),
                                                                                     sticky="w")
        self.register_username_entry = ttkbs.Entry(self.register_window)
        self.register_username_entry.grid(row=0, column=1, padx=10, pady=(75, 5))

        ttkbs.Label(self.register_window, text="Password:", foreground="white").grid(row=1, column=0, padx=10, pady=5,
                                                                                     sticky="w")
        self.register_password_entry = ttkbs.Entry(self.register_window, show="*")
        self.register_password_entry.grid(row=1, column=1, padx=10, pady=5)

        ttkbs.Label(self.register_window, text="Confirm Password:", foreground="white").grid(row=2, column=0, padx=10,
                                                                                             pady=5, sticky="w")
        self.confirm_password_entry = ttkbs.Entry(self.register_window, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.current_profile_picture = PhotoImage(file="pfp/placeholder_profile.png").subsample(5)
        placeholder_label = ttkbs.Label(self.register_window, image=self.current_profile_picture)
        placeholder_label.image = self.current_profile_picture
        placeholder_label.place(x=325, y=75)

        upload_button = ctk.CTkButton(self.register_window, text="UPLOAD", command=self.upload_profile_picture,
                                      fg_color='#4e9f3d', hover_color='#1E5128', width=10)
        upload_button.place(x=350, y=190)

        register_button = ctk.CTkButton(self.register_window, text="REGISTER", command=self.register_user
                                        , fg_color='#4e9f3d', hover_color='#1E5128')
        register_button.place(x=132, y=190)

        back_button = ttkbs.Button(self.register_window, style='T.OutlineButton', text="Back",
                                   command=lambda: self.register_window.withdraw())
        back_button.place(x=430, y=235)

        window_width = 500
        window_height = 270
        screen_width = self.register_window.winfo_screenwidth()
        screen_height = self.register_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.register_window.resizable(False, False)

    def upload_profile_picture(self):
        pfp_file_path = filedialog.askopenfilename(title="Select Profile Picture",
                                                   filetypes=[("Image files", "*.png;*.jpg;*.jpeg")],
                                                   parent=self.register_window)

        if pfp_file_path:
            pil_image = Image.open(pfp_file_path)

            pil_image = pil_image.resize((120, 120))

            pil_image = pil_image.convert("RGBA")
            mask = Image.new("L", pil_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 120, 120), fill=255)
            pil_image.putalpha(mask)

            self.current_profile_picture = ImageTk.PhotoImage(pil_image)

            placeholder_label = ttkbs.Label(
                self.register_window,
                image=self.current_profile_picture,
                borderwidth=2,
                relief='flat'
            )
            placeholder_label.image = self.current_profile_picture
            placeholder_label.place(x=320, y=63)

            self.pfp_file_path = pfp_file_path

    def register_user(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if username == "" or password == "":
            Messagebox.show_error("Username and password cannot be empty!", "Registration Error",
                                  parent=self.inv_frame1)
        elif password != confirm_password:
            Messagebox.show_error("Password and Confirm Password do not match!", "Registration Error",
                                  parent=self.inv_frame1)
        else:
            pfp_file_path = getattr(self, 'pfp_file_path', "pfp/placeholder_profile.png")

            if SCMS_BackEnd.register_user(username, password, pfp_file_path):
                Messagebox.show_info("You can now log in", "Registration Successful", parent=self.inv_frame1)
                self.register_window.withdraw()
            else:
                Messagebox.show_error("Username already exists. Please choose a different username.",
                                      "Registration Failed", parent=self.inv_frame1)


def create_main_window(root, current_user):
    manufacturer_entry_values = {}
    company_entry_values = {}
    retailer_entry_values = {}
    product_entry_values = {}

    def update_db(clickAction):
        global message
        active_frame = None
        entry_ids = []
        entry_values = {}
        if manufacturer_frame.winfo_ismapped():
            active_frame = manufacturer_frame
            entry_values = manufacturer_entry_values
            entry_ids = ["manufacturer_id", "manufacturer_address", "manufacturer_name", "manufacturer_contact"]
        elif company_frame.winfo_ismapped():
            active_frame = company_frame
            entry_values = company_entry_values
            entry_ids = ["company_id", "company_name", "company_address", "company_contact"]
        elif retailer_frame.winfo_ismapped():
            active_frame = retailer_frame
            entry_values = retailer_entry_values
            entry_ids = ["retailer_id", "retailer_name", "retailer_address", "retailer_contact", "retailer_company_id"]
        elif product_frame.winfo_ismapped():
            active_frame = product_frame
            entry_values = product_entry_values
            entry_ids = ["product_id", "product_name", "stock", "product_price", "product_manufacturer_id",
                         "product_retailer_id"]

        success = False
        if clickAction == "ADD":
            for entry_id in entry_ids:
                entry_widget = entry_values.get(entry_id)
                if entry_widget.get() == "":
                    Messagebox.show_error("ID field cannot be empty!", "Invalid ID Entry", parent=inv_frame)
                    return
            data = {}
            for entry_id in entry_ids:
                entry_widget = entry_values.get(entry_id)
                data[entry_id] = entry_widget.get()

            if active_frame == manufacturer_frame:
                success, message = SCMS_BackEnd.add_manufacturer_data(**data)
            elif active_frame == company_frame:
                success, message = SCMS_BackEnd.add_company_data(**data)
            elif active_frame == retailer_frame:
                success, message = SCMS_BackEnd.add_retailer_data(**data)
                update_combobox_options(retailer_frame, entry_values,
                                        retailer_treeview)
            elif active_frame == product_frame:
                success, message = SCMS_BackEnd.add_product_data(**data)
                update_combobox_options(product_frame, entry_values,
                                        product_treeview)
            if success:
                Messagebox.show_info("Entry was added successfully.", "Entry Added", parent=inv_frame)

                if active_frame == manufacturer_frame:
                    manufacturer_data = SCMS_BackEnd.fetch_manufacturer_data()
                    update_treeview(manufacturer_treeview,
                                    data=manufacturer_data)
                elif active_frame == company_frame:
                    company_data = SCMS_BackEnd.fetch_company_data()
                    update_treeview(company_treeview,
                                    data=company_data)
                elif active_frame == retailer_frame:
                    retailer_data = SCMS_BackEnd.fetch_retailer_data()
                    update_treeview(retailer_treeview,
                                    data=retailer_data)

                elif active_frame == product_frame:
                    product_data = SCMS_BackEnd.fetch_product_data()
                    update_treeview(product_treeview,
                                    data=product_data)
            else:
                Messagebox.show_error(message, "Entry Failed", parent=inv_frame)
        elif clickAction == "UPDATE":
            for entry_id in entry_ids:
                entry_widget = entry_values.get(entry_id)
                if entry_widget.get() == "":
                    Messagebox.show_error("ID field cannot be empty!", "Invalid ID Entry", parent=inv_frame)
                    return
            data = {}
            for entry_id in entry_ids:
                entry_widget = entry_values.get(entry_id)
                data[entry_id] = entry_widget.get()

            if active_frame == manufacturer_frame:
                success, message = SCMS_BackEnd.update_manufacturer_data(**data)
            elif active_frame == company_frame:
                success, message = SCMS_BackEnd.update_company_data(**data)
            elif active_frame == retailer_frame:
                success, message = SCMS_BackEnd.update_retailer_data(**data)
                update_combobox_options(retailer_frame, entry_values,
                                        retailer_treeview)
            elif active_frame == product_frame:
                success, message = SCMS_BackEnd.update_product_data(**data)
                update_combobox_options(product_frame, entry_values,
                                        product_treeview)

            if success:
                Messagebox.show_info("Entry Update Successfully!", "Entry Updated", parent=inv_frame)

                if active_frame == manufacturer_frame:
                    manufacturer_data = SCMS_BackEnd.fetch_manufacturer_data()
                    update_treeview(manufacturer_treeview,
                                    data=manufacturer_data)
                elif active_frame == company_frame:
                    company_data = SCMS_BackEnd.fetch_company_data()
                    update_treeview(company_treeview,
                                    data=company_data)
                elif active_frame == retailer_frame:
                    retailer_data = SCMS_BackEnd.fetch_retailer_data()
                    update_treeview(retailer_treeview,
                                    data=retailer_data)
                elif active_frame == product_frame:
                    product_data = SCMS_BackEnd.fetch_product_data()
                    update_treeview(product_treeview,
                                    data=product_data)

            else:
                Messagebox.show_error(message, "Update Entry Failed", parent=inv_frame)
        elif clickAction == "DELETE":
            for entry_id in entry_ids:
                entry_widget = entry_values.get(entry_id)
                if entry_widget.get() == "":
                    Messagebox.show_error("ID field cannot be empty!", "Invalid ID Entry", parent=inv_frame)
                    return
            delete_id = entry_values.get(entry_ids[0]).get()
            if active_frame == manufacturer_frame:
                success, message = SCMS_BackEnd.delete_manufacturer_data(delete_id)
            elif active_frame == company_frame:
                success, message = SCMS_BackEnd.delete_company_data(delete_id)
            elif active_frame == retailer_frame:
                success, message = SCMS_BackEnd.delete_retailer_data(delete_id)
                update_combobox_options(retailer_frame, entry_values,
                                        retailer_treeview)
            elif active_frame == product_frame:
                success, message = SCMS_BackEnd.delete_product_data(delete_id)
                update_combobox_options(product_frame, entry_values,
                                        product_treeview)

            if success:
                Messagebox.show_info("Entry Deleted!", "Entry Deleted.", parent=inv_frame)
                if active_frame == manufacturer_frame:
                    manufacturer_data = SCMS_BackEnd.fetch_manufacturer_data()
                    update_treeview(manufacturer_treeview,
                                    data=manufacturer_data)
                elif active_frame == company_frame:
                    company_data = SCMS_BackEnd.fetch_company_data()
                    update_treeview(company_treeview,
                                    data=company_data)
                elif active_frame == retailer_frame:
                    retailer_data = SCMS_BackEnd.fetch_retailer_data()
                    update_treeview(retailer_treeview,
                                    data=retailer_data)

                elif active_frame == product_frame:
                    product_data = SCMS_BackEnd.fetch_product_data()
                    update_treeview(product_treeview, data=product_data)
                clear_entries(active_frame)
            else:
                Messagebox.show_error(message, "Failed Deletion", parent=inv_frame)
        elif clickAction == "CLEAR":
            clear_entries(active_frame)

        elif clickAction == "GRAPH":
            if display_graph():
                return

    def update_frame(actions):
        manufacturer_frame.place_forget()
        company_frame.place_forget()
        retailer_frame.place_forget()
        product_frame.place_forget()

        if actions == "Manufacturer":
            manufacturer_frame.place(x=475, y=280, anchor="center")
        elif actions == "Company":
            company_frame.place(x=475, y=280, anchor="center")
        elif actions == "Retailer":
            retailer_frame.place(x=475, y=280, anchor="center")
            update_combobox_options(retailer_frame, retailer_entry_values, retailer_treeview)
        elif actions == "Product":
            product_frame.place(x=475, y=280, anchor="center")
            update_combobox_options(product_frame, product_entry_values,
                                    product_treeview)

    def create_manufacturer_frame(entry_values):
        frame = ttkbs.Frame(entry_frame, style="tabs.TFrame", borderwidth=1)
        ttkbs.Label(frame, text="Manufacturers", style='tabsLabel.Label', font=('Helvetica', 18, 'bold'),
                    ).grid(row=0, column=0, columnspan=7, pady=5)
        ttkbs.Label(frame, text="Manufacturer ID:", style='tabsLabel.Label').grid(row=1, column=0, sticky="e", pady=5,
                                                                                  padx=5)
        entry_values["manufacturer_id"] = ttkbs.Entry(frame)
        entry_values["manufacturer_id"].grid(row=1, column=1, pady=5, padx=5)

        ttkbs.Label(frame, background="#1E5128", text="Manufacturer Address:", style='TLabel').grid(row=1, column=4,
                                                                                                    sticky="e", pady=5,
                                                                                                    padx=5)
        entry_values["manufacturer_address"] = ttkbs.Entry(frame)
        entry_values["manufacturer_address"].grid(row=1, column=5, pady=5, padx=5)

        ttkbs.Label(frame, background="#1E5128", text="Manufacturer Name:", style='TLabel').grid(row=2, column=0,
                                                                                                 sticky="e", pady=5,
                                                                                                 padx=5)
        entry_values["manufacturer_name"] = ttkbs.Entry(frame)
        entry_values["manufacturer_name"].grid(row=2, column=1, pady=5, padx=5)

        ttkbs.Label(frame, background="#1E5128", text="Manufacturer Contact:", style='TLabel').grid(row=2, column=4,
                                                                                                    sticky="e", pady=5,
                                                                                                    padx=5)
        entry_values["manufacturer_contact"] = ttkbs.Entry(frame)
        entry_values["manufacturer_contact"].grid(row=2, column=5, pady=5, padx=5)

        col_data = ["Manufacturer ID", "Manufacturer Name", "Manufacturer Address", "Manufacturer Contact"]
        manufacturer_data = SCMS_BackEnd.fetch_manufacturer_data()
        row_data = manufacturer_data

        manufacturer_treeview = ttkbs.Treeview(frame, columns=col_data, show="headings", selectmode="browse",
                                               style='Treeview')

        manufacturer_treeview.heading("#1", text="Manufacturer ID",
                                      command=lambda: sort_treeview(manufacturer_treeview, "#1", False))
        manufacturer_treeview.heading("#2", text="Manufacturer Name",
                                      command=lambda: sort_treeview(manufacturer_treeview, "#2", False))
        manufacturer_treeview.heading("#3", text="Manufacturer Address",
                                      command=lambda: sort_treeview(manufacturer_treeview, "#3", False))
        manufacturer_treeview.heading("#4", text="Manufacturer Contact",
                                      command=lambda: sort_treeview(manufacturer_treeview, "#4", False))

        for data in col_data:
            manufacturer_treeview.column(data, width=229)

        for row in row_data:
            manufacturer_treeview.insert("", "end", values=row)

        manufacturer_treeview.grid(row=3, column=0, columnspan=7, pady=(10, 0))

        def populate_manufacturer_entry_widgets(event):
            selected_item = manufacturer_treeview.selection()

            if selected_item:
                values_tuple = manufacturer_treeview.item(selected_item, 'values')

                if len(values_tuple) == 4:
                    manufacturer_id, manufacturer_name, manufacturer_address, manufacturer_contact = values_tuple

                    entry_values["manufacturer_id"].delete(0, "end")
                    entry_values["manufacturer_id"].insert(0, manufacturer_id)
                    entry_values["manufacturer_name"].delete(0, "end")
                    entry_values["manufacturer_name"].insert(0, manufacturer_name)
                    entry_values["manufacturer_address"].delete(0, "end")
                    entry_values["manufacturer_address"].insert(0, manufacturer_address)
                    entry_values["manufacturer_contact"].delete(0, "end")
                    entry_values["manufacturer_contact"].insert(0, manufacturer_contact)

        manufacturer_treeview.bind("<<TreeviewSelect>>", populate_manufacturer_entry_widgets)

        def update_search_results(event):
            category = search_menu_var.get()
            query = search_entry.get().lower()
            search_menu["text"] = category

            manufacturer_treeview.delete(*manufacturer_treeview.get_children())
            for row in row_data:
                if category == "Manufacturer ID":
                    if query in row[0].lower():
                        manufacturer_treeview.insert("", "end", values=row)
                elif category == "Manufacturer Name":
                    if query in row[1].lower():
                        manufacturer_treeview.insert("", "end", values=row)
                elif category == "Manufacturer Address":
                    if query in row[2].lower():
                        manufacturer_treeview.insert("", "end", values=row)
                elif category == "Manufacturer Contact":
                    if query in row[3].lower():
                        manufacturer_treeview.insert("", "end", values=row)

        ttkbs.Label(frame, text="Search:", style="TLabel", background="#1E5128").grid(row=4, columnspan=7, pady=10,
                                                                                      sticky='n')
        search_menu_var = tk.StringVar()
        search_menu_var.set("Category")
        search_menu = ttkbs.Menubutton(frame, textvariable=search_menu_var, width=20)
        search_menu.place(x=630, y=429, anchor='center')
        search_menu.menu = tk.Menu(search_menu, tearoff=0)
        search_menu["menu"] = search_menu.menu

        for category in col_data:
            search_menu.menu.add_radiobutton(label=category, variable=search_menu_var, value=category)

        search_entry = ttkbs.Entry(frame)
        search_entry.place(x=800, y=429, anchor='center')
        search_entry.bind("<KeyRelease>", update_search_results)

        return frame, manufacturer_treeview

    def create_company_frame(entry_values):
        frame = ttkbs.Frame(entry_frame, style="tabs.TFrame", borderwidth=1)
        ttkbs.Label(frame, text="Company", style='tabsLabel.Label', font=('Helvetica', 18, 'bold'),
                    justify="center").grid(row=0, column=0, columnspan=7, pady=5)
        ttkbs.Label(frame, text="Company ID:", style='tabsLabel.Label').grid(row=1, column=0, sticky="e", pady=5,
                                                                             padx=5)
        entry_values["company_id"] = ttkbs.Entry(frame)
        entry_values["company_id"].grid(row=1, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Company Name:", style='tabsLabel.Label').grid(row=2, column=0, sticky="e", pady=5,
                                                                               padx=5)
        entry_values["company_name"] = ttkbs.Entry(frame)
        entry_values["company_name"].grid(row=2, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Company Address:", style='tabsLabel.Label').grid(row=1, column=4, sticky="e", pady=5,
                                                                                  padx=5)
        entry_values["company_address"] = ttkbs.Entry(frame)
        entry_values["company_address"].grid(row=1, column=5, pady=5, padx=5)

        ttkbs.Label(frame, text="Company Contact:", style='tabsLabel.Label').grid(row=2, column=4, sticky="e", pady=5,
                                                                                  padx=5)
        entry_values["company_contact"] = ttkbs.Entry(frame)
        entry_values["company_contact"].grid(row=2, column=5, pady=5, padx=5)

        col_data = ["Company ID", "Company Name", "Company Address", "Company Contact"]
        company_data = SCMS_BackEnd.fetch_company_data()
        row_data = company_data

        company_treeview = ttkbs.Treeview(frame, columns=col_data, show="headings", selectmode="browse",
                                          style='Treeview')

        company_treeview.heading("#1", text="Company ID", command=lambda: sort_treeview(company_treeview, "#1", False))
        company_treeview.heading("#2", text="Company Name",
                                 command=lambda: sort_treeview(company_treeview, "#2", False))
        company_treeview.heading("#3", text="Company Address",
                                 command=lambda: sort_treeview(company_treeview, "#3", False))
        company_treeview.heading("#4", text="Company Contact",
                                 command=lambda: sort_treeview(company_treeview, "#4", False))

        for data in col_data:
            company_treeview.column(data, width=229)

        for row in row_data:
            company_treeview.insert("", "end", values=row)

        company_treeview.grid(row=3, column=0, columnspan=7, pady=(10, 0))

        def populate_company_entry_widgets(event):
            selected_item = company_treeview.selection()
            if selected_item:
                values_tuple = company_treeview.item(selected_item, 'values')
                if len(values_tuple) == 4:
                    company_id, company_name, company_address, company_contact = values_tuple
                    entry_values["company_id"].delete(0, "end")
                    entry_values["company_id"].insert(0, company_id)
                    entry_values["company_name"].delete(0, "end")
                    entry_values["company_name"].insert(0, company_name)
                    entry_values["company_address"].delete(0, "end")
                    entry_values["company_address"].insert(0, company_address)
                    entry_values["company_contact"].delete(0, "end")
                    entry_values["company_contact"].insert(0, company_contact)

        company_treeview.bind("<<TreeviewSelect>>", populate_company_entry_widgets)

        def update_search_results(event):
            category = search_menu_var.get()
            query = search_entry.get().lower()
            search_menu["text"] = category
            company_treeview.delete(*company_treeview.get_children())
            for row in row_data:
                if category == "Company ID" and query in row[0].lower():
                    company_treeview.insert("", "end", values=row)
                elif category == "Company Name" and query in row[1].lower():
                    company_treeview.insert("", "end", values=row)
                elif category == "Company Address" and query in row[2].lower():
                    company_treeview.insert("", "end", values=row)
                elif category == "Company Contact" and query in row[3].lower():
                    company_treeview.insert("", "end", values=row)

        ttkbs.Label(frame, text="Search:", style="TLabel", background="#1E5128").grid(row=4, columnspan=7, pady=10,
                                                                                      sticky='n')
        search_menu_var = tk.StringVar()
        search_menu_var.set("Category")
        search_menu = ttkbs.Menubutton(frame, textvariable=search_menu_var, width=20)
        search_menu.place(x=630, y=429, anchor='center')
        search_menu.menu = tk.Menu(search_menu, tearoff=0)
        search_menu["menu"] = search_menu.menu

        for category in col_data:
            search_menu.menu.add_radiobutton(label=category, variable=search_menu_var, value=category)

        search_entry = ttkbs.Entry(frame)
        search_entry.place(x=800, y=429, anchor='center')
        search_entry.bind("<KeyRelease>", update_search_results)

        return frame, company_treeview

    def create_retailer_frame(entry_values):
        frame = ttkbs.Frame(entry_frame, style="tabs.TFrame")
        ttkbs.Label(frame, text="Retailer", style='tabsLabel.Label', font=('Helvetica', 18, 'bold')).grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=6,
                                                                                                          pady=5,
                                                                                                          sticky="n")

        ttkbs.Label(frame, text="Retailer ID:", style='tabsLabel.Label').grid(row=1, column=0, sticky="e", pady=5,
                                                                              padx=5)
        entry_values["retailer_id"] = ttkbs.Entry(frame)
        entry_values["retailer_id"].grid(row=1, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Retailer Name:", style='tabsLabel.Label').grid(row=2, column=0, sticky="e", pady=5,
                                                                                padx=5)
        entry_values["retailer_name"] = ttkbs.Entry(frame)
        entry_values["retailer_name"].grid(row=2, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Retailer Address:", style='tabsLabel.Label').grid(row=1, column=2, sticky="e", pady=5,
                                                                                   padx=5)
        entry_values["retailer_address"] = ttkbs.Entry(frame)
        entry_values["retailer_address"].grid(row=1, column=3, pady=5, padx=5)

        ttkbs.Label(frame, text="Retailer Contact:", style='tabsLabel.Label').grid(row=2, column=2, sticky="e", pady=5,
                                                                                   padx=5)
        entry_values["retailer_contact"] = ttkbs.Entry(frame)
        entry_values["retailer_contact"].grid(row=2, column=3, pady=5, padx=5)

        ttkbs.Label(frame, text="Company ID:", style='tabsLabel.Label').grid(row=1, column=4, sticky="e", pady=5,
                                                                             padx=5)
        company_ids = SCMS_BackEnd.fetch_company_ids()
        entry_values["retailer_company_id"] = ttkbs.Combobox(frame, values=company_ids)
        entry_values["retailer_company_id"].grid(row=1, column=5, pady=5, padx=5)

        col_data = ["Retailer ID", "Retailer Name", "Retailer Address", "Retailer Contact", "Company ID"]
        retailer_data = SCMS_BackEnd.fetch_retailer_data()
        row_data = retailer_data

        retailer_treeview = ttkbs.Treeview(frame, columns=col_data, show="headings", selectmode="browse",
                                           style='Treeview')

        retailer_treeview.heading("#1", text="Retailer ID",
                                  command=lambda: sort_treeview(retailer_treeview, "#1", False))
        retailer_treeview.heading("#2", text="Retailer Name",
                                  command=lambda: sort_treeview(retailer_treeview, "#2", False))
        retailer_treeview.heading("#3", text="Retailer Address",
                                  command=lambda: sort_treeview(retailer_treeview, "#3", False))
        retailer_treeview.heading("#4", text="Retailer Contact",
                                  command=lambda: sort_treeview(retailer_treeview, "#4", False))
        retailer_treeview.heading("#5", text="Company ID",
                                  command=lambda: sort_treeview(retailer_treeview, "#5", False))

        for data in col_data:
            retailer_treeview.column(data, width=183)

        for row in row_data:
            retailer_treeview.insert("", "end", values=row)

        retailer_treeview.grid(row=4, column=0, columnspan=6, pady=(10, 0))

        def populate_retailer_entry_widgets(event):
            selected_item = retailer_treeview.selection()

            if selected_item:
                values_tuple = retailer_treeview.item(selected_item, 'values')

                if len(values_tuple) == 5:
                    retailer_id, retailer_name, retailer_address, retailer_contact, retailer_company_id = values_tuple
                    entry_values["retailer_id"].delete(0, "end")
                    entry_values["retailer_id"].insert(0, retailer_id)
                    entry_values["retailer_name"].delete(0, "end")
                    entry_values["retailer_name"].insert(0, retailer_name)
                    entry_values["retailer_address"].delete(0, "end")
                    entry_values["retailer_address"].insert(0, retailer_address)
                    entry_values["retailer_contact"].delete(0, "end")
                    entry_values["retailer_contact"].insert(0, retailer_contact)
                    entry_values["retailer_company_id"].set(retailer_company_id)

        retailer_treeview.bind("<<TreeviewSelect>>", populate_retailer_entry_widgets)

        def update_search_results(event):
            category = search_menu_var.get()
            query = search_entry.get().lower()

            search_menu["text"] = category
            retailer_treeview.delete(*retailer_treeview.get_children())
            for row in row_data:
                if category == "Retailer ID":
                    if query in row[0].lower():
                        retailer_treeview.insert("", "end", values=row)
                elif category == "Retailer Name":
                    if query in row[1].lower():
                        retailer_treeview.insert("", "end", values=row)
                elif category == "Retailer Address":
                    if query in row[2].lower():
                        retailer_treeview.insert("", "end", values=row)
                elif category == "Retailer Contact":
                    if query in row[3].lower():
                        retailer_treeview.insert("", "end", values=row)
                elif category == "Company ID":
                    if query in row[4].lower():
                        retailer_treeview.insert("", "end", values=row)

        ttkbs.Label(frame, text="Search:", style="TLabel", background="#1E5128").grid(row=5, columnspan=7, pady=10,
                                                                                      sticky='n')
        search_menu_var = tk.StringVar()
        search_menu_var.set("Category")
        search_menu = ttkbs.Menubutton(frame, textvariable=search_menu_var, width=20)
        search_menu.place(x=630, y=429, anchor='center')
        search_menu.menu = tk.Menu(search_menu, tearoff=0)
        search_menu["menu"] = search_menu.menu

        for category in col_data:
            search_menu.menu.add_radiobutton(label=category, variable=search_menu_var, value=category)

        search_entry = ttkbs.Entry(frame)
        search_entry.place(x=800, y=429, anchor='center')
        search_entry.bind("<KeyRelease>", update_search_results)

        return frame, retailer_treeview

    def create_product_frame(entry_values):
        frame = ttkbs.Frame(entry_frame, style="tabs.TFrame")
        ttkbs.Label(frame, style='tabsLabel.Label', text="Product", font=('Helvetica', 18, 'bold')).grid(row=0,
                                                                                                         column=0,
                                                                                                         columnspan=7,
                                                                                                         sticky="n",
                                                                                                         pady=5)

        ttkbs.Label(frame, text="Product ID:", style='tabsLabel.Label').grid(row=1, column=0, sticky="e", pady=5,
                                                                             padx=5)
        entry_values["product_id"] = ttkbs.Entry(frame)
        entry_values["product_id"].grid(row=1, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Product Name:", style='tabsLabel.Label').grid(row=2, column=0, sticky="e", pady=5,
                                                                               padx=5)
        entry_values["product_name"] = ttkbs.Entry(frame)
        entry_values["product_name"].grid(row=2, column=1, pady=5, padx=5)

        ttkbs.Label(frame, text="Stock:", style='tabsLabel.Label').grid(row=1, column=2, sticky="e", pady=5,
                                                                        padx=5)
        entry_values["stock"] = ttkbs.Spinbox(frame, from_=1, to=100, width=16)
        entry_values["stock"].grid(row=1, column=3, pady=5, padx=5)

        ttkbs.Label(frame, text="Product Price:", style='tabsLabel.Label').grid(row=2, column=2, sticky="e", pady=5,
                                                                                padx=5)
        entry_values["product_price"] = ttkbs.Entry(frame)
        entry_values["product_price"].grid(row=2, column=3, pady=5, padx=5)

        ttkbs.Label(frame, text="Manufacturer ID:", style='tabsLabel.Label').grid(row=1, column=4, sticky="e", pady=5,
                                                                                  padx=5)
        manufacturer_ids = SCMS_BackEnd.fetch_manufacturer_ids()
        entry_values["product_manufacturer_id"] = ttkbs.Combobox(frame, values=manufacturer_ids)
        entry_values["product_manufacturer_id"].grid(row=1, column=5, pady=5, padx=5)

        ttkbs.Label(frame, text="Retailer ID:", style='tabsLabel.Label').grid(row=2, column=4, sticky="e", pady=5,
                                                                              padx=5)
        retailer_ids = SCMS_BackEnd.fetch_retailer_ids()
        entry_values["product_retailer_id"] = ttkbs.Combobox(frame, values=retailer_ids)
        entry_values["product_retailer_id"].grid(row=2, column=5, pady=5, padx=5)

        col_data = ["Product ID", "Product Name", "Stock", "Product Price", "Manufacturer ID", "Retailer ID"]
        product_data = SCMS_BackEnd.fetch_product_data()
        row_data = product_data

        product_treeview = ttkbs.Treeview(frame, columns=col_data, show="headings", selectmode="browse",
                                          style='Treeview')

        product_treeview.heading("#1", text="Product ID", command=lambda: sort_treeview(product_treeview, "#1", False))
        product_treeview.heading("#2", text="Product Name",
                                 command=lambda: sort_treeview(product_treeview, "#2", False))
        product_treeview.heading("#3", text="Stock",
                                 command=lambda: sort_treeview(product_treeview, "#3", False))
        product_treeview.heading("#4", text="Product Price",
                                 command=lambda: sort_treeview(product_treeview, "#4", False))
        product_treeview.heading("#5", text="Manufacturer ID",
                                 command=lambda: sort_treeview(product_treeview, "#5", False))
        product_treeview.heading("#6", text="Retailer ID", command=lambda: sort_treeview(product_treeview, "#6", False))

        for data in col_data:
            product_treeview.column(data, width=153)

        for row in row_data:
            product_treeview.insert("", "end", values=row)

        product_treeview.grid(row=4, column=0, columnspan=7, pady=(10, 0))

        def populate_product_entry_widgets(event):
            selected_item = product_treeview.selection()

            if selected_item:
                values_tuple = product_treeview.item(selected_item, 'values')

                if len(values_tuple) == 6:
                    product_id, product_name, stock, product_price, product_manufacturer_id, product_retailer_id = values_tuple
                    entry_values["product_id"].delete(0, "end")
                    entry_values["product_id"].insert(0, product_id)
                    entry_values["product_name"].delete(0, "end")
                    entry_values["product_name"].insert(0, product_name)
                    entry_values["stock"].set(stock)
                    entry_values["product_price"].delete(0, "end")
                    entry_values["product_price"].insert(0, product_price)
                    entry_values["product_manufacturer_id"].set(product_manufacturer_id)
                    entry_values["product_retailer_id"].set(product_retailer_id)

        product_treeview.bind("<<TreeviewSelect>>", populate_product_entry_widgets)

        def update_search_results():
            category = search_menu_var.get()
            query = search_entry.get().lower()
            search_menu["text"] = category

            product_treeview.delete(*product_treeview.get_children())

            for row in row_data:
                if category == "Product ID":
                    if query in row[0].lower():
                        product_treeview.insert("", "end", values=row)
                elif category == "Product Name":
                    if query in row[1].lower():
                        product_treeview.insert("", "end", values=row)
                elif category == "Stock":
                    if query in row[2].lower():
                        product_treeview.insert("", "end", values=row)
                elif category == "Product Price":
                    if query in row[3].lower():
                        product_treeview.insert("", "end", values=row)
                elif category == "Manufacturer ID":
                    if query in row[4].lower():
                        product_treeview.insert("", "end", values=row)
                elif category == "Retailer ID":
                    if query in row[5].lower():
                        product_treeview.insert("", "end", values=row)

        ttkbs.Label(frame, text="Search:", style="TLabel", background="#1E5128").grid(row=5, columnspan=7, pady=10,
                                                                                      sticky='n')
        search_menu_var = tk.StringVar()
        search_menu_var.set("Category")
        search_menu = ttkbs.Menubutton(frame, textvariable=search_menu_var, width=20)
        search_menu.place(x=630, y=429, anchor='center')
        search_menu.menu = tk.Menu(search_menu, tearoff=0)
        search_menu["menu"] = search_menu.menu

        for category in col_data:
            search_menu.menu.add_radiobutton(label=category, variable=search_menu_var, value=category)

        search_entry = ttkbs.Entry(frame)
        search_entry.place(x=800, y=429, anchor='center')
        search_entry.bind("<KeyRelease>", update_search_results)

        scan_barcode_button = ttkbs.Button(frame, text="Scan Barcode", command=scan_barcode)
        scan_barcode_button.place(x=200, y=429, anchor='center')

        return frame, product_treeview

    def update_combobox_options(frame, entry_values, treeview):
        active_frame = frame

        if active_frame == retailer_frame:
            company_ids = SCMS_BackEnd.fetch_company_ids()

            if "retailer_company_id" in entry_values:
                entry_values["retailer_company_id"].destroy()
            entry_values["retailer_company_id"] = ttkbs.Combobox(frame, values=company_ids)
            entry_values["retailer_company_id"].grid(row=1, column=5, pady=5, padx=5)

        elif active_frame == product_frame:
            retailer_ids = SCMS_BackEnd.fetch_retailer_ids()
            manufacturer_ids = SCMS_BackEnd.fetch_manufacturer_ids()

            if "product_manufacturer_id" in entry_values:
                entry_values["product_manufacturer_id"].destroy()
            entry_values["product_manufacturer_id"] = ttkbs.Combobox(frame, values=manufacturer_ids)
            entry_values["product_manufacturer_id"].grid(row=1, column=5, pady=5, padx=5)
            if "product_retailer_id" in entry_values:
                entry_values["product_retailer_id"].destroy()
            entry_values["product_retailer_id"] = ttkbs.Combobox(frame, values=retailer_ids)
            entry_values["product_retailer_id"].grid(row=2, column=5, pady=5, padx=5)

            product_data = SCMS_BackEnd.fetch_product_data()
            update_treeview(treeview, data=product_data)

    def scan_barcode(window_width=300, window_height=250, timeout_seconds=30):
        cap = cv2.VideoCapture(0) #default cam
        barcode_scanned = False
        start_time = time.time()

        while not barcode_scanned and (time.time() - start_time) < timeout_seconds:
            _, frame = cap.read()
            frame = cv2.resize(frame, (window_width, window_height))
            cv2.putText(frame, "Scan Barcode here", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.imshow("Barcode Scanner", frame)
            #decode scanned barcode
            barcodes = decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                print(f"Scanned Barcode: {barcode_data}")

                select_product_by_barcode(barcode_data)
                barcode_scanned = True  #exit loop when true

            key = cv2.waitKey(1)
            if key == 8:
                break

        cap.release()
        cv2.destroyAllWindows()

        if not barcode_scanned:
            threading.Thread(target=show_info_message,
                             args=("Barcode Scan Timeout", "Barcode not found within the timeout period.")).start()

    def select_product_by_barcode(scanned_product_id):
        barcode_found = False

        for item in product_treeview.get_children():
            values = product_treeview.item(item, 'values')
            if values and values[0].lower() == scanned_product_id.lower():
                product_treeview.selection_set(item)
                barcode_found = True
            else:
                product_treeview.selection_remove(item)

        if not barcode_found:
            threading.Thread(target=show_info_message, args=(
                "Barcode not found", f"The barcode '{scanned_product_id}' is not found in the database.")).start()

    def show_info_message(title, message):
        messagebox.showinfo(title, message)

    def clear_entries(frame):
        for widget in frame.winfo_children():
            if isinstance(widget, ttkbs.Entry):
                widget.delete(0, "end")

    def sort_treeview(tree, col, reverse):
        data = [(tree.set(item, col), item) for item in tree.get_children()]

        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            tree.move(item[1], "", index)

        tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))

    def update_treeview(treeview, data):
        for item in treeview.get_children():
            treeview.delete(item)

        for row in data:
            treeview.insert("", "end", values=row)

    def display_graph():
        try:
            product_data = SCMS_BackEnd.fetch_product_data()

            if not product_data:
                Messagebox.show_warning("No data available for plotting.", "No Data", parent=inv_frame)
                return False

            product_names = [item[1] for item in product_data]
            stock_values = [item[2] for item in product_data]

            cmap = plt.get_cmap('viridis', len(product_names))

            plt.bar(product_names, stock_values, color=[cmap(i) for i in range(len(product_names))])

            plt.xlabel('Product Name')
            plt.ylabel('Stock')
            plt.title('Product Stock Levels')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()

            plt.show()

            return True

        except Exception as e:
            print(f"Error: {e}")
            Messagebox.show_error("Error occurred while plotting.", "Plotting Error", parent=inv_frame)
            return False

        except Exception as e:
            print(f"Error: {e}")
            Messagebox.show_error("Error occurred while plotting.", "Plotting Error", parent=inv_frame)
            return False

    def update_status_bar():
        if current_user is not None:
            user_info = f"User | {current_user}"
        else:
            user_info = "Guest"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text.set(f"{user_info}\nDate & Time | {current_time}\n_____________________________")
        main_window.after(1000, update_status_bar)

    main_window = ttkbs.Toplevel(root)
    main_window.title("Supply Chain Management System")
    main_window.iconphoto(False, tk.PhotoImage(file="images/supply_icon.png"))
    main_window_width = 1200
    main_window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    main_x = (screen_width - main_window_width) // 2
    main_y = (screen_height - main_window_height) // 2

    main_window.geometry(f"{main_window_width}x{main_window_height}+{main_x}+{main_y}")
    main_window.resizable(False, False)

    label = ttkbs.Label(main_window, text="SUPPLY CHAIN MANAGEMENT SYSTEM", font=('Consolas', 18, 'bold'),
                        background="#4E9F3D", anchor="center")
    label.pack(side="top", fill="x")

    inv_frame = Frame(main_window)
    inv_frame.place(x=425, y=200)
    ttkbs.Style().configure('tabs.TFrame', background="#1E5128", bordercolor="#4E9F3D", relief="solid")
    ttkbs.Style().configure('tabsLabel.Label', background="#1E5128")
    ttkbs.Style().configure('button.TFrame', background="#1E5128")
    ttkbs.Style().configure("Treeview.Heading", background="#4E9F3D", foreground="white")
    ttkbs.Style().configure("Treeview", rowheight=25, rowwidth=100, anchor='center')

    entry_frame = ttkbs.Frame(main_window, width=1200, height=600)
    entry_frame.place_configure(x=25, y=50)

    manufacturer_frame, manufacturer_treeview = create_manufacturer_frame(manufacturer_entry_values)
    company_frame, company_treeview = create_company_frame(company_entry_values)
    retailer_frame, retailer_treeview = create_retailer_frame(retailer_entry_values)
    product_frame, product_treeview = create_product_frame(product_entry_values)

    query_tabs = ttkbs.Frame(main_window, width=400, height=500, )
    query_tabs.place(x=500, y=60, anchor="n")

    update_frame("Manufacturer")
    addActions = ["Manufacturer", "Company", "Retailer", "Product"]

    # icons
    add_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/add.png'))
    del_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/delete.png'))
    upd_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/update.png'))
    clr_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/clear.png'))
    graph_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/graph.png'))
    manu_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/manufacturer.png'))
    comp_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/company.png'))
    ret_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/retailer.png'))
    prd_ico = ctk.CTkImage(ttkbs.Image.open(fp='images/product.png'))
    for addAction in addActions:
        button = ctk.CTkButton(query_tabs, text=addAction, command=lambda a=addAction: update_frame(a))
        button.grid(row=0, column=addActions.index(addAction), padx=5)
        if addAction == "Manufacturer":
            button.configure(image=manu_ico, compound='right', anchor='n',
                             fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)
        elif addAction == "Company":
            button.configure(image=comp_ico, compound='right', anchor='n',
                             fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)
        elif addAction == "Retailer":
            button.configure(image=ret_ico, compound='right', anchor='n',
                             fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)
        elif addAction == "Product":
            button.configure(image=prd_ico, compound='right', anchor='n',
                             fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)

    button_frame = ttkbs.Frame(main_window, style='button.TFrame')
    button_frame.pack(side="right", fill="y")
    profile_picture_path = SCMS_BackEnd.get_profile_picture_path(current_user)
    pil_image = Image.open(profile_picture_path)

    pil_image = pil_image.resize((120, 120))

    pil_image = pil_image.convert("RGBA")
    mask = Image.new("L", pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 120, 120), fill=255)
    pil_image.putalpha(mask)

    profile_image = ImageTk.PhotoImage(pil_image)

    profile_label = ttkbs.Label(button_frame, image=profile_image, background="#1E5128")
    profile_label.image = profile_image
    profile_label.pack(side='top', pady=(20, 0))

    status_text = tk.StringVar()
    status_bar = ttkbs.Label(button_frame, font=('Helvetica', 8, 'bold'), textvariable=status_text,
                             background="#1E5128",
                             justify='center')
    status_bar.place(x=5, y=150)

    update_status_bar()
    clickActions = ["ADD", "UPDATE", "DELETE", "CLEAR", "GRAPH", "LOGOUT"]
    for action in clickActions:
        if action == "ADD" or action == "UPDATE" or action == "DELETE" or action == "CLEAR":
            button = ctk.CTkButton(button_frame, text=action, command=lambda a=action: update_db(a))
            button.pack(side="top", fill="x")
            button.configure(bg_color='#1E5128', fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)
            if action == "ADD":
                button.pack(side="top", pady=(75, 5), padx=25)
                button.configure(image=add_ico, compound='right', anchor='center')
            if action == "UPDATE":
                button.pack(side="top", pady=(0, 5), padx=25)
                button.configure(image=upd_ico, compound='right', anchor='center')
            if action == "DELETE":
                button.pack(side="top", pady=(0, 5), padx=25)
                button.configure(image=del_ico, compound='right', anchor='center')
            if action == "CLEAR":
                button.pack(side="top", pady=(0, 5), padx=25)
                button.configure(image=clr_ico, compound='right', anchor='center')

        elif action == "GRAPH":
            graph_button = ctk.CTkButton(button_frame, text=action, command=lambda a=action: update_db(a))
            graph_button.configure(image=graph_ico, compound='right', anchor='center',
                                   bg_color='#1E5128', fg_color='#4e9f3d', hover_color='#004300', corner_radius=5)
            graph_button.pack(side="top", pady=(50, 5), padx=25)


        elif action == "LOGOUT":
            logout_button = ctk.CTkButton(button_frame, text=action, command=lambda: logout(main_window))
            logout_button.configure(width=5, bg_color='#1E5128', fg_color='#4e9f3d', hover_color='#004300',
                                    corner_radius=5)
            logout_button.place(x=120, y=575)

    def logout(main_window):
        if hasattr(main_window, 'current_user'):
            main_window.current_user = None
        choice = Messagebox.okcancel("Are you sure you want to log out?", "Logout Confirmation",
                                     buttons=['Cancel:secondary', 'Ok:primary'], alert=True, parent=inv_frame)
        if choice == "Ok":
            main_window.withdraw()
            logi_sync.deiconify()


if __name__ == "__main__":
    SCMS_BackEnd.check_and_create_database()
    logi_sync = Tk()
    app = LOGISYNC(logi_sync)
    logi_sync.mainloop()
