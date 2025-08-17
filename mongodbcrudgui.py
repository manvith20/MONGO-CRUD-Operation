import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# ----- MongoDB Connection -----
client = MongoClient("mongodb://localhost:27017/")  # Change if using Atlas
db = client["studentdb"]
collection = db["students"]

# ----- Functions -----
def create_record():
    name = entry_name.get()
    age = entry_age.get()
    if name and age:
        collection.insert_one({"name": name, "age": age})
        messagebox.showinfo("Success", "Record added successfully!")
        clear_entries()
        read_records()
    else:
        messagebox.showwarning("Error", "All fields are required!")

def read_records():
    listbox.delete(0, tk.END)
    for doc in collection.find():
        listbox.insert(tk.END, f"{doc['_id']} | {doc['name']} | {doc['age']}")

def update_record():
    try:
        selected = listbox.get(listbox.curselection())
        doc_id = selected.split(" | ")[0]
        new_name = entry_name.get()
        new_age = entry_age.get()
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"name": new_name, "age": new_age}})
        messagebox.showinfo("Success", "Record updated successfully!")
        clear_entries()
        read_records()
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
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)

# ----- GUI -----
root = tk.Tk()
root.title("MongoDB CRUD App")

# Labels and Entries
tk.Label(root, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Age:").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)

# Buttons
tk.Button(root, text="Create", command=create_record).grid(row=2, column=0)
tk.Button(root, text="Read", command=read_records).grid(row=2, column=1)
tk.Button(root, text="Update", command=update_record).grid(row=3, column=0)
tk.Button(root, text="Delete", command=delete_record).grid(row=3, column=1)

# Listbox to display records
listbox = tk.Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=2)

# Import ObjectId for updating/deleting
from bson import ObjectId

root.mainloop()
# Ensure to run this script in an environment where MongoDB is running
# and pymongo is installed.