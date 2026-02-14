#!/usr/bin/env python3
import tkinter as tk

from checkbook_helper.gui import CheckbookApp


def main():
    root = tk.Tk()
    CheckbookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
