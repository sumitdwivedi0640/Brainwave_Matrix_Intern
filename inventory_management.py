import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# File paths
USER_FILE = 'data/users.json'
PRODUCT_FILE = 'data/products.json'

# Load and save functions


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# User authentication


def authenticate(username, password):
    users = load_json(USER_FILE)
    return users.get(username) == password

# Product management


def add_product(product_id, name, quantity, price):
    products = load_json(PRODUCT_FILE)
    products[product_id] = {
        'name': name,
        'quantity': quantity,
        'price': price
    }
    save_json(PRODUCT_FILE, products)


def edit_product(product_id, name, quantity, price):
    products = load_json(PRODUCT_FILE)
    if product_id in products:
        products[product_id] = {
            'name': name,
            'quantity': quantity,
            'price': price
        }
        save_json(PRODUCT_FILE, products)
    else:
        return "Product not found."


def delete_product(product_id):
    products = load_json(PRODUCT_FILE)
    if product_id in products:
        del products[product_id]
        save_json(PRODUCT_FILE, products)
    else:
        return "Product not found."


def get_product(product_id):
    products = load_json(PRODUCT_FILE)
    return products.get(product_id)


def list_products():
    products = load_json(PRODUCT_FILE)
    return products


def low_stock_alert(threshold):
    products = load_json(PRODUCT_FILE)
    low_stock = {pid: details for pid, details in products.items()
                 if details['quantity'] < threshold}
    return low_stock


def sales_summary():
    products = load_json(PRODUCT_FILE)
    summary = {pid: details for pid, details in products.items()
               if details['quantity'] > 0}
    return summary

# GUI application


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        self.create_login_screen()

    def create_login_screen(self):
        tk.Label(self.root, text="Username").pack(pady=5)
        tk.Entry(self.root, textvariable=self.username).pack(pady=5)
        tk.Label(self.root, text="Password").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show="*").pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        try:
            username = self.username.get()
            password = self.password.get()
            if authenticate(username, password):
                self.username.set('')
                self.password.set('')
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Button(self.root, text="Add Product",
                  command=self.add_product).pack(pady=10)
        tk.Button(self.root, text="Edit Product",
                  command=self.edit_product).pack(pady=10)
        tk.Button(self.root, text="Delete Product",
                  command=self.delete_product).pack(pady=10)
        tk.Button(self.root, text="View Products",
                  command=self.view_products).pack(pady=10)
        tk.Button(self.root, text="Low Stock Alert",
                  command=self.low_stock_alert).pack(pady=10)
        tk.Button(self.root, text="Sales Summary",
                  command=self.sales_summary).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=20)

    def add_product(self):
        pid = simpledialog.askstring("Product ID", "Enter Product ID:")
        name = simpledialog.askstring("Product Name", "Enter Product Name:")
        quantity = simpledialog.askinteger("Quantity", "Enter Quantity:")
        price = simpledialog.askfloat("Price", "Enter Price:")
        if pid and name and quantity is not None and price is not None:
            add_product(pid, name, quantity, price)
            messagebox.showinfo("Success", "Product added successfully")

    def edit_product(self):
        pid = simpledialog.askstring("Product ID", "Enter Product ID:")
        product = get_product(pid)
        if product:
            name = simpledialog.askstring(
                "Product Name", "Enter new Product Name:", initialvalue=product['name'])
            quantity = simpledialog.askinteger(
                "Quantity", "Enter new Quantity:", initialvalue=product['quantity'])
            price = simpledialog.askfloat(
                "Price", "Enter new Price:", initialvalue=product['price'])
            if name and quantity is not None and price is not None:
                result = edit_product(pid, name, quantity, price)
                if result:
                    messagebox.showerror("Error", result)
                else:
                    messagebox.showinfo(
                        "Success", "Product updated successfully")
        else:
            messagebox.showerror("Error", "Product not found")

    def delete_product(self):
        pid = simpledialog.askstring("Product ID", "Enter Product ID:")
        if pid:
            result = delete_product(pid)
            if result:
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Product deleted successfully")

    def view_products(self):
        products = list_products()
        if products:
            message = "\n".join(
                [f"ID: {pid}, Name: {details['name']}, Quantity: {details['quantity']}, Price: ${details['price']:.2f}" for pid, details in products.items()])
            messagebox.showinfo("Product List", message)
        else:
            messagebox.showinfo("Product List", "No products available")

    def low_stock_alert(self):
        threshold = simpledialog.askinteger(
            "Threshold", "Enter stock threshold:")
        if threshold is not None:
            low_stock = low_stock_alert(threshold)
            if low_stock:
                message = "\n".join(
                    [f"ID: {pid}, Name: {details['name']}, Quantity: {details['quantity']}" for pid, details in low_stock.items()])
                messagebox.showinfo("Low Stock Alert", message)
            else:
                messagebox.showinfo("Low Stock Alert",
                                    "No products below threshold")

    def sales_summary(self):
        summary = sales_summary()
        if summary:
            message = "\n".join(
                [f"ID: {pid}, Name: {details['name']}, Quantity: {details['quantity']}, Price: ${details['price']:.2f}" for pid, details in summary.items()])
            messagebox.showinfo("Sales Summary", message)
        else:
            messagebox.showinfo("Sales Summary", "No products with sales")

    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
