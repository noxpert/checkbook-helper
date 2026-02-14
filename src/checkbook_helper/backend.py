from decimal import Decimal, ROUND_HALF_UP


def parse_amount(value):
    if isinstance(value, Decimal):
        amount = value
    else:
        text = str(value).strip()
        if not text:
            raise ValueError("Amount is required")
        amount = Decimal(text)
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def normalize_description(description):
    text = str(description).strip()
    return text if text else "Transaction"


class CheckbookLedger:
    def __init__(self, starting_balance="0.00"):
        self.entries = []
        self._starting_balance = parse_amount(starting_balance)

    def set_starting_balance(self, value):
        self._starting_balance = parse_amount(value)

    def add_entry(self, description, amount, entry_type):
        if entry_type not in ("add", "subtract"):
            raise ValueError("Entry type must be 'add' or 'subtract'")
        entry = {
            "description": normalize_description(description),
            "amount": parse_amount(amount),
            "type": entry_type,
        }
        self.entries.append(entry)
        return entry

    def clear(self):
        self.entries = []

    def build_display_rows(self):
        rows = []
        running_total = self._starting_balance
        rows.append(
            {
                "description": "Starting Balance",
                "amount": f"{running_total:.2f}",
                "running_total": f"{running_total:.2f}",
            }
        )
        for entry in self.entries:
            amount = entry["amount"]
            if entry["type"] == "add":
                running_total += amount
                amount_display = f"+{amount:.2f}"
            else:
                running_total -= amount
                amount_display = f"-{amount:.2f}"
            rows.append(
                {
                    "description": entry["description"],
                    "amount": amount_display,
                    "running_total": f"{running_total:.2f}",
                }
            )
        return rows
