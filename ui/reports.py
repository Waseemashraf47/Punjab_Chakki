import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
import csv
import datetime

class ReportsWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = Database()
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
                                    values=["All Time", "Today", "This Week", "This Month"], state="readonly")
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.load_data)
        
        tk.Button(ctrl_frame, text="Refresh", command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Export CSV", command=self.export_csv, bg="#4CAF50", fg="white").pack(side=tk.RIGHT)

        # Totals Display
        self.summary_label = tk.Label(self, text="Total Sales: 0.00 | Transactions: 0", font=("Arial", 12, "bold"))
        self.summary_label.pack(anchor="w", pady=5)

        # Sales List Treeview
        columns = ("id", "date", "total", "method", "user")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="Sale ID")
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("total", text="Total Amount")
        self.tree.heading("method", text="Payment Method")
        self.tree.heading("user", text="User (ID)")
        
        self.tree.column("id", width=50)
        self.tree.column("date", width=150)
        
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

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
            
            if include:
                filtered_sales.append(sale)

        # Update Tree and Summary
        total_amount = 0.0
        for s in filtered_sales:
            self.tree.insert("", tk.END, values=(s["id"], s["timestamp"], s["total_amount"], s["payment_method"], s["user_id"]))
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
                    writer.writerow(["Sale ID", "Date", "Total Amount", "Payment Method", "User ID"])
                    for s in self.current_data:
                         writer.writerow([s["id"], s["timestamp"], s["total_amount"], s["payment_method"], s["user_id"]])
                messagebox.showinfo("Success", "Data exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
