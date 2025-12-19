import sqlite3
import hashlib
import os

DB_NAME = "punjab_chakki.db"

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.seed_data()

    def connect(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Users Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL  -- 'owner' or 'worker'
            )
        """)

        # Products Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT UNIQUE,
                price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                category TEXT,
                low_stock_threshold INTEGER DEFAULT 10
            )
        """)

        # Sales Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                discount REAL DEFAULT 0.0,
                payment_method TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Sale Items Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price_at_sale REAL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        self.conn.commit()
        
        # Migration: Add discount column if not exists
        try:
             self.cursor.execute("SELECT discount FROM sales LIMIT 1")
        except sqlite3.OperationalError:
             print("Migrating: Adding discount column to sales table...")
             self.cursor.execute("ALTER TABLE sales ADD COLUMN discount REAL DEFAULT 0.0")
             self.conn.commit()

    def seed_data(self):
        # Check if users exist code
        self.cursor.execute("SELECT count(*) FROM users")
        if self.cursor.fetchone()[0] == 0:
            print("Seeding initial users...")
            # Default Owner: admin / admin123
            self.add_user("admin", "admin123", "owner")
            # Default Worker: worker / worker123
            self.add_user("worker", "worker123", "worker")
        
        # Check if products exist (Optional: Seed a few sample products)
        self.cursor.execute("SELECT count(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
             print("Seeding sample products...")
             self.add_product("Wheat Flour (10kg)", "WF10", 500, 100, "Flour", 20)
             self.add_product("Rice (1kg)", "RI01", 150, 50, "Grains", 10)

    def add_user(self, username, password, role):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                (username, password_hash, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        return self.cursor.fetchone()

    # --- Product Helpers ---
    def add_product(self, name, sku, price, stock, category, threshold):
        try:
            self.cursor.execute("INSERT INTO products (name, sku, price, stock_quantity, category, low_stock_threshold) VALUES (?, ?, ?, ?, ?, ?)",
                                (name, sku, price, stock, category, threshold))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def update_stock(self, product_id, quantity_change):
        # quantity_change can be positive (add stock) or negative (sale)
        self.cursor.execute("UPDATE products SET stock_quantity = stock_quantity + ? WHERE id = ?", (quantity_change, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    def update_product_complete(self, product_id, name, sku, price, stock, category, threshold):
         self.cursor.execute("""
            UPDATE products 
            SET name=?, sku=?, price=?, stock_quantity=?, category=?, low_stock_threshold=?
            WHERE id=?
         """, (name, sku, price, stock, category, threshold, product_id))
         self.conn.commit()


    # --- Sales Helpers ---
    def record_sale(self, user_id, items, total_amount, payment_method, discount=0.0):
        # items is a list of tuples: (product_id, quantity, price_at_sale)
        try:
            self.cursor.execute("INSERT INTO sales (user_id, total_amount, payment_method, discount) VALUES (?, ?, ?, ?)",
                                (user_id, total_amount, payment_method, discount))
            sale_id = self.cursor.lastrowid
            
            for item in items:
                p_id, qty, price = item
                self.cursor.execute("INSERT INTO sale_items (sale_id, product_id, quantity, price_at_sale) VALUES (?, ?, ?, ?)",
                                    (sale_id, p_id, qty, price))
                # Update stock
                self.update_stock(p_id, -qty)
            
            self.conn.commit()
            return sale_id
        except Exception as e:
            print(f"Error recording sale: {e}")
            self.conn.rollback()
            return None

    def get_sales_report(self, filter_type="all"):
        # Basic reporting placeholder
        query = "SELECT * FROM sales ORDER BY timestamp DESC"
        # In a real app, I'd add date filtering logic here based on filter_type
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    print("Database initialized.")
