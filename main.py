import sys
from src.gui.main_window import LibraryManagementSystem
import tkinter as tk
from ttkbootstrap import Style

def main():
    root = tk.Tk()
    style = Style(theme="cosmo")
    app = LibraryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()