from decimal import Decimal

import pytest

from checkbook_helper.backend import CheckbookLedger, parse_amount


def test_parse_amount_rounds_half_up():
    assert parse_amount("1.005") == Decimal("1.01")
    assert parse_amount("2") == Decimal("2.00")


def test_add_entry_and_running_totals():
    ledger = CheckbookLedger("100.00")
    ledger.add_entry("Paycheck", "50.25", "add")
    ledger.add_entry("Groceries", "12.10", "subtract")

    rows = ledger.build_display_rows()

    assert rows[0]["description"] == "Starting Balance"
    assert rows[0]["running_total"] == "100.00"
    assert rows[1]["amount"] == "+50.25"
    assert rows[1]["running_total"] == "150.25"
    assert rows[2]["amount"] == "-12.10"
    assert rows[2]["running_total"] == "138.15"


def test_blank_description_defaults():
    ledger = CheckbookLedger()
    ledger.add_entry("   ", "5.00", "subtract")
    rows = ledger.build_display_rows()
    assert rows[1]["description"] == "Transaction"


def test_invalid_entry_type_rejected():
    ledger = CheckbookLedger()
    with pytest.raises(ValueError):
        ledger.add_entry("Oops", "1.00", "transfer")
