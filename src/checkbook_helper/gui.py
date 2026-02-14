import tkinter as tk
from tkinter import ttk

from checkbook_helper.backend import CheckbookLedger


class CheckbookApp:
    def __init__(self, root, ledger=None):
        self.root = root
        self.root.title("Checkbook Calculator")
        self.root.geometry("600x500")

        self.ledger = ledger or CheckbookLedger()

        self.setup_ui()

    def setup_ui(self):
        balance_frame = ttk.LabelFrame(self.root, text="Starting Balance", padding=10)
        balance_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(balance_frame, text="Starting Amount:").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.starting_balance = tk.StringVar(value="0.00")
        balance_entry = ttk.Entry(
            balance_frame, textvariable=self.starting_balance, width=15
        )
        balance_entry.grid(row=0, column=1, padx=5)

        ttk.Button(balance_frame, text="Update", command=self.update_totals).grid(
            row=0, column=2, padx=5
        )

        entry_frame = ttk.LabelFrame(self.root, text="Add Transaction", padding=10)
        entry_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(entry_frame, text="Description:").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.description_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.description_var, width=30).grid(
            row=0, column=1, padx=5
        )

        ttk.Label(entry_frame, text="Amount:").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.amount_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.amount_var, width=15).grid(
            row=1, column=1, padx=5, sticky="w"
        )

        ttk.Label(entry_frame, text="Type:").grid(
            row=2, column=0, sticky="w", padx=5
        )
        self.type_var = tk.StringVar(value="subtract")
        ttk.Radiobutton(
            entry_frame, text="Add (+)", variable=self.type_var, value="add"
        ).grid(row=2, column=1, sticky="w", padx=5)
        ttk.Radiobutton(
            entry_frame, text="Subtract (-)", variable=self.type_var, value="subtract"
        ).grid(row=2, column=2, sticky="w")

        ttk.Button(entry_frame, text="Add Entry", command=self.add_entry).grid(
            row=3, column=1, pady=10
        )

        results_frame = ttk.LabelFrame(
            self.root, text="Transactions & Running Total", padding=10
        )
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Description", "Amount", "Running Total")
        self.tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Running Total", text="Running Total")

        self.tree.column("Description", width=250)
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Running Total", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(
            side="right"
        )

    def add_entry(self):
        try:
            self.ledger.add_entry(
                self.description_var.get(),
                self.amount_var.get(),
                self.type_var.get(),
            )
            self.description_var.set("")
            self.amount_var.set("")
            self.update_totals()
        except Exception as exc:
            print(f"Error adding entry: {exc}")

    def update_totals(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.ledger.set_starting_balance(self.starting_balance.get())
            for row in self.ledger.build_display_rows():
                self.tree.insert(
                    "", "end", values=(row["description"], row["amount"], row["running_total"])
                )
        except Exception as exc:
            print(f"Error updating totals: {exc}")

    def clear_all(self):
        self.ledger.clear()
        self.update_totals()
