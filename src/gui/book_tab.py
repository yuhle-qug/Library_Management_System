import tkinter as tk
from tkinter import ttk, messagebox
from src.core.models import Book
from src.core.data_handler import data_handler
from src.utils.logger import logger

FONT = ("Arial Unicode MS", 11)

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

        ttk.Button(center_frame, text="Thêm sách mới", style="Pastel.TButton", command=self.show_add_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Cập nhật sách", style="Pastel.TButton", command=self.show_update_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Tìm kiếm sách", style="Pastel.TButton", command=self.show_search_book_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Xóa sách", style="Pastel.TButton", command=self.delete_book_window).pack(side='left', padx=10)

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
        tinh_trang_combo = ttk.Combobox(add_window, values=["Mới", "Đã sử dụng"])
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
        the_loai_list = [
            "Khoa học", "Lịch sử", "Tiểu thuyết", "Truyện ngắn", "Tâm lý", "Kinh tế", "Chính trị",
            "Tôn giáo", "Triết học", "Thiếu nhi", "Giáo trình", "Công nghệ", "Kỹ thuật", "Y học", "Khác..."
        ]
        the_loai_combo = ttk.Combobox(update_window, values=the_loai_list)
        the_loai_combo.set(book.the_loai if book.the_loai in the_loai_list else "Khác...")
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
        so_luong_entry.insert(0, str(book.so_luong))
        so_luong_entry.pack(pady=5)

        ttk.Label(update_window, text="Tình trạng:").pack(pady=5)
        tinh_trang_combo = ttk.Combobox(update_window, values=["Mới", "Đã sử dụng"])
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
        ttk.Button(update_window, text="Cập nhật",style="Pastel.TButton", command=update_book).pack(pady=20)

    def delete_book_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần xóa")
            return
        book_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách '{book_id}' không?"):
            if data_handler.is_book_borrowed(book_id):
                messagebox.showerror("Lỗi", "Không thể xóa sách đang được mượn hoặc quá hạn!")
                return
            data_handler.delete_book(book_id)
            self.update_book_list()
            messagebox.showinfo("Thành công", "Đã xóa sách thành công!")

    def show_search_book_window(self):
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("Tìm kiếm sách")
        search_window.geometry("900x600")
        search_window.transient(self.main_window.root)
        search_window.grab_set()
        ttk.Label(search_window, text="Tìm kiếm theo:").pack(pady=5)
        criteria = ["Tất cả", "Mã sách", "Tên sách", "Tác giả", "Thể loại", "Nhà xuất bản"]
        criteria_combo = ttk.Combobox(search_window, values=criteria, state="readonly")
        criteria_combo.current(0)
        criteria_combo.pack(pady=5)
        ttk.Label(search_window, text="Từ khóa:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        # Frame for search results Treeview
        results_frame = ttk.Frame(search_window)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Treeview for search results
        columns = ('ma_sach', 'ten_sach', 'tac_gia', 'the_loai', 'so_luong', 'tinh_trang', 'nha_xuat_ban')
        results_tree = ttk.Treeview(results_frame, columns=columns, show='headings')

        # Define columns for the results Treeview
        results_tree.heading('ma_sach', text='Mã sách')
        results_tree.heading('ten_sach', text='Tên sách')
        results_tree.heading('tac_gia', text='Tác giả')
        results_tree.heading('the_loai', text='Thể loại')
        results_tree.heading('so_luong', text='Số lượng')
        results_tree.heading('tinh_trang', text='Tình trạng')
        results_tree.heading('nha_xuat_ban', text='Nhà xuất bản')

        # Set column widths (optional, can adjust as needed)
        results_tree.column('ma_sach', width=80)
        results_tree.column('ten_sach', width=150)
        results_tree.column('tac_gia', width=120)
        results_tree.column('the_loai', width=80)
        results_tree.column('so_luong', width=60)
        results_tree.column('tinh_trang', width=80)
        results_tree.column('nha_xuat_ban', width=120)

        # Add scrollbar to results Treeview
        results_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=results_tree.yview)
        results_tree.configure(yscrollcommand=results_scrollbar.set)
        results_scrollbar.pack(side='right', fill='y')
        results_tree.pack(side='left', fill='both', expand=True)

        def search():
            field = criteria_combo.get()
            keyword = search_entry.get().strip().lower()
            found_books = []
            for book in data_handler.books_db.values():
                if field == "Tất cả":
                    if (keyword in book.ma_sach.lower() or
                        keyword in book.ten_sach.lower() or
                        keyword in book.tac_gia.lower() or
                        keyword in book.the_loai.lower() or
                        keyword in book.nha_xuat_ban.lower()):
                        found_books.append(book)
                elif field == "Mã sách" and keyword in book.ma_sach.lower():
                    found_books.append(book)
                elif field == "Tên sách" and keyword in book.ten_sach.lower():
                    found_books.append(book)
                elif field == "Tác giả" and keyword in book.tac_gia.lower():
                    found_books.append(book)
                elif field == "Thể loại" and keyword in book.the_loai.lower():
                    found_books.append(book)
                elif field == "Nhà xuất bản" and keyword in book.nha_xuat_ban.lower():
                    found_books.append(book)
            if found_books:
                logger.info(f"search: Found {len(found_books)} books.")
                # Clear previous results in the search window Treeview
                for item in results_tree.get_children():
                    results_tree.delete(item)
                # Insert new results
                for idx, book in enumerate(found_books):
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow' # Reuse row tags
                    values = (
                        book.ma_sach,
                        book.ten_sach,
                        book.tac_gia,
                        book.the_loai,
                        book.so_luong,
                        book.tinh_trang,
                        book.nha_xuat_ban
                    )
                    results_tree.insert('', 'end', values=values, tags=(tag,))
                results_tree.tag_configure('evenrow', background='#ffffff') # Reuse row tags config
                results_tree.tag_configure('oddrow', background='#E3F6FF') # Reuse row tags config

                results_tree.update_idletasks() # Update the search results Treeview

                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_books)} sách")
            else:
                logger.info("search: No books found.")
                # Xóa toàn bộ các hàng trong Treeview khi không tìm thấy kết quả
                for item in results_tree.get_children():
                    results_tree.delete(item)
                results_tree.update_idletasks() # Update the search results Treeview
                messagebox.showinfo("Kết quả", "Không tìm thấy sách nào")

        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)

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
            # Optionally show an error message to the user
            # messagebox.showerror("Lỗi", f"Không thể cập nhật hiển thị sách: {e}")