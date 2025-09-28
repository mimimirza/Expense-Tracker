import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    date TEXT
)
""")
conn.commit()

# Functions
def add_expense():
    category = category_var.get()
    amount = amount_var.get()
    date = date_var.get()
    
    if category and amount and date:
        try:
            cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", 
                           (category, float(amount), date))
            conn.commit()
            messagebox.showinfo("✅ Success", "Expense added successfully!")
            clear_inputs()
            view_expenses()
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    else:
        messagebox.showwarning("⚠ Input Error", "Please fill all fields")

def view_expenses():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def view_summary():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def clear_inputs():
    category_var.set("")
    amount_var.set("")
    date_var.set("")

# GUI setup
root = tk.Tk()
root.title("💰 Expense Tracker")
root.geometry("650x400")
root.configure(bg="#f0f4f7")  # light grey-blue background

# Input fields
category_var = tk.StringVar()
amount_var = tk.StringVar()
date_var = tk.StringVar()

# Labels & Entries
tk.Label(root, text="Category", font=("Arial", 12, "bold"), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=category_var, font=("Arial", 11)).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Amount", font=("Arial", 12, "bold"), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=amount_var, font=("Arial", 11)).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Date (YYYY-MM-DD)", font=("Arial", 12, "bold"), bg="#f0f4f7").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=date_var, font=("Arial", 11)).grid(row=2, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="➕ Add Expense", command=add_expense, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, pady=10)
tk.Button(root, text="📄 View Expenses", command=view_expenses, bg="#2196F3", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=1, pady=10)
tk.Button(root, text="📊 View Summary", command=view_summary, bg="#9C27B0", fg="white", font=("Arial", 11, "bold")).grid(row=3, column=2, pady=10)

# Table
columns = ("ID", "Category", "Amount", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

# Style for Treeview
style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#E8E8E8", fieldbackground="#E8E8E8")
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#D3D3D3")

for col in columns:
    tree.heading(col, text=col)

tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Expand table with window resize
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(2, weight=1)

# Run the app
root.mainloop()

# Close connection when app is closed
conn.close()
