import tkinter as tk
from tkinter import ttk
from ui.login import LoginWindow

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide the main root initially
        
        # Configure Styles
        style = ttk.Style()
        style.theme_use('clam') # 'clam' usually looks better on Linux than default
        style.configure("Treeview", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        self.current_user = None
        self.show_login()
        
        self.root.mainloop()

    def show_login(self):
        # We use Toplevel for login or just a separate window logic
        # But simpler: use the root as the container manager
        
        # Create a Toplevel for login so we can destroy it easily
        self.login_root = tk.Toplevel(self.root)
        self.login_frame = LoginWindow(self.login_root, self.on_login_success)
        
        # Force focus
        self.login_root.grab_set()
        
        # Handle close: if login is closed without success, exit app
        self.login_root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def on_login_success(self, user):
        self.current_user = user
        print(f"Logged in as: {user['username']} ({user['role']})")
        
        self.login_root.destroy()
        self.root.deiconify() # Show main window container
        self.root.title(f"Punjab Aata Chakki - {user['role'].title()} Mode")
        self.root.geometry("1024x768")
        try:
            self.root.attributes('-zoomed', True) # Maximize on Linux
        except:
            self.root.state('zoomed') # Maximize on Windows fallback
        
        from ui.main_window import MainWindow
        self.main_window = MainWindow(self.root, self.current_user, self.logout)

    def logout(self):
        self.current_user = None
        self.root.withdraw()
        # Destroy all children of root to clear the dashboard
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_login()

if __name__ == "__main__":
    App()
