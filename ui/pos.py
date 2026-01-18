# import tkinter as tk
# from tkinter import ttk, messagebox, simpledialog
# from database import Database
# import datetime
# import os

# class POSWindow(tk.Frame):
#     def __init__(self, parent, user):
#         super().__init__(parent)
#         self.db = Database()
#         self.user = user
#         self.cart = [] # List of dicts: {id, name, price, qty, total}
#         self.pack(fill=tk.BOTH, expand=True)

#         self.create_layout()
#         self.load_products()

#     def create_layout(self):
#         # Paned Window: Left (Product List), Right (Cart)
#         self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL)
#         self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
#         # --- Left Side: Product Selection ---
#         left_frame = tk.Frame(self.paned)
#         self.paned.add(left_frame, width=400)
        
#         # Search Bar
#         search_frame = tk.Frame(left_frame)
#         search_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
#         self.search_var = tk.StringVar()
#         self.search_var.trace("w", self.filter_products)
#         tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
#         # Category Filter
#         tk.Label(search_frame, text="Category:").pack(side=tk.LEFT)
#         self.cat_filter_var = tk.StringVar(value="All")
#         self.cat_filter = ttk.Combobox(search_frame, textvariable=self.cat_filter_var, values=["All"], state="readonly", width=10)
#         self.cat_filter.pack(side=tk.LEFT, padx=5)
#         self.cat_filter.bind("<<ComboboxSelected>>", self.filter_products)
        
#         # Refresh Button
#         tk.Button(search_frame, text="Refresh", command=self.load_products, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
        
#         # Product List (Treeview)
#         columns = ("id", "name", "price", "stock")
#         self.prod_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
#         self.prod_tree.heading("id", text="ID")
#         self.prod_tree.heading("name", text="Product")
#         self.prod_tree.heading("price", text="Price")
#         self.prod_tree.heading("stock", text="Stock")
        
#         self.prod_tree.column("id", width=50)
#         self.prod_tree.column("name", width=150)
#         self.prod_tree.column("price", width=80)
#         self.prod_tree.column("stock", width=80)
        
#         self.prod_tree.column("stock", width=80)
        
#         self.prod_tree.pack(fill=tk.BOTH, expand=True)
#         self.prod_tree.bind("<Double-1>", self.add_to_cart)

#         # Configure tags for zebra striping
#         self.prod_tree.tag_configure('odd', background='#e0e0e0')
#         self.prod_tree.tag_configure('even', background='white')

#         # --- Right Side: Cart & Checkout ---
#         right_frame = tk.Frame(self.paned, bg="#f9f9f9", padx=10, pady=10)
#         self.paned.add(right_frame)
        
#         tk.Label(right_frame, text="Current Cart", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=5)

#         # --- Customer Details ---
#         cust_frame = tk.Frame(right_frame, bg="#f9f9f9")
#         cust_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(cust_frame, text="Customer Name:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", padx=5)
#         self.cust_name_var = tk.StringVar()
#         tk.Entry(cust_frame, textvariable=self.cust_name_var).grid(row=0, column=1, sticky="EW", padx=5)
        
#         tk.Label(cust_frame, text="Contact No:", bg="#f9f9f9").grid(row=0, column=2, sticky="w", padx=5)
#         self.cust_contact_var = tk.StringVar()
#         tk.Entry(cust_frame, textvariable=self.cust_contact_var).grid(row=0, column=3, sticky="EW", padx=5)
        
#         cust_frame.columnconfigure(1, weight=1)
#         cust_frame.columnconfigure(3, weight=1)

#         # Cart Treeview
#         cart_cols = ("sys_id", "name", "price", "qty", "total") 
#         self.cart_tree = ttk.Treeview(right_frame, columns=cart_cols, show="headings", height=15)
#         self.cart_tree.heading("sys_id", text="ID")
#         self.cart_tree.heading("name", text="Item")
#         self.cart_tree.heading("price", text="Price")
#         self.cart_tree.heading("qty", text="Qty")
#         self.cart_tree.heading("total", text="Total")
        
#         self.cart_tree.column("sys_id", width=0, stretch=tk.NO) # Hidden ID
#         self.cart_tree.column("name", width=150)
#         self.cart_tree.column("price", width=80)
#         self.cart_tree.column("qty", width=60)
#         self.cart_tree.column("total", width=100)
        
#         self.cart_tree.pack(fill=tk.BOTH, expand=True)
#         # self.cart_tree.bind("<Double-1>", self.remove_from_cart) # Disabled as per request
#         self.cart_tree.bind("<<TreeviewSelect>>", self.on_cart_select)
        
#         # controls Frame (Qty + Price + Remove) - All in one line
#         controls_frame = tk.Frame(right_frame, bg="#e0e0e0", pady=5)
#         controls_frame.pack(fill=tk.X, pady=5)
        
#         # --- Quantity Section ---
#         tk.Button(controls_frame, text=" - ", command=lambda: self.adjust_qty(-1), font=("Arial", 12, "bold"), width=4).pack(side=tk.LEFT, padx=(5, 0))
        
#         self.qty_entry = tk.Entry(controls_frame, width=5, justify="center", font=("Arial", 12))
#         self.qty_entry.pack(side=tk.LEFT, padx=5)
#         self.qty_entry.bind("<Return>", lambda e: self.apply_manual_qty())
        
#         tk.Button(controls_frame, text=" + ", command=lambda: self.adjust_qty(1), font=("Arial", 12, "bold"), width=4).pack(side=tk.LEFT, padx=(0, 15))

#         # --- Separator (Visual spacer) ---
#         ttk.Separator(controls_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5)

#         # --- Price Section ---
#         tk.Label(controls_frame, text="Set Total: ", bg="#e0e0e0").pack(side=tk.LEFT, padx=(15, 0))
#         self.target_price_entry = tk.Entry(controls_frame, width=8)
#         self.target_price_entry.pack(side=tk.LEFT, padx=5)
#         tk.Button(controls_frame, text="Set", command=self.set_qty_by_price, bg="#2196F3", fg="white", width=4).pack(side=tk.LEFT)

#         # --- Remove Button (Far Right) ---
#         tk.Button(controls_frame, text="Remove", command=lambda: self.remove_from_cart(None), bg="#f44336", fg="white").pack(side=tk.RIGHT, padx=5)

#         # Totals & Actions
#         bottom_frame = tk.Frame(right_frame, bg="#f9f9f9")
#         bottom_frame.pack(fill=tk.X, pady=10)
        
#         # --- Discount Section ---
#         disc_frame = tk.Frame(bottom_frame, bg="#f9f9f9")
#         disc_frame.pack(fill=tk.X, pady=5)
        
#         tk.Label(disc_frame, text="Discount:", bg="#f9f9f9").pack(side=tk.LEFT)
#         self.disc_val_var = tk.StringVar(value="0")
#         self.disc_val_entry = tk.Entry(disc_frame, textvariable=self.disc_val_var, width=5)
#         self.disc_val_entry.pack(side=tk.LEFT, padx=5)
#         self.disc_val_entry.bind("<Return>", self.calculate_totals)
#         self.disc_val_entry.bind("<FocusOut>", self.calculate_totals)
        
#         self.disc_type_var = tk.StringVar(value="Fixed")
#         self.disc_type = ttk.Combobox(disc_frame, textvariable=self.disc_type_var, values=["Fixed", "%"], state="readonly", width=6)
#         self.disc_type.pack(side=tk.LEFT, padx=5)
#         self.disc_type.bind("<<ComboboxSelected>>", self.calculate_totals)
        
#         tk.Button(disc_frame, text="Apply", command=self.calculate_totals, bg="#FFC107", width=6).pack(side=tk.LEFT, padx=5)

#         self.total_label = tk.Label(bottom_frame, text="Subtotal: 0.00\nDiscount: -0.00\nTotal: 0.00", font=("Arial", 16, "bold"), fg="#D32F2F", bg="#f9f9f9", justify=tk.RIGHT)
#         self.total_label.pack(side=tk.TOP, pady=10, anchor="e")
        
#         tk.Label(bottom_frame, text="Payment Method:", bg="#f9f9f9").pack(anchor="w")
#         self.payment_method = ttk.Combobox(bottom_frame, values=["Cash", "Card", "Online"], state="readonly")
#         self.payment_method.set("Cash")
#         self.payment_method.pack(fill=tk.X)
        
#         tk.Button(bottom_frame, text="CHECKOUT", command=self.checkout, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2).pack(fill=tk.X, pady=15)

#     def set_qty_by_price(self):
#         selected = self.cart_tree.selection()
#         if not selected:
#             messagebox.showwarning("Warning", "Select an item in the cart first.")
#             return
            
#         try:
#             target_total = float(self.target_price_entry.get())
#             if target_total <= 0: return
            
#             p_id = self.cart_tree.item(selected[0])["values"][0] # Hidden ID
            
#             for item in self.cart:
#                 if item["id"] == p_id:
#                     # Calculate new quantity: Total / Unit Price
#                     new_qty = target_total / item["price"]
                    
#                     # Check stock logic if needed (Assuming stock is float)
#                     product = next((p for p in self.all_products if p["id"] == p_id), None)
#                     if product and new_qty > float(product["stock_quantity"]):
#                          messagebox.showwarning("Stock Limit", f"Insufficient stock. Max: {product['stock_quantity']}")
#                          return

#                     item["qty"] = new_qty
#                     item["total"] = target_total
#                     break
            
#             self.refresh_cart()
#             self.target_price_entry.delete(0, tk.END)
            
#         except ValueError:
#             messagebox.showerror("Error", "Invalid Price Amount")

#     def load_products(self):
#         # Store full list for filtering
#         self.all_products = self.db.get_all_products()
        
#         # Extract unique categories for filter
#         categories = sorted(list(set(p["category"] for p in self.all_products if p["category"])))
#         self.cat_filter['values'] = ["All"] + categories
        
#         self.update_product_list(self.all_products)

#     def update_product_list(self, products):
#         for item in self.prod_tree.get_children():
#             self.prod_tree.delete(item)
#         for i, p in enumerate(products):
#             tag = 'even' if i % 2 == 0 else 'odd'
#             self.prod_tree.insert("", tk.END, values=(p["id"], p["name"], f"{p['price']:.2f}", f"{p['stock_quantity']:.2f}"), tags=(tag,))

#     def filter_products(self, *args):
#         query = self.search_var.get().lower()
#         cat_filter = self.cat_filter_var.get()
        
#         filtered = []
#         for p in self.all_products:
#             match_query = query in p["name"].lower() or query in str(p["sku"]).lower()
#             match_cat = (cat_filter == "All") or (p["category"] == cat_filter)
            
#             if match_query and match_cat:
#                 filtered.append(p)
                
#         self.update_product_list(filtered)

#     def add_to_cart(self, event):
#         selected = self.prod_tree.selection()
#         if not selected: return
        
#         item_vals = self.prod_tree.item(selected[0])["values"]
#         p_id, name, price, stock = item_vals
        
#         # Convert to correct types
#         price = float(price)
#         stock = float(stock) # Allow fractional stock
        
#         # Check if already in cart
#         for item in self.cart:
#             if item["id"] == p_id:
#                 if item["qty"] + 1 <= stock: # Check against stock
#                     item["qty"] += 1.0
#                     item["total"] = item["qty"] * price
#                     self.refresh_cart()
#                 else:
#                     messagebox.showwarning("Stock Limit", "Not enough stock available!")
#                 return

#         if stock > 0:
#             self.cart.append({
#                 "id": p_id,
#                 "name": name,
#                 "price": price,
#                 "qty": 1.0,
#                 "total": price
#             })
#             self.refresh_cart()
#         else:
#              messagebox.showwarning("Out of Stock", "This item is out of stock.")

#     def adjust_qty(self, delta):
#         selected = self.cart_tree.selection()
#         if not selected: 
#              # Optionally warn only if user clicked a button, but ignore silently is fine too
#              return
        
#         item_vals = self.cart_tree.item(selected[0])["values"]
#         # sys_id is hidden at index 0 (if visible index might shift but we kept it index 0)
#         # Note: values tuple usually returns strings for numbers.
#         p_id = item_vals[0]
        
#         for i, item in enumerate(self.cart):
#             if item["id"] == p_id:
#                 new_qty = item["qty"] + delta
                
#                 # Check stock limit if adding
#                 if delta > 0:
#                      # We need to find the product stock again
#                      product = next((p for p in self.all_products if p["id"] == p_id), None)
#                      if product and new_qty > product["stock_quantity"]:
#                          messagebox.showwarning("Stock Limit", f"Only {product['stock_quantity']} in stock.")
#                          return

#                 if new_qty > 0:
#                     item["qty"] = new_qty
#                     item["total"] = item["qty"] * item["price"]
#                 else:
#                     # If qty becomes 0, remove it
#                     self.cart.pop(i)
#                     p_id = None # Don't select if removed
#                 break
#         self.refresh_cart(selected_id=p_id)
        
#         # Update entry if item still exists
#         updated_item = next((i for i in self.cart if i["id"] == p_id), None)
#         if updated_item:
#             self.qty_entry.delete(0, tk.END)
#             self.qty_entry.insert(0, str(updated_item["qty"]))
#         else:
#              self.qty_entry.delete(0, tk.END)

#     def on_cart_select(self, event):
#         selected = self.cart_tree.selection()
#         if not selected: return
        
#         item_vals = self.cart_tree.item(selected[0])["values"]
#         # item_vals[3] is qty string from treeview
#         # But better to get from self.cart source of truth
#         p_id = item_vals[0]
        
#         item = next((i for i in self.cart if i["id"] == p_id), None)
#         if item:
#             self.qty_entry.delete(0, tk.END)
#             self.qty_entry.insert(0, str(item["qty"]))

#     def apply_manual_qty(self):
#         selected = self.cart_tree.selection()
#         if not selected:
#              messagebox.showwarning("Selection", "Please select an item in the cart.")
#              return

#         try:
#              new_qty = float(self.qty_entry.get())
#              if new_qty <= 0:
#                  messagebox.showwarning("Invalid Quantity", "Quantity must be positive.")
#                  return
#         except ValueError:
#              messagebox.showerror("Invalid Input", "Please enter a valid number.")
#              return

#         item_vals = self.cart_tree.item(selected[0])["values"]
#         p_id = item_vals[0]

#         for i, item in enumerate(self.cart):
#             if item["id"] == p_id:
#                 # Check stock
#                 product = next((p for p in self.all_products if p["id"] == p_id), None)
#                 if product and new_qty > product["stock_quantity"]:
#                         messagebox.showwarning("Stock Limit", f"Only {product['stock_quantity']} in stock.")
#                         # Reset entry to current valid qty
#                         self.qty_entry.delete(0, tk.END)
#                         self.qty_entry.insert(0, str(item['qty']))
#                         return
                
#                 item["qty"] = new_qty
#                 item["total"] = item["qty"] * item["price"]
#                 break
        
#         self.refresh_cart(selected_id=p_id)

#     def remove_from_cart(self, event):
#         selected = self.cart_tree.selection()
#         if not selected: return
        
#         # Find item index
#         item_vals = self.cart_tree.item(selected[0])["values"]
#         p_id = item_vals[0]
        
#         for i, item in enumerate(self.cart):
#             if item["id"] == p_id:
#                 # User requested full removal (or we are simplifying behavior)
#                 self.cart.pop(i)
#                 p_id = None # item gone, clear selection
#                 break
#         self.refresh_cart(selected_id=p_id)

#     def refresh_cart(self, selected_id=None):
#         for item in self.cart_tree.get_children():
#             self.cart_tree.delete(item)
        
#         total = 0.0
#         for item in self.cart:
#             # Display Qty with 2 decimals
#             iid = self.cart_tree.insert("", tk.END, values=(item["id"], item["name"], item["price"], f"{item['qty']:.2f}", f"{item['total']:.2f}"))
#             total += item["total"]
            
#             if selected_id and item["id"] == selected_id:
#                 self.cart_tree.selection_set(iid)
#                 self.cart_tree.focus(iid)
        
#         self.calculate_totals()

#     def calculate_totals(self, event=None):
#         subtotal = sum(item["total"] for item in self.cart)
#         discount_val = 0.0
#         self.discount_amt = 0.0
        
#         try:
#             val_str = self.disc_val_var.get()
#             if val_str:
#                 discount_val = float(val_str)
#         except ValueError:
#             pass
            
#         if self.disc_type_var.get() == "%":
#             self.discount_amt = subtotal * (discount_val / 100)
#         else: # Fixed
#             self.discount_amt = discount_val
            
#         total = subtotal - self.discount_amt
#         if total < 0: total = 0
        
#         self.total_label.config(text=f"Subtotal: {subtotal:.2f}\nDiscount: -{self.discount_amt:.2f}\nTotal: {total:.2f}")
#         return subtotal, total

#     def checkout(self):
#         if not self.cart:
#             messagebox.showwarning("Empty Cart", "Add items to cart first.")
#             return

#         subtotal, total = self.calculate_totals()
        
#         confirm = messagebox.askyesno("Confirm Sale", f"Subtotal: {subtotal:.2f}\nDiscount: {self.discount_amt:.2f}\nTotal: {total:.2f}\nProceed?")
        
#         if confirm:
#             # Prepare data for DB
#             # items: (product_id, quantity, price_at_sale)
#             sale_items = [(x["id"], x["qty"], x["price"]) for x in self.cart]
            
#             cust_name = self.cust_name_var.get().strip()
#             cust_contact = self.cust_contact_var.get().strip()
            
#             sale_id = self.db.record_sale(self.user["id"], sale_items, total, self.payment_method.get(), self.discount_amt, cust_name, cust_contact)
            
#             if sale_id:
#                 # Ask (optional) to print receipt
#                 if messagebox.askyesno("Print Receipt", "Do you want to print the receipt?"):
#                     self.print_receipt(sale_id, subtotal, self.discount_amt, total, self.payment_method.get(), cust_name, cust_contact)
                
#                 messagebox.showinfo("Success", "Sale recorded successfully!")
#                 self.db.log_activity(self.user["id"], f"Recorded sale ID: {sale_id}, Total: {total:.2f}")
#                 self.cart = []
#                 self.refresh_cart()
#                 self.cust_name_var.set("")
#                 self.cust_contact_var.set("")
#                 self.load_products() # Refresh stock display
#             else:
#                 messagebox.showerror("Error", "Failed to record sale.")

#     def print_receipt(self, sale_id, subtotal, discount, total, method, cust_name="", cust_contact=""):
#         # Generate a text receipt
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         lines = [
#             "--------------------------------",
#             "       PUNJAB AATA CHAKKI       ",
#             "   Trolly Adda, near Gondal Market,  ",
#             "    Al-Noor Colony Sector No. 3     ",
#             " Contact: 0335-554875, 0332-5596926 ",
#             "--------------------------------",
#             f"Date: {timestamp}",
#             f"Sale ID: {sale_id}",
#             f"Staff: {self.user['username']}"
#         ]
        
#         if cust_name:
#             lines.append(f"Customer: {cust_name}")
#         if cust_contact:
#             lines.append(f"Contact: {cust_contact}")
            
#         lines.append("--------------------------------")
#         lines.append(f"{'Item':<20} {'Qty':<5} {'Total'}")
        
#         for item in self.cart:
#             lines.append(f"{item['name']:<20} {item['qty']:<5.2f} {item['total']:.2f}")
            
#         lines.append("--------------------------------")
#         lines.append(f"Subtotal: {subtotal:.2f}")
#         lines.append(f"Discount: -{discount:.2f}")
#         lines.append(f"TOTAL:    {total:.2f}")
#         lines.append(f"Paid via: {method}")
#         lines.append("--------------------------------")
#         lines.append("      Thank you for visiting!   ")
#         lines.append("--------------------------------")
        
#         receipt_text = "\n".join(lines)
        
#         # Save to file
#         filename = f"receipt_{sale_id}.txt"
#         with open(filename, "w") as f:
#             f.write(receipt_text)
            
#         # Try to print (Platform specific)
#         try:
#             if os.name == "nt": # Windows
#                 os.startfile(filename, "print")
#             else: # Linux
#                 # Using lp command
#                 os.system(f"lp {filename}")
#         except Exception as e:
#             print(f"Printing failed: {e}")
#             # Fallback: Just show it was saved
#             pass


import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import Database
import datetime
import os

class POSWindow(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.db = Database()
        self.user = user
        self.cart = [] # List of dicts: {id, name, price, qty, total}
        self.pack(fill=tk.BOTH, expand=True)

        self.create_layout()
        self.load_products()

    def create_layout(self):
        # Paned Window: Left (Product List), Right (Cart)
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # --- Left Side: Product Selection ---
        left_frame = tk.Frame(self.paned)
        self.paned.add(left_frame, width=400)
        
        # Search Bar
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_products)
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Category Filter
        tk.Label(search_frame, text="Category:").pack(side=tk.LEFT)
        self.cat_filter_var = tk.StringVar(value="All")
        self.cat_filter = ttk.Combobox(search_frame, textvariable=self.cat_filter_var, values=["All"], state="readonly", width=10)
        self.cat_filter.pack(side=tk.LEFT, padx=5)
        self.cat_filter.bind("<<ComboboxSelected>>", self.filter_products)
        
        # Refresh Button
        tk.Button(search_frame, text="Refresh", command=self.load_products, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Product List (Treeview)
        columns = ("id", "name", "price", "stock")
        self.prod_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        self.prod_tree.heading("id", text="ID")
        self.prod_tree.heading("name", text="Product")
        self.prod_tree.heading("price", text="Price")
        self.prod_tree.heading("stock", text="Stock")
        
        self.prod_tree.column("id", width=50)
        self.prod_tree.column("name", width=150)
        self.prod_tree.column("price", width=80)
        self.prod_tree.column("stock", width=80)
        
        self.prod_tree.column("stock", width=80)
        
        self.prod_tree.pack(fill=tk.BOTH, expand=True)
        self.prod_tree.bind("<Double-1>", self.add_to_cart)

        # Configure tags for zebra striping
        self.prod_tree.tag_configure('odd', background='#e0e0e0')
        self.prod_tree.tag_configure('even', background='white')

        # --- Right Side: Cart & Checkout ---
        right_frame = tk.Frame(self.paned, bg="#f9f9f9", padx=10, pady=10)
        self.paned.add(right_frame)
        
        tk.Label(right_frame, text="Current Cart", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=5)

        # --- Customer Details ---
        cust_frame = tk.Frame(right_frame, bg="#f9f9f9")
        cust_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(cust_frame, text="Customer Name:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", padx=5)
        self.cust_name_var = tk.StringVar()
        tk.Entry(cust_frame, textvariable=self.cust_name_var).grid(row=0, column=1, sticky="EW", padx=5)
        
        tk.Label(cust_frame, text="Contact No:", bg="#f9f9f9").grid(row=0, column=2, sticky="w", padx=5)
        self.cust_contact_var = tk.StringVar()
        tk.Entry(cust_frame, textvariable=self.cust_contact_var).grid(row=0, column=3, sticky="EW", padx=5)
        
        cust_frame.columnconfigure(1, weight=1)
        cust_frame.columnconfigure(3, weight=1)

        # Totals & Actions (Checkout Section)
        bottom_frame = tk.Frame(right_frame, bg="#f9f9f9")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10) # Pack at bottom-most position
        
        # controls Frame (Qty + Price + Remove) - All in one line
        controls_frame = tk.Frame(right_frame, bg="#e0e0e0", pady=5)
        controls_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5) # Pack above bottom_frame
        
        # Cart Treeview
        cart_cols = ("sys_id", "name", "price", "qty", "total") 
        self.cart_tree = ttk.Treeview(right_frame, columns=cart_cols, show="headings", height=10) # Reduced height
        self.cart_tree.heading("sys_id", text="ID")
        self.cart_tree.heading("name", text="Item")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("total", text="Total")
        
        self.cart_tree.column("sys_id", width=0, stretch=tk.NO) # Hidden ID
        self.cart_tree.column("name", width=150)
        self.cart_tree.column("price", width=80)
        self.cart_tree.column("qty", width=60)
        self.cart_tree.column("total", width=100)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Update bindings
        # self.cart_tree.bind("<Double-1>", self.remove_from_cart) # Disabled as per request
        self.cart_tree.bind("<<TreeviewSelect>>", self.on_cart_select)

        # --- Quantity Section ---
        tk.Button(controls_frame, text=" - ", command=lambda: self.adjust_qty(-1), font=("Arial", 12, "bold"), width=4).pack(side=tk.LEFT, padx=(5, 0))
        
        self.qty_entry = tk.Entry(controls_frame, width=5, justify="center", font=("Arial", 12))
        self.qty_entry.pack(side=tk.LEFT, padx=5)
        self.qty_entry.bind("<Return>", lambda e: self.apply_manual_qty())
        
        tk.Button(controls_frame, text=" + ", command=lambda: self.adjust_qty(1), font=("Arial", 12, "bold"), width=4).pack(side=tk.LEFT, padx=(0, 15))

        # --- Separator (Visual spacer) ---
        ttk.Separator(controls_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # --- Price Section ---
        tk.Label(controls_frame, text="Set Total: ", bg="#e0e0e0").pack(side=tk.LEFT, padx=(15, 0))
        self.target_price_entry = tk.Entry(controls_frame, width=8)
        self.target_price_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Set", command=self.set_qty_by_price, bg="#2196F3", fg="white", width=4).pack(side=tk.LEFT)

        # --- Remove Button (Far Right) ---
        tk.Button(controls_frame, text="Remove", command=lambda: self.remove_from_cart(None), bg="#f44336", fg="white").pack(side=tk.RIGHT, padx=5)

        
        # --- Discount Section ---
        disc_frame = tk.Frame(bottom_frame, bg="#f9f9f9")
        disc_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(disc_frame, text="Discount:", bg="#f9f9f9").pack(side=tk.LEFT)
        self.disc_val_var = tk.StringVar(value="0")
        self.disc_val_entry = tk.Entry(disc_frame, textvariable=self.disc_val_var, width=5)
        self.disc_val_entry.pack(side=tk.LEFT, padx=5)
        self.disc_val_entry.bind("<Return>", self.calculate_totals)
        self.disc_val_entry.bind("<FocusOut>", self.calculate_totals)
        
        self.disc_type_var = tk.StringVar(value="Fixed")
        self.disc_type = ttk.Combobox(disc_frame, textvariable=self.disc_type_var, values=["Fixed", "%"], state="readonly", width=6)
        self.disc_type.pack(side=tk.LEFT, padx=5)
        self.disc_type.bind("<<ComboboxSelected>>", self.calculate_totals)
        
        tk.Button(disc_frame, text="Apply", command=self.calculate_totals, bg="#FFC107", width=6).pack(side=tk.LEFT, padx=5)

        self.total_label = tk.Label(bottom_frame, text="Subtotal: 0.00\nDiscount: -0.00\nTotal: 0.00", font=("Arial", 16, "bold"), fg="#D32F2F", bg="#f9f9f9", justify=tk.RIGHT)
        self.total_label.pack(side=tk.TOP, pady=10, anchor="e")
        
        tk.Label(bottom_frame, text="Payment Method:", bg="#f9f9f9").pack(anchor="w")
        self.payment_method = ttk.Combobox(bottom_frame, values=["Cash", "Card", "Online"], state="readonly")
        self.payment_method.set("Cash")
        self.payment_method.pack(fill=tk.X)
        
        tk.Button(bottom_frame, text="CHECKOUT", command=self.checkout, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2).pack(fill=tk.X, pady=15)

    def set_qty_by_price(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item in the cart first.")
            return
            
        try:
            target_total = float(self.target_price_entry.get())
            if target_total <= 0: return
            
            p_id = self.cart_tree.item(selected[0])["values"][0] # Hidden ID
            
            for item in self.cart:
                if item["id"] == p_id:
                    # Calculate new quantity: Total / Unit Price
                    new_qty = target_total / item["price"]
                    
                    # Check stock logic if needed (Assuming stock is float)
                    product = next((p for p in self.all_products if p["id"] == p_id), None)
                    if product and new_qty > float(product["stock_quantity"]):
                         messagebox.showwarning("Stock Limit", f"Insufficient stock. Max: {product['stock_quantity']}")
                         return

                    item["qty"] = new_qty
                    item["total"] = target_total
                    break
            
            self.refresh_cart()
            self.target_price_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid Price Amount")

    def load_products(self):
        # Store full list for filtering
        self.all_products = self.db.get_all_products()
        
        # Extract unique categories for filter
        categories = sorted(list(set(p["category"] for p in self.all_products if p["category"])))
        self.cat_filter['values'] = ["All"] + categories
        
        self.update_product_list(self.all_products)

    def update_product_list(self, products):
        for item in self.prod_tree.get_children():
            self.prod_tree.delete(item)
        for i, p in enumerate(products):
            tag = 'even' if i % 2 == 0 else 'odd'
            self.prod_tree.insert("", tk.END, values=(p["id"], p["name"], f"{p['price']:.2f}", f"{p['stock_quantity']:.2f}"), tags=(tag,))

    def filter_products(self, *args):
        query = self.search_var.get().lower()
        cat_filter = self.cat_filter_var.get()
        
        filtered = []
        for p in self.all_products:
            match_query = query in p["name"].lower() or query in str(p["sku"]).lower()
            match_cat = (cat_filter == "All") or (p["category"] == cat_filter)
            
            if match_query and match_cat:
                filtered.append(p)
                
        self.update_product_list(filtered)

    def add_to_cart(self, event):
        selected = self.prod_tree.selection()
        if not selected: return
        
        item_vals = self.prod_tree.item(selected[0])["values"]
        p_id, name, price, stock = item_vals
        
        # Convert to correct types
        price = float(price)
        stock = float(stock) # Allow fractional stock
        
        # Check if already in cart
        for item in self.cart:
            if item["id"] == p_id:
                if item["qty"] + 1 <= stock: # Check against stock
                    item["qty"] += 1.0
                    item["total"] = item["qty"] * price
                    self.refresh_cart()
                else:
                    messagebox.showwarning("Stock Limit", "Not enough stock available!")
                return

        if stock > 0:
            self.cart.append({
                "id": p_id,
                "name": name,
                "price": price,
                "qty": 1.0,
                "total": price
            })
            self.refresh_cart()
        else:
             messagebox.showwarning("Out of Stock", "This item is out of stock.")

    def adjust_qty(self, delta):
        selected = self.cart_tree.selection()
        if not selected: 
             # Optionally warn only if user clicked a button, but ignore silently is fine too
             return
        
        item_vals = self.cart_tree.item(selected[0])["values"]
        # sys_id is hidden at index 0 (if visible index might shift but we kept it index 0)
        # Note: values tuple usually returns strings for numbers.
        p_id = item_vals[0]
        
        for i, item in enumerate(self.cart):
            if item["id"] == p_id:
                new_qty = item["qty"] + delta
                
                # Check stock limit if adding
                if delta > 0:
                     # We need to find the product stock again
                     product = next((p for p in self.all_products if p["id"] == p_id), None)
                     if product and new_qty > product["stock_quantity"]:
                         messagebox.showwarning("Stock Limit", f"Only {product['stock_quantity']} in stock.")
                         return

                if new_qty > 0:
                    item["qty"] = new_qty
                    item["total"] = item["qty"] * item["price"]
                else:
                    # If qty becomes 0, remove it
                    self.cart.pop(i)
                    p_id = None # Don't select if removed
                break
        self.refresh_cart(selected_id=p_id)
        
        # Update entry if item still exists
        updated_item = next((i for i in self.cart if i["id"] == p_id), None)
        if updated_item:
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, str(updated_item["qty"]))
        else:
             self.qty_entry.delete(0, tk.END)

    def on_cart_select(self, event):
        selected = self.cart_tree.selection()
        if not selected: return
        
        item_vals = self.cart_tree.item(selected[0])["values"]
        # item_vals[3] is qty string from treeview
        # But better to get from self.cart source of truth
        p_id = item_vals[0]
        
        item = next((i for i in self.cart if i["id"] == p_id), None)
        if item:
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, str(item["qty"]))

    def apply_manual_qty(self):
        selected = self.cart_tree.selection()
        if not selected:
             messagebox.showwarning("Selection", "Please select an item in the cart.")
             return

        try:
             new_qty = float(self.qty_entry.get())
             if new_qty <= 0:
                 messagebox.showwarning("Invalid Quantity", "Quantity must be positive.")
                 return
        except ValueError:
             messagebox.showerror("Invalid Input", "Please enter a valid number.")
             return

        item_vals = self.cart_tree.item(selected[0])["values"]
        p_id = item_vals[0]

        for i, item in enumerate(self.cart):
            if item["id"] == p_id:
                # Check stock
                product = next((p for p in self.all_products if p["id"] == p_id), None)
                if product and new_qty > product["stock_quantity"]:
                        messagebox.showwarning("Stock Limit", f"Only {product['stock_quantity']} in stock.")
                        # Reset entry to current valid qty
                        self.qty_entry.delete(0, tk.END)
                        self.qty_entry.insert(0, str(item['qty']))
                        return
                
                item["qty"] = new_qty
                item["total"] = item["qty"] * item["price"]
                break
        
        self.refresh_cart(selected_id=p_id)

    def remove_from_cart(self, event):
        selected = self.cart_tree.selection()
        if not selected: return
        
        # Find item index
        item_vals = self.cart_tree.item(selected[0])["values"]
        p_id = item_vals[0]
        
        for i, item in enumerate(self.cart):
            if item["id"] == p_id:
                # User requested full removal (or we are simplifying behavior)
                self.cart.pop(i)
                p_id = None # item gone, clear selection
                break
        self.refresh_cart(selected_id=p_id)

    def refresh_cart(self, selected_id=None):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        total = 0.0
        for item in self.cart:
            # Display Qty with 2 decimals
            iid = self.cart_tree.insert("", tk.END, values=(item["id"], item["name"], item["price"], f"{item['qty']:.2f}", f"{item['total']:.2f}"))
            total += item["total"]
            
            if selected_id and item["id"] == selected_id:
                self.cart_tree.selection_set(iid)
                self.cart_tree.focus(iid)
        
        self.calculate_totals()

    def calculate_totals(self, event=None):
        subtotal = sum(item["total"] for item in self.cart)
        discount_val = 0.0
        self.discount_amt = 0.0
        
        try:
            val_str = self.disc_val_var.get()
            if val_str:
                discount_val = float(val_str)
        except ValueError:
            pass
            
        if self.disc_type_var.get() == "%":
            self.discount_amt = subtotal * (discount_val / 100)
        else: # Fixed
            self.discount_amt = discount_val
            
        total = subtotal - self.discount_amt
        if total < 0: total = 0
        
        self.total_label.config(text=f"Subtotal: {subtotal:.2f}\nDiscount: -{self.discount_amt:.2f}\nTotal: {total:.2f}")
        return subtotal, total

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add items to cart first.")
            return

        subtotal, total = self.calculate_totals()
        
        confirm = messagebox.askyesno("Confirm Sale", f"Subtotal: {subtotal:.2f}\nDiscount: {self.discount_amt:.2f}\nTotal: {total:.2f}\nProceed?")
        
        if confirm:
            # Prepare data for DB
            # items: (product_id, quantity, price_at_sale)
            sale_items = [(x["id"], x["qty"], x["price"]) for x in self.cart]
            
            cust_name = self.cust_name_var.get().strip()
            cust_contact = self.cust_contact_var.get().strip()
            
            sale_id = self.db.record_sale(self.user["id"], sale_items, total, self.payment_method.get(), self.discount_amt, cust_name, cust_contact)
            
            if sale_id:
                # Ask (optional) to print receipt
                if messagebox.askyesno("Print Receipt", "Do you want to print the receipt?"):
                    self.print_receipt(sale_id, subtotal, self.discount_amt, total, self.payment_method.get(), cust_name, cust_contact)
                
                messagebox.showinfo("Success", "Sale recorded successfully!")
                self.db.log_activity(self.user["id"], f"Recorded sale ID: {sale_id}, Total: {total:.2f}")
                self.cart = []
                self.refresh_cart()
                self.cust_name_var.set("")
                self.cust_contact_var.set("")
                self.load_products() # Refresh stock display
            else:
                messagebox.showerror("Error", "Failed to record sale.")
    def print_receipt(self, sale_id, subtotal, discount, total, method, cust_name="", cust_contact=""):
            WIDTH = 48  # SAFE width for Windows + 80mm printer
            SEP = "-" * WIDTH
        
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
            lines = [
                SEP,
                "PUNJAB AATA CHAKKI".center(WIDTH),
                "Trolly Adda, Near Gondal Market".center(WIDTH),
                "0335-5548775 | 0332-5596926".center(WIDTH),
                SEP,
                f"Date: {timestamp}",
                f"Sale ID: {sale_id}",
                f"Staff: {self.user['username']}",
                SEP,
                f"{'Item':<18}{'Qty':>6}{'Rate':>8}{'Amt':>8}",
                SEP
            ]
        
            for item in self.cart:
                name = item["name"][:18]        # HARD LIMIT to prevent wrapping
                qty = f"{item['qty']:.2f}"
                rate = f"{item['price']:.2f}"
                amt = f"{item['total']:.2f}"
        
                # ONE LINE PER ITEM — NO WRAP POSSIBLE
                lines.append(f"{name:<18}{qty:>6}{rate:>8}{amt:>8}")
        
            lines.extend([
                SEP,
                f"{'Subtotal:':<30}{subtotal:>18.2f}",
                f"{'Discount:':<30}-{discount:>17.2f}",
                f"{'TOTAL:':<30}{total:>18.2f}",
                f"Paid via: {method}",
                SEP,
                "Thank you for visiting!".center(WIDTH),
                SEP
            ])
        
            receipt_text = "\n".join(lines)
        
            filename = f"receipt_{sale_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(receipt_text)
        
            try:
                if os.name == "nt":
                    os.startfile(filename, "print")
                else:
                    os.system(f"lp {filename}")
            except Exception as e:
                print(f"Printing failed: {e}")
                pass

    # def print_receipt(self, sale_id, subtotal, discount, total, method, cust_name="", cust_contact=""):
    #         # Generate a text receipt with minimal width for thermal printer
    #         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
    #         # Using narrower formatting for thermal printer (80mm ~ 42 chars)
    #         # Reduced all widths and removed unnecessary spacing
    #         lines = [
    #             "-" * 15,
    #             "    PUNJAB AATA CHAKKI    ",
    #             "Trolly Adda, near Gondal",
    #             "  Market, Al-Noor Colony  ",
    #             "    Sector No. 3     ",
    #             "Contact: 0335-5548775",
    #             "        0332-5596926",
    #             "-" * 15,
    #             f"Date: {timestamp}",
    #             f"Sale ID: {sale_id}",
    #             f"Staff: {self.user['username']}"
    #         ]
            
    #         if cust_name:
    #             lines.append(f"Customer: {cust_name}")
    #         if cust_contact:
    #             lines.append(f"Contact: {cust_contact}")
                
    #         lines.append("-" * 15)
            
    #         # Narrower item formatting - reduced column widths
    #         lines.append(f"{'Item':<16} {'Qty':<6} {'Total':>8}")
    #         lines.append("-" * 15)
            
    #         for item in self.cart:
    #             # Truncate item name if too long
    #             item_name = item['name']
    #             if len(item_name) > 16:
    #                 item_name = item_name[:13] + "..."
                
    #             lines.append(f"{item_name:<16} {item['qty']:<6.2f} {item['total']:>8.2f}")
                
    #         lines.append("-" * 15)
            
    #         # Right-aligned totals in narrower format
    #         lines.append(f"Subtotal: {subtotal:>33.2f}")
    #         lines.append(f"Discount: -{discount:>31.2f}")
    #         lines.append(f"TOTAL: {total:>35.2f}")
    #         lines.append(f"Paid via: {method}")
    #         lines.append("-" * 15)
    #         lines.append("  Thank you for visiting!  ")
    #         lines.append("-" * 15)
            
    #         receipt_text = "\n".join(lines)
            
    #         # Save to file
    #         filename = f"receipt_{sale_id}.txt"
    #         with open(filename, "w") as f:
    #             f.write(receipt_text)
                
    #         # Try to print (Platform specific)
    #         try:
    #             if os.name == "nt": # Windows
    #                 os.startfile(filename, "print")
    #             else: # Linux
    #                 # Using lp command with smaller font options if supported
    #                 # Try to use condensed mode or smaller font
    #                 os.system(f"lp -o cpi=12 -o lpi=8 {filename}")
    #         except Exception as e:
    #             print(f"Printing failed: {e}")
    #             # Fallback: Just show it was saved
    #             pass
    # def print_receipt(self, sale_id, subtotal, discount, total, method, cust_name="", cust_contact=""):
    #     # Generate a text receipt
    #     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     lines = [
    #         "--------------------------------",
    #         "       PUNJAB AATA CHAKKI       ",
    #         "   Trolly Adda, near Gondal Market,  ",
    #         "    Al-Noor Colony Sector No. 3     ",
    #         " Contact: 0335-5548775, 0332-5596926 ",
    #         "--------------------------------",
    #         f"Date: {timestamp}",
    #         f"Sale ID: {sale_id}",
    #         f"Staff: {self.user['username']}"
    #     ]
        
    #     if cust_name:
    #         lines.append(f"Customer: {cust_name}")
    #     if cust_contact:
    #         lines.append(f"Contact: {cust_contact}")
            
    #     lines.append("--------------------------------")
    #     lines.append(f"{'Item':<20} {'Qty':<5} {'Total'}")
        
    #     for item in self.cart:
    #         lines.append(f"{item['name']:<20} {item['qty']:<5.2f} {item['total']:.2f}")
            
    #     lines.append("--------------------------------")
    #     lines.append(f"Subtotal: {subtotal:.2f}")
    #     lines.append(f"Discount: -{discount:.2f}")
    #     lines.append(f"TOTAL:    {total:.2f}")
    #     lines.append(f"Paid via: {method}")
    #     lines.append("--------------------------------")
    #     lines.append("      Thank you for visiting!   ")
    #     lines.append("--------------------------------")
        
    #     receipt_text = "\n".join(lines)
        
    #     # Save to file
    #     filename = f"receipt_{sale_id}.txt"
    #     with open(filename, "w") as f:
    #         f.write(receipt_text)
            
    #     # Try to print (Platform specific)
    #     try:
    #         if os.name == "nt": # Windows
    #             os.startfile(filename, "print")
    #         else: # Linux
    #             # Using lp command
    #             os.system(f"lp {filename}")
    #     except Exception as e:
    #         print(f"Printing failed: {e}")
    #         # Fallback: Just show it was saved
    #         pass
