from tkinter import messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
from tkinter import ttk
import reader_manager
import tracking_manager
import data_handler
from models import Book, Reader, TrackBook
from logger import logger
from datetime import datetime, timedelta
import customtkinter as ctk
from ttkbootstrap.dialogs import DatePickerDialog
from PIL import Image, ImageTk

class MyDatePicker:
    def __init__(self, parent):
        self.dialog = DatePickerDialog(
            parent=parent,
            title="Chọn ngày",
            firstweekday=0  # 0: Thứ 2, 6: Chủ nhật
        )
        
    def get_date(self):
        return self.dialog.date_selected

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Thư Viện")
        self.root.geometry("1200x800")

        self.style = ttk.Style()
        # Theme "cosmo" đã được áp dụng cho root.

        # Tạo khoảng trống ở đầu 
        spacing_frame = ttk.Frame(root)
        spacing_frame.pack(pady=10)

        # Tạo frame chứa logo và tiêu đề
        header_frame = ttk.Frame(root)
        header_frame.pack(pady=(0,10), padx=20, fill='x')
        self.style.configure("Header.TFrame", background="#E3F2FD")
        header_frame.configure(style="Header.TFrame")
        try:
            # Đường dẫn đến file logo của bạn
            logo_path = "assets/hust.png"  # Thay đổi đường dẫn phù hợp
            logo_image = Image.open(logo_path)
            # Điều chỉnh kích thước logo
            desired_height = 70  # Chiều cao mong muốn
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
        

        # --- STYLE CHO NOTEBOOK VÀ TAB (THỬ NGHIỆM NÂNG CAO) ---
        active_tab_bg = "white"
        active_tab_fg = "#003366"
        # Màu cho tab không active có thể lấy từ theme để đồng bộ hơn
        # Ví dụ, màu nền của một button không được nhấn trong theme cosmo
        try:
            # Thử lấy màu nền mặc định của một widget trong theme
            inactive_tab_bg = self.style.lookup('TButton', 'background')
            inactive_tab_fg = self.style.lookup('TButton', 'foreground')
            tab_hover_bg = self.style.lookup('TButton', 'background', ('active',))
            if not inactive_tab_bg: inactive_tab_bg = "#E0EFFF" # Fallback
            if not inactive_tab_fg: inactive_tab_fg = "#495057" # Fallback
            if not tab_hover_bg: tab_hover_bg = "#C8E0FF" # Fallback
        except tk.TclError: # Nếu lookup không thành công
            inactive_tab_bg = "#F0F0F0" # Màu xám rất nhạt
            inactive_tab_fg = "#333333"
            tab_hover_bg = "#E0E0E0"

        # Cấu hình layout để có thể style các element con của Tab
        # Cảnh báo: Việc thay đổi layout có thể phức tạp và không ổn định giữa các theme/OS
        # Thử nghiệm này có thể không hoạt động như mong đợi hoặc làm vỡ layout
        try:
            self.style.element_create("CustomTab.padding", "from", "default")
            self.style.element_create("CustomTab.focus", "from", "default")
            self.style.element_create("CustomTab.label", "from", "default")

            # Cấu trúc layout cơ bản của một tab, có thể khác nhau tùy theme
            # Thường bao gồm padding, focus indicator, và label
            # self.style.layout("TNotebook.Tab", [
            #     ("CustomTab.padding", {"sticky": "nswe", "children": [
            #         ("CustomTab.focus", {"sticky": "nswe", "children": [
            #             ("CustomTab.label", {"side": "top", "sticky": ""})
            #         ]})
            #     ]})
            # ])
            # Vì việc thay đổi layout quá phức tạp và dễ lỗi, ta sẽ tập trung vào configure và map
            # cho các element mà theme "cosmo" có thể sử dụng.

            # Style cho các thành phần của TNotebook.Tab
            # Thử nhắm vào các sub-element mà theme có thể sử dụng
            # Các tên element như 'Tab.background', 'Tab.selected', 'Tab.active' có thể không chuẩn
            # và phụ thuộc vào cách theme "cosmo" định nghĩa.

            self.style.configure("TNotebook", borderwidth=0) # Bỏ viền ngoài của notebook
            self.style.configure("TNotebook.Client", background=active_tab_bg) # Nền client trắng

            self.style.configure(
                "TNotebook.Tab",
                background=inactive_tab_bg,
                foreground=inactive_tab_fg,
                font=('Arial Unicode MS', 10),
                padding=[18, 6],
                relief="flat",
                borderwidth=0 # Thử bỏ viền tab
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
                font=[("selected", ('Arial Unicode MS', 10, 'bold'))],
                # lightcolor=[("selected", active_tab_bg)], # Thử ảnh hưởng đến màu highlight
                # bordercolor=[("selected", active_tab_bg)] # Thử ảnh hưởng đến màu viền
            )
        except Exception as e:
            logger.error(f"Lỗi khi cố gắng style Notebook tab chi tiết: {e}")
            # Nếu có lỗi, quay lại cấu hình đơn giản hơn
            self.style.configure("TNotebook.Tab", padding=[18, 6], font=('Arial Unicode MS', 10))
            self.style.map("TNotebook.Tab",
                           font=[("selected", ('Arial Unicode MS', 10, 'bold'))])


        # --- KẾT THÚC STYLE CHO NOTEBOOK VÀ TAB ---

        self.notebook = ttk.Notebook(self.root) # Không cần style tùy chỉnh ở đây nữa
        self.notebook.pack(expand=True, fill='both', padx=10, pady=(5, 10))

        self.book_tab = ttk.Frame(self.notebook)
        self.reader_tab = ttk.Frame(self.notebook)
        self.tracking_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.book_tab, text=' Quản lý Sách ')
        self.notebook.add(self.reader_tab, text=' Quản lý Bạn đọc ')
        self.notebook.add(self.tracking_tab, text=' Mượn/Trả Sách ')

        # ... (phần còn lại của __init__) ...
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
            background="#E9ECEF",
            foreground="#495057",
            relief="flat",
            borderwidth=0,
            padding=(5,5)
        )
        self.style.map('Treeview',
            background=[('selected', '#BBE2EC')],
            foreground=[('selected', '#1a365d')]
        )

        self.setup_book_tab()
        self.setup_reader_tab()
        self.setup_tracking_tab()

        self.check_and_update_overdue_books()
        self.update_tracking_list()
# Đảm bảo hàm này được định nghĩa

    # ... (các hàm khác không đổi) ...
    def check_and_update_overdue_books(self):
        """
        Kiểm tra và cập nhật trạng thái sách quá hạn trong cơ sở dữ liệu.
        """
        from datetime import date, datetime, timedelta
        today = date.today()
        due_days_limit = 30
        overdue_records = []

        for record in data_handler.tracking_records:
            if record.trang_thai == "Đang mượn":
                try:
                    ngay_muon_dt = datetime.strptime(record.ngay_muon, "%d/%m/%Y").date()
                    overdue_days = (today - ngay_muon_dt).days - due_days_limit
                    
                    if overdue_days > 0:
                        record.trang_thai = "Quá hạn"
                        reader_info = data_handler.readers_db.get(record.ma_ban_doc)
                        if reader_info:
                            overdue_records.append({
                                'reader_name': reader_info.ten,
                                'book_id': record.ma_sach_muon,
                                'days_overdue': overdue_days
                            })
                except ValueError as e:
                    logger.error(f"Lỗi định dạng ngày mượn cho record: {record.ma_sach_muon} của bạn đọc {record.ma_ban_doc}")

        # Lưu trạng thái cập nhật vào file JSON
        data_handler.save_data()
        return overdue_records

    def setup_book_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.book_tab, style = "TabContent.TFrame")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame, 
            text="Thêm sách mới", 
            fg_color="#5AAA7A", 
            corner_radius=5,            font=("Segoe UI", 13, "bold"),
            text_color="white",            command=self.show_add_book_window
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            btn_frame, 
            text="Cập nhật sách", 
            fg_color="#587F98", 
            corner_radius=5, 
            font=("Segoe UI", 13, "bold"),
            text_color="white",        command=self.show_update_book_window
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            btn_frame, 
            text="Tìm kiếm sách", 
            fg_color="#B95A2D", 
            corner_radius=5, 
            font=("Segoe UI", 13, "bold"),
            text_color="white",        command=self.show_search_book_window
        ).pack(side=tk.LEFT, padx=5)

        # Frame chứa các tùy chọn sắp xếp và lọc
        filter_frame = ttk.Frame(self.book_tab)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Sắp xếp theo:").pack(side=tk.LEFT, padx=5)
        # Thêm tùy chọn sắp xếp theo ID vào combobox
        self.sort_by = ttk.Combobox(filter_frame, values=["ID", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"], state="readonly")
        self.sort_by.pack(side=tk.LEFT, padx=5)
        self.sort_by.bind("<<ComboboxSelected>>", lambda e: self.update_book_list())

        ttk.Label(filter_frame, text="Lọc theo thể loại:").pack(side=tk.LEFT, padx=5)
        self.filter_by_genre = ttk.Combobox(
            filter_frame, 
            values=["Tất cả", "Khoa học", "Văn học", "Lịch sử", "Thiếu nhi", "Kinh tế", "Tâm lý", "Công nghệ", "Y học", "Khác"],
            state="readonly"
        )
        self.filter_by_genre.pack(side=tk.LEFT, padx=5)
        self.filter_by_genre.bind("<<ComboboxSelected>>", lambda e: self.update_book_list())

        # Frame chứa Treeview và Scrollbar
        tree_frame = ttk.Frame(self.book_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Thêm thanh cuộn
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("Mã sách", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"), show="headings")
        self.book_tree.pack(fill='both', expand=True)

        tree_scroll.config(command=self.book_tree.yview)

        # Cấu hình và đặt chiều rộng cho các cột
        self.book_tree.column("Mã sách", width=100, anchor="center")
        self.book_tree.column("Tiêu đề", width=300, anchor="w")
        self.book_tree.column("Tác giả", width=200, anchor="w")
        self.book_tree.column("Thể loại", width=150, anchor="center")
        self.book_tree.column("Số lượng", width=100, anchor="center")
        self.book_tree.column("Tình trạng", width=150, anchor="center")

        for col in ["Mã sách", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"]:
            self.book_tree.heading(col, text=col)

        # Gọi update_book_list() để sắp xếp mặc định theo ID khi khởi động
        self.update_book_list()

    def setup_reader_tab(self):
    # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.reader_tab)
        btn_frame.pack(pady=20)
         # Thêm frame mới cho các tùy chọn sắp xếp và lọc
        filter_frame = ttk.Frame(self.reader_tab)
        filter_frame.pack(pady=10)
        # Tùy chọn sắp xếp
        ttk.Label(filter_frame, text="Sắp xếp theo:").pack(side=tk.LEFT, padx=5)
        self.reader_sort_by = ttk.Combobox(
            filter_frame, 
            values=["Mã bạn đọc", "Tên", "Ngày sinh"],
            state="readonly"
        )
        self.reader_sort_by.pack(side=tk.LEFT, padx=5)
        self.reader_sort_by.set("Mã bạn đọc")  # Giá trị mặc định
        self.reader_sort_by.bind("<<ComboboxSelected>>", lambda e: self.update_reader_list())
        # Tùy chọn lọc theo giới tính
        ttk.Label(filter_frame, text="Lọc theo giới tính:").pack(side=tk.LEFT, padx=5)
        self.filter_by_gender = ttk.Combobox(
            filter_frame, 
            values=["Tất cả", "Nam", "Nữ", "Khác"],
            state="readonly"
        )
        self.filter_by_gender.pack(side=tk.LEFT, padx=5)
        self.filter_by_gender.set("Tất cả")  # Giá trị mặc định
        self.filter_by_gender.bind("<<ComboboxSelected>>", lambda e: self.update_reader_list())

        ctk.CTkButton(
            btn_frame,
            text="Thêm bạn đọc",
            fg_color="#5AAA7A",
            corner_radius=5,
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            command=self.show_add_reader_window
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Cập nhật thông tin",
            fg_color="#587F98",
            corner_radius=5,
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            command=self.show_update_reader_window
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Tìm kiếm bạn đọc",
            fg_color="#B95A2D",
            corner_radius=5,
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            command=self.show_search_reader_window
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Xóa bạn đọc",
            fg_color="#D9534F",
            corner_radius=5,
            font=("Segoe UI", 13, "bold"),
            text_color="white",
            command=self.delete_reader
        ).pack(side=tk.LEFT, padx=5)
        # Treeview để hiển thị danh sách bạn đọc
        tree_frame = ttk.Frame(self.reader_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.reader_tree = ttk.Treeview(
            tree_frame,
            columns=('Mã bạn đọc', 'Tên', 'Ngày sinh', 'Giới tính', 'Địa chỉ', 'SDT'),
            yscrollcommand=tree_scroll.set,
            bootstyle="primary",
            show="headings"
        )
        tree_scroll.config(command=self.reader_tree.yview)

        self.reader_tree.heading('Mã bạn đọc', text='Mã bạn đọc')
        self.reader_tree.heading('Tên', text='Tên')
        self.reader_tree.heading('Ngày sinh', text='Ngày sinh')
        self.reader_tree.heading('Giới tính', text='Giới tính')
        self.reader_tree.heading('Địa chỉ', text='Địa chỉ')
        self.reader_tree.heading('SDT', text='Điện thoại')
        

        self.reader_tree.column('Mã bạn đọc', anchor='c', width=80)
        self.reader_tree.column('Tên', anchor='w', width=200)
        self.reader_tree.column('Ngày sinh', anchor='c', width=120)
        self.reader_tree.column('Giới tính', anchor='c', width=100)
        self.reader_tree.column('Địa chỉ', anchor='w', width=250)
        self.reader_tree.column('SDT', anchor='w', width=150)
        

        self.reader_tree.pack(fill='both', expand=True)
        self.reader_tree.tag_configure('oddrow', background='#E8F4FA')
        self.reader_tree.tag_configure('evenrow', background='#FFFFFF')

        # Thiết lập kiểu Treeview giống tab Quản lý Sách
        self.reader_tree.configure(style="Treeview")

        self.update_reader_list()
    def delete_reader(self):
        if not self.reader_tree.selection():
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn đọc cần xóa!")
            return

        selected_item = self.reader_tree.selection()[0]
        reader_id_from_tree = self.reader_tree.item(selected_item)['values'][0]
        reader_id_key = str(reader_id_from_tree)

        if reader_id_key not in data_handler.readers_db:
            messagebox.showerror("Lỗi", f"Mã bạn đọc '{reader_id_key}' không tồn tại trong cơ sở dữ liệu!")
            return

        # Kiểm tra nếu bạn đọc đang mượn sách
        borrowed_books = [
            record for record in data_handler.tracking_records
            if record.ma_ban_doc == reader_id_key and record.trang_thai in ["Đang mượn", "Quá hạn"]
        ]
        if borrowed_books:
            messagebox.showerror(
                "Lỗi",
                f"Không thể xóa bạn đọc '{reader_id_key}' vì đang có sách mượn chưa trả!"
            )
            return

        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bạn đọc '{reader_id_key}'?"):
            return

        # Xóa bạn đọc
        del data_handler.readers_db[reader_id_key]
        data_handler.save_data()
        self.update_reader_list()
        messagebox.showinfo("Thành công", f"Đã xóa bạn đọc '{reader_id_key}'!")
    def setup_tracking_tab(self):
        # Frame chứa các nút chức năng
        
        btn_frame = ttk.Frame(self.tracking_tab)
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
        btn_frame,
        text="Mượn sách",
        fg_color="#5AAA7A",
        corner_radius=5,
        font=("Segoe UI", 13, "bold"),
        text_color="white",
        command=self.show_borrow_window
    ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
        btn_frame,
        text="Trả sách",
        fg_color="#587F98",
        corner_radius=5,
        font=("Segoe UI", 13, "bold"),
        text_color="white",
        command=self.show_return_window  # Chỉ mở cửa sổ trả sách, không cho phép trả trực tiếp
    ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
        btn_frame,
        text="Xem lịch sử",
        fg_color="#B95A2D",
        corner_radius=5,
        font=("Segoe UI", 13, "bold"),
        text_color="white",
        command=self.show_history_window
    ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
        btn_frame,
        text="Sách quá hạn",
        fg_color="#D9534F",
        corner_radius=5,
        font=("Segoe UI", 13, "bold"),
        text_color="white",
        command=self.show_overdue_books_window
    ).pack(side=tk.LEFT, padx=5)

        # Treeview để hiển thị danh sách mượn/trả
        tree_frame = ttk.Frame(self.tracking_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tracking_tree = ttk.Treeview(
            tree_frame,
            columns=('Bạn đọc', 'Sách', 'Ngày mượn', 'Ngày trả', 'Trạng thái'),
            yscrollcommand=tree_scroll.set,
            bootstyle="primary",
            selectmode="none",
            show="headings"
        )
        tree_scroll.config(command=self.tracking_tree.yview)

        self.tracking_tree.heading('Bạn đọc', text='Bạn đọc')
        self.tracking_tree.heading('Sách', text='Sách')
        self.tracking_tree.heading('Ngày mượn', text='Ngày mượn')
        self.tracking_tree.heading('Ngày trả', text='Ngày trả')
        self.tracking_tree.heading('Trạng thái', text='Trạng thái')

        self.tracking_tree.column('Bạn đọc', anchor='c', width=80)
        self.tracking_tree.column('Sách', anchor='w', width=150)
        self.tracking_tree.column('Ngày mượn', anchor='center', width=120)
        self.tracking_tree.column('Ngày trả', anchor='center', width=120)
        self.tracking_tree.column('Trạng thái', anchor='center', width=100)

        self.tracking_tree.pack(fill='both', expand=True)

        self.tracking_tree.tag_configure('oddrow', background='#E8F4FA')
        self.tracking_tree.tag_configure('evenrow', background='#FFFFFF')

        # Thiết lập kiểu Treeview giống tab Quản lý Sách
        self.tracking_tree.configure(style="Treeview")

        self.update_tracking_list()
    # Các phương thức hiển thị cửa sổ chức năng
    
    def show_add_book_window(self):
        logger.info("Mở cửa sổ thêm sách mới")
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm Sách Mới")
        add_window.geometry("600x800")

        ttk.Label(add_window, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(add_window, width=50)
        ma_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(add_window, width=50)
        tac_gia_entry.pack(pady=5)

        ttk.Label(add_window, text="Thể loại:").pack(pady=5)
        the_loai_var = tk.StringVar(value="Fiction")
        the_loai_combobox = ttk.Combobox(
            add_window, textvariable=the_loai_var, state="readonly",
            values=["Fiction", "Non-Fiction", "Science", "History", "Biography", "Khác..."],
            width=49
        )
        the_loai_combobox.pack(pady=5)

        # Custom input for 'Khác...'
        custom_the_loai_var = tk.StringVar()
        custom_the_loai_label = ttk.Label(add_window, text="Nhập thể loại khác")
        custom_the_loai_entry = ttk.Entry(add_window, textvariable=custom_the_loai_var, width=50)

        def on_the_loai_change(event):
            if the_loai_var.get() == "Khác...":
                custom_the_loai_label.pack(pady=5)  # Ensure the label is displayed
                custom_the_loai_entry.pack(pady=5)
            else:
                custom_the_loai_label.pack_forget()  # Hide the label when not needed
                custom_the_loai_entry.pack_forget()
        the_loai_combobox.bind("<<ComboboxSelected>>", on_the_loai_change)

        ttk.Label(add_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(add_window, width=50)
        ten_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(add_window, width=50)
        so_luong_entry.pack(pady=5)

        ttk.Label(add_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_var = tk.StringVar(value="New")
        tinh_trang_combobox = ttk.Combobox(
            add_window, textvariable=tinh_trang_var, state="readonly",
            values=["New", "Used"],
            width=49
        )
        tinh_trang_combobox.pack(pady=5)

        ttk.Label(add_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(add_window, width=50)
        nha_xuat_ban_entry.pack(pady=5)

        def save_book():
            try:
                # Lấy dữ liệu từ các trường nhập liệu
                ma_sach = ma_sach_entry.get().strip()
                ten_sach = ten_sach_entry.get().strip()
                tac_gia = tac_gia_entry.get().strip()
                the_loai = custom_the_loai_var.get().strip() if the_loai_var.get() == "Khác..." else the_loai_var.get()
                so_luong = so_luong_entry.get().strip()
                tinh_trang = tinh_trang_var.get().strip()
                nha_xuat_ban = nha_xuat_ban_entry.get().strip()

                # Kiểm tra dữ liệu đầu vào
                if not all([ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban]):
                    raise ValueError("Vui lòng điền đầy đủ thông tin!")

                if not so_luong.isdigit() or int(so_luong) <= 0:
                    raise ValueError("Số lượng phải là một số nguyên dương!")

                # Kiểm tra mã sách đã tồn tại
                if ma_sach in data_handler.books_db:
                    raise ValueError("Mã sách đã tồn tại!")
                # Không ép thể loại thành "Khác", giữ nguyên giá trị người dùng nhập
                if the_loai_var.get() == "Khác..." and custom_the_loai_var.get().strip():
                    the_loai = custom_the_loai_var.get().strip()
                existing_genres = self.filter_by_genre['values']

                # Tạo đối tượng sách mới
                new_book = Book(
                    ma_sach=ma_sach,
                    ten_sach=ten_sach,
                    tac_gia=tac_gia,
                    the_loai=the_loai,
                    so_luong=int(so_luong),
                    tinh_trang=tinh_trang,
                    nha_xuat_ban=nha_xuat_ban
                )

                # Lưu vào cơ sở dữ liệu
                data_handler.books_db[ma_sach] = new_book
                data_handler.save_data()
                # Cập nhật danh sách hiển thị
                self.update_book_list()

                # Hiển thị thông báo thành công
                logger.info(f"Thêm sách mới thành công: {ma_sach}")
                messagebox.showinfo("Thành công", "Đã thêm sách mới!")
                add_window.destroy()

            except ValueError as e:
                logger.error(f"Lỗi khi thêm sách: {str(e)}")
                messagebox.showerror("Lỗi", str(e))

        ttk.Button(add_window, 
                   text="Lưu",
                   bootstyle="success",
                command=save_book).pack(pady=20)

    def show_update_book_window(self):
        logger.info("Mở cửa sổ cập nhật sách")
        if not self.book_tree.selection():
            logger.warning("Không có sách nào được chọn để cập nhật")
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần cập nhật!")
            return
            
        selected_item = self.book_tree.selection()[0]
        book_id_from_tree = self.book_tree.item(selected_item)['values'][0]
        book_id_key = str(book_id_from_tree) # Đảm bảo key là string

        if book_id_key not in data_handler.books_db: # Sử dụng key string
            logger.error(f"Mã sách '{book_id_key}' không tồn tại trong cơ sở dữ liệu!")
            messagebox.showerror("Lỗi", f"Mã sách '{book_id_key}' không tồn tại trong cơ sở dữ liệu!")
            return
        book = data_handler.books_db[book_id_key] # Lấy sách bằng key string

        logger.info(f"Mở cửa sổ cập nhật cho sách: {book_id_key}")
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Cập Nhật Thông Tin Sách")
        update_window.geometry("500x700")
        ttk.Label(update_window, text="Cập nhật thông tin sách", font=("Arial", 16)).pack(pady=10)
        # Form fields
        ttk.Label(update_window, text="Mã sách:").pack(pady=5)
        ma_sach_display_label = ttk.Label(update_window, text=book.ma_sach)
        ma_sach_display_label.pack(pady=5)

        ttk.Label(update_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(update_window, width=50)
        tac_gia_entry.insert(0, book.tac_gia)
        tac_gia_entry.pack(pady=5)

        ttk.Label(update_window, text="Thể loại:").pack(pady=5)
        the_loai_var = tk.StringVar(value=book.the_loai)
        the_loai_combobox = ttk.Combobox(
            update_window, textvariable=the_loai_var, state="readonly",
            values=["Fiction", "Non-Fiction", "Science", "History", "Biography", "Khác..."],
            width = 49
        )
        the_loai_combobox.pack(pady=5)

        # Custom input for 'Khác...'
        custom_the_loai_var = tk.StringVar()
        custom_the_loai_label = ttk.Label(update_window, text="Nhập thể loại khác")
        custom_the_loai_entry = ttk.Entry(update_window, textvariable=custom_the_loai_var, width=50)
        def on_the_loai_change(event):
            if the_loai_var.get() == "Khác...":
                custom_the_loai_label.pack(pady=5)
                custom_the_loai_entry.pack(pady=5)
            else:
                custom_the_loai_label.pack_forget()
                custom_the_loai_entry.pack_forget()
        the_loai_combobox.bind("<<ComboboxSelected>>", on_the_loai_change)

        ttk.Label(update_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(update_window, width=50)
        ten_sach_entry.insert(0, book.ten_sach)
        ten_sach_entry.pack(pady=5)
        
        ttk.Label(update_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(update_window, width=50)
        so_luong_entry.insert(0, str(book.so_luong))
        so_luong_entry.pack(pady=5)

        ttk.Label(update_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_var = tk.StringVar(value="New")
        tinh_trang_combobox = ttk.Combobox(
            update_window, textvariable=tinh_trang_var, state="readonly",
            values=["New", "Used"],
            width=49
        )
        tinh_trang_combobox.pack(pady=5)

        ttk.Label(update_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(update_window, width=50)
        nha_xuat_ban_entry.insert(0, book.nha_xuat_ban)
        nha_xuat_ban_entry.pack(pady=5)
        
        # Update logic
        def update_book():
            try:
                book.ten_sach = ten_sach_entry.get().strip()
                book.tac_gia = tac_gia_entry.get().strip()
                book.the_loai = custom_the_loai_var.get().strip() if the_loai_var.get() == "Khác..." else the_loai_var.get()
                book.so_luong = int(so_luong_entry.get().strip())
                book.tinh_trang = tinh_trang_combobox.get().strip()
                book.nha_xuat_ban = nha_xuat_ban_entry.get().strip()

                if the_loai_var.get() == "Khác..." and custom_the_loai_var.get().strip():
                    book.the_loai = custom_the_loai_var.get().strip()

                #Lưu dữ liệu
                data_handler.save_data()
                self.update_book_list()
                update_window.destroy()
                
                #thông báo cập nhật thành công 
                messagebox.showinfo("Thành công", "Thông tin sách đã được cập nhật!")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

        ttk.Button(update_window,
                    text="Cập nhật",
                     bootstyle="success",
                     command=update_book).pack(pady=20)

    def sort_books(self):
        criteria = self.sort_criteria.get()
        if criteria == "Tên sách":
            sorted_books = sorted(data_handler.books_db.values(), key=lambda b: b.ten_sach)
        elif criteria == "Tác giả":
            sorted_books = sorted(data_handler.books_db.values(), key=lambda b: b.tac_gia)
        elif criteria == "Thể loại":
            sorted_books = sorted(data_handler.books_db.values(), key=lambda b: b.the_loai)
        elif criteria == "Số lượng":
            sorted_books = sorted(data_handler.books_db.values(), key=lambda b: b.so_luong)
        elif criteria == "Tình trạng":
            sorted_books = sorted(data_handler.books_db.values(), key=lambda b: b.tinh_trang)
        else:
            sorted_books = data_handler.books_db.values()

        self.update_book_list(sorted_books)

    def filter_books(self):
        genre = self.filter_genre.get()
        if genre == "Tất cả":
            filtered_books = data_handler.books_db.values()
        else:
            filtered_books = [b for b in data_handler.books_db.values() if b.the_loai == genre]

        self.update_book_list(filtered_books)

    def update_book_list(self, books=None):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        # Lấy danh sách sách từ books_db nếu không được truyền vào
        if books is None:
            books = list(data_handler.books_db.values())

        # Danh sách thể loại sẵn có 
        predefined_genres = ["Khoa học", "Văn học", "Lịch sử", "Thiếu nhi", "Kinh tế", "Tâm lý", "Công nghệ", "Y học"]
        # Lọc theo thể loại nếu được chọn
        selected_genre = self.filter_by_genre.get() if hasattr(self, 'filter_by_genre') else None
        if selected_genre and selected_genre != "Tất cả":
            if selected_genre == "Khác":
                # Lọc các sách có thể loại không nằm trong danh sách sẵn có
                books = [book for book in books if book.the_loai not in predefined_genres]
            else:
                # Lọc các sách có thể loại khớp với thể loại được chọn
                books = [book for book in books if book.the_loai == selected_genre]

        # Sắp xếp theo tiêu chí được chọn
        sort_criteria = self.sort_by.get() if hasattr(self, 'sort_by') else None
        if sort_criteria == "Tiêu đề":
            books.sort(key=lambda x: x.ten_sach)
        elif sort_criteria == "Tác giả":
            books.sort(key=lambda x: x.tac_gia)
        elif sort_criteria == "Thể loại":
            books.sort(key=lambda x: x.the_loai)
        elif sort_criteria == "Số lượng":
            books.sort(key=lambda x: x.so_luong, reverse=True)
        elif sort_criteria == "Tình trạng":
            books.sort(key=lambda x: x.tinh_trang)
        else:  # Mặc định sắp xếp theo ID
            books.sort(key=lambda x: int(x.ma_sach) if x.ma_sach.isdigit() else x.ma_sach)

        # Thêm dữ liệu vào Treeview với màu xen kẽ
        for index, book in enumerate(books):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.book_tree.insert("", "end", values=(
                book.ma_sach,
                book.ten_sach,
                book.tac_gia,
                book.the_loai,
                book.so_luong,
                book.tinh_trang
            ), tags=(tag,))

        # Định nghĩa màu sắc cho các dòng xen kẽ
        self.book_tree.tag_configure('oddrow', background='#E8F4FA')
        self.book_tree.tag_configure('evenrow', background='#FFFFFF')

    def show_search_book_window(self):
        logger.info("Mở cửa sổ tìm kiếm sách")
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm Kiếm Sách")
        search_window.geometry("800x250")

        # ComboBox for search criteria
        ttk.Label(search_window, text="Chọn tiêu chí tìm kiếm:").pack(pady=5)
        search_criteria_var = tk.StringVar(value="Mã sách")
        search_criteria_combobox = ttk.Combobox(
            search_window, textvariable=search_criteria_var, state="readonly",
            values=["Mã sách", "Tên", "Tác giả", "Thể loại"]
        )
        search_criteria_combobox.pack(pady=5)
        # Search entry
        ttk.Label(search_window, text="Nhập từ khóa tìm kiếm:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        def search():
            keyword = search_entry.get().strip().lower()
            criteria = search_criteria_var.get()
            found_books = []

            for book in data_handler.books_db.values():
                if criteria == "Mã sách" and keyword in book.ma_sach.lower():
                    found_books.append(book)
                elif criteria == "Tên" and keyword in book.ten_sach.lower():
                    found_books.append(book)
                elif criteria == "Tác giả" and keyword in book.tac_gia.lower():
                    found_books.append(book)
                elif criteria == "Thể loại" and keyword in book.the_loai.lower():
                    found_books.append(book)

            # Display results
            result_window = tk.Toplevel(search_window)
            result_window.title("Kết Quả Tìm Kiếm")
            result_window.geometry("600x400")

            result_tree = ttk.Treeview(
                result_window,
                columns=("Mã bạn đọc", "Tên", "Ngày sinh", "Giới tính", "Địa chỉ", "Số điện thoại"),
                show="headings"
            )
            result_tree.heading("Mã bạn đọc", text="Mã bạn đọc")
            result_tree.heading("Tên", text="Tên")
            result_tree.heading("Ngày sinh", text="Ngày sinh")
            result_tree.heading("Giới tính", text="Giới tính")
            result_tree.heading("Địa chỉ", text="Địa chỉ")
            result_tree.heading("Số điện thoại", text="Số điện thoại")
            result_tree.pack(pady=10, padx=10, fill="both", expand=True)

            # Add results to Treeview
            for book in found_books:
                result_tree.insert("", "end", values=(
                    book.ma_sach,
                    book.ten_sach,
                    book.tac_gia,
                    book.the_loai,
                    book.so_luong,
                    book.tinh_trang
                ))

        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)
    def show_add_reader_window(self):
        logger.info("Mở cửa sổ thêm bạn đọc mới")
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm Bạn Đọc Mới")
        add_window.geometry("700x800")

        form = ScrolledFrame(add_window) # Sử dụng ScrolledFrame
        form.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)


        # Form fields
        ttk.Label(form, text="Mã bạn đọc:").pack(pady=5)
        ma_doc_entry = ttk.Entry(form, width=50) # Tăng chiều rộng
        ma_doc_entry.pack(pady=5)

        ttk.Label(form, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(form, width=50) # Tăng chiều rộng
        ten_entry.pack(pady=5)

        ttk.Label(form, text="Ngày sinh (DD/MM/YYYY):").pack(pady=5)
        ttk.Label(form, text="Vui lòng chọn ngày sinh bằng nút bên dưới (sử dụng chuột phải để di chuyển giữa các năm)").pack(pady=5)
        ngay_sinh_entry = ttk.Entry(form, width=50) # Tăng chiều rộng
        ngay_sinh_entry.pack(pady=5)

        def open_date_picker_for_add(): # Đổi tên hàm để tránh xung đột nếu có hàm tương tự
            try:
                # Đảm bảo add_window vẫn tồn tại và là Toplevel hợp lệ
                if not add_window.winfo_exists():
                    logger.error("Cửa sổ 'Thêm Bạn Đọc' không còn tồn tại.")
                    return

                # Sử dụng add_window làm parent cho DatePickerDialog
                date_dialog = DatePickerDialog(
                    parent=add_window, # Quan trọng: chỉ định parent
                    title="Chọn ngày sinh",
                    firstweekday=0 # 0: Thứ 2, 6: Chủ nhật
                )
                # date_dialog.show() # Phương thức show() sẽ hiển thị dialog và chờ người dùng chọn

                # Sau khi dialog đóng, kiểm tra kết quả
                selected_date_obj = date_dialog.date_selected
                if selected_date_obj:
                    formatted_date = selected_date_obj.strftime("%d/%m/%Y")
                    ngay_sinh_entry.delete(0, tk.END)
                    ngay_sinh_entry.insert(0, formatted_date)
                    logger.info(f"Ngày sinh đã chọn (Thêm bạn đọc): {formatted_date}")
                else:
                    logger.info("Người dùng không chọn ngày nào (Thêm bạn đọc).")

            except Exception as e:
                logger.error(f"Lỗi khi mở DatePickerDialog (Thêm bạn đọc): {e}", exc_info=True)
                messagebox.showerror("Lỗi DatePicker", f"Không thể mở lịch chọn ngày: {e}", parent=add_window)


        ttk.Button(form, text="Chọn ngày", command=open_date_picker_for_add, bootstyle="info-outline").pack(pady=5)


        ttk.Label(form, text="Giới tính:").pack(pady=5)
        gioi_tinh_combobox = ttk.Combobox(form, values=["Nam", "Nữ", "Khác"], width=49) # Tăng chiều rộng
        gioi_tinh_combobox.pack(pady=5)
        gioi_tinh_combobox.current(0) # Chọn mặc định "Nam"

        ttk.Label(form, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(form, width=50) # Tăng chiều rộng
        dia_chi_entry.pack(pady=5)

        ttk.Label(form, text="Số điện thoại:").pack(pady=5)
        sdt_entry = ttk.Entry(form, width=50) # Tăng chiều rộng
        sdt_entry.pack(pady=5)

        def save_reader():
            try:
                ma_doc = ma_doc_entry.get().strip()
                ten = ten_entry.get().strip()
                ngay_sinh = ngay_sinh_entry.get().strip()
                gioi_tinh = gioi_tinh_combobox.get()
                dia_chi = dia_chi_entry.get().strip()
                sdt = sdt_entry.get().strip()

                if not all([ma_doc, ten, ngay_sinh]):
                    raise ValueError("Vui lòng điền đầy đủ thông tin bắt buộc!")

                if ma_doc in data_handler.readers_db:
                    raise ValueError("Mã bạn đọc đã tồn tại!")

                try:
                    datetime.strptime(ngay_sinh, "%d/%m/%Y")
                except ValueError as date_err:
                    raise ValueError("Định dạng ngày sinh không hợp lệ! Vui lòng sử dụng định dạng DD/MM/YYYY")
                if not sdt.isdigit():
                    raise ValueError("Số điện thoại chỉ được chứa các ký tự số!")
                new_reader = Reader(
                    ma_ban_doc=ma_doc,
                    ten=ten,
                    ngay_sinh=ngay_sinh,
                    gioi_tinh=gioi_tinh,
                    dia_chi=dia_chi,
                    so_dien_thoai=sdt
                )

                data_handler.readers_db[ma_doc] = new_reader
                data_handler.save_data()
                self.update_reader_list()
                logger.info(f"Thêm bạn đọc mới thành công: {ma_doc}")
                messagebox.showinfo("Thành công", "Đã thêm bạn đọc mới!", parent=add_window)
                add_window.destroy()

            except ValueError as e:
                logger.error(f"Lỗi khi thêm bạn đọc: {str(e)}")
                messagebox.showerror("Lỗi", str(e), parent=add_window)
            except Exception as e:
                logger.error(f"Lỗi không mong muốn khi thêm bạn đọc: {str(e)}")
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi không mong muốn: {str(e)}", parent=add_window)


        button_frame = ttk.Frame(form)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Lưu", command=save_reader, bootstyle="success").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Hủy", command=add_window.destroy, bootstyle="danger").pack(side=tk.LEFT, padx=10)

    def update_reader_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)

        # Lấy danh sách bạn đọc từ readers_db
        readers = list(data_handler.readers_db.values())
        #lọc theo giới tính 
        selected_gender = self.filter_by_gender.get()
        if selected_gender != "Tất cả":
            readers = [reader for reader in readers if reader.gioi_tinh == selected_gender]
        sort_by = self.reader_sort_by.get()
        if sort_by == "Tên":
            readers.sort(key=lambda x: x.ten)
        elif sort_by == "Ngày sinh":
        # Chuyển đổi chuỗi ngày thành đối tượng datetime để so sánh
            readers.sort(key=lambda x: datetime.strptime(x.ngay_sinh, "%d/%m/%Y"))
        else:  # Mặc định sắp xếp theo Mã bạn đọc
            readers.sort(key=lambda x: int(x.ma_ban_doc) if x.ma_ban_doc.isdigit() else x.ma_ban_doc)
        # Sắp xếp theo tiêu chí được chọn

        # Thêm dữ liệu vào Treeview với màu xen kẽ
        for index, reader in enumerate(readers):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.reader_tree.insert("", "end", values=(
                reader.ma_ban_doc, reader.ten, reader.ngay_sinh, reader.gioi_tinh, reader.dia_chi, reader.so_dien_thoai
            ), tags=(tag,))

        # Định nghĩa màu sắc cho các dòng xen kẽ
        self.reader_tree.tag_configure('oddrow', background='#E8F4FA')
        self.reader_tree.tag_configure('evenrow', background='#FFFFFF')

    def show_update_reader_window(self):
        logger.info("Mở cửa sổ cập nhật bạn đọc")
        if not self.reader_tree.selection():
            logger.warning("Không có bạn đọc nào được chọn để cập nhật")
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn đọc cần cập nhật!")
            return
            
        selected_item = self.reader_tree.selection()[0]
        reader_id_from_tree = self.reader_tree.item(selected_item)['values'][0] #
        reader_id_key = str(reader_id_from_tree) # Chuyển đổi sang chuỗi
        
        if reader_id_key not in data_handler.readers_db:
            logger.error(f"Mã bạn đọc '{reader_id_key}' không tồn tại!") # Log lỗi nếu không tìm thấy
            messagebox.showerror("Lỗi", f"Mã bạn đọc '{reader_id_key}' không tồn tại trong cơ sở dữ liệu!")
            return

        reader = data_handler.readers_db[reader_id_key]
        logger.info(f"Mở cửa sổ cập nhật cho bạn đọc: {reader_id_key}")

        update_window = tk.Toplevel(self.root)
        update_window.title("Cập Nhật Thông Tin Bạn Đọc")
        update_window.geometry("500x800")
        
        form = ScrolledFrame(update_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Mã bạn đọc (hiển thị, không cho sửa)
        ttk.Label(form, text="Mã bạn đọc:").pack(pady=5) #
        ma_doc_display = ttk.Label(form, text=reader.ma_ban_doc) # Giả sử reader.ma_ban_doc là chuỗi
        ma_doc_display.pack(pady=5)

        ttk.Label(form, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(form, width=50)
        ten_entry.insert(0, reader.ten)
        ten_entry.pack(pady=5)
        
        ttk.Label(form, text="Ngày sinh:").pack(pady=5)
        ngay_sinh_entry = ttk.Entry(form, width=50)
        ngay_sinh_entry.insert(0, reader.ngay_sinh)
        ngay_sinh_entry.pack(pady=5)

        ttk.Label(form, text="Giới tính:").pack(pady=5)
        gioi_tinh_current = reader.gioi_tinh
        gioi_tinh_combobox = ttk.Combobox(form, values=["Nam", "Nữ", "Khác"], width=49)
        if gioi_tinh_current in gioi_tinh_combobox['values']:
            gioi_tinh_combobox.set(gioi_tinh_current)
        gioi_tinh_combobox.pack(pady=5)

        ttk.Label(form, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(form, width=50)
        dia_chi_entry.insert(0, reader.dia_chi)
        dia_chi_entry.pack(pady=5)
        
        ttk.Label(form, text="Số điện thoại:").pack(pady=5)
        sdt_entry = ttk.Entry(form, width=50)
        sdt_entry.insert(0, reader.so_dien_thoai)
        sdt_entry.pack(pady=5)

        def update_reader():
            try:
                # Update reader info
                reader.ten = ten_entry.get().strip()
                reader.ngay_sinh = ngay_sinh_entry.get().strip()
                reader.gioi_tinh = gioi_tinh_combobox.get()

                reader.dia_chi = dia_chi_entry.get().strip()
                reader.so_dien_thoai = sdt_entry.get().strip()
                
                self.update_reader_list()
                logger.info(f"Cập nhật thông tin bạn đọc thành công: {reader_id_key}")
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin bạn đọc!")
                data_handler.save_data()
                update_window.destroy()
            except Exception as e:
                logger.error(f"Lỗi khi cập nhật bạn đọc: {str(e)}")
                messagebox.showerror("Lỗi", str(e))

        button_frame = ttk.Frame(form)
        button_frame.pack(fill=X, pady=20)
        
        ttk.Button(
            button_frame,
            text="Hủy",
            bootstyle="secondary",
            command=update_window.destroy
        ).pack(side=RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cập nhật",
            bootstyle="success",
            command=update_reader
        ).pack(side=RIGHT)
        
    def show_search_reader_window(self):
        logger.info("Mở cửa sổ tìm kiếm bạn đọc")
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm Kiếm Bạn Đọc")
        search_window.geometry("450x250") # Điều chỉnh kích thước nếu cần

        # ComboBox for search criteria
        ttk.Label(search_window, text="Chọn tiêu chí tìm kiếm:").pack(pady=5)
        search_criteria_var = tk.StringVar(value="Mã bạn đọc") # Đặt giá trị mặc định
        search_criteria_combobox = ttk.Combobox(
            search_window, textvariable=search_criteria_var, state="readonly",
            values=["Mã bạn đọc", "Tên", "Số điện thoại"] # Các tiêu chí tìm kiếm bạn đọc
        )
        search_criteria_combobox.pack(pady=5)

        # Search entry
        ttk.Label(search_window, text="Nhập từ khóa tìm kiếm:").pack(pady=5)
        search_entry = ttk.Entry(search_window, width=40) # Tăng chiều rộng ô nhập
        search_entry.pack(pady=5)

        def search():
            keyword = search_entry.get().strip().lower()
            criteria = search_criteria_var.get() # Lấy tiêu chí người dùng đã chọn
            found_readers = []

            if not keyword:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập từ khóa tìm kiếm.", parent=search_window)
                return

            for reader_obj in data_handler.readers_db.values(): # Duyệt qua danh sách bạn đọc
                match = False
                if criteria == "Mã bạn đọc":
                    if keyword in str(reader_obj.ma_ban_doc).lower(): # Chuyển sang str để đảm bảo
                        match = True
                elif criteria == "Tên":
                    if keyword in str(reader_obj.ten).lower():
                        match = True
                elif criteria == "Số điện thoại":
                    # Đảm bảo so_dien_thoai không None trước khi gọi lower()
                    sdt_str = str(reader_obj.so_dien_thoai) if reader_obj.so_dien_thoai is not None else ""
                    if keyword in sdt_str.lower():
                        match = True
                
                if match:
                    found_readers.append(reader_obj)

            # Display results
            result_window = tk.Toplevel(search_window)
            result_window.title("Kết Quả Tìm Kiếm Bạn Đọc")
            result_window.geometry("1100x400") # Điều chỉnh kích thước để hiển thị đủ cột

            result_tree = ttk.Treeview(
                result_window,
                columns=("Mã bạn đọc", "Tên", "Ngày sinh", "Giới tính", "Địa chỉ", "Số điện thoại"),
                show="headings"
            )
            # Đặt tên cột
            result_tree.heading("Mã bạn đọc", text="Mã BĐ")
            result_tree.heading("Tên", text="Họ Tên")
            result_tree.heading("Ngày sinh", text="Ngày Sinh")
            result_tree.heading("Giới tính", text="Giới Tính")
            result_tree.heading("Địa chỉ", text="Địa Chỉ")
            result_tree.heading("Số điện thoại", text="SĐT")

            # Điều chỉnh độ rộng cột (tùy chọn)
            result_tree.column("Mã bạn đọc", width=80, anchor='center')
            result_tree.column("Tên", width=200)
            result_tree.column("Ngày sinh", width=100, anchor='center')
            result_tree.column("Giới tính", width=70, anchor='center')
            result_tree.column("Địa chỉ", width=250)
            result_tree.column("Số điện thoại", width=120, anchor='center')

            result_tree.pack(pady=10, padx=10, fill="both", expand=True)

            if not found_readers:
                result_tree.insert("", "end", values=("Không tìm thấy bạn đọc nào phù hợp.", "", "", "", "", ""))
            else:
                for reader_obj in found_readers:
                    result_tree.insert("", "end", values=(
                        reader_obj.ma_ban_doc,
                        reader_obj.ten,
                        reader_obj.ngay_sinh,
                        reader_obj.gioi_tinh,
                        reader_obj.dia_chi,
                        reader_obj.so_dien_thoai
                    ))

        ttk.Button(search_window, text="Tìm kiếm", command=search, bootstyle="primary").pack(pady=20)
    # ... (các hàm khác) ...
    def show_borrow_window(self):
        logger.info("Mở cửa sổ mượn sách")
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Mượn Sách")
        borrow_window.geometry("400x300")

        # Nhập mã bạn đọc
        ttk.Label(borrow_window, text="Mã bạn đọc:").pack(pady=5)
        reader_id_var = tk.StringVar()
        reader_id_entry = ttk.Entry(borrow_window, textvariable=reader_id_var)
        reader_id_entry.pack(pady=5)

        # Nhập mã sách
        ttk.Label(borrow_window, text="Mã sách:").pack(pady=5)
        book_id_var = tk.StringVar()
        book_id_entry = ttk.Entry(borrow_window, textvariable=book_id_var)
        book_id_entry.pack(pady=5)

        def borrow_book():
            try:
                reader_id = reader_id_var.get().strip()
                book_id = book_id_var.get().strip()

                if reader_id not in data_handler.readers_db:
                    raise ValueError("Mã bạn đọc không tồn tại!")
                if book_id not in data_handler.books_db:
                    raise ValueError("Mã sách không tồn tại!")

                book = data_handler.books_db[book_id]
                if book.so_luong <= 0:
                    raise ValueError("Sách đã hết!")

                # Check if already borrowed
                for record in data_handler.tracking_records:
                    if (record.ma_ban_doc == reader_id and 
                        record.ma_sach_muon == book_id and 
                        record.trang_thai == "Đang mượn"):
                        raise ValueError("Bạn đọc đã mượn cuốn sách này và chưa trả!")

                # Display confirmation popup
                reader_name = data_handler.readers_db[reader_id].ten
                confirmation_message = (
                    f"Xác nhận mượn sách:\n\n"
                    f"Mã bạn đọc: {reader_id}\n"
                    f"Tên bạn đọc: {reader_name}\n"
                    f"Mã sách: {book_id}\n"
                    f"Tên sách: {book.ten_sach}\n"
                    f"Tác giả: {book.tac_gia}\n"
                    f"Thể loại: {book.the_loai}\n"
                )

                if not messagebox.askyesno("Xác nhận", confirmation_message):
                    return

                # Create borrow record
                now = datetime.now().strftime("%d/%m/%Y")
                new_record = TrackBook(
                    ma_ban_doc=reader_id,
                    ma_sach_muon=book_id,
                    ten_sach_muon=book.ten_sach,
                    ngay_muon=now
                )

                # Update book quantity
                book.so_luong -= 1

                # Save record
                data_handler.tracking_records.append(new_record)
                self.update_tracking_list()
                self.update_book_list()
                data_handler.save_data()

                logger.info(f"Mượn sách thành công: {book_id} bởi {reader_id}")
                messagebox.showinfo("Thành công", "Đã ghi nhận mượn sách!")
                borrow_window.destroy()

            except ValueError as e:
                logger.error(f"Lỗi khi mượn sách: {str(e)}")
                messagebox.showerror("Lỗi", str(e))

        ttk.Button(borrow_window, text="Mượn sách", command=borrow_book).pack(pady=20)

    def update_tracking_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tracking_tree.get_children():
            self.tracking_tree.delete(item)

        # Lấy danh sách mượn/trả từ tracking_records
        trackings = data_handler.tracking_records

        # Thêm dữ liệu vào Treeview với màu xen kẽ
        for index, tracking in enumerate(trackings):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tracking_tree.insert("", "end", values=(
                tracking.ma_ban_doc, tracking.ten_sach_muon, tracking.ngay_muon, tracking.ngay_tra, tracking.trang_thai
            ), tags=(tag,))

        # Định nghĩa màu sắc cho các dòng xen kẽ
        self.tracking_tree.tag_configure('oddrow', background='#E8F4FA')
        self.tracking_tree.tag_configure('evenrow', background='#FFFFFF')
        logger.debug("Đã cập nhật xong danh sách mượn/trả")
    
    def show_return_window(self):
        logger.info("Mở cửa sổ trả sách")
        return_window = tk.Toplevel(self.root)
        return_window.title("Trả Sách")
        return_window.geometry("800x800")

        # Nhập mã bạn đọc
        ttk.Label(return_window, text="Nhập mã bạn đọc:").pack(pady=5)
        reader_id_var = tk.StringVar()
        reader_id_entry = ttk.Entry(return_window, textvariable=reader_id_var)
        reader_id_entry.pack(pady=5)

        def update_treeview():
            reader_id = reader_id_var.get().strip()
            if not reader_id:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã bạn đọc!")
                return

            # Xóa dữ liệu cũ trong Treeview
            for item in return_tree.get_children():
                return_tree.delete(item)

            # Lấy danh sách sách mượn của bạn đọc
            borrowed_records = [
                record for record in data_handler.tracking_records
                if record.ma_ban_doc == reader_id and record.trang_thai == "Đang mượn"
            ]

            if not borrowed_records:
                messagebox.showinfo("Thông báo", "Không tìm thấy sách mượn cho bạn đọc này!")
                return

            for record in borrowed_records:
                return_tree.insert("", "end", values=(
                    record.ma_sach_muon,
                    record.ten_sach_muon,
                    record.ngay_muon,
                    record.trang_thai
                ))

        ttk.Button(return_window, text="Tìm", command=update_treeview).pack(pady=5)

        # Treeview để hiển thị danh sách sách mượn
        tree_frame = ttk.Frame(return_window)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        return_tree = ttk.Treeview(
            tree_frame,
            columns=("Mã sách", "Tên sách", "Ngày mượn", "Trạng thái"),
            show="headings"
        )
        return_tree.heading("Mã sách", text="Mã sách")
        return_tree.heading("Tên sách", text="Tên sách")
        return_tree.heading("Ngày mượn", text="Ngày mượn")
        return_tree.heading("Trạng thái", text="Trạng thái")

        return_tree.pack(fill='both', expand=True)

        def return_books():
            selected_items = return_tree.selection()
            if not selected_items:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần trả!")
                return

            for item in selected_items:
                values = return_tree.item(item, "values")
                ma_sach, ten_sach, ngay_muon, trang_thai = values

                # Tìm record trong tracking_records
                record = next((r for r in data_handler.tracking_records if r.ma_sach_muon == ma_sach), None)
                if record:
                    record.ngay_tra = datetime.now().strftime("%d/%m/%Y")
                    record.trang_thai = "Đã trả"

                    # Cập nhật số lượng sách trong books_db
                    book = data_handler.books_db.get(ma_sach)
                    if book:
                        book.so_luong += 1

        data_handler.save_data()
        messagebox.showinfo("Thành công", "Đã ghi nhận trả sách!")
        return_window.destroy()

        ttk.Button(return_window, text="Trả sách", command=return_books).pack(pady=20)

    def show_history_window(self):
        logger.info("Mở cửa sổ xem lịch sử mượn/trả")
        history_window = tk.Toplevel(self.root)
        history_window.title("Lịch Sử Mượn/Trả Sách")
        history_window.geometry("1100x600")
        
        # Search frame
        search_frame = ttk.Frame(history_window)
        search_frame.pack(fill=X, padx=20, pady=20)
        
        ttk.Label(search_frame, text="Tìm theo mã bạn đọc:").pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Result tree
        tree = ttk.Treeview(
            history_window,
            columns=('Mã bạn đọc', 'Bạn đọc', 'Sách', 'Ngày mượn', 'Ngày trả', 'Trạng thái'),
            show = 'headings'
        )
        tree.heading('Mã bạn đọc', text='Mã bạn đọc')
        tree.heading('Bạn đọc', text='Bạn đọc')
        tree.heading('Sách', text='Sách')
        tree.heading('Ngày mượn', text='Ngày mượn')
        tree.heading('Ngày trả', text='Ngày trả')
        tree.heading('Trạng thái', text='Trạng thái')
        tree.pack(pady=10, padx=20, fill=BOTH, expand=True)

        tree.column('Mã bạn đọc', width=100, anchor='center')
        tree.column('Bạn đọc', width=150, anchor='w')
        tree.column('Sách', width=200, anchor='w')
        tree.column('Ngày mượn', width=120, anchor='center')
        tree.column('Ngày trả', width=120, anchor='center')
        tree.column('Trạng thái', width=100, anchor='center')
        tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        def search_history(*args):
            keyword = search_var.get().strip().lower()
            
            # Clear current items
            for item in tree.get_children():
                tree.delete(item)
            
            # Add filtered items
            for record in data_handler.tracking_records:
                reader = data_handler.readers_db.get(record.ma_ban_doc)
                if not reader:
                    continue
                    
                if not keyword or keyword == record.ma_ban_doc:
                    # Xử lý hiển thị ngày trả và trạng thái
                    ngay_tra_display = ""
                    if record.trang_thai == "Đã trả":
                        ngay_tra_display = record.ngay_tra
                    elif record.trang_thai == "Quá hạn":
                        ngay_tra_display = "Chưa trả"
                    else:  # Đang mượn
                        ngay_tra_display = "Chưa trả"
                    tree.insert('', 'end', values=(
                        record.ma_ban_doc,
                        reader.ten,
                        record.ten_sach_muon,
                        record.ngay_muon,
                        ngay_tra_display,
                        record.trang_thai
                    ))
        
        search_var.trace('w', search_history)
        search_history()
    def show_overdue_books_window(self):
        logger.info("Mở cửa sổ danh sách sách quá hạn")
        overdue_window = tk.Toplevel(self.root)
        overdue_window.title("Danh Sách Sách Quá Hạn")
        overdue_window.geometry("1100x600")

        overdue_tree_frame = ttk.Frame(overdue_window)
        overdue_tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        overdue_tree = ttk.Treeview(
            overdue_tree_frame,
            columns=("Mã bạn đọc", "Bạn đọc", "Sách", "Ngày mượn", "Số ngày quá hạn"),
            show="headings"
        )
        overdue_tree.heading("Mã bạn đọc", text="Mã bạn đọc")
        overdue_tree.heading("Bạn đọc", text="Bạn đọc")
        overdue_tree.heading("Sách", text="Sách")
        overdue_tree.heading("Ngày mượn", text="Ngày mượn")
        overdue_tree.heading("Số ngày quá hạn", text="Số ngày quá hạn")
        overdue_tree.column("Mã bạn đọc", width=100, anchor="center")
        overdue_tree.column("Bạn đọc", width=200, anchor="w")
        overdue_tree.column("Sách", width=300, anchor="w")
        overdue_tree.column("Ngày mượn", width=150, anchor="center")
        overdue_tree.column("Số ngày quá hạn", width=150, anchor="center")

        overdue_tree.pack(fill='both', expand=True)

        from datetime import date
        today = date.today()
        overdue_records = []

        for record in data_handler.tracking_records:
            if record.trang_thai == "Quá hạn":
                # Lấy thông tin bạn đọc
                reader = data_handler.readers_db.get(record.ma_ban_doc)
                if not reader:
                    continue
                ngay_muon_dt = datetime.strptime(record.ngay_muon, "%d/%m/%Y").date()
                overdue_days = (today - ngay_muon_dt).days
                overdue_records.append((record.ma_ban_doc, record.ten_sach_muon, record.ngay_muon, overdue_days))
                overdue_tree.insert("", "end", values=(
                record.ma_ban_doc,
                reader.ten,  # Thêm tên bạn đọc
                record.ten_sach_muon,
                record.ngay_muon,
                f"{overdue_days} ngày"
            ))

        ttk.Button(overdue_window, text="Đóng", command=overdue_window.destroy).pack(pady=10)

        # Lưu trạng thái cập nhật vào file JSON
        data_handler.save_data()