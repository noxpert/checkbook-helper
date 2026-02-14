#!/usr/bin/env python3
"""
Simple Checkbook Calculator
A basic GUI application for tracking checkbook balance with running totals.
"""

import tkinter as tk
from tkinter import ttk
from decimal import Decimal, ROUND_HALF_UP


class CheckbookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkbook Calculator")
        self.root.geometry("600x500")
        
        # Store entries as list of [description, amount, type]
        self.entries = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Starting balance section
        balance_frame = ttk.LabelFrame(self.root, text="Starting Balance", padding=10)
        balance_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(balance_frame, text="Starting Amount:").grid(row=0, column=0, sticky="w", padx=5)
        self.starting_balance = tk.StringVar(value="0.00")
        balance_entry = ttk.Entry(balance_frame, textvariable=self.starting_balance, width=15)
        balance_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(balance_frame, text="Update", command=self.update_totals).grid(row=0, column=2, padx=5)
        
        # Entry section
        entry_frame = ttk.LabelFrame(self.root, text="Add Transaction", padding=10)
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(entry_frame, text="Description:").grid(row=0, column=0, sticky="w", padx=5)
        self.description_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.description_var, width=30).grid(row=0, column=1, padx=5)
        
        ttk.Label(entry_frame, text="Amount:").grid(row=1, column=0, sticky="w", padx=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.amount_var, width=15).grid(row=1, column=1, padx=5, sticky="w")
        
        ttk.Label(entry_frame, text="Type:").grid(row=2, column=0, sticky="w", padx=5)
        self.type_var = tk.StringVar(value="subtract")
        ttk.Radiobutton(entry_frame, text="Add (+)", variable=self.type_var, value="add").grid(row=2, column=1, sticky="w", padx=5)
        ttk.Radiobutton(entry_frame, text="Subtract (-)", variable=self.type_var, value="subtract").grid(row=2, column=2, sticky="w")
        
        ttk.Button(entry_frame, text="Add Entry", command=self.add_entry).grid(row=3, column=1, pady=10)
        
        # Results section
        results_frame = ttk.LabelFrame(self.root, text="Transactions & Running Total", padding=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for displaying entries
        columns = ("Description", "Amount", "Running Total")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Running Total", text="Running Total")
        
        self.tree.column("Description", width=250)
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Running Total", width=120, anchor="e")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Clear button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side="right")
        
    def add_entry(self):
        """Add a new entry and update the display"""
        try:
            description = self.description_var.get().strip()
            if not description:
                description = "Transaction"
            
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                return
            
            # Parse and validate amount
            amount = Decimal(amount_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            entry_type = self.type_var.get()
            
            # Store the entry
            self.entries.append({
                'description': description,
                'amount': amount,
                'type': entry_type
            })
            
            # Clear input fields
            self.description_var.set("")
            self.amount_var.set("")
            
            # Update display
            self.update_totals()
            
        except Exception as e:
            # In a real app, you'd show this in a message box
            print(f"Error adding entry: {e}")
    
    def update_totals(self):
        """Recalculate and display all running totals"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Get starting balance
            running_total = Decimal(self.starting_balance.get()).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            
            # Add starting balance row
            self.tree.insert("", "end", values=(
                "Starting Balance",
                f"{running_total:.2f}",
                f"{running_total:.2f}"
            ))
            
            # Process each entry
            for entry in self.entries:
                amount = entry['amount']
                if entry['type'] == 'add':
                    running_total += amount
                    amount_display = f"+{amount:.2f}"
                else:
                    running_total -= amount
                    amount_display = f"-{amount:.2f}"
                
                self.tree.insert("", "end", values=(
                    entry['description'],
                    amount_display,
                    f"{running_total:.2f}"
                ))
                
        except Exception as e:
            print(f"Error updating totals: {e}")
    
    def clear_all(self):
        """Clear all entries"""
        self.entries = []
        self.update_totals()


def main():
    root = tk.Tk()
    app = CheckbookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
