import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from bson import ObjectId

# ----- MongoDB Connection -----
client = MongoClient("mongodb://localhost:27017/")  # Change if using Atlas
db = client["studentdb"]
collection = db["students"]

# ----- Functions -----
def create_record():
    student_id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()
    if student_id and name and age:
        collection.insert_one({"student_id": student_id, "name": name, "age": age})
        messagebox.showinfo("Success", "Record added successfully!")
        clear_entries()
        read_records()
    else:
        messagebox.showwarning("Error", "All fields are required!")

def read_records():
    listbox.delete(0, tk.END)
    for doc in collection.find():
        listbox.insert(
            tk.END, f"{doc['_id']} | {doc['student_id']} | {doc['name']} | {doc['age']}"
        )

def update_record():
    try:
        selected = listbox.get(listbox.curselection())
        doc_id = selected.split(" | ")[0]
        new_id = entry_id.get()
        new_name = entry_name.get()
        new_age = entry_age.get()
        if new_id and new_name and new_age:
            collection.update_one(
                {"_id": ObjectId(doc_id)},
                {"$set": {"student_id": new_id, "name": new_name, "age": new_age}},
            )
            messagebox.showinfo("Success", "Record updated successfully!")
            clear_entries()
            read_records()
        else:
            messagebox.showwarning("Error", "All fields are required for update.")
    except:
        messagebox.showwarning("Error", "Select a record to update.")

def delete_record():
    try:
        selected = listbox.get(listbox.curselection())
        doc_id = selected.split(" | ")[0]
        collection.delete_one({"_id": ObjectId(doc_id)})
        messagebox.showinfo("Success", "Record deleted successfully!")
        read_records()
    except:
        messagebox.showwarning("Error", "Select a record to delete.")

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

# ----- GUI -----
root = tk.Tk()
root.title("Student Management System (MongoDB CRUD)")
root.geometry("750x500")
root.config(bg="#f0f8ff")  # Light background

# Heading
tk.Label(root, text="📘 Student Management System", bg="#f0f8ff",
         fg="#0b3d91", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

# Labels
label_color = "#002147"  # dark navy
tk.Label(root, text="Student ID:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=1, column=0, pady=5, sticky="e")
entry_id = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_id.grid(row=1, column=1, pady=5)

tk.Label(root, text="Name:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=2, column=0, pady=5, sticky="e")
entry_name = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_name.grid(row=2, column=1, pady=5)

tk.Label(root, text="Age:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=3, column=0, pady=5, sticky="e")
entry_age = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_age.grid(row=3, column=1, pady=5)

# ----- Button Styles (ttk) -----
style = ttk.Style()
style.theme_use("clam")  # ensures colors work across platforms

style.configure("Green.TButton", background="#4CAF50", foreground="white", font=("Arial", 11, "bold"))
style.map("Green.TButton", background=[("active", "#45a049")])

style.configure("Blue.TButton", background="#2196F3", foreground="white", font=("Arial", 11, "bold"))
style.map("Blue.TButton", background=[("active", "#1976D2")])

style.configure("Orange.TButton", background="#FF9800", foreground="white", font=("Arial", 11, "bold"))
style.map("Orange.TButton", background=[("active", "#e68900")])

style.configure("Red.TButton", background="#F44336", foreground="white", font=("Arial", 11, "bold"))
style.map("Red.TButton", background=[("active", "#d32f2f")])

# Buttons (now using ttk)
ttk.Button(root, text="Create", command=create_record, style="Green.TButton").grid(row=4, column=0, pady=10)
ttk.Button(root, text="Read", command=read_records, style="Blue.TButton").grid(row=4, column=1, pady=10)
ttk.Button(root, text="Update", command=update_record, style="Orange.TButton").grid(row=5, column=0, pady=10)
ttk.Button(root, text="Delete", command=delete_record, style="Red.TButton").grid(row=5, column=1, pady=10)

# Listbox
listbox = tk.Listbox(root, width=85, height=12, bg="#ffffff", fg="#004d00", font=("Courier", 11, "bold"))
listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

root.mainloop()
 