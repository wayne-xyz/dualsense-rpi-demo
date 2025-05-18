import tkinter as tk
from tkinter import ttk, messagebox

class PinCodeSetterWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Set PIN Code")
        
        # PIN entry variables
        self.pin_var = tk.StringVar()
        self.confirm_pin_var = tk.StringVar()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create PIN entry fields
        ttk.Label(self.main_frame, text="Enter New PIN:").grid(row=0, column=0, columnspan=3, pady=5)
        self.pin_entry = ttk.Entry(self.main_frame, textvariable=self.pin_var, justify='center', show='*')
        self.pin_entry.grid(row=1, column=0, columnspan=3, pady=5, padx=10, sticky=(tk.W, tk.E))
        
        ttk.Label(self.main_frame, text="Confirm PIN:").grid(row=2, column=0, columnspan=3, pady=5)
        self.confirm_entry = ttk.Entry(self.main_frame, textvariable=self.confirm_pin_var, justify='center', show='*')
        self.confirm_entry.grid(row=3, column=0, columnspan=3, pady=5, padx=10, sticky=(tk.W, tk.E))
        
        # Create numeric buttons
        self.create_number_pad()
        
        # Create control buttons
        self.enter_btn = ttk.Button(self.main_frame, text="Set PIN", command=self.set_pin)
        self.enter_btn.grid(row=7, column=1, pady=5)
        
        self.clear_btn = ttk.Button(self.main_frame, text="Clear", command=self.clear_pin)
        self.clear_btn.grid(row=7, column=2, pady=5)

    def create_number_pad(self):
        # Numbers 1-9
        numbers = [(i+1) for i in range(9)]
        for i, num in enumerate(numbers):
            row = (i // 3) + 4
            col = i % 3
            btn = ttk.Button(self.main_frame, text=str(num), 
                           command=lambda n=num: self.add_number(n))
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Number 0
        btn_0 = ttk.Button(self.main_frame, text="0", 
                          command=lambda: self.add_number(0))
        btn_0.grid(row=7, column=0, padx=5, pady=5)

    def add_number(self, number):
        if self.pin_entry is self.window.focus_get():
            current = self.pin_var.get()
            self.pin_var.set(current + str(number))
        elif self.confirm_entry is self.window.focus_get():
            current = self.confirm_pin_var.get()
            self.confirm_pin_var.set(current + str(number))

    def clear_pin(self):
        self.pin_var.set("")
        self.confirm_pin_var.set("")

    def set_pin(self):
        pin = self.pin_var.get()
        confirm_pin = self.confirm_pin_var.get()
        
        if pin == confirm_pin and pin != "":
            global STORED_PIN
            STORED_PIN = pin
            messagebox.showinfo("Success", "PIN has been set successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "PINs do not match or are empty!")
            self.clear_pin()

class PinCodeVerifierWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Verify PIN Code")
        
        # PIN entry variable
        self.pin_var = tk.StringVar()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create PIN entry field
        ttk.Label(self.main_frame, text="Enter PIN:").grid(row=0, column=0, columnspan=3, pady=5)
        self.pin_entry = ttk.Entry(self.main_frame, textvariable=self.pin_var, justify='center', show='*')
        self.pin_entry.grid(row=1, column=0, columnspan=3, pady=5, padx=10, sticky=(tk.W, tk.E))
        
        # Create numeric buttons
        self.create_number_pad()
        
        # Create control buttons
        self.enter_btn = ttk.Button(self.main_frame, text="Verify", command=self.verify_pin)
        self.enter_btn.grid(row=5, column=1, pady=5)
        
        self.clear_btn = ttk.Button(self.main_frame, text="Clear", command=self.clear_pin)
        self.clear_btn.grid(row=5, column=2, pady=5)

    def create_number_pad(self):
        # Numbers 1-9
        numbers = [(i+1) for i in range(9)]
        for i, num in enumerate(numbers):
            row = (i // 3) + 2
            col = i % 3
            btn = ttk.Button(self.main_frame, text=str(num), 
                           command=lambda n=num: self.add_number(n))
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Number 0
        btn_0 = ttk.Button(self.main_frame, text="0", 
                          command=lambda: self.add_number(0))
        btn_0.grid(row=5, column=0, padx=5, pady=5)

    def add_number(self, number):
        current = self.pin_var.get()
        self.pin_var.set(current + str(number))

    def clear_pin(self):
        self.pin_var.set("")

    def verify_pin(self):
        pin = self.pin_var.get()
        if pin == STORED_PIN:
            messagebox.showinfo("Success", "PIN verified successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Incorrect PIN!")
            self.clear_pin()

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Playsense ID PIN Code System")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons with larger size
        ttk.Button(self.main_frame, text="Set PIN Code", 
                  command=self.open_setter, width=80).grid(row=0, column=0, pady=20, padx=20)
        
        ttk.Button(self.main_frame, text="Verify PIN Code", 
                  command=self.open_verifier, width=80).grid(row=1, column=0, pady=20, padx=20)

    def open_setter(self):
        PinCodeSetterWindow()

    def open_verifier(self):
        if 'STORED_PIN' not in globals():
            messagebox.showerror("Error", "Please set a PIN first!")
            return
        PinCodeVerifierWindow()

# Global variable to store the PIN
STORED_PIN = None

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
