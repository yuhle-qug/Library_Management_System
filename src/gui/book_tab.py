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

        # Update button definitions
        ttk.Button(
            center_frame, 
            text="Thêm sách mới",
            command=self.show_add_book_window
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            center_frame,
            text="Cập nhật thông tin",
            command=self.show_update_book_window,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            center_frame, 
            text="Tìm kiếm sách",
            command=self.show_search_book_window,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            center_frame, 
            text="Xóa sách",
            command=self.delete_book_window,
        ).pack(side=tk.LEFT, padx=5)

        # Frame chứa các điều khiển sắp xếp và lọc
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(fill='x', padx=10, pady=5)

        # Phần sắp xếp
        sort_frame = ttk.LabelFrame(controls_frame, text="Sắp xếp")
        sort_frame.pack(side='left', padx=5, fill='x', expand=True)
        ttk.Label(sort_frame, text="Sắp xếp theo:").pack(side='left', padx=5)
        self.sort_by_combo = ttk.Combobox(sort_frame, values=["Mã sách", "Tên sách", "Tác giả", "Số lượng"], state="readonly")
        self.sort_by_combo.current(0)  # Mặc định sắp xếp theo Mã sách
        self.sort_by_combo.pack(side='left', padx=5)

        ttk.Label(sort_frame, text="Thứ tự:").pack(side='left', padx=5)
        self.sort_order_combo = ttk.Combobox(sort_frame, values=["Tăng dần", "Giảm dần"], state="readonly")
        self.sort_order_combo.current(0)  # Mặc định tăng dần
        self.sort_order_combo.pack(side='left', padx=5)

        # Phần lọc
        filter_frame = ttk.LabelFrame(controls_frame, text="Lọc")
        filter_frame.pack(side='left', padx=5, fill='x', expand=True)

        ttk.Label(filter_frame, text="Lọc theo:").pack(side='left', padx=5)
        self.filter_by_combo = ttk.Combobox(filter_frame, values=["Thể loại", "Tình trạng"], state="readonly")
        self.filter_by_combo.pack(side='left', padx=5)

        ttk.Label(filter_frame, text="Giá trị:").pack(side='left', padx=5)

        # Frame to hold dynamic filter value widget
        self.filter_value_frame = ttk.Frame(filter_frame)
        self.filter_value_frame.pack(side='left', padx=5, fill='x', expand=True)

        # Initial dummy widget (will be replaced)
        self.current_filter_value_widget = ttk.Entry(self.filter_value_frame)
        self.current_filter_value_widget.pack(fill='x', expand=True)

        self.filter_by_combo.bind('<<ComboboxSelected>>', self.on_filter_criteria_change)

        # Nút điều khiển
        control_buttons_frame = ttk.Frame(controls_frame)
        control_buttons_frame.pack(side='left', padx=5)

        ttk.Button(control_buttons_frame, text="Áp dụng", style="Pastel.TButton", command=self.apply_filters).pack(side='left', padx=5)
        ttk.Button(control_buttons_frame, text="Reset", style="Pastel.TButton", command=self.reset_filters).pack(side='left', padx=5)

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

    def on_filter_criteria_change(self, event):
        # Clear current filter value widget
        for widget in self.filter_value_frame.winfo_children():
            widget.destroy()

        selected_criteria = self.filter_by_combo.get()

        if selected_criteria == "Thể loại":
            values = self.get_unique_book_genres()
            self.current_filter_value_widget = ttk.Combobox(self.filter_value_frame, values=values, state="readonly")
            self.current_filter_value_widget.pack(fill='x', expand=True)
            # Set default to "Tất cả" if it exists
            if "Tất cả" in values:
                self.current_filter_value_widget.set("Tất cả")
        elif selected_criteria == "Tình trạng":
            values = self.get_unique_book_statuses()
            self.current_filter_value_widget = ttk.Combobox(self.filter_value_frame, values=values, state="readonly")
            self.current_filter_value_widget.pack(fill='x', expand=True)
            # Set default to "Tất cả" if it exists
            if "Tất cả" in values:
                self.current_filter_value_widget.set("Tất cả")
        else:
            # Fallback to entry for other criteria (should not happen with current values)
            self.current_filter_value_widget = ttk.Entry(self.filter_value_frame)
            self.current_filter_value_widget.pack(fill='x', expand=True)

    def get_unique_book_genres(self):
        genres = set()
        for book in data_handler.books_db.values():
            genres.add(book.the_loai)
        # Simply return all unique genres found in the data, plus "Tất cả"
        genre_list = ["Tất cả"] + sorted(list(genres))
        return genre_list

    def get_unique_book_statuses(self):
        statuses = set()
        for book in data_handler.books_db.values():
            statuses.add(book.tinh_trang)
        status_list = ["Tất cả"] + sorted(list(statuses))
        return status_list

    def apply_filters(self):
        # Lấy các giá trị từ controls
        sort_field = self.sort_by_combo.get()
        sort_order = self.sort_order_combo.get()
        filter_field = self.filter_by_combo.get()
        # Get value from the currently active filter widget
        if isinstance(self.current_filter_value_widget, ttk.Combobox):
             filter_value = self.current_filter_value_widget.get().strip()
        else:
             # Should not happen with current filter criteria
             filter_value = self.current_filter_value_widget.get().strip().lower()

        # Chuyển đổi tên trường sang tên thuộc tính
        field_map = {
            "Mã sách": "ma_sach",
            "Tên sách": "ten_sach",
            "Tác giả": "tac_gia",
            "Số lượng": "so_luong",
            "Thể loại": "the_loai",
            "Tình trạng": "tinh_trang",
            "Nhà xuất bản": "nha_xuat_ban" # Keep for sorting/other potential uses if needed
        }

        # Lọc dữ liệu
        filtered_books = list(data_handler.books_db.values())

        if filter_field and filter_value and filter_value != "Tất cả":
            field = field_map[filter_field]
            if filter_field == "Số lượng":
                # Handle numerical filter for quantity (if quantity filter was needed)
                # For now, quantity filter is not in the combo, but keep the logic if needed later
                pass # This part might need adjustment if quantity filter is re-added
            else:
                 # Standard text/category filter (sensitive for Combobox selection)
                 filtered_books = [
                     book for book in filtered_books
                     if str(getattr(book, field)) == filter_value
                 ]

        # Sắp xếp dữ liệu
        if sort_field:
            field = field_map[sort_field]
            reverse = sort_order == "Giảm dần"
            try:
                # Handle potential type issues with sorting, e.g., sorting numbers
                if sort_field == "Số lượng":
                     filtered_books.sort(key=lambda x: int(getattr(x, field)), reverse=reverse)
                else:
                    filtered_books.sort(key=lambda x: getattr(x, field), reverse=reverse)
            except Exception as e:
                logger.error(f"Lỗi khi sắp xếp sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể sắp xếp danh sách: {e}")
                return # Stop if sorting fails

        logger.info(f"apply_filters: Filtered and sorted {len(filtered_books)} books.")

        # Cập nhật Treeview
        logger.info(f"apply_filters: Calling update_book_list with {len(filtered_books)} books.")
        self.update_book_list(filtered_books)

    def reset_filters(self):
        # Reset các controls về giá trị mặc định
        self.sort_by_combo.current(0)
        self.sort_order_combo.current(0)
        self.filter_by_combo.set("") # Clear filter criteria selection
        # Clear and reset the dynamic filter value widget
        for widget in self.filter_value_frame.winfo_children():
            widget.destroy()
        # Re-add a default empty entry or set the appropriate default combo if needed
        # For now, just clear the frame. The on_filter_criteria_change will set the widget when a criteria is selected.

        # Hiển thị lại danh sách gốc (sắp xếp theo mã sách tăng dần)
        books = sorted(data_handler.books_db.values(), key=lambda x: x.ma_sach)
        self.update_book_list(books)

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
        the_loai_list = [
            "Khoa học", "Lịch sử", "Tiểu thuyết", "Truyện ngắn", "Tâm lý", "Kinh tế", "Chính trị",
            "Tôn giáo", "Triết học", "Thiếu nhi", "Giáo trình", "Công nghệ", "Kỹ thuật", "Y học", "Khác..."
        ]
        the_loai_combo = ttk.Combobox(add_window, values=the_loai_list)
        the_loai_combo.pack(pady=5)
        
        # Frame chứa label và entry cho thể loại khác
        other_genre_frame = ttk.Frame(add_window)
        other_genre_frame.pack(pady=5)
        other_genre_label = ttk.Label(other_genre_frame, text="Nhập thể loại sách mới tại đây:")
        other_genre_entry = ttk.Entry(other_genre_frame)
        other_genre_label.pack(pady=2)
        other_genre_entry.pack(pady=2)
        other_genre_frame.pack_forget()  # Ẩn frame ban đầu

        def on_the_loai_change(event):
            if the_loai_combo.get() == "Khác...":
                other_genre_frame.pack(pady=5)
            else:
                other_genre_frame.pack_forget()

        the_loai_combo.bind('<<ComboboxSelected>>', on_the_loai_change)

        ttk.Label(add_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(add_window)
        so_luong_entry.pack(pady=5)

        ttk.Label(add_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_combo = ttk.Combobox(add_window, values=["Mới", "Đã sử dụng"], state="readonly")
        tinh_trang_combo.current(0)
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
                if the_loai == "Khác...":
                    the_loai = other_genre_entry.get().strip()
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
        ttk.Button(add_window, text="Lưu", style="Pastel.TButton", command=save_book).pack(pady=20)

    def show_update_book_window(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần cập nhật!")
            return

        # Lấy thông tin sách được chọn
        book_id = str(self.tree.item(selected_item[0])['values'][0])
        book = data_handler.books_db.get(book_id)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách!")
            return

        # Tạo cửa sổ mới
        update_window = tk.Toplevel(self.main_window.root)
        update_window.title("Cập nhật sách")
        update_window.geometry("600x700")
        update_window.transient(self.main_window.root)
        update_window.grab_set()

        # Tạo các trường nhập liệu
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
        the_loai_list = [
            "Khoa học", "Lịch sử", "Tiểu thuyết", "Truyện ngắn", "Tâm lý", "Kinh tế", "Chính trị",
            "Tôn giáo", "Triết học", "Thiếu nhi", "Giáo trình", "Công nghệ", "Kỹ thuật", "Y học", "Khác..."
        ]
        the_loai_combo = ttk.Combobox(update_window, values=the_loai_list)
        the_loai_combo.set(book.the_loai)
        the_loai_combo.pack(pady=5)
        
        # Frame chứa label và entry cho thể loại khác
        other_genre_frame = ttk.Frame(update_window)
        other_genre_frame.pack(pady=5)
        other_genre_label = ttk.Label(other_genre_frame, text="Nhập thể loại sách mới tại đây:")
        other_genre_entry = ttk.Entry(other_genre_frame)
        other_genre_label.pack(pady=2)
        other_genre_entry.pack(pady=2)
        if book.the_loai not in the_loai_list:
            other_genre_entry.insert(0, book.the_loai)
        else:
            other_genre_frame.pack_forget()

        def on_the_loai_change_update(event):
            if the_loai_combo.get() == "Khác...":
                other_genre_frame.pack(pady=5)
            else:
                other_genre_frame.pack_forget()
        the_loai_combo.bind('<<ComboboxSelected>>', on_the_loai_change_update)

        ttk.Label(update_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(update_window)
        so_luong_entry.insert(0, book.so_luong)
        so_luong_entry.pack(pady=5)

        ttk.Label(update_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_combo = ttk.Combobox(update_window, values=["Có sẵn", "Đã mượn", "Đang sửa chữa"], state="readonly")
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
                if the_loai == "Khác...":
                    the_loai = other_genre_entry.get().strip()
                if not the_loai:
                    messagebox.showerror("Lỗi", "Vui lòng chọn thể loại")
                    return

                try:
                    so_luong = int(so_luong_entry.get())
                    if so_luong < 0:
                        raise ValueError("Số lượng phải là số không âm")
                    
                    # Kiểm tra số lượng sách đang mượn
                    so_sach_dang_muon = data_handler.count_borrowed_books(book.ma_sach)
                    if so_luong < so_sach_dang_muon:
                        raise ValueError(f"Số lượng sách không được nhỏ hơn số sách đang được mượn ({so_sach_dang_muon} quyển)")

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
        ttk.Button(update_window, text="Cập nhật", style="Pastel.TButton", command=update_book).pack(pady=20)

    def delete_book_window(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần xóa!")
            return

        # Lấy thông tin sách được chọn
        book_id = str(self.tree.item(selected_item[0])['values'][0])
        book = data_handler.books_db.get(book_id)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách!")
            return

        # Kiểm tra xem sách có đang được mượn không
        if data_handler.is_book_borrowed(book_id):
            messagebox.showerror("Lỗi", "Không thể xóa sách đang được mượn!")
            return

        # Hiển thị hộp thoại xác nhận
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách có Mã sách: {book_id}?"):
            try:
                # Thực hiện xóa sách bằng data_handler
                data_handler.delete_book(book_id)
                self.update_book_list()
                messagebox.showinfo("Thành công", "Đã xóa sách thành công!")
            except Exception as e:
                logger.error(f"Lỗi khi xóa sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể xóa sách: {e}")

    def show_search_book_window(self):
        # Tạo cửa sổ tìm kiếm
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("Tìm kiếm sách")
        search_window.geometry("800x600")
        search_window.transient(self.main_window.root)
        search_window.grab_set()

        # Frame chứa các điều khiển tìm kiếm
        search_controls_frame = ttk.Frame(search_window)
        search_controls_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(search_controls_frame, text="Tìm kiếm theo:").pack(side='left', padx=5)
        search_criteria = ["Mã sách", "Tên sách", "Tác giả", "Thể loại", "Tình trạng", "Nhà xuất bản"]
        self.search_criteria_combo = ttk.Combobox(search_controls_frame, values=search_criteria, state="readonly")
        self.search_criteria_combo.current(0)
        self.search_criteria_combo.pack(side='left', padx=5)

        ttk.Label(search_controls_frame, text="Từ khóa:").pack(side='left', padx=5)
        self.search_keyword_entry = ttk.Entry(search_controls_frame)
        self.search_keyword_entry.pack(side='left', padx=5, expand=True, fill='x')
        self.search_keyword_entry.bind('<Return>', lambda event=None: self.search(search_tree))
        #TreeView
         # Frame chứa Treeview để hiển thị kết quả tìm kiếm
        tree_frame = ttk.Frame(search_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)


            # Tạo Treeview
        columns = ('ma_sach', 'ten_sach', 'tac_gia', 'the_loai', 'so_luong', 'tinh_trang', 'nha_xuat_ban')
        search_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        search_tree.heading('ma_sach', text='Mã sách')
        search_tree.heading('ten_sach', text='Tên sách')
        search_tree.heading('tac_gia', text='Tác giả')
        search_tree.heading('the_loai', text='Thể loại')
        search_tree.heading('so_luong', text='Số lượng')
        search_tree.heading('tinh_trang', text='Tình trạng')
        search_tree.heading('nha_xuat_ban', text='Nhà xuất bản')

        # Đặt độ rộng cột
        search_tree.column('ma_sach', width=100)
        search_tree.column('ten_sach', width=200)
        search_tree.column('tac_gia', width=150)
        search_tree.column('the_loai', width=100)
        search_tree.column('so_luong', width=80)
        search_tree.column('tinh_trang', width=100)
        search_tree.column('nha_xuat_ban', width=150)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=search_tree.yview)
        search_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        search_tree.pack(side='left', fill='both', expand=True)
        ttk.Button(search_controls_frame, text="Tìm kiếm", command=lambda: self.search(search_tree)).pack(side='left', padx=5)

    def search(self, treeview):
        try:
            # Lấy tiêu chí tìm kiếm và từ khóa
            search_criteria = self.search_criteria_combo.get()
            search_keyword = self.search_keyword_entry.get().strip()

            if not search_keyword:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
                return

            # Chuyển đổi tiêu chí tìm kiếm sang tên thuộc tính
            field_map = {
                "Mã sách": "ma_sach",
                "Tên sách": "ten_sach",
                "Tác giả": "tac_gia",
                "Thể loại": "the_loai",
                "Tình trạng": "tinh_trang",
                "Nhà xuất bản": "nha_xuat_ban"
            }

            field = field_map.get(search_criteria)
            if not field:
                messagebox.showerror("Lỗi", "Tiêu chí tìm kiếm không hợp lệ!")
                return

            # Lọc danh sách sách theo từ khóa
            filtered_books = [
                book for book in data_handler.books_db.values()
                if search_keyword.lower() in str(getattr(book, field)).lower()
            ]

            # Xóa dữ liệu cũ trong Treeview
            for item in treeview.get_children():
                treeview.delete(item)

            # Thêm dữ liệu mới vào Treeview
            for idx, book in enumerate(filtered_books):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                values = (
                    book.ma_sach,
                    book.ten_sach,
                    book.tac_gia,
                    book.the_loai,
                    book.so_luong,
                    book.tinh_trang,
                    book.nha_xuat_ban
                )
                treeview.insert('', 'end', values=values, tags=(tag,))

            treeview.tag_configure('evenrow', background='#ffffff')
            treeview.tag_configure('oddrow', background='#E3F6FF')

            # Hiển thị thông báo kết quả tìm kiếm
            if filtered_books:
                messagebox.showinfo("Kết quả tìm kiếm", f"Tìm thấy {len(filtered_books)} quyển sách.")
            else:
                messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy quyển sách nào.")

        except Exception as e:
            logger.error(f"Lỗi khi tìm kiếm sách: {e}")
            messagebox.showerror("Lỗi", f"Không thể thực hiện tìm kiếm: {e}")
    def update_book_list(self, books=None):
        logger.info(f"update_book_list called with {len(books) if books is not None else 'default'} books.")
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Temporarily hide headings to force redraw
        # self.tree.config(show='') # Commenting out this line as it might cause issues

        # Lấy danh sách sách cần hiển thị
        if books is None:
            books = sorted(data_handler.books_db.values(), key=lambda x: x.ma_sach)

        # Thêm dữ liệu mới vào Treeview
        try:
            for idx, book in enumerate(books):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                values = (
                    book.ma_sach,
                    book.ten_sach,
                    book.tac_gia,
                    book.the_loai,
                    book.so_luong,
                    book.tinh_trang,
                    book.nha_xuat_ban
                )
                logger.info(f"update_book_list: Inserting values for book {book.ma_sach}: {values}")
                self.tree.insert('', 'end', values=values, tags=(tag,))

            self.tree.tag_configure('evenrow', background='#ffffff')
            self.tree.tag_configure('oddrow', background='#E3F6FF')

            # Show headings again
            # self.tree.config(show='headings') # Commenting out this line

            self.tree.update_idletasks() # Explicitly update the Treeview display

        except Exception as e:
            logger.error(f"Lỗi khi cập nhật Treeview sách: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật hiển thị sách: {e}")