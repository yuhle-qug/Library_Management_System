import sys
from src.gui.main_window import LibraryManagementSystem
import tkinter as tk
from ttkbootstrap import Style


def main():
    try:
        root = tk.Tk()
        app = LibraryManagementSystem(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nĐóng chương trình an toàn...")
        try:
            root.destroy()
        except:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()