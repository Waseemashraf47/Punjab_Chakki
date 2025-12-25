import tkinter as tk
from tkinter import ttk
from database import Database

class ActivityLogWindow(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.db = Database()
        self.user = user
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_logs()

    def create_widgets(self):
        tk.Label(self, text="System Activity Logs", font=("Arial", 14, "bold"), pady=10).pack()
        
        # Refresh Button
        tk.Button(self, text="Refresh Logs", command=self.load_logs, bg="#2196F3", fg="white").pack(pady=5)

        # Logs Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("timestamp", "user", "action")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("user", text="User")
        self.tree.heading("action", text="Action")
        
        self.tree.column("timestamp", width=150)
        self.tree.column("user", width=100)
        self.tree.column("action", width=500)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Zebra striping
        self.tree.tag_configure("odd", background="#f2f2f2")
        self.tree.tag_configure("even", background="white")

    def load_logs(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        logs = self.db.get_activities()
        for i, log in enumerate(logs):
            tag = "even" if i % 2 == 0 else "odd"
            # log: timestamp, username, action
            self.tree.insert("", tk.END, values=(log["timestamp"], log["username"], log["action"]), tags=(tag,))
