import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class UserManagementWindow(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.db = Database()
        self.user = user
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        # Top Frame: Create User
        create_frame = tk.LabelFrame(self, text="Create New User", padx=10, pady=10)
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(create_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(create_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(create_frame, text="Password:").grid(row=0, column=2, padx=5, pady=5)
        self.password_entry = tk.Entry(create_frame, show="*")
        self.password_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(create_frame, text="Role:").grid(row=0, column=4, padx=5, pady=5)
        
        # Admin can only create workers. Owner can create both.
        roles = ["worker"]
        if self.user['role'] == 'owner':
            roles.append("admin")
            
        self.role_var = tk.StringVar(value="worker")
        self.role_entry = ttk.Combobox(create_frame, textvariable=self.role_var, values=roles, state="readonly")
        self.role_entry.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(create_frame, text="Create Account", command=self.create_user, bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10)

        # Bottom Frame: User List
        list_frame = tk.LabelFrame(self, text="User Accounts", padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("id", "username", "role")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        
        self.tree.column("id", width=50)
        self.tree.column("username", width=200)
        self.tree.column("role", width=150)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Button(list_frame, text="Delete Selected", command=self.delete_user, bg="#F44336", fg="white").pack(side=tk.TOP, pady=10, padx=10)

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        users = self.db.get_all_users()
        for u in users:
            # Skip showing owner to prevent accidental deletion if they are logged in as owner? 
            # Or just show everything.
            self.tree.insert("", tk.END, values=(u["id"], u["username"], u["role"]))

    def create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
            
        if self.db.add_user(username, password, role):
            messagebox.showinfo("Success", f"User '{username}' created successfully")
            self.db.log_activity(self.user["id"], f"Created user: {username} with role: {role}")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.load_users()
        else:
            messagebox.showerror("Error", "Username already exists")

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a user to delete")
            return
            
        user_vals = self.tree.item(selected[0])["values"]
        user_id = user_vals[0]
        username = user_vals[1]
        role = user_vals[2]
        
        # Restrictions:
        # 1. Cannot delete yourself
        if user_id == self.user["id"]:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
            
        # 2. Admin cannot delete owner or other admins (depending on strictness)
        # Requirement: "Admin should have right to create or delete worker account... and also another admin account"
        # "but that admin account should not have right to create another admin account".
        
        if self.user["role"] == "admin":
            if role == "owner":
                messagebox.showerror("Error", "Admins cannot delete owners")
                return
            # The requirement says Admin CAN delete another admin? "and also another admin account by its name"
            # So I will allow it.
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete user '{username}'?"):
            if self.db.delete_user(user_id):
                messagebox.showinfo("Success", f"User '{username}' deleted")
                self.db.log_activity(self.user["id"], f"Deleted user: {username}")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to delete user")
