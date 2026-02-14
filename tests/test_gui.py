import os
import sys

import pytest
import tkinter as tk

from checkbook_helper.backend import CheckbookLedger
from checkbook_helper.gui import CheckbookApp


def _tk_available():
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        return False
    return True


@pytest.fixture
def tk_root():
    if not _tk_available():
        pytest.skip("Tk display not available")
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def app(tk_root):
    ledger = CheckbookLedger()
    return CheckbookApp(tk_root, ledger=ledger)


def test_gui_add_entry_updates_tree(app):
    app.starting_balance.set("100.00")
    app.description_var.set("Coffee")
    app.amount_var.set("2.50")
    app.type_var.set("subtract")

    app.add_entry()

    rows = [app.tree.item(item)["values"] for item in app.tree.get_children()]
    assert rows[0] == ["Starting Balance", "100.00", "100.00"]
    assert rows[1] == ["Coffee", "-2.50", "97.50"]


def test_gui_clear_all_resets_entries(app):
    app.starting_balance.set("25.00")
    app.description_var.set("Deposit")
    app.amount_var.set("10.00")
    app.type_var.set("add")
    app.add_entry()

    app.clear_all()

    rows = [app.tree.item(item)["values"] for item in app.tree.get_children()]
    assert rows == [["Starting Balance", "25.00", "25.00"]]
