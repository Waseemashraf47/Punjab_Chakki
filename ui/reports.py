import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
import csv
import datetime

class ReportsWindow(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.db = Database()
        self.user = user
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Controls Frame
        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(ctrl_frame, text="Filter by:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="All Time")
        filter_combo = ttk.Combobox(ctrl_frame, textvariable=self.filter_var, 
                                    values=["All Time", "Today", "This Week", "This Month", "This Year"], state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.load_data)
        
        tk.Button(ctrl_frame, text="Refresh", command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Export CSV", command=self.export_csv, bg="#4CAF50", fg="white").pack(side=tk.RIGHT)

        # Backup & Restore Section (Owner Only)
        if self.user['role'] == 'owner':
            mgmt_frame = tk.LabelFrame(self, text="Database Management", padx=10, pady=5)
            mgmt_frame.pack(fill=tk.X, pady=10)
            
            tk.Button(mgmt_frame, text="Backup Database", command=self.backup_db, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(mgmt_frame, text="Restore Database", command=self.restore_db, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Label(mgmt_frame, text="(Owner Only)", fg="gray").pack(side=tk.LEFT, padx=5)

        # Totals Display
        self.summary_label = tk.Label(self, text="Total Sales: 0.00 | Transactions: 0", font=("Arial", 12, "bold"))
        self.summary_label.pack(anchor="w", pady=5)

        # Sales List Treeview
        columns = ("id", "date", "customer", "contact", "total", "method", "user")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="Sale ID")
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("total", text="Total Amount")
        self.tree.heading("method", text="Payment Method")
        self.tree.heading("user", text="Seller")
        
        self.tree.column("id", width=50)
        self.tree.column("date", width=150)
        self.tree.column("customer", width=120)
        self.tree.column("contact", width=120)
        
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Tags for zebra striping
        self.tree.tag_configure("odd", background="#e0e0e0")
        self.tree.tag_configure("even", background="white")

    def load_data(self, event=None):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filter_val = self.filter_var.get()
        all_sales = self.db.get_sales_report() # Currently returns raw list
        
        filtered_sales = []
        now = datetime.datetime.now()
        
        for sale in all_sales:
            # sale: [id, timestamp, total_amount, payment_method, user_id]
            # timestamp format: "YYYY-MM-DD HH:MM:SS"
            sale_dt = datetime.datetime.strptime(sale["timestamp"], "%Y-%m-%d %H:%M:%S")
            
            include = False
            if filter_val == "All Time":
                include = True
            elif filter_val == "Today":
                if sale_dt.date() == now.date():
                    include = True
            elif filter_val == "This Week":
                # Basic week check
                start_week = now - datetime.timedelta(days=now.weekday())
                if sale_dt.date() >= start_week.date():
                    include = True
            elif filter_val == "This Month":
                if sale_dt.month == now.month and sale_dt.year == now.year:
                    include = True
            elif filter_val == "This Year":
                if sale_dt.year == now.year:
                    include = True
            
            if include:
                filtered_sales.append(sale)

        # Update Tree and Summary
        total_amount = 0.0
        for i, s in enumerate(filtered_sales):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=(
                s["id"], s["timestamp"], s["customer_name"], s["customer_contact"], 
                f"{s['total_amount']:.2f}", s["payment_method"], s["seller_name"]
            ), tags=(tag,))
            total_amount += s["total_amount"]
            
        self.summary_label.config(text=f"Total Sales: {total_amount:.2f} | Transactions: {len(filtered_sales)}")
        self.current_data = filtered_sales # Store for export

    def export_csv(self):
        if not hasattr(self, 'current_data') or not self.current_data:
            messagebox.showwarning("Warning", "No data to export")
            return
            
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            try:
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Sale ID", "Date", "Customer Name", "Contact No", "Total Amount", "Payment Method", "Seller"])
                    for s in self.current_data:
                         writer.writerow([s["id"], s["timestamp"], s["customer_name"], s["customer_contact"], s["total_amount"], s["payment_method"], s["seller_name"]])
                messagebox.showinfo("Success", "Data exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def backup_db(self):
        filename = filedialog.asksaveasfilename(defaultextension=".db", 
                                              filetypes=[("Database Files", "*.db")],
                                              initialfile=f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        if filename:
            if self.db.backup_database(filename):
                messagebox.showinfo("Success", "Backup created successfully")
            else:
                messagebox.showerror("Error", "Backup failed")

    def restore_db(self):
        if not messagebox.askyesno("Confirm Restore", "Restoring will OVERWRITE current data. Proceed?"):
            return
            
        filename = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
        if filename:
            if self.db.restore_database(filename):
                messagebox.showinfo("Success", "Database restored. Application might need restart to refresh all views.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Restore failed")
