import tkinter as tk
from tkinter import messagebox
import json
from datetime import date

FILE = "expenses.json"

def load_expenses():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense():
    category = category_entry.get()
    desc = desc_entry.get()
    amount = amount_entry.get()

    if not category or not desc or not amount:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    entry = {
        "date": str(date.today()),
        "category": category,
        "description": desc,
        "amount": amount
    }

    expenses.append(entry)
    save_expenses(expenses)
    update_listbox()
    update_total()
    clear_entries()
    messagebox.showinfo("Success", "Expense added!")

def update_listbox():
    listbox.delete(0, tk.END)
    for e in expenses:
        listbox.insert(tk.END, f"{e['date']} | {e['category']} | {e['description']} | ₹{e['amount']}")

def update_total():
    total = sum(e["amount"] for e in expenses)
    total_label.config(text=f"Total Spent: ₹{total}")

def clear_entries():
    category_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# --- GUI setup ---
root = tk.Tk()
root.title("Expense Tracker 💰")
root.geometry("500x500")

expenses = load_expenses()

# Labels and Entries
tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Description:").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white").pack(pady=5)

# Expense list
listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=10)

# Total label
total_label = tk.Label(root, text="Total Spent: ₹0", font=("Arial", 12, "bold"))
total_label.pack()

update_listbox()
update_total()

root.mainloop()
