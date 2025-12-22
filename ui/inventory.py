import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class InventoryWindow(tk.Frame):
    def __init__(self, parent, user_role):
        super().__init__(parent)
        self.db = Database()
        self.user_role = user_role
        self.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Top Frame for Inputs (Only if Owner)
        if self.user_role == "owner":
            input_frame = tk.LabelFrame(self, text="Manage Product", padx=10, pady=10)
            input_frame.pack(fill=tk.X, padx=10, pady=5)

            # Name
            tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
            self.name_entry = tk.Entry(input_frame)
            self.name_entry.grid(row=0, column=1, padx=5, pady=5)

            # SKU
            tk.Label(input_frame, text="SKU:").grid(row=0, column=2, padx=5, pady=5)
            self.sku_entry = tk.Entry(input_frame)
            self.sku_entry.grid(row=0, column=3, padx=5, pady=5)

            # Category
            tk.Label(input_frame, text="Category:").grid(row=0, column=4, padx=5, pady=5)
            self.category_entry = ttk.Combobox(input_frame, values=["Flour", "Grains", "Spices", "General"], state="normal")
            self.category_entry.grid(row=0, column=5, padx=5, pady=5)

            # Price
            tk.Label(input_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
            self.price_entry = tk.Entry(input_frame)
            self.price_entry.grid(row=1, column=1, padx=5, pady=5)

            # Stock
            tk.Label(input_frame, text="Stock:").grid(row=1, column=2, padx=5, pady=5)
            self.stock_entry = tk.Entry(input_frame)
            self.stock_entry.grid(row=1, column=3, padx=5, pady=5)

            # Threshold
            tk.Label(input_frame, text="Low Alert:").grid(row=1, column=4, padx=5, pady=5)
            self.threshold_entry = tk.Entry(input_frame)
            self.threshold_entry.grid(row=1, column=5, padx=5, pady=5)

            # Buttons
            btn_frame = tk.Frame(input_frame)
            btn_frame.grid(row=2, column=0, columnspan=6, pady=10)
            
            tk.Button(btn_frame, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Update Selected", command=self.update_product, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Delete Selected", command=self.delete_product, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields, bg="grey", fg="white").pack(side=tk.LEFT, padx=5)

        # Treeview Configuration
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("id", "name", "sku", "category", "price", "stock", "threshold")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=30)
        
        self.tree.heading("name", text="Name")
        self.tree.heading("sku", text="SKU")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("threshold", text="Low Alert")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Tags for low stock
        self.tree.tag_configure("low_stock", background="#ffcccc")
        # Tags for zebra striping
        self.tree.tag_configure("odd", background="#e0e0e0")
        self.tree.tag_configure("even", background="white")

    def load_data(self):
        # Clear current data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        products = self.db.get_all_products()
        for i, p in enumerate(products):
            # p keys: id, name, sku, price, stock_quantity, category, low_stock_threshold
            tags = ()
            if p["stock_quantity"] <= p["low_stock_threshold"]:
                tags = ("low_stock",)
            else:
                # Apply striping only if not low stock (to preserve warning color)
                tags = ("even",) if i % 2 == 0 else ("odd",)
            
            self.tree.insert("", tk.END, values=(
                p["id"], p["name"], p["sku"], p["category"], 
                p["price"], p["stock_quantity"], p["low_stock_threshold"]
            ), tags=tags)

    def add_product(self):
        try:
            name = self.name_entry.get()
            sku = self.sku_entry.get()
            category = self.category_entry.get()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
            threshold = int(self.threshold_entry.get())

            if not name or not sku:
                messagebox.showerror("Error", "Name and SKU are required")
                return

            if self.db.add_product(name, sku, price, stock, category, threshold):
                messagebox.showinfo("Success", "Product added successfully")
                self.clear_fields()
                self.load_data()
            else:
                messagebox.showerror("Error", "SKU might already exist")
        except ValueError:
            messagebox.showerror("Error", "Price, Stock, and Threshold must be numbers")

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            item = self.tree.item(selected[0])
            p_id = item["values"][0]
            self.db.delete_product(p_id)
            self.load_data()
            self.clear_fields()

    def update_product(self):
        # Note: This is a full replacement update based on ID
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to update")
            return

        try:
            item = self.tree.item(selected[0])
            p_id = item["values"][0] # ID is at index 0
            
            name = self.name_entry.get()
            sku = self.sku_entry.get()
            category = self.category_entry.get()
            price = float(self.price_entry.get())
            # For update, we might handle stock differently (add/remove) but simple override is okay for now
            # However, usually stock is adjusted via transactions. 
            # I'll allow full edit for Owner.
            stock = int(self.stock_entry.get()) 
            threshold = int(self.threshold_entry.get())
            
            # We need a db method update_product_details. I'll need to check if I added it.
            # I added update_product_details but it didn't include stock.
            # Let's handle stock separately or Update the DB method.
            # Actually, I'll update the DB method in a moment using a tool, 
            # or I can just run a raw query here. For cleaner code, I will update database.py next.
            # Wait, I did implement update_product_details but I missed stock in the SQL update.
            # I'll just use a direct query for now or fix it in next step.
            
            # Fixing database.py is cleaner. I will assume it's fixed or I will fix it.
            # Let's assume I will fix database.py in the next step to include stock update or proper method.
            
            # Using the existing method for now (which I need to verify)
            # The existing method in database.py:
            # def update_product_details(self, product_id, name, sku, price, category, threshold):
            # It misses stock.
            
            # I will fix database.py in the next turn. For now, I will write this code assuming the method signature
            # will be `update_product_complete(self, product_id, name, sku, price, stock, category, threshold)`
            
            self.db.update_product_complete(p_id, name, sku, price, stock, category, threshold)
            
            messagebox.showinfo("Success", "Product updated")
            self.load_data()
            self.clear_fields()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid numeric values")

    def on_select(self, event):
        if self.user_role != "owner": return
        
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            vals = item["values"]
            # vals: id, name, sku, category, price, stock, threshold
            
            self.clear_fields()
            self.name_entry.insert(0, vals[1])
            self.sku_entry.insert(0, vals[2])
            self.category_entry.set(vals[3])
            self.price_entry.insert(0, vals[4])
            self.stock_entry.insert(0, vals[5])
            self.threshold_entry.insert(0, vals[6])

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.sku_entry.delete(0, tk.END)
        self.category_entry.set("")
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.threshold_entry.delete(0, tk.END)
