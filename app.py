import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Global variable to store transactions and budgets
transactions = []
budgets = {}

# Load data from CSV (if any)
def load_data():
    global transactions, budgets
    try:
        with open('transactions.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if row[0] == 'Income' or row[0] == 'Expense':
                    transactions.append(row)
    except FileNotFoundError:
        pass

    try:
        with open('budgets.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                budgets[row[0]] = float(row[1])
    except FileNotFoundError:
        pass


# Save data to CSV
def save_data():
    with open('transactions.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Amount', 'Category', 'Date'])
        writer.writerows(transactions)

    with open('budgets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for category, budget in budgets.items():
            writer.writerow([category, budget])

# Add a transaction (Income or Expense)
def add_transaction():
    global transactions
    transaction_type = transaction_type_var.get()
    amount = amount_var.get()
    category = category_var.get()
    date = date_var.get()

    if not amount or not category or not date:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    # Add to the transactions list
    transactions.append([transaction_type, amount, category, date])
    save_data()
    update_transaction_list()
    messagebox.showinfo("Success", f"{transaction_type} added successfully!")

# Update the transaction listbox
def update_transaction_list():
    transaction_listbox.delete(0, tk.END)
    for transaction in transactions:
        transaction_listbox.insert(tk.END, f"{transaction[3]} - {transaction[0]} {transaction[1]} - {transaction[2]}")

# Set a budget for a category
def set_budget():
    category = category_budget_var.get()
    budget = budget_var.get()

    if not category or not budget:
        messagebox.showerror("Input Error", "Please fill in both category and budget.")
        return

    try:
        budget = float(budget)
    except ValueError:
        messagebox.showerror("Input Error", "Budget must be a number.")
        return

    budgets[category] = budget
    save_data()
    update_budget_list()
    messagebox.showinfo("Success", f"Budget for {category} set to ${budget}.")

# Update the budget listbox
def update_budget_list():
    budget_listbox.delete(0, tk.END)
    for category, budget in budgets.items():
        budget_listbox.insert(tk.END, f"{category}: ${budget}")

# Show spending vs budget graph
def show_graph():
    categories = {}
    for transaction in transactions:
        category = transaction[2]
        amount = transaction[1]
        if category not in categories:
            categories[category] = 0
        if transaction[0] == "Expense":
            categories[category] += amount
        elif transaction[0] == "Income":
            categories[category] -= amount

    labels = list(categories.keys())
    values = list(categories.values())
    budget_labels = list(budgets.keys())
    budget_values = [budgets.get(label, 0) for label in budget_labels]

    # Plot graph
    plt.bar(labels, values, label='Spending/Income')
    plt.bar(budget_labels, budget_values, label='Budget', alpha=0.5)
    plt.xlabel('Categories')
    plt.ylabel('Amount ($)')
    plt.title('Spending vs Budget')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main window
root = tk.Tk()
root.title("Personal Finance Tracker")

# Load existing data
load_data()

# Transaction input variables
transaction_type_var = tk.StringVar()
amount_var = tk.StringVar()
category_var = tk.StringVar()
date_var = tk.StringVar()

# Budget input variables
category_budget_var = tk.StringVar()
budget_var = tk.StringVar()

# Transaction form
frame_transaction = tk.LabelFrame(root, text="Add Transaction", padx=10, pady=10)
frame_transaction.grid(row=0, column=0, padx=10, pady=10)

tk.Label(frame_transaction, text="Type").grid(row=0, column=0)
tk.OptionMenu(frame_transaction, transaction_type_var, "Income", "Expense").grid(row=0, column=1)
tk.Label(frame_transaction, text="Amount").grid(row=1, column=0)
tk.Entry(frame_transaction, textvariable=amount_var).grid(row=1, column=1)
tk.Label(frame_transaction, text="Category").grid(row=2, column=0)
tk.Entry(frame_transaction, textvariable=category_var).grid(row=2, column=1)
tk.Label(frame_transaction, text="Date (YYYY-MM-DD)").grid(row=3, column=0)
tk.Entry(frame_transaction, textvariable=date_var).grid(row=3, column=1)
tk.Button(frame_transaction, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2)

# Budget form
frame_budget = tk.LabelFrame(root, text="Set Budget", padx=10, pady=10)
frame_budget.grid(row=1, column=0, padx=10, pady=10)

tk.Label(frame_budget, text="Category").grid(row=0, column=0)
tk.Entry(frame_budget, textvariable=category_budget_var).grid(row=0, column=1)
tk.Label(frame_budget, text="Budget Amount").grid(row=1, column=0)
tk.Entry(frame_budget, textvariable=budget_var).grid(row=1, column=1)
tk.Button(frame_budget, text="Set Budget", command=set_budget).grid(row=2, column=0, columnspan=2)

# Transaction listbox
frame_transaction_list = tk.LabelFrame(root, text="Transaction List", padx=10, pady=10)
frame_transaction_list.grid(row=2, column=0, padx=10, pady=10)

transaction_listbox = tk.Listbox(frame_transaction_list, width=50, height=10)
transaction_listbox.grid(row=0, column=0)
update_transaction_list()

# Budget listbox
frame_budget_list = tk.LabelFrame(root, text="Budget List", padx=10, pady=10)
frame_budget_list.grid(row=3, column=0, padx=10, pady=10)

budget_listbox = tk.Listbox(frame_budget_list, width=50, height=10)
budget_listbox.grid(row=0, column=0)
update_budget_list()

# Graph button
tk.Button(root, text="Show Spending vs Budget", command=show_graph).grid(row=4, column=0, padx=10, pady=10)

# Run the application
root.mainloop()
