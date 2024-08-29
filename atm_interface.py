import tkinter as tk
from tkinter import messagebox
import json


class ATM:
    def __init__(self):
        self.load_data()
        self.current_pin = None
        self.window = tk.Tk()
        self.window.title("ATM Interface")
        self.create_login_widgets()

    def load_data(self):
        """Load user data from a JSON file."""
        with open('users.json', 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        """Save user data to a JSON file."""
        with open('users.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_login_widgets(self):
        """Create widgets for the login screen."""
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Enter PIN:").pack()
        self.pin_entry = tk.Entry(self.login_frame, show='*')
        self.pin_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.login).pack()

    def login(self):
        """Handle user login."""
        pin = self.pin_entry.get()
        if pin in self.data:
            self.current_pin = pin
            self.login_frame.pack_forget()
            self.create_atm_widgets()
        else:
            messagebox.showerror("Error", "Invalid PIN")

    def create_atm_widgets(self):
        """Create widgets for the ATM interface."""
        self.atm_frame = tk.Frame(self.window)
        self.atm_frame.pack()

        tk.Label(self.atm_frame,
                 text=f"Welcome {self.data[self.current_pin]['name']}").pack()

        tk.Label(self.atm_frame, text="Enter amount:").pack()
        self.amount_entry = tk.Entry(self.atm_frame)
        self.amount_entry.pack()

        tk.Button(self.atm_frame, text="Check Balance",
                  command=self.check_balance).pack()
        tk.Button(self.atm_frame, text="Deposit", command=self.deposit).pack()
        tk.Button(self.atm_frame, text="Withdraw",
                  command=self.withdraw).pack()
        tk.Button(self.atm_frame, text="Transaction History",
                  command=self.view_history).pack()
        tk.Button(self.atm_frame, text="Change PIN",
                  command=self.change_pin).pack()
        tk.Button(self.atm_frame, text="Logout", command=self.logout).pack()

    def check_balance(self):
        """Display current balance."""
        balance = self.data[self.current_pin]['balance']
        messagebox.showinfo(
            "Balance", f"Your current balance is ${balance:.2f}")

    def deposit(self):
        """Deposit amount to the account."""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            self.data[self.current_pin]['balance'] += amount
            self.data[self.current_pin]['transactions'].append(
                f"Deposited ${amount:.2f}")
            self.save_data()
            messagebox.showinfo(
                "Success", f"Deposited ${amount:.2f}. New balance is ${self.data[self.current_pin]['balance']:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        """Withdraw amount from the account."""
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            if amount > self.data[self.current_pin]['balance']:
                raise ValueError("Insufficient funds.")
            self.data[self.current_pin]['balance'] -= amount
            self.data[self.current_pin]['transactions'].append(
                f"Withdrew ${amount:.2f}")
            self.save_data()
            messagebox.showinfo(
                "Success", f"Withdrew ${amount:.2f}. New balance is ${self.data[self.current_pin]['balance']:.2f}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_history(self):
        """Display transaction history."""
        history = "\n".join(self.data[self.current_pin]['transactions'])
        messagebox.showinfo("Transaction History",
                            f"Transaction History:\n{history}")

    def change_pin(self):
        """Change the user's PIN."""
        self.change_pin_window = tk.Toplevel(self.window)
        self.change_pin_window.title("Change PIN")

        tk.Label(self.change_pin_window, text="Old PIN:").pack()
        self.old_pin_entry = tk.Entry(self.change_pin_window, show='*')
        self.old_pin_entry.pack()

        tk.Label(self.change_pin_window, text="New PIN:").pack()
        self.new_pin_entry = tk.Entry(self.change_pin_window, show='*')
        self.new_pin_entry.pack()

        tk.Button(self.change_pin_window, text="Change PIN",
                  command=self.update_pin).pack()

    def update_pin(self):
        """Update the PIN after validation."""
        old_pin = self.old_pin_entry.get()
        new_pin = self.new_pin_entry.get()

        if old_pin != self.current_pin:
            messagebox.showerror("Error", "Old PIN is incorrect")
            return

        if new_pin in self.data:
            messagebox.showerror("Error", "New PIN already in use")
            return

        self.data[new_pin] = self.data.pop(old_pin)
        self.current_pin = new_pin
        self.save_data()
        self.change_pin_window.destroy()
        messagebox.showinfo("Success", "PIN changed successfully")

    def logout(self):
        """Logout and return to login screen."""
        self.atm_frame.pack_forget()
        self.login_frame.pack()

    def run(self):
        self.window.mainloop()


# Run the ATM interface
atm = ATM()
atm.run()
