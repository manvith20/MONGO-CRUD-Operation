import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient

# ----- MongoDB Connection -----
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
collection = db["students"]

# ensure `id` is unique (different from MongoDB’s internal `_id`)
collection.create_index("id", unique=True)

# ----- Functions -----
def create_record():
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()
    age = entry_age.get().strip()

    if not (student_id and name and age):
        messagebox.showwarning("Error", "All fields are required!")
        return

    try:
        age_val = int(age)
    except ValueError:
        messagebox.showwarning("Error", "Age must be a number.")
        return

    try:
        collection.insert_one({"id": student_id, "name": name, "age": age_val})
        messagebox.showinfo("Success", "Record added successfully!")
        clear_entries()
        read_records()
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))

def read_records():
    listbox.delete(0, tk.END)
    for doc in collection.find().sort("id", 1):
        listbox.insert(
            tk.END, f"{doc.get('id','')} | {doc.get('name','')} | {doc.get('age','')}"
        )

def get_selected_student_id():
    try:
        selected = listbox.get(listbox.curselection())
        return selected.split(" | ")[0].strip()
    except IndexError:
        return None

def update_record():
    student_id = get_selected_student_id()
    if student_id is None:
        messagebox.showwarning("Error", "Select a record to update.")
        return

    new_name = entry_name.get().strip()
    new_age = entry_age.get().strip()

    if not (new_name and new_age):
        messagebox.showwarning("Error", "Name & Age required for update.")
        return

    try:
        age_val = int(new_age)
    except ValueError:
        messagebox.showwarning("Error", "Age must be a number.")
        return

    try:
        collection.update_one(
            {"id": student_id}, {"$set": {"name": new_name, "age": age_val}}
        )
        messagebox.showinfo("Success", "Record updated successfully!")
        clear_entries()
        read_records()
    except Exception as e:
        messagebox.showerror("Update Error", str(e))

def delete_record():
    student_id = get_selected_student_id()
    if student_id is None:
        messagebox.showwarning("Error", "Select a record to delete.")
        return

    try:
        collection.delete_one({"id": student_id})
        messagebox.showinfo("Success", "Record deleted successfully!")
        read_records()
    except Exception as e:
        messagebox.showerror("Delete Error", str(e))

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

# ----- GUI -----
root = tk.Tk()
root.title("Student Management System (MongoDB CRUD)")
root.geometry("750x550")
root.config(bg="#f0f8ff")

# Heading
tk.Label(
    root, text="📘 Student Management System", bg="#f0f8ff",
    fg="#0b3d91", font=("Arial", 18, "bold")
).grid(row=0, column=0, columnspan=2, pady=15)

# Labels & Entries
label_color = "#002147"

tk.Label(root, text="ID:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5)
entry_id = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_id.grid(row=1, column=1, pady=5)

tk.Label(root, text="Name:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="e", pady=5)
entry_name = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_name.grid(row=2, column=1, pady=5)

tk.Label(root, text="Age:", bg="#f0f8ff", fg=label_color, font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="e", pady=5)
entry_age = tk.Entry(root, font=("Arial", 12), fg="black", bg="white")
entry_age.grid(row=3, column=1, pady=5)

# Button Styles
style = ttk.Style()
style.theme_use("clam")

style.configure("Green.TButton", background="#4CAF50", foreground="white", font=("Arial", 11, "bold"))
style.configure("Blue.TButton", background="#2196F3", foreground="white", font=("Arial", 11, "bold"))
style.configure("Orange.TButton", background="#FF9800", foreground="white", font=("Arial", 11, "bold"))
style.configure("Red.TButton", background="#F44336", foreground="white", font=("Arial", 11, "bold"))

# Buttons
ttk.Button(root, text="Create", command=create_record, style="Green.TButton").grid(row=4, column=0, pady=10)
ttk.Button(root, text="Read", command=read_records, style="Blue.TButton").grid(row=4, column=1, pady=10)
ttk.Button(root, text="Update", command=update_record, style="Orange.TButton").grid(row=5, column=0, pady=10)
ttk.Button(root, text="Delete", command=delete_record, style="Red.TButton").grid(row=5, column=1, pady=10)

# Listbox
listbox = tk.Listbox(root, width=90, height=15, bg="#ffffff", fg="#004d00", font=("Courier", 11, "bold"))
listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

# Initial read
read_records()

root.mainloop()
 