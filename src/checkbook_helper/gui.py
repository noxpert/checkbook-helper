import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import ttk

from checkbook_helper.backend import CheckbookLedger


class CheckbookApp:
    def __init__(self, root, ledger=None):
        self.root = root
        self.root.title("Checkbook Calculator")
        self.root.geometry("900x900")

        self.ledger = ledger or CheckbookLedger()
        self._editing_index = None
        self._tree_entry_index = {}

        self.scale_fonts(2)
        self.configure_styles()
        self.setup_ui()
        self.bind_shortcuts()

    def scale_fonts(self, factor):
        font_names = (
            "TkDefaultFont",
            "TkTextFont",
            "TkFixedFont",
            "TkMenuFont",
            "TkHeadingFont",
            "TkCaptionFont",
            "TkSmallCaptionFont",
            "TkIconFont",
        )
        for name in font_names:
            try:
                font = tkfont.nametofont(name)
            except tk.TclError:
                continue
            size = font.cget("size")
            new_size = int(size * factor)
            if new_size == 0:
                new_size = size
            font.configure(size=new_size)

    def configure_styles(self):
        style = ttk.Style(self.root)
        style.configure("Treeview", rowheight=36)
        button_font = tkfont.nametofont("TkDefaultFont").copy()
        heading_font = tkfont.nametofont("TkHeadingFont").copy()
        button_font.configure(size=self.halve_font_size(button_font.cget("size")))
        heading_font.configure(size=self.halve_font_size(heading_font.cget("size")))
        style.configure("TButton", padding=(12, 0), font=button_font)
        style.configure("Treeview.Heading", font=heading_font)
        style.configure("TLabelframe", padding=12)
        style.configure("TLabelframe.Label", padding=(6, 4))
        self.button_ipady = self.calculate_button_ipady(69, button_font)

    def halve_font_size(self, size):
        if size == 0:
            return size
        new_size = int(size / 2)
        if new_size == 0:
            return 1 if size > 0 else -1
        return new_size

    def calculate_button_ipady(self, target_height_px, button_font):
        text_height = button_font.metrics("linespace")
        ipady = int((target_height_px - text_height) / 2)
        return max(0, ipady)

    def bind_shortcuts(self):
        self.root.bind_all("<Control-Return>", self.handle_add_shortcut)
        self.root.bind_all("<Control-plus>", self.handle_add_type_shortcut)
        self.root.bind_all("<Control-equal>", self.handle_add_type_shortcut)
        self.root.bind_all("<Control-Shift-equal>", self.handle_add_type_shortcut)
        self.root.bind_all("<Control-Key-plus>", self.handle_add_type_shortcut)
        self.root.bind_all("<Control-KP_Add>", self.handle_add_type_shortcut)
        self.root.bind_all("<Control-minus>", self.handle_subtract_type_shortcut)
        self.root.bind_all("<Control-KP_Subtract>", self.handle_subtract_type_shortcut)

    def setup_ui(self):
        balance_frame = ttk.LabelFrame(self.root, text="Starting Balance", padding=12)
        balance_frame.pack(fill="x", padx=15, pady=12)

        ttk.Label(balance_frame, text="Starting Amount:").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.starting_balance = tk.StringVar(value="0.00")
        balance_entry = ttk.Entry(
            balance_frame, textvariable=self.starting_balance, width=15
        )
        balance_entry.grid(row=0, column=1, padx=5)

        ttk.Button(balance_frame, text="Update", command=self.update_totals).grid(
            row=0, column=2, padx=5, ipady=self.button_ipady
        )

        entry_frame = ttk.LabelFrame(self.root, text="Add Transaction", padding=12)
        entry_frame.pack(fill="x", padx=15, pady=12)

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
            row=3, column=1, pady=10, sticky="w", ipady=self.button_ipady
        )
        ttk.Button(entry_frame, text="Edit Selected", command=self.edit_selected).grid(
            row=3, column=2, pady=10, sticky="w", ipady=self.button_ipady
        )
        ttk.Button(entry_frame, text="Save Edit", command=self.save_edit).grid(
            row=3, column=3, pady=10, sticky="w", ipady=self.button_ipady
        )

        results_frame = ttk.LabelFrame(
            self.root, text="Transactions & Running Total", padding=12
        )
        results_frame.pack(fill="both", expand=True, padx=15, pady=12)

        columns = ("Description", "Amount", "Running Total")
        self.tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Running Total", text="Running Total")

        self.tree.column("Description", width=320)
        self.tree.column("Amount", width=140, anchor="e")
        self.tree.column("Running Total", width=180, anchor="e")

        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=15, pady=10)
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(
            side="left", padx=6, ipady=self.button_ipady
        )
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(
            side="left", padx=6, ipady=self.button_ipady
        )
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(
            side="right", padx=6, ipady=self.button_ipady
        )

    def handle_add_shortcut(self, event):
        self.add_entry()

    def handle_add_type_shortcut(self, event):
        self.type_var.set("add")

    def handle_subtract_type_shortcut(self, event):
        self.type_var.set("subtract")

    def show_help(self):
        message = (
            "1) Enter a description and amount.\n"
            "2) Choose Add (+) or Subtract (-).\n"
            "3) Click Add Entry (or press Ctrl+Enter).\n"
            "4) Select a row to edit or delete it.\n"
            "5) Update the starting balance and click Update."
        )
        messagebox.showinfo("How to Use", message)

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

    def edit_selected(self):
        index = self.get_selected_entry_index()
        if index is None:
            return
        entry = self.ledger.entries[index]
        self.description_var.set(entry["description"])
        self.amount_var.set(f"{entry['amount']:.2f}")
        self.type_var.set(entry["type"])
        self._editing_index = index

    def save_edit(self):
        if self._editing_index is None:
            return
        try:
            self.ledger.update_entry(
                self._editing_index,
                self.description_var.get(),
                self.amount_var.get(),
                self.type_var.get(),
            )
            self.description_var.set("")
            self.amount_var.set("")
            self._editing_index = None
            self.update_totals()
        except Exception as exc:
            print(f"Error saving entry: {exc}")

    def delete_selected(self):
        index = self.get_selected_entry_index()
        if index is None:
            return
        try:
            self.ledger.delete_entry(index)
            if self._editing_index == index:
                self._editing_index = None
                self.description_var.set("")
                self.amount_var.set("")
            elif self._editing_index is not None and self._editing_index > index:
                self._editing_index -= 1
            self.update_totals()
        except Exception as exc:
            print(f"Error deleting entry: {exc}")

    def get_selected_entry_index(self):
        selection = self.tree.selection()
        if not selection:
            return None
        iid = selection[0]
        return self._tree_entry_index.get(iid)

    def update_totals(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._tree_entry_index = {}

        try:
            self.ledger.set_starting_balance(self.starting_balance.get())
            for row in self.ledger.build_display_rows():
                if row["entry_index"] is None:
                    iid = "starting-balance"
                else:
                    iid = f"entry-{row['entry_index']}"
                self.tree.insert(
                    "",
                    "end",
                    iid=iid,
                    values=(row["description"], row["amount"], row["running_total"]),
                )
                self._tree_entry_index[iid] = row["entry_index"]
        except Exception as exc:
            print(f"Error updating totals: {exc}")

    def clear_all(self):
        self.ledger.clear()
        self.update_totals()
