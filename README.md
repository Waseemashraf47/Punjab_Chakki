# Punjab Aata Chakki Management System

A comprehensive shop management solution for inventory tracking, sales processing (POS), and reporting.

## Key Functionalities

### 1. Point of Sale (POS) & Checkout
- **Product Search**: Quickly find products by name or SKU.
- **Category Filtering**: Filter products by category (Flour, Grains, etc.).
- **Smart Cart**: 
    - Adjust quantities using +/- buttons or manual entry.
    - Set quantity automatically based on a target total price (e.g., "Give me 500 Rs worth of flour").
- **Checkout**:
    - Record customer details (Name & Contact).
    - Apply discounts (Fixed amount or Percentage).
    - Support for multiple payment methods (Cash, Card, Online).
    - Automatic receipt generation and printing (saved as `.txt` files).

### 2. Inventory Management
- **Add & Update Products**: Manage names, SKUs, categories, prices, and stock levels.
- **Low Stock Alerts**: Visual indicators (red highlighting) for products below the low-stock threshold.
- **Real-time Synchronization**: Stock is automatically deducted when a sale is completed at the POS.

### 3. User Management & Security
- **Role-Based Access Control**:
    - **Owner**: Full access to all features, including deleting users and changing passwords.
    - **Admin**: Can manage inventory, check reports, and create/manage **Worker** accounts. Cannot create other admins.
    - **Worker**: Access limited to the POS system.
- **Security**: Passwords are securely hashed (SHA-256) in the database.
- **Data Persistence**: Sales and activities are preserved even if the associated user account is deleted.

### 4. Reports & Analytics
- **Sales History**: Filterable by Date ranges (Today, This Week, This Month).
- **Seller Tracking**: Every sale records the name of the seller who processed it.
- **Export**: Export sales data to CSV for external analysis.

### 5. Activity Logs
- **Audit Trail**: Monitors critical actions across the system.
- **Transparency**: Logs include who added a product, who changed a password, and who deleted a user.

## System Requirements
- OS: Linux (optimized for Ubuntu) or Windows.
- Python 3.8+
- SQLite3 (Included)

## Getting Started
1. Run `python3 main.py`.
2. Login with your credentials.
3. The application will automatically maximize for the best user experience.
