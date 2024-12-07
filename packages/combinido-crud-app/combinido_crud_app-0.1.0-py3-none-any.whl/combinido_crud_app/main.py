import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog

import csv
import sqlite3

# Class for database initialization
class Database:
    def __init__(self, db_name="users2.db"):
        self.db_name = db_name
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                address TEXT
            )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_user(self, name, email, phone, address):
        try:
            query = "INSERT INTO users (name, email, phone, address) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (name, email, phone, address))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_user(self, user_id, name, email, phone, address):
        query = "UPDATE users SET name = ?, email = ?, phone = ?, address = ? WHERE id = ?"
        self.cursor.execute(query, (name, email, phone, address, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def search_users(self, search_term):
        query = "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?"
        self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        return self.cursor.fetchall()

    def get_all_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# Class to initialize user data constructor
class User:
    def __init__(self, user_id=None, name="", email="", phone="", address=""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def __str__(self):
        return f"ID: {self.user_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}, Address: {self.address}"

# Class for the user interface logic using TTKINter
class UserInterface:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        self.root.title("Simple Python CRUD System")
        self.root.geometry("800x600")

        # Text field variables
        self.id_var = ttk.StringVar()
        self.name_var = ttk.StringVar()
        self.email_var = ttk.StringVar()
        self.phone_var = ttk.StringVar()
        self.address_var = ttk.StringVar()
        self.search_var = ttk.StringVar()

        self.build_ui()

    def build_ui(self):
        frame_top = ttk.Frame(self.root, padding=20)
        frame_top.pack(fill=X)

        # Text fields
        ttk.Label(frame_top, text="ID").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(frame_top, textvariable=self.id_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="Name").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(frame_top, textvariable=self.name_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="Email").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(frame_top, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_top, text="Phone").grid(row=1, column=2, padx=5, pady=5)
        ttk.Entry(frame_top, textvariable=self.phone_var).grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_top, text="Address").grid(row=2, column=2, padx=5, pady=5)
        ttk.Entry(frame_top, textvariable=self.address_var).grid(row=2, column=3, padx=5, pady=5)

        # Buttons
        ttk.Button(frame_top, text="Add", bootstyle=SUCCESS, command=self.add_user).grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        ttk.Button(frame_top, text="Update", bootstyle=INFO, command=self.update_user).grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(frame_top, text="Delete", bootstyle=DANGER, command=self.delete_user).grid(row=3, column=2, padx=5, pady=10, sticky="ew")
        ttk.Button(frame_top, text="Export", bootstyle=SECONDARY, command=self.export_to_csv).grid(row=3, column=3, padx=5, pady=10, sticky="ew")
        ttk.Button(frame_top, text="Clear", bootstyle=SECONDARY, command=self.clear_fields).grid(row=3, column=4, padx=5, pady=10, sticky="ew")

        # Search bar
        frame_search = ttk.Frame(self.root, padding=10)
        frame_search.pack(fill=X)

        ttk.Entry(frame_search, textvariable=self.search_var, width=50).pack(side=LEFT, padx=5)
        ttk.Button(frame_search, text="Search", bootstyle=PRIMARY, command=self.search_users).pack(side=LEFT, padx=5)

        label_table = ttk.Label(self.root, text="User List", font=("Arial", 12, "bold"))
        label_table.pack(pady=5)

        # Table
        columns = ("ID", "Name", "Email", "Phone Number", "Address")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_user)

        self.load_users()

    # CRUD Functionalities 
    def add_user(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not email or not phone or not address:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        success = self.db.add_user(name, email, phone, address)
        if success:
            messagebox.showinfo("Success", "User added successfully!")
            self.clear_fields()
            self.load_users()
        else:
            messagebox.showerror("Error", "Email already exists!")

    def update_user(self):
        user_id = self.id_var.get()
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address.get().strip()

        if not name or not email or not phone or not address:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        self.db.update_user(user_id, name, email, phone, address)
        messagebox.showinfo("Success", "User updated successfully!")
        self.clear_fields()
        self.load_users()

    def delete_user(self):
        user_id = self.id_var.get()
        if not user_id:
            messagebox.showwarning("Input Error", "Please select a user to delete!")
            return
        self.db.delete_user(user_id)
        messagebox.showinfo("Success", "User deleted successfully!")
        self.clear_fields()
        self.load_users()

    def search_users(self):
        search_term = self.search_var.get().strip()
        users = self.db.search_users(search_term)
        self.update_treeview(users)

    def load_users(self):
        users = self.db.get_all_users()
        self.update_treeview(users)

    def update_treeview(self, users):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for user in users:
            self.tree.insert("", ttk.END, values=user)

    def select_user(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item)["values"]
            self.id_var.set(item_data[0])
            self.name_var.set(item_data[1])
            self.email_var.set(item_data[2])
            self.phone_var.set(item_data[3])
            self.address_var.set(item_data[4])

    def clear_fields(self):
        self.id_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.search_var.set("")

    # Export data as CSV
    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        users = self.db.get_all_users()
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email"])
                writer.writerows(users)
            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    db = Database()
    root = ttk.Window(themename="solar")
    app = UserInterface(root, db)
    root.mainloop()

    db.close()


if __name__ == "__main__":
    main()
