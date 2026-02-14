# checkbook-helper
Simple Python Tkinter app to run locally and aid entry of deposits and charges in paper checkbook register.

Since my wife and I still use a paper checkbook register, I want a simple way to calculate the charges and deposits. I often add multiple at the same time and when I do I use a spreadsheet or calculator to get the math right. This app is supposed to be slightly simpler than those tools.

## Features
- Easy-to-use interface for calculating transactions
- Automatic calculation of running balance

## Development
- Run tests with coverage: `make test`
- Run the app: `make run`
- Or run `python checkbook_calculator.py`
- Or run `python -m checkbook_helper`

## Keyboard Shortcuts
- Add entry: `Ctrl+Enter`
- Set type to add: `Ctrl++`
- Set type to subtract: `Ctrl+-`

## Technology
- Python 3.10+
- Tkinter
- Pytest
- pytest-cov

## AI Usage
- Initial version generated with Claude AI
- Updates made with JetBrains AI Assistant with Codex Agent

## License
- MIT License
