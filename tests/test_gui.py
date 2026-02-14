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


def test_gui_edit_entry_updates_tree(app):
    app.starting_balance.set("20.00")
    app.description_var.set("Lunch")
    app.amount_var.set("5.00")
    app.type_var.set("subtract")
    app.add_entry()

    app.tree.selection_set("entry-0")
    app.edit_selected()
    assert app.description_var.get() == "Lunch"

    app.description_var.set("Dinner")
    app.amount_var.set("7.50")
    app.save_edit()

    rows = [app.tree.item(item)["values"] for item in app.tree.get_children()]
    assert rows[1] == ["Dinner", "-7.50", "12.50"]


def test_gui_delete_entry_updates_tree(app):
    app.starting_balance.set("30.00")
    app.description_var.set("A")
    app.amount_var.set("10.00")
    app.type_var.set("subtract")
    app.add_entry()

    app.description_var.set("B")
    app.amount_var.set("5.00")
    app.add_entry()

    app.tree.selection_set("entry-0")
    app.delete_selected()

    rows = [app.tree.item(item)["values"] for item in app.tree.get_children()]
    assert rows[1] == ["B", "-5.00", "25.00"]


def test_gui_keyboard_shortcuts(app):
    app.type_var.set("subtract")
    app.handle_add_type_shortcut(None)
    assert app.type_var.get() == "add"

    app.handle_subtract_type_shortcut(None)
    assert app.type_var.get() == "subtract"

    app.starting_balance.set("10.00")
    app.description_var.set("Snack")
    app.amount_var.set("2.00")
    app.handle_add_shortcut(None)

    rows = [app.tree.item(item)["values"] for item in app.tree.get_children()]
    assert rows[1] == ["Snack", "-2.00", "8.00"]


def test_gui_help_dialog(app, monkeypatch):
    captured = {}

    def fake_showinfo(title, message):
        captured["title"] = title
        captured["message"] = message

    monkeypatch.setattr("checkbook_helper.gui.messagebox.showinfo", fake_showinfo)
    app.show_help()

    assert captured["title"] == "How to Use"
    assert "Ctrl+Enter" in captured["message"]
