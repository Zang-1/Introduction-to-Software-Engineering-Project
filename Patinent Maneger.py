import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os

# ===== DATABASE =====
def connect_db():
    return sqlite3.connect("patients.db")

def init_db():
    # chỉ chạy SQL khi chưa có database
    if not os.path.exists("patients.db"):
        conn = connect_db()
        cursor = conn.cursor()

        with open("patients.sql", "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

        conn.commit()
        conn.close()

# ===== APP =====
class PatientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Management System")
        self.root.geometry("900x500")
        self.root.configure(bg="#f4f6f8")

        # TITLE
        tk.Label(root, text="PATIENT MANAGEMENT SYSTEM",
                 font=("Arial", 18, "bold"),
                 bg="#f4f6f8", fg="#2c3e50").pack(pady=10)

        main = tk.Frame(root, bg="#f4f6f8")
        main.pack(fill="both", expand=True)

        # LEFT (FORM)
        left = tk.Frame(main, bg="white", bd=2, relief="groove")
        left.pack(side="left", padx=10, pady=10, fill="y")

        labels = ["ID", "Name", "Age", "Gender", "Phone"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(left, text=text, bg="white").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(left)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[text] = entry

        # Buttons
        tk.Button(left, text="Add", bg="#2ecc71", fg="white",
                  command=self.add_patient).grid(row=6, column=0, pady=10)

        tk.Button(left, text="Update", bg="#3498db", fg="white",
                  command=self.update_patient).grid(row=6, column=1)

        tk.Button(left, text="Delete", bg="#e74c3c", fg="white",
                  command=self.delete_patient).grid(row=7, column=0)

        tk.Button(left, text="Clear", bg="#95a5a6", fg="white",
                  command=self.clear).grid(row=7, column=1)

        # RIGHT (TABLE)
        right = tk.Frame(main, bg="white", bd=2, relief="groove")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Search
        self.search_entry = tk.Entry(right)
        self.search_entry.pack(side="left", padx=5, pady=5)

        tk.Button(right, text="Search", bg="#f39c12", fg="white",
                  command=self.search).pack(side="left")

        tk.Button(right, text="Refresh", bg="#34495e", fg="white",
                  command=self.view).pack(side="left", padx=5)

        # Table
        self.tree = ttk.Treeview(right,
                                 columns=("ID", "Name", "Age", "Gender", "Phone"),
                                 show="headings")

        for col in ("ID", "Name", "Age", "Gender", "Phone"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select)

        self.view()

    # ===== FUNCTIONS =====
    def get_data(self):
        return (
            self.entries["ID"].get(),
            self.entries["Name"].get(),
            self.entries["Age"].get(),
            self.entries["Gender"].get(),
            self.entries["Phone"].get()
        )

    def add_patient(self):
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?)", self.get_data())
            conn.commit()
            messagebox.showinfo("Success", "Added!")
        except:
            messagebox.showerror("Error", "ID exists!")
        conn.close()
        self.view()

    def view(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def search(self):
        keyword = self.search_entry.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", (f"%{keyword}%",))

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def update_patient(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE patients
        SET name=?, age=?, gender=?, phone=?
        WHERE patient_id=?
        """, (
            self.entries["Name"].get(),
            self.entries["Age"].get(),
            self.entries["Gender"].get(),
            self.entries["Phone"].get(),
            self.entries["ID"].get()
        ))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Updated!")
        self.view()

    def delete_patient(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM patients WHERE patient_id=?", (self.entries["ID"].get(),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Deleted!")
        self.view()

    def clear(self):
        for e in self.entries.values():
            e.delete(0, tk.END)

    def select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")

        if values:
            keys = ["ID", "Name", "Age", "Gender", "Phone"]
            for i, key in enumerate(keys):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, values[i])

# ===== RUN =====
if __name__ == "__main__":
    init_db()  # chỉ tạo DB lần đầu
    root = tk.Tk()
    app = PatientApp(root)
    root.mainloop()