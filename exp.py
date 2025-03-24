import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

CSV_FILE = "expenses.csv"
expenses = []

def load_expenses():
    global expenses
    expenses.clear()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                expenses.append(row)
    update_expense_list()
    update_total()

def save_expenses():
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Category", "Amount", "Description"])
        writer.writerows(expenses)

def add_expense():
    category, amount, description = category_var.get(), amount_entry.get(), description_entry.get()
    if category and amount and description:
        try:
            amount = float(amount)
            if amount > 0:
                expenses.append([len(expenses) + 1, category, amount, description])
                save_expenses()
                load_expenses()
                clear_inputs()
            else:
                messagebox.showerror("Error", "Enter a positive amount.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
    else:
        messagebox.showerror("Error", "Fill all fields.")

def delete_expense():
    selected_item = expense_list.selection()
    if selected_item:
        item_index = expense_list.index(selected_item)
        del expenses[item_index]
        save_expenses()
        load_expenses()
    else:
        messagebox.showwarning("Warning", "Select an expense to delete.")

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Category", "Amount", "Description"])
            writer.writerows(expenses)
        messagebox.showinfo("Success", "Expenses exported successfully!")

def clear_inputs():
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_var.set("")

def update_expense_list():
    expense_list.delete(*expense_list.get_children())
    for expense in expenses:
        expense_list.insert("", "end", values=expense)

def update_total():
    total = sum(float(expense[2]) for expense in expenses)
    total_label.config(text=f"Total Expenses: ₹{total:.2f}")

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("850x500")

expense_frame = ttk.Frame(root)
expense_frame.pack(pady=10)

category_var = tk.StringVar()
ttk.Label(expense_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
category_dropdown = ttk.Combobox(expense_frame, textvariable=category_var, values=("Food", "Transportation", "Entertainment", "Bills", "Other"))
category_dropdown.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(expense_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(expense_frame)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(expense_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
description_entry = ttk.Entry(expense_frame)
description_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(expense_frame, text="Add Expense", command=add_expense).grid(row=3, column=0, pady=5)
ttk.Button(expense_frame, text="Delete Selected", command=delete_expense).grid(row=3, column=1, pady=5)
ttk.Button(expense_frame, text="Export to CSV", command=export_to_csv).grid(row=3, column=2, pady=5)

columns = ("ID", "Category", "Amount", "Description")
expense_list = ttk.Treeview(expense_frame, columns=columns, show="headings")
for col in columns:
    expense_list.heading(col, text=col)
expense_list.grid(row=4, column=0, columnspan=3)

total_label = ttk.Label(expense_frame, text="Total Expenses: ₹0.00", font=("Arial", 14))
total_label.grid(row=5, column=0, columnspan=3, pady=10)

load_expenses()
root.mainloop()
