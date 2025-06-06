import tkinter as tk
from tkinter import ttk, messagebox
from src.core.models import Book
from src.core.data_handler import data_handler
from src.utils.logger import logger

class BookTab:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.frame = ttk.Frame(parent)
        self.setup_ui()

    def setup_ui(self):
        # Frame chứa các nút chức năng
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', padx=10, pady=5)

        center_frame = ttk.Frame(button_frame)
        center_frame.pack(anchor='center')

        # Tạo các nút chức năng
        ttk.Button(center_frame, text="Thêm sách mới", command=self.show_add_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Cập nhật sách", command=self.show_update_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Tìm kiếm sách", command=self.show_search_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Sắp xếp", command=self.sort_books).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Lọc", command=self.filter_books).pack(side='left', padx=10)

        # Frame chứa Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_sach', 'ten_sach', 'tac_gia', 'the_loai', 'so_luong', 'tinh_trang', 'nha_xuat_ban')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        self.tree.heading('ma_sach', text='Mã sách')
        self.tree.heading('ten_sach', text='Tên sách')
        self.tree.heading('tac_gia', text='Tác giả')
        self.tree.heading('the_loai', text='Thể loại')
        self.tree.heading('so_luong', text='Số lượng')
        self.tree.heading('tinh_trang', text='Tình trạng')
        self.tree.heading('nha_xuat_ban', text='Nhà xuất bản')

        # Đặt độ rộng cột
        self.tree.column('ma_sach', width=100)
        self.tree.column('ten_sach', width=200)
        self.tree.column('tac_gia', width=150)
        self.tree.column('the_loai', width=100)
        self.tree.column('so_luong', width=80)
        self.tree.column('tinh_trang', width=100)
        self.tree.column('nha_xuat_ban', width=150)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        # Cập nhật danh sách sách
        self.update_book_list()

    def show_add_book_window(self):
        # Tạo cửa sổ mới
        add_window = tk.Toplevel(self.main_window.root)
        add_window.title("Thêm sách mới")
        add_window.geometry("600x700")
        add_window.transient(self.main_window.root)
        add_window.grab_set()

        # Tạo các trường nhập liệu
        ttk.Label(add_window, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(add_window)
        ma_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(add_window)
        ten_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(add_window)
        tac_gia_entry.pack(pady=5)

        ttk.Label(add_window, text="Thể loại:").pack(pady=5)
        the_loai_combo = ttk.Combobox(add_window, values=["Fiction", "Non-Fiction", "Science", "History", "Biography", "Khác..."])
        the_loai_combo.pack(pady=5)

        def on_the_loai_change(event):
            if the_loai_combo.get() == "Khác...":
                custom_the_loai = tk.simpledialog.askstring("Thể loại", "Nhập thể loại mới:")
                if custom_the_loai:
                    the_loai_combo.set(custom_the_loai)

        the_loai_combo.bind('<<ComboboxSelected>>', on_the_loai_change)

        ttk.Label(add_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(add_window)
        so_luong_entry.pack(pady=5)

        ttk.Label(add_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_combo = ttk.Combobox(add_window, values=["New", "Used"])
        tinh_trang_combo.pack(pady=5)

        ttk.Label(add_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(add_window)
        nha_xuat_ban_entry.pack(pady=5)

        def save_book():
            try:
                ma_sach = ma_sach_entry.get().strip()
                if not ma_sach:
                    messagebox.showerror("Lỗi", "Mã sách không được để trống")
                    return

                if ma_sach in data_handler.books_db:
                    messagebox.showerror("Lỗi", "Mã sách đã tồn tại")
                    return

                ten_sach = ten_sach_entry.get().strip()
                if not ten_sach:
                    messagebox.showerror("Lỗi", "Tên sách không được để trống")
                    return

                tac_gia = tac_gia_entry.get().strip()
                if not tac_gia:
                    messagebox.showerror("Lỗi", "Tác giả không được để trống")
                    return

                the_loai = the_loai_combo.get()
                if not the_loai:
                    messagebox.showerror("Lỗi", "Vui lòng chọn thể loại")
                    return

                try:
                    so_luong = int(so_luong_entry.get())
                    if so_luong < 0:
                        raise ValueError("Số lượng phải là số không âm")
                except ValueError as e:
                    messagebox.showerror("Lỗi", f"Số lượng không hợp lệ: {e}")
                    return

                tinh_trang = tinh_trang_combo.get()
                if not tinh_trang:
                    messagebox.showerror("Lỗi", "Vui lòng chọn tình trạng")
                    return

                nha_xuat_ban = nha_xuat_ban_entry.get().strip()
                if not nha_xuat_ban:
                    messagebox.showerror("Lỗi", "Nhà xuất bản không được để trống")
                    return

                new_book = Book(ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban)
                data_handler.books_db[ma_sach] = new_book
                data_handler.save_data()
                self.update_book_list()
                messagebox.showinfo("Thành công", f"Đã thêm sách '{ten_sach}' thành công")
                add_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi thêm sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể thêm sách: {e}")

        # Nút lưu
        ttk.Button(add_window, text="Lưu", command=save_book).pack(pady=20)

    def show_update_book_window(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần cập nhật")
            return

        # Lấy thông tin sách được chọn
        book_id = self.tree.item(selected_item[0])['values'][0]
        book = data_handler.books_db.get(book_id)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách")
            return

        # Tạo cửa sổ cập nhật
        update_window = tk.Toplevel(self.main_window.root)
        update_window.title("Cập nhật thông tin sách")
        update_window.geometry("600x700")
        update_window.transient(self.main_window.root)
        update_window.grab_set()

        # Tạo các trường nhập liệu với giá trị hiện tại
        ttk.Label(update_window, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(update_window)
        ma_sach_entry.insert(0, book.ma_sach)
        ma_sach_entry.configure(state='readonly')
        ma_sach_entry.pack(pady=5)

        ttk.Label(update_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(update_window)
        ten_sach_entry.insert(0, book.ten_sach)
        ten_sach_entry.pack(pady=5)

        ttk.Label(update_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(update_window)
        tac_gia_entry.insert(0, book.tac_gia)
        tac_gia_entry.pack(pady=5)

        ttk.Label(update_window, text="Thể loại:").pack(pady=5)
        the_loai_combo = ttk.Combobox(update_window, values=["Fiction", "Non-Fiction", "Science", "History", "Biography", "Khác..."])
        the_loai_combo.set(book.the_loai)
        the_loai_combo.pack(pady=5)

        def on_the_loai_change(event):
            if the_loai_combo.get() == "Khác...":
                custom_the_loai = tk.simpledialog.askstring("Thể loại", "Nhập thể loại mới:")
                if custom_the_loai:
                    the_loai_combo.set(custom_the_loai)

        the_loai_combo.bind('<<ComboboxSelected>>', on_the_loai_change)

        ttk.Label(update_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(update_window)
        so_luong_entry.insert(0, str(book.so_luong))
        so_luong_entry.pack(pady=5)

        ttk.Label(update_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_combo = ttk.Combobox(update_window, values=["New", "Used"])
        tinh_trang_combo.set(book.tinh_trang)
        tinh_trang_combo.pack(pady=5)

        ttk.Label(update_window, text="Nhà xuất bản:").pack(pady=5)
        nha_xuat_ban_entry = ttk.Entry(update_window)
        nha_xuat_ban_entry.insert(0, book.nha_xuat_ban)
        nha_xuat_ban_entry.pack(pady=5)

        def update_book():
            try:
                ten_sach = ten_sach_entry.get().strip()
                if not ten_sach:
                    messagebox.showerror("Lỗi", "Tên sách không được để trống")
                    return

                tac_gia = tac_gia_entry.get().strip()
                if not tac_gia:
                    messagebox.showerror("Lỗi", "Tác giả không được để trống")
                    return

                the_loai = the_loai_combo.get()
                if not the_loai:
                    messagebox.showerror("Lỗi", "Vui lòng chọn thể loại")
                    return

                try:
                    so_luong = int(so_luong_entry.get())
                    if so_luong < 0:
                        raise ValueError("Số lượng phải là số không âm")
                except ValueError as e:
                    messagebox.showerror("Lỗi", f"Số lượng không hợp lệ: {e}")
                    return

                tinh_trang = tinh_trang_combo.get()
                if not tinh_trang:
                    messagebox.showerror("Lỗi", "Vui lòng chọn tình trạng")
                    return

                nha_xuat_ban = nha_xuat_ban_entry.get().strip()
                if not nha_xuat_ban:
                    messagebox.showerror("Lỗi", "Nhà xuất bản không được để trống")
                    return

                # Cập nhật thông tin sách
                book.ten_sach = ten_sach
                book.tac_gia = tac_gia
                book.the_loai = the_loai
                book.so_luong = so_luong
                book.tinh_trang = tinh_trang
                book.nha_xuat_ban = nha_xuat_ban

                data_handler.save_data()
                self.update_book_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin sách")
                update_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi cập nhật sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể cập nhật sách: {e}")

        # Nút cập nhật
        ttk.Button(update_window, text="Cập nhật", command=update_book).pack(pady=20)
    def sort_books(self):
        # Tạo cửa sổ sắp xếp
        sort_window = tk.Toplevel(self.main_window.root)
        sort_window.title("Sắp xếp sách")
        sort_window.geometry("300x200")
        sort_window.transient(self.main_window.root)
        sort_window.grab_set()

        # Tạo các tùy chọn sắp xếp
        ttk.Label(sort_window, text="Sắp xếp theo:").pack(pady=10)
        sort_by = ttk.Combobox(sort_window, values=["Mã sách", "Tên sách", "Tác giả", "Số lượng"])
        sort_by.pack(pady=5)

        ttk.Label(sort_window, text="Thứ tự:").pack(pady=10)
        order = ttk.Combobox(sort_window, values=["Tăng dần", "Giảm dần"])
        order.pack(pady=5)

        def apply_sort():
            sort_field = sort_by.get()
            sort_order = order.get()
            
            if not sort_field or not sort_order:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn đầy đủ thông tin sắp xếp")
                return

            # Chuyển đổi tên trường sang tên thuộc tính
            field_map = {
                "Mã sách": "ma_sach",
                "Tên sách": "ten_sach",
                "Tác giả": "tac_gia",
                "Số lượng": "so_luong"
            }
            
            field = field_map[sort_field]
            reverse = sort_order == "Giảm dần"
            
            # Sắp xếp danh sách sách
            sorted_books = sorted(
                data_handler.books_db.values(),
                key=lambda x: getattr(x, field),
                reverse=reverse
            )
            
            self.update_book_list(sorted_books)
            sort_window.destroy()

        # Nút áp dụng
        ttk.Button(sort_window, text="Áp dụng", command=apply_sort).pack(pady=20)
    def filter_books(self):
        # Tạo cửa sổ lọc
        filter_window = tk.Toplevel(self.main_window.root)
        filter_window.title("Lọc sách")
        filter_window.geometry("300x250")
        filter_window.transient(self.main_window.root)
        filter_window.grab_set()

        # Tạo các tùy chọn lọc
        ttk.Label(filter_window, text="Lọc theo:").pack(pady=10)
        filter_by = ttk.Combobox(filter_window, values=["Thể loại", "Tình trạng", "Nhà xuất bản"])
        filter_by.pack(pady=5)

        ttk.Label(filter_window, text="Giá trị:").pack(pady=10)
        filter_value = ttk.Entry(filter_window)
        filter_value.pack(pady=5)

        def apply_filter():
            filter_field = filter_by.get()
            value = filter_value.get().strip()
            
            if not filter_field or not value:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin lọc")
                return

            # Chuyển đổi tên trường sang tên thuộc tính
            field_map = {
                "Thể loại": "the_loai",
                "Tình trạng": "tinh_trang",
                "Nhà xuất bản": "nha_xuat_ban"
            }
            
            field = field_map[filter_field]
            
            # Lọc danh sách sách
            filtered_books = [
                book for book in data_handler.books_db.values()
                if str(getattr(book, field)).lower() == value.lower()
            ]
            
            self.update_book_list(filtered_books)
            filter_window.destroy()

        # Nút áp dụng
        ttk.Button(filter_window, text="Áp dụng", command=apply_filter).pack(pady=20)

    def update_book_list(self, books=None):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy danh sách sách cần hiển thị
        if books is None:
            books = data_handler.books_db.values()

        # Thêm dữ liệu mới vào Treeview
        for book in books:
            self.tree.insert('', 'end', values=(
                book.ma_sach,
                book.ten_sach,
                book.tac_gia,
                book.the_loai,
                book.so_luong,
                book.tinh_trang,
                book.nha_xuat_ban
            ))

    def show_search_book_window(self):
        # Tạo cửa sổ tìm kiếm
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("Tìm kiếm sách")
        search_window.geometry("400x200")
        search_window.transient(self.main_window.root)
        search_window.grab_set()

        # Tạo các trường tìm kiếm
        ttk.Label(search_window, text="Nhập từ khóa tìm kiếm:").pack(pady=10)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        def search():
            search_term = search_entry.get().strip().lower()
            if not search_term:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")
                return

            # Tìm kiếm sách
            found_books = []
            for book in data_handler.books_db.values():
                if (search_term in book.ma_sach.lower() or
                    search_term in book.ten_sach.lower() or
                    search_term in book.tac_gia.lower() or
                    search_term in book.the_loai.lower() or
                    search_term in book.nha_xuat_ban.lower()):
                    found_books.append(book)

            if found_books:
                self.update_book_list(found_books)
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách")
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy sách nào")
                self.update_book_list()  # Hiển thị lại tất cả sách

            search_window.destroy()

        # Nút tìm kiếm
        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)