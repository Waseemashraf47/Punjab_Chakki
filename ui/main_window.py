import tkinter as tk
from tkinter import ttk
from ui.inventory import InventoryWindow
from ui.pos import POSWindow
from ui.reports import ReportsWindow
from ui.users import UserManagementWindow
from ui.logs import ActivityLogWindow

class MainWindow:
    def __init__(self, root, user, logout_callback):
        self.root = root
        self.user = user
        self.logout_callback = logout_callback
        
        # Header
        self.create_header()
        
        # Navigation (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize Tabs
        self.init_tabs()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#333", height=50)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(header_frame, text="Punjab Aata Chakki Management System", 
                               fg="white", bg="#333", font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        user_info = f"User: {self.user['username']} | Role: {self.user['role'].upper()}"
        user_label = tk.Label(header_frame, text=user_info, fg="#ddd", bg="#333")
        user_label.pack(side=tk.RIGHT, padx=10)
        
        logout_btn = tk.Button(header_frame, text="Logout", command=self.logout_callback, 
                               bg="#f44336", fg="white", font=("Arial", 9))
        logout_btn.pack(side=tk.RIGHT, padx=10)

    def init_tabs(self):
        # POS Tab (Accessible to everyone)
        self.pos_frame = tk.Frame(self.notebook)
        self.notebook.add(self.pos_frame, text="POS & Checkout")
        self.pos_app = POSWindow(self.pos_frame, self.user)
        
        # Inventory Tab (Owner Only)
        if self.user['role'] == 'owner':
            self.inventory_frame = tk.Frame(self.notebook)
            self.notebook.add(self.inventory_frame, text="Inventory Management")
            self.inventory_app = InventoryWindow(self.inventory_frame, self.user)
            
            # Reports Tab (Owner Only)
            self.reports_frame = tk.Frame(self.notebook)
            self.notebook.add(self.reports_frame, text="Reports & Analytics")
            self.reports_app = ReportsWindow(self.reports_frame)
            
        # User Management & Logs (Owner and Admin Only)
        if self.user['role'] in ['owner', 'admin']:
            self.users_frame = tk.Frame(self.notebook)
            self.notebook.add(self.users_frame, text="User Management")
            self.users_app = UserManagementWindow(self.users_frame, self.user)
            
            self.logs_frame = tk.Frame(self.notebook)
            self.notebook.add(self.logs_frame, text="Activity Logs")
            self.logs_app = ActivityLogWindow(self.logs_frame, self.user)
