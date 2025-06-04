import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import book_manager
import reader_manager
import tracking_manager
import data_handler
from models import Book, Reader, TrackBook
from logger import logger
from datetime import datetime
from logger import logger
import customtkinter as ctk

class LibraryManagementSystem:    
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Thư Viện")
        self.root.geometry("1200x800")
        self.style = ttk.Style()

        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Tạo các tab
        self.book_tab = ttk.Frame(self.notebook)
        self.reader_tab = ttk.Frame(self.notebook)
        self.tracking_tab = ttk.Frame(self.notebook)

        # Thêm các tab vào notebook
        self.notebook.add(self.book_tab, text='Quản lý Sách')
        self.notebook.add(self.reader_tab, text='Quản lý Bạn đọc')
        self.notebook.add(self.tracking_tab, text='Mượn/Trả Sách')

        # Khởi tạo giao diện cho từng tab
        self.setup_book_tab()
        self.setup_reader_tab()
        self.setup_tracking_tab()

        #Font chữ mặc định 
        self.style.configure('.', font=('Segoe UI', 11, 'bold'))

        #thiết lập treeview
        self.style.configure("Treeview", rowheight=100, font = ('Arial', 11))

        #thiết lập các nút 
        self.style.configure("TButton", font=("Segoe UI", 11, "bold"))  # Áp dụng cho tất cả các nút

    def setup_book_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.book_tab)
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
        self.sort_by = ttk.Combobox(filter_frame, values=["Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"], state="readonly")
        self.sort_by.pack(side=tk.LEFT, padx=5)
        self.sort_by.bind("<<ComboboxSelected>>", lambda e: self.update_book_list())

        ttk.Label(filter_frame, text="Lọc theo thể loại:").pack(side=tk.LEFT, padx=5)
        self.filter_by_genre = ttk.Combobox(filter_frame, values=["Tất cả", "Fiction", "Non-Fiction", "Science", "History", "Biography"], state="readonly")
        self.filter_by_genre.pack(side=tk.LEFT, padx=5)
        self.filter_by_genre.bind("<<ComboboxSelected>>", lambda e: self.update_book_list())

        # Frame chứa Treeview và Scrollbar
        tree_frame = ttk.Frame(self.book_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Thêm thanh cuộn
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.book_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("ID", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"), show="headings")
        self.book_tree.pack(fill='both', expand=True)

        tree_scroll.config(command=self.book_tree.yview)

        for col in ["ID", "Tiêu đề", "Tác giả", "Thể loại", "Số lượng", "Tình trạng"]:
            self.book_tree.heading(col, text=col)

        self.update_book_list()

    def setup_reader_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.reader_tab)
        btn_frame.pack(pady=20)

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

        # Treeview để hiển thị danh sách bạn đọc
        tree_frame = ttk.Frame(self.reader_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.reader_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Tên', 'Ngày sinh', 'Giới tính', 'Địa chỉ', 'SDT'),
            yscrollcommand=tree_scroll.set,
            bootstyle="primary"
        )
        tree_scroll.config(command=self.reader_tree.yview)

        self.reader_tree.heading('ID', text='Mã bạn đọc')
        self.reader_tree.heading('Tên', text='Tên')
        self.reader_tree.heading('Ngày sinh', text='Ngày sinh')
        self.reader_tree.heading('Giới tính', text='Giới tính')
        self.reader_tree.heading('Địa chỉ', text='Địa chỉ')
        self.reader_tree.heading('SDT', text='Điện thoại')
        

        self.reader_tree.column('ID', anchor='c', width=120)
        self.reader_tree.column('Tên', anchor='w', width=250)
        self.reader_tree.column('Ngày sinh', anchor='center', width=120)
        self.reader_tree.column('Giới tính', anchor='center', width=100)
        self.reader_tree.column('Địa chỉ', anchor='w', width=250)
        self.reader_tree.column('SDT', anchor='w', width=150)
        

        self.reader_tree.pack(fill='both', expand=True)
        self.reader_tree.tag_configure('oddrow', background='#E8F4FA')
        self.reader_tree.tag_configure('evenrow', background='#FFFFFF')

        # Thiết lập kiểu Treeview giống tab Quản lý Sách
        self.reader_tree.configure(style="Treeview")

        self.update_reader_list()

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
        command=self.show_return_window
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

        # Treeview để hiển thị danh sách mượn/trả
        tree_frame = ttk.Frame(self.tracking_tab)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tracking_tree = ttk.Treeview(
            tree_frame,
            columns=('Bạn đọc', 'Sách', 'Ngày mượn', 'Ngày trả', 'Trạng thái'),
            yscrollcommand=tree_scroll.set,
            bootstyle="primary"
        )
        tree_scroll.config(command=self.tracking_tree.yview)

        self.tracking_tree.heading('Bạn đọc', text='Bạn đọc')
        self.tracking_tree.heading('Sách', text='Sách')
        self.tracking_tree.heading('Ngày mượn', text='Ngày mượn')
        self.tracking_tree.heading('Ngày trả', text='Ngày trả')
        self.tracking_tree.heading('Trạng thái', text='Trạng thái')

        self.tracking_tree.column('Bạn đọc', anchor='c', width=100)
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
        add_window = ttk.Toplevel(self.root)
        add_window.title("Thêm Sách Mới")
        add_window.geometry("600x800")

        ttk.Label(add_window, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(add_window)
        ma_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(add_window)
        tac_gia_entry.pack(pady=5)

        ttk.Label(add_window, text="Thể loại:").pack(pady=5)
        the_loai_entry = ttk.Entry(add_window)
        the_loai_entry.pack(pady=5)

        ttk.Label(add_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(add_window)
        ten_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(add_window)
        so_luong_entry.pack(pady=5)

        ttk.Label(add_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_entry = ttk.Entry(add_window)
        tinh_trang_entry.pack(pady=5)

        ttk.Label(add_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(add_window)
        nha_xuat_ban_entry.pack(pady=5)

        def save_book():
            try:
                # Lấy dữ liệu từ các trường nhập liệu
                ma_sach = ma_sach_entry.get().strip()
                ten_sach = ten_sach_entry.get().strip()
                tac_gia = tac_gia_entry.get().strip()
                the_loai = the_loai_entry.get().strip()
                so_luong = so_luong_entry.get().strip()
                tinh_trang = tinh_trang_entry.get().strip()
                nha_xuat_ban = nha_xuat_ban_entry.get().strip()

                # Kiểm tra dữ liệu đầu vào
                if not all([ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban]):
                    raise ValueError("Vui lòng điền đầy đủ thông tin!")

                if not so_luong.isdigit() or int(so_luong) <= 0:
                    raise ValueError("Số lượng phải là một số nguyên dương!")

                # Kiểm tra mã sách đã tồn tại
                if ma_sach in data_handler.books_db:
                    raise ValueError("Mã sách đã tồn tại!")

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
        update_window.geometry("400x700")
        ttk.Label(update_window, text="Cập nhật thông tin sách", font=("Arial", 16)).pack(pady=10)
        # Form fields
        ttk.Label(update_window, text="Mã sách:").pack(pady=5)
        ma_sach_display_label = ttk.Label(update_window, text=book.ma_sach)
        ma_sach_display_label.pack(pady=5)

        ttk.Label(update_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(update_window)
        tac_gia_entry.insert(0, book.tac_gia)
        tac_gia_entry.pack(pady=5)

        ttk.Label(update_window, text="Thể loại:").pack(pady=5)
        the_loai_entry = ttk.Entry(update_window)
        the_loai_entry.insert(0, book.the_loai)
        the_loai_entry.pack(pady=5)

        ttk.Label(update_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(update_window)
        ten_sach_entry.insert(0, book.ten_sach)
        ten_sach_entry.pack(pady=5)
        
        ttk.Label(update_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(update_window)
        so_luong_entry.insert(0, str(book.so_luong))
        so_luong_entry.pack(pady=5)

        ttk.Label(update_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_entry = ttk.Entry(update_window)
        tinh_trang_entry.insert(0, book.tinh_trang)
        tinh_trang_entry.pack(pady=5)

        ttk.Label(update_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(update_window)
        nha_xuat_ban_entry.insert(0, book.nha_xuat_ban)
        nha_xuat_ban_entry.pack(pady=5)
        
        def update_book():
            try:
                book.ten_sach = ten_sach_entry.get().strip()
                book.tac_gia = tac_gia_entry.get().strip()
                book.so_luong = int(so_luong_entry.get().strip())
                book.tinh_trang = tinh_trang_entry.get().strip()
                book.nha_xuat_ban = nha_xuat_ban_entry.get().strip()
                book.the_loai = the_loai_entry.get().strip()

                self.update_book_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin sách!")
                data_handler.save_data()
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")

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

    def update_book_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        # Lấy danh sách sách từ books_db
        books = list(data_handler.books_db.values())

        # Lọc theo thể loại nếu được chọn
        selected_genre = self.filter_by_genre.get()
        if selected_genre and selected_genre != "Tất cả":
            books = [book for book in books if book.the_loai == selected_genre]

        # Sắp xếp theo tiêu chí được chọn
        sort_criteria = self.sort_by.get()
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

        # Thêm dữ liệu vào Treeview với màu xen kẽ
        for index, book in enumerate(books):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.book_tree.insert("", "end", values=(
                book.ma_sach, book.ten_sach, book.tac_gia, book.the_loai, book.so_luong, book.tinh_trang
            ), tags=(tag,))

        # Định nghĩa màu sắc cho các dòng xen kẽ
        self.book_tree.tag_configure('oddrow', background='#E8F4FA')
        self.book_tree.tag_configure('evenrow', background='#FFFFFF')

    def show_search_book_window(self):
        logger.info("Mở cửa sổ tìm kiếm sách")
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm Kiếm Sách")
        search_window.geometry("800x200")

        ttk.Label(search_window, text="Nhập từ khóa tìm kiếm:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        def search():
            keyword = search_entry.get().strip().lower()
            found_books = []
            for book in data_handler.books_db.values():
                if (keyword in book.ma_sach.lower() or
                    keyword in book.ten_sach.lower() or
                    keyword in book.tac_gia.lower()):
                    found_books.append(book)
            
            # Hiển thị kết quả
            result_window = tk.Toplevel(search_window)
            result_window.title("Kết Quả Tìm Kiếm")
            result_window.geometry("600x400")
            
            result_tree = ttk.Treeview(result_window, 
                                     columns=('ID', 'Tên', 'Tác giả', 'Số lượng', 'Tình trạng', 'Nhà xuất bản', 'Thể loại'))
            result_tree.heading('ID', text='Mã sách')
            result_tree.heading('Tên', text='Tên sách')
            result_tree.heading('Tác giả', text='Tác giả')
            result_tree.heading('Số lượng', text='Số lượng')
            result_tree.heading('Tình trạng', text='Tình trạng')
            result_tree.heading('Nhà xuất bản', text='Nhà xuất bản')
            result_tree.heading('Thể loại', text='Thể loại')
            result_tree.pack(pady=10, padx=10, fill='both', expand=True)
            # Thêm kết quả vào treeview
            for book in found_books:
                result_tree.insert('', 'end', values=(
                    book.ma_sach,
                    book.ten_sach,
                    book.tac_gia,
                    book.so_luong,
                    book.tinh_trang,
                    book.nha_xuat_ban,
                    book.the_loai
                ))

        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)    
    def show_add_reader_window(self):
        logger.info("Mở cửa sổ thêm bạn đọc mới")
        add_window = ttk.Toplevel(self.root)
        add_window.title("Thêm Bạn Đọc Mới")
        add_window.geometry("400x600")  
        
        form = ScrolledFrame(add_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Form fields
        ttk.Label(form, text="Mã bạn đọc:").pack(pady=5)
        ma_doc_entry = ttk.Entry(form)
        ma_doc_entry.pack(pady=5)
        
        ttk.Label(form, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(form)
        ten_entry.pack(pady=5)
        
        ttk.Label(form, text="Ngày sinh (DD/MM/YYYY):").pack(pady=5)
        ngay_sinh_entry = ttk.Entry(form)
        ngay_sinh_entry.pack(pady=5)
        
        ttk.Label(form, text="Giới tính:").pack(pady=5)
        gioi_tinh_combobox = ttk.Combobox(form, values=["Nam", "Nữ", "Khác"])
        gioi_tinh_combobox.pack(pady=5)
        
        ttk.Label(form, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(form)
        dia_chi_entry.pack(pady=5)
        
        ttk.Label(form, text="Số điện thoại:").pack(pady=5)
        sdt_entry = ttk.Entry(form)
        sdt_entry.pack(pady=5)

        def save_reader():
            try:
                ma_doc = ma_doc_entry.get().strip()
                if ma_doc in data_handler.readers_db:
                    raise ValueError("Mã bạn đọc đã tồn tại!")
                
                # Validate required fields
                if not all([ma_doc, ten_entry.get().strip(), ngay_sinh_entry.get().strip()]):
                    raise ValueError("Vui lòng điền đầy đủ thông tin bắt buộc!")
                
                # Create new reader
                new_reader = Reader(
                    ma_ban_doc=ma_doc,
                    ten=ten_entry.get().strip(),
                    ngay_sinh=ngay_sinh_entry.get().strip(),
                    gioi_tinh=gioi_tinh_combobox.get(),
                    dia_chi=dia_chi_entry.get().strip(),
                    so_dien_thoai=sdt_entry.get().strip()
                )
                
                # Save to database
                data_handler.readers_db[ma_doc] = new_reader
                data_handler.save_data()
                self.update_reader_list()
                
                logger.info(f"Thêm bạn đọc mới thành công: {ma_doc}")
                messagebox.showinfo("Thành công", "Đã thêm bạn đọc mới!")
                
                add_window.destroy()
                
            except ValueError as e:
                logger.error(f"Lỗi khi thêm bạn đọc: {str(e)}")
                messagebox.showerror("Lỗi", str(e))

        # Buttons
        button_frame = ttk.Frame(form)
        button_frame.pack(fill=X, pady=20)
        
        ttk.Button(
            button_frame,
            text="Hủy",
            bootstyle="secondary",
            command=add_window.destroy
        ).pack(side=RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Lưu",
            bootstyle="success",
            command=save_reader
        ).pack(side=RIGHT)

    def update_reader_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)

        # Lấy danh sách bạn đọc từ readers_db
        readers = list(data_handler.readers_db.values())

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

        update_window = ttk.Toplevel(self.root)
        update_window.title("Cập Nhật Thông Tin Bạn Đọc")
        update_window.geometry("400x600")
        
        form = ScrolledFrame(update_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Mã bạn đọc (hiển thị, không cho sửa)
        ttk.Label(form, text="Mã bạn đọc:").pack(pady=5) #
        ma_doc_display = ttk.Label(form, text=reader.ma_ban_doc) # Giả sử reader.ma_ban_doc là chuỗi
        ma_doc_display.pack(pady=5)

        ttk.Label(form, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(form)
        ten_entry.insert(0, reader.ten)
        ten_entry.pack(pady=5)
        
        ttk.Label(form, text="Ngày sinh:").pack(pady=5)
        ngay_sinh_entry = ttk.Entry(form)
        ngay_sinh_entry.insert(0, reader.ngay_sinh)
        ngay_sinh_entry.pack(pady=5)
        ttk.Label(form, text="Giới tính:").pack(pady=5) #

        gioi_tinh_current = reader.gioi_tinh #
        gioi_tinh_combobox = ttk.Combobox(form, values=["Nam", "Nữ", "Khác"]) #
        if gioi_tinh_current in gioi_tinh_combobox['values']: #
            gioi_tinh_combobox.set(gioi_tinh_current) #
        gioi_tinh_combobox.pack(pady=5) #

        ttk.Label(form, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(form)
        dia_chi_entry.insert(0, reader.dia_chi)
        dia_chi_entry.pack(pady=5)
        
        ttk.Label(form, text="Số điện thoại:").pack(pady=5)
        sdt_entry = ttk.Entry(form)
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
        search_window = ttk.Toplevel(self.root)
        search_window.title("Tìm Kiếm Bạn Đọc")
        search_window.geometry("400x200")

        ttk.Label(search_window, text="Nhập từ khóa tìm kiếm:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        def search():
            keyword = search_entry.get().strip().lower()
            found_readers = []
            for reader in data_handler.readers_db.values():
                if (keyword in reader.ma_ban_doc.lower() or
                    keyword in reader.ten.lower() or
                    keyword in reader.so_dien_thoai.lower()):
                    found_readers.append(reader)
            
            # Hiển thị kết quả
            result_window = ttk.Toplevel(search_window)
            result_window.title("Kết Quả Tìm Kiếm")
            result_window.geometry("600x400")
            
            result_tree = ttk.Treeview(
                result_window, 
                columns=('ID', 'Tên', 'SĐT', 'Địa chỉ'),
                bootstyle="primary"
            )
            result_tree.heading('ID', text='Mã bạn đọc')
            result_tree.heading('Tên', text='Tên')
            result_tree.heading('SĐT', text='Số điện thoại')
            result_tree.heading('Địa chỉ', text='Địa chỉ')
            result_tree.pack(pady=10, padx=10, fill='both', expand=True)
            
            for reader in found_readers:
                result_tree.insert('', 'end', values=(
                    reader.ma_ban_doc,
                    reader.ten,
                    reader.so_dien_thoai,
                    reader.dia_chi
                ))

        ttk.Button(
            search_window,
            text="Tìm kiếm",
            bootstyle="primary",
            command=search
        ).pack(pady=20)    
    def show_borrow_window(self):
        logger.info("Mở cửa sổ mượn sách")
        borrow_window = ttk.Toplevel(self.root)
        borrow_window.title("Mượn Sách")
        borrow_window.geometry("500x400")
        
        # Form
        form = ScrolledFrame(borrow_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Bạn đọc selection
        ttk.Label(form, text="Chọn bạn đọc:").pack(pady=5)
        reader_var = tk.StringVar()
        reader_cb = ttk.Combobox(form, textvariable=reader_var)
        reader_cb['values'] = [f"{r.ma_ban_doc} - {r.ten}" for r in data_handler.readers_db.values()]
        reader_cb.pack(pady=5)
        
        # Sách selection
        ttk.Label(form, text="Chọn sách:").pack(pady=5)
        book_var = tk.StringVar()
        book_cb = ttk.Combobox(form, textvariable=book_var)
        book_cb['values'] = [f"{b.ma_sach} - {b.ten_sach}" for b in data_handler.books_db.values()]
        book_cb.pack(pady=5)

        def borrow_book():
            try:
                reader_id = reader_var.get().split(' - ')[0]
                book_id = book_var.get().split(' - ')[0]
                
                if reader_id not in data_handler.readers_db:
                    raise ValueError("Vui lòng chọn bạn đọc!")
                if book_id not in data_handler.books_db:
                    raise ValueError("Vui lòng chọn sách!")
                
                book = data_handler.books_db[book_id]
                if book.so_luong <= 0:
                    raise ValueError("Sách đã hết!")
                
                # Check if already borrowed
                for record in data_handler.tracking_records:
                    if (record.ma_ban_doc == reader_id and 
                        record.ma_sach_muon == book_id and 
                        record.trang_thai == "Borrowed"):
                        raise ValueError("Bạn đọc đã mượn cuốn sách này và chưa trả!")
                
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
        
        ttk.Button(
            form,
            text="Mượn sách",
            bootstyle="success",
            command=borrow_book
        ).pack(pady=20)

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
        return_window = ttk.Toplevel(self.root)
        return_window.title("Trả Sách")
        return_window.geometry("500x400")
        
        # Form
        form = ScrolledFrame(return_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        # Get borrowed books
        borrowed_records = [record for record in data_handler.tracking_records 
                          if record.trang_thai == "Borrowed"]
        
        if not borrowed_records:
            messagebox.showinfo("Thông báo", "Không có sách nào đang được mượn!")
            return_window.destroy()
            return
        
        # Create selection
        ttk.Label(form, text="Chọn sách cần trả:").pack(pady=5)
        record_var = tk.StringVar()
        record_cb = ttk.Combobox(form, textvariable=record_var)
        record_values = []
        for record in borrowed_records:
            reader = data_handler.readers_db[record.ma_ban_doc]
            record_values.append(f"{record.ma_sach_muon} - {record.ten_sach_muon} (Bạn đọc: {reader.ten})")
        record_cb['values'] = record_values
        record_cb.pack(pady=5)

        def return_book():
            try:
                if not record_var.get():
                    raise ValueError("Vui lòng chọn sách cần trả!")
                
                book_id = record_var.get().split(' - ')[0]
                
                # Find the record
                record = None
                for r in borrowed_records:
                    if r.ma_sach_muon == book_id:
                        record = r
                        break
                
                if not record:
                    raise ValueError("Không tìm thấy thông tin mượn sách!")
                
                # Update record
                now = datetime.now().strftime("%d/%m/%Y")
                record.ngay_tra = now
                record.trang_thai = "Returned"
                
                # Update book quantity
                book = data_handler.books_db[book_id]
                book.so_luong += 1
                
                self.update_tracking_list()
                self.update_book_list()
                data_handler.save_data()
                
                logger.info(f"Trả sách thành công: {book_id}")
                messagebox.showinfo("Thành công", "Đã ghi nhận trả sách!")
                return_window.destroy()
                
            except ValueError as e:
                logger.error(f"Lỗi khi trả sách: {str(e)}")
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(
            form,
            text="Trả sách",
            bootstyle="success",
            command=return_book
        ).pack(pady=20)

    def show_history_window(self):
        logger.info("Mở cửa sổ xem lịch sử mượn/trả")
        history_window = ttk.Toplevel(self.root)
        history_window.title("Lịch Sử Mượn/Trả Sách")
        history_window.geometry("800x600")
        
        # Search frame
        search_frame = ttk.Frame(history_window)
        search_frame.pack(fill=X, padx=20, pady=20)
        
        ttk.Label(search_frame, text="Tìm theo bạn đọc:").pack(side=LEFT)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=LEFT, padx=5)
        
        # Result tree
        tree = ttk.Treeview(
            history_window,
            columns=('Bạn đọc', 'Sách', 'Ngày mượn', 'Ngày trả', 'Trạng thái'),
            bootstyle="primary"
        )
        tree.heading('Bạn đọc', text='Bạn đọc')
        tree.heading('Sách', text='Sách')
        tree.heading('Ngày mượn', text='Ngày mượn')
        tree.heading('Ngày trả', text='Ngày trả')
        tree.heading('Trạng thái', text='Trạng thái')
        tree.pack(pady=10, padx=20, fill=BOTH, expand=True)
        
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
                    
                if not keyword or keyword in reader.ten.lower():
                    tree.insert('', 'end', values=(
                        reader.ten,
                        record.ten_sach_muon,
                        record.ngay_muon,
                        record.ngay_tra or "Chưa trả",
                        record.trang_thai
                    ))
        
        search_var.trace('w', search_history)
        search_history()

if __name__ == "__main__":
    data_handler.load_data()
    root = ttk.Window(themename="cosmo")
    app = LibraryManagementSystem(root)
    root.mainloop()
    data_handler.save_data()