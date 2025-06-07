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
        self.root.geometry("1500x800")
        
        # Thêm protocol xử lý khi đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        # Kiểm tra và cập nhật sách quá hạn khi khởi động
        self.check_and_update_overdue_books()
        self.update_tracking_list()
        self._setup_custom_button_style()
   
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
        # Style cho nhãn in đậm
        self.style.configure(
            "Bold.TLabel",
            font=('Arial Unicode MS', 11, 'bold')
        )


    def update_tracking_list(self):
        self.tracking_tab.update_tracking_list()

    def _setup_custom_button_style(self):
            # BƯỚC 1: KÍCH HOẠT THEME 'clam' ĐỂ ĐẢM BẢO TÙY CHỈNH ĐƯỢC ÁP DỤNG

            # BƯỚC 2: ĐỊNH NGHĨA CÁC MÀU SẮC
            button_styles = {
                "Add.TButton": {"background": "#28a745", "hover_bg": "#218838", "foreground": "white"},
                "Update.TButton": {"background": "#007bff", "hover_bg": "#0069d9", "foreground": "white"},
                "Delete.TButton": {"background": "#dc3545", "hover_bg": "#c82333", "foreground": "white"},
                "Info.TButton": {"background": "#17a2b8", "hover_bg": "#138496", "foreground": "white"},
                "Action.TButton": {"background": "#ffc107", "hover_bg": "#e0a800", "foreground": "black"},
            }
            
            # BƯỚC 3: CẤU HÌNH STYLE CHO TỪNG LOẠI NÚT
            for style_name, colors in button_styles.items():
                self.style.configure(
                    style_name,
                    font=("Arial Unicode MS", 11, "bold"),
                    foreground=colors["foreground"],
                    background=colors["background"],
                    borderwidth=0,
                    padding=8,
                    relief="flat"
                )
                self.style.map(
                    style_name,
                    background=[
                        ("active", colors["hover_bg"]),
                        ("pressed", colors["background"]) # Giữ màu nền khi nhấn
                    ],
                    foreground=[("active", colors["foreground"])]
                )
    def on_closing(self):
        """Xử lý khi đóng chương trình"""
        try:
            # Lưu dữ liệu trước khi thoát
            data_handler.save_data()
            self.root.destroy()
        except Exception as e:
            logger.error(f"Lỗi khi đóng chương trình: {e}")
            self.root.destroy()

    def check_and_update_overdue_books(self):
        """
        Kiểm tra và cập nhật trạng thái sách quá hạn khi khởi động ứng dụng.
        """
        try:
            current_date = datetime.now()
            max_borrow_days = 30  # Số ngày mượn tối đa
            overdue_count = 0

            # Kiểm tra từng bản ghi mượn sách
            for record in data_handler.tracking_db.values():
                if record.trang_thai == "Đang mượn":  # Chỉ kiểm tra sách đang được mượn
                    try:
                        # Chuyển ngày mượn sang datetime object
                        borrow_date = datetime.strptime(record.ngay_muon, "%d/%m/%Y")
                        days_borrowed = (current_date - borrow_date).days

                        # Nếu số ngày mượn vượt quá giới hạn
                        if days_borrowed > max_borrow_days:
                            record.trang_thai = "Quá hạn"
                            overdue_count += 1
                    except ValueError as e:
                        logger.error(f"Lỗi xử lý định dạng ngày tháng cho bản ghi {record}: {e}")
                        continue

            # Lưu thay đổi vào CSDL nếu có sách quá hạn
            if overdue_count > 0:
                data_handler.save_data()
                logger.info(f"Đã cập nhật {overdue_count} sách sang trạng thái quá hạn")
                messagebox.showwarning("Thông báo", f"Có {overdue_count} sách chuyển sang trạng thái quá hạn!")

        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra sách quá hạn: {e}")
            messagebox.showerror("Lỗi", f"Không thể kiểm tra sách quá hạn: {e}")