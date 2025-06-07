from tkinter import messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import customtkinter as ctk
from ttkbootstrap.dialogs import DatePickerDialog

from src.core.models import Book, Reader, TrackBook
from src.core.data_handler import data_handler
from src.utils.logger import logger
from src.gui.book_tab import BookTab
from src.gui.reader_tab import ReaderTab
from src.gui.tracking_tab import TrackingTab
from src.gui.date_picker import MyDatePicker

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Thư Viện")
        self.root.geometry("1200x800")

        self.style = ttk.Style()
        self._setup_custom_button_style()
        self._setup_header()
        self._setup_notebook_style()
        self._setup_notebook()
        self._setup_treeview_style()

        # Khởi tạo các tab
        self.book_tab = BookTab(self.notebook, self)
        self.reader_tab = ReaderTab(self.notebook, self)
        self.tracking_tab = TrackingTab(self.notebook, self)

        self.notebook.add(self.book_tab.frame, text="Quản lý Sách")
        self.notebook.add(self.reader_tab.frame, text="Quản lý Bạn đọc")
        self.notebook.add(self.tracking_tab.frame, text="Mượn/Trả Sách")

        self.check_and_update_overdue_books()
        self.update_tracking_list()
        self._setup_custom_button_style()
    def _setup_custom_button_style(self):
        style = ttk.Style()
        style.configure(
            "Pastel.TButton",
            font=("Arial", 11, "bold"),
            foreground="#333",
            background="#B4E4FF",  # Màu pastel xanh nhạt
            borderwidth=0,
            focusthickness=3,
            focuscolor="#AEE2FF",
            padding=8,
            relief="flat"
        )
        style.map(
            "Pastel.TButton",
            background=[("active", "#AEE2FF"), ("pressed", "#B4E4FF")]
        )
   
    def _setup_header(self):
        # Tạo khoảng trống ở đầu 
        spacing_frame = ttk.Frame(self.root)
        spacing_frame.pack(pady=10)

        # Tạo frame chứa logo và tiêu đề
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=(0,10), padx=20, fill='x')
        self.style.configure("Header.TFrame", background="#E3F2FD")
        header_frame.configure(style="Header.TFrame")
        try:
            # Đường dẫn đến file logo
            logo_path = "assets/hust.png"
            logo_image = Image.open(logo_path)
            # Điều chỉnh kích thước logo
            desired_height = 70
            ratio = desired_height / float(logo_image.size[1])
            width = int(float(logo_image.size[0]) * float(ratio))
            logo_image = logo_image.resize((width, desired_height), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            
            logo_label = ttk.Label(
                header_frame,
                image=logo_photo,
                background="#E3F2FD"
            )
            logo_label.image = logo_photo  # Giữ reference để tránh garbage collection
            logo_label.pack(side=tk.LEFT, padx=(0, 20))
            title_label = ttk.Label(
                header_frame,
                text="HỆ THỐNG QUẢN LÝ THƯ VIỆN",
                font=("Arial Unicode MS", 24, "bold"),
                foreground="#2C3E50",
                background="#E3F2FD",
                padding=(0, 10)
            )
            title_label.pack(side=tk.LEFT)
        except Exception as e:
            logger.error(f"Không thể tải logo: {e}")

    def _setup_notebook_style(self):
        active_tab_bg = "white"
        active_tab_fg = "#003366"
        try:
            inactive_tab_bg = self.style.lookup('TButton', 'background')
            inactive_tab_fg = self.style.lookup('TButton', 'foreground')
            tab_hover_bg = self.style.lookup('TButton', 'background', ('active',))
            if not inactive_tab_bg: inactive_tab_bg = "#E0EFFF"
            if not inactive_tab_fg: inactive_tab_fg = "#495057"
            if not tab_hover_bg: tab_hover_bg = "#C8E0FF"
        except tk.TclError:
            inactive_tab_bg = "#F0F0F0"
            inactive_tab_fg = "#333333"
            tab_hover_bg = "#E0E0E0"

        try:
            self.style.element_create("CustomTab.padding", "from", "default")
            self.style.element_create("CustomTab.focus", "from", "default")
            self.style.element_create("CustomTab.label", "from", "default")

            self.style.configure("TNotebook", borderwidth=0)
            self.style.configure("TNotebook.Client", background=active_tab_bg)

            self.style.configure(
                "TNotebook.Tab",
                background=inactive_tab_bg,
                foreground=inactive_tab_fg,
                font=('Arial Unicode MS', 10),
                padding=[18, 6],
                relief="flat",
                borderwidth=0
            )
            self.style.map(
                "TNotebook.Tab",
                background=[
                    ("selected", active_tab_bg),
                    ("active", tab_hover_bg)
                ],
                foreground=[
                    ("selected", active_tab_fg),
                    ("active", active_tab_fg)
                ],
                font=[("selected", ('Arial Unicode MS', 10, 'bold'))]
            )
        except Exception as e:
            logger.error(f"Lỗi khi cố gắng style Notebook tab chi tiết: {e}")
            self.style.configure("TNotebook.Tab", padding=[18, 6], font=('Arial Unicode MS', 10))
            self.style.map("TNotebook.Tab",
                        font=[("selected", ('Arial Unicode MS', 10, 'bold'))])

    def _setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=(5, 10))
    def _setup_treeview_style(self):
        self.style.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#333333",
            rowheight=30,
            font=('Arial Unicode MS', 10),
            borderwidth=0,
            relief="flat"
        )
        self.style.configure(
            "Treeview.Heading",
            font=('Arial Unicode MS', 11, 'bold'),
            background="#1976D2",
            foreground="#ffffff",
            relief="flat",
            borderwidth=0,
            padding=(5,5)
        )
        self.style.map('Treeview',
            background=[('selected', '#BBE2EC')],
            foreground=[('selected', '#1a365d')]
        )

    def check_and_update_overdue_books(self):
        current_date = datetime.now()
        for track in data_handler.tracking_db.values():
            if track.trang_thai == "Borrowed":
                borrow_date = datetime.strptime(track.ngay_muon, "%d/%m/%Y")
                if (current_date - borrow_date).days > 14:  # Quá 14 ngày
                    track.trang_thai = "Overdue"
        data_handler.save_data()

    def update_tracking_list(self):
        self.tracking_tab.update_tracking_list()