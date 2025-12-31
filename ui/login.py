import tkinter as tk
from tkinter import messagebox
from database import Database

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()
        
        self.root.title("Login - Punjab Aata Chakki")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        # Frame for login content
        frame = tk.Frame(self.root, bg="#ffffff", padx=40, pady=40, relief=tk.RAISED, bd=1)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(frame, text="System Login", font=("Arial", 24, "bold"), bg="#ffffff").pack(pady=(0, 40))

        # Username
        tk.Label(frame, text="Username:", font=("Arial", 14), bg="#ffffff").pack(anchor="w")
        self.username_entry = tk.Entry(frame, width=40, font=("Arial", 12))
        self.username_entry.pack(pady=10)

        # Password
        tk.Label(frame, text="Password:", font=("Arial", 14), bg="#ffffff").pack(anchor="w")
        self.password_entry = tk.Entry(frame, width=40, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', lambda event: self.login())

        # Login Button
        tk.Button(frame, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), width=30).pack(pady=40)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.verify_user(username, password)
        if user:
            # content of user row: [id, username, password_hash, role]
            # user is a sqlite3.Row object, so we can access by key if row_factory is set, 
            # but let's be safe and convert to dict for the callback
            user_data = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            self.on_login_success(user_data)
        else:
            messagebox.showerror("Error", "Invalid username or password")
