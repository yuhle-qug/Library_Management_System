import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.core.models import TrackBook
from src.core.data_handler import data_handler
from src.utils.logger import logger

FONT = ("Arial Unicode MS", 11)

class TrackingTab:
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

        ttk.Button(center_frame, text="Mượn sách", style="Pastel.TButton", command=self.show_borrow_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Trả sách", style="Pastel.TButton", command=self.show_return_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Xem lịch sử", style="Pastel.TButton", command=self.show_history_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Sách quá hạn", style="Pastel.TButton", command=self.show_overdue_books_window).pack(side='left', padx=10)
        # Frame chứa Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'ngay_tra', 'trang_thai')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        self.tree.heading('ma_ban_doc', text='Mã bạn đọc')
        self.tree.heading('ma_sach_muon', text='Mã sách')
        self.tree.heading('ten_sach_muon', text='Tên sách')
        self.tree.heading('ngay_muon', text='Ngày mượn')
        self.tree.heading('ngay_tra', text='Ngày trả')
        self.tree.heading('trang_thai', text='Trạng thái')

        # Đặt độ rộng cột
        self.tree.column('ma_ban_doc', width=100)
        self.tree.column('ma_sach_muon', width=100)
        self.tree.column('ten_sach_muon', width=200)
        self.tree.column('ngay_muon', width=100)
        self.tree.column('ngay_tra', width=100)
        self.tree.column('trang_thai', width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        # Cập nhật danh sách mượn/trả
        self.update_tracking_list()

    def show_borrow_window(self):
        # Tạo cửa sổ mượn sách
        borrow_window = tk.Toplevel(self.main_window.root)
        borrow_window.title("Mượn sách")
        borrow_window.geometry("600x600") # Adjusted geometry to fit new search frames
        borrow_window.transient(self.main_window.root)
        borrow_window.grab_set()

        # Khung tìm kiếm bạn đọc
        reader_search_frame = ttk.LabelFrame(borrow_window, text="Tìm kiếm bạn đọc")
        reader_search_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(reader_search_frame, text="Tìm theo:", font=FONT).pack(side='left', padx=5)
        reader_criteria = ["Mã bạn đọc", "Họ tên"]
        reader_criteria_combo = ttk.Combobox(reader_search_frame, values=reader_criteria, state="readonly", font=FONT)
        reader_criteria_combo.current(0)
        reader_criteria_combo.pack(side='left', padx=5, expand=True, fill='x')

        reader_keyword_entry = ttk.Entry(reader_search_frame, font=FONT)
        reader_keyword_entry.pack(side='left', padx=5, expand=True, fill='x')

        def search_readers():
            field = reader_criteria_combo.get()
            keyword = reader_keyword_entry.get().strip().lower()
            filtered_readers = []
            for reader in data_handler.readers_db.values():
                if (field == "Mã bạn đọc" and keyword in reader.ma_ban_doc.lower()) or \
                   (field == "Họ tên" and keyword in reader.ten.lower()):
                    filtered_readers.append(reader.ma_ban_doc)
            # Update the main reader combobox
            ma_ban_doc_combo['values'] = filtered_readers
            if filtered_readers:
                ma_ban_doc_combo.current(0)
            else:
                ma_ban_doc_combo.set("") # Clear combobox if no results

        ttk.Button(reader_search_frame, text="Tìm", command=search_readers).pack(side='left', padx=5)

        # ComboBox chọn bạn đọc sau khi tìm kiếm
        ttk.Label(borrow_window, text="Chọn bạn đọc:", font=FONT).pack(pady=5)
        ma_ban_doc_combo = ttk.Combobox(borrow_window, font=FONT, state="readonly") # Make read-only after search
        ma_ban_doc_combo['values'] = [reader.ma_ban_doc for reader in data_handler.readers_db.values()]
        ma_ban_doc_combo.pack(pady=5, fill="x", padx=10)

        # Khung tìm kiếm sách
        book_search_frame = ttk.LabelFrame(borrow_window, text="Tìm kiếm sách có sẵn")
        book_search_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(book_search_frame, text="Tìm theo:", font=FONT).pack(side='left', padx=5)
        book_criteria = ["Mã sách", "Tên sách"]
        book_criteria_combo = ttk.Combobox(book_search_frame, values=book_criteria, state="readonly", font=FONT)
        book_criteria_combo.current(0)
        book_criteria_combo.pack(side='left', padx=5, expand=True, fill='x')

        book_keyword_entry = ttk.Entry(book_search_frame, font=FONT)
        book_keyword_entry.pack(side='left', padx=5, expand=True, fill='x')

        def search_books():
            field = book_criteria_combo.get()
            keyword = book_keyword_entry.get().strip().lower()
            filtered_books = []
            for book in data_handler.books_db.values():
                if book.so_luong > 0: # Only show available books
                    if (field == "Mã sách" and keyword in book.ma_sach.lower()) or \
                       (field == "Tên sách" and keyword in book.ten_sach.lower()):
                        filtered_books.append(book.ma_sach)
            # Update the main book combobox
            ma_sach_combo['values'] = filtered_books
            if filtered_books:
                ma_sach_combo.current(0)
            else:
                ma_sach_combo.set("") # Clear combobox if no results

        ttk.Button(book_search_frame, text="Tìm", command=search_books).pack(side='left', padx=5)

        # ComboBox chọn sách sau khi tìm kiếm
        ttk.Label(borrow_window, text="Chọn sách:", font=FONT).pack(pady=5)
        ma_sach_combo = ttk.Combobox(borrow_window, font=FONT, state="readonly") # Make read-only after search
        ma_sach_combo['values'] = [book.ma_sach for book in data_handler.books_db.values() if book.so_luong > 0]
        ma_sach_combo.pack(pady=5, fill="x", padx=10)

        def borrow_book():
            try:
                ma_ban_doc = ma_ban_doc_combo.get()
                if not ma_ban_doc:
                    messagebox.showerror("Lỗi", "Vui lòng chọn mã bạn đọc")
                    return

                ma_sach = ma_sach_combo.get()
                if not ma_sach:
                    messagebox.showerror("Lỗi", "Vui lòng chọn mã sách")
                    return

                # Kiểm tra sách có sẵn không (kiểm tra lại vì danh sách combobox chỉ hiển thị sách có sẵn)
                book = data_handler.books_db.get(ma_sach)
                if not book or book.so_luong <= 0:
                    messagebox.showerror("Lỗi", "Sách không có sẵn để mượn")
                    return

                # Kiểm tra bạn đọc đã mượn sách này chưa
                for track in data_handler.tracking_db.values():
                    # Sử dụng cả mã sách và mã bạn đọc để kiểm tra trùng lặp chính xác hơn
                    if (track.ma_ban_doc == ma_ban_doc and 
                        track.ma_sach_muon == ma_sach and 
                        track.trang_thai in ("Đang mượn", "Quá hạn")):
                        messagebox.showerror("Lỗi", "Bạn đọc đang mượn cuốn sách này hoặc có bản ghi mượn chưa hoàn thành.")
                        return

                # Tạo bản ghi mượn sách mới
                ngay_muon = datetime.now().strftime("%d/%m/%Y")
                new_track = TrackBook(
                    ma_ban_doc=ma_ban_doc,
                    ma_sach_muon=ma_sach,
                    ten_sach_muon=book.ten_sach,
                    ngay_muon=ngay_muon
                )
                # Tạo key duy nhất bao gồm cả ngày mượn để tránh trùng lặp khi cùng 1 bạn đọc mượn cùng 1 sách nhiều lần
                track_key = f"{ma_ban_doc}_{ma_sach}_{ngay_muon}"

                if not ma_ban_doc:
                    messagebox.showerror("Lỗi", "Không tìm thấy bạn đọc với mã này.")
                    return

                if not book:
                    messagebox.showerror("Lỗi", "Không tìm thấy sách với mã này.")
                    return

                if book.so_luong <= 0:
                    messagebox.showwarning("Cảnh báo", f"Sách '{book.ten_sach}' hiện không có sẵn.")
                    return

                # Confirmation dialog before borrowing
                confirm_message = (
                    f"BẠN CÓ CHẮC CHẮN MUỐN THỰC HIỆN GIAO DỊCH NÀY?\n\n"
                    f"- Bạn đọc: {ma_ban_doc} - {ma_ban_doc}\n"
                    f"- Sách mượn: {ma_sach} - {book.ten_sach}"
                )
                if messagebox.askyesno("Xác nhận mượn sách", confirm_message):
                    # Proceed with borrowing
                    data_handler.tracking_db[track_key] = new_track
                    book.so_luong -= 1
                    data_handler.save_data()
                    self.main_window.update_tracking_list() # Update main tracking list
                    messagebox.showinfo("Thành công", "Mượn sách thành công!")
                    borrow_window.destroy()
                else:
                    # Cancel borrowing
                    messagebox.showinfo("Thông báo", "Giao dịch mượn sách đã bị hủy.")

            except Exception as e:
                logger.error(f"Lỗi khi mượn sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể thực hiện mượn sách: {e}")

        # Nút mượn sách
        ttk.Button(borrow_window, text="Mượn sách", style="Pastel.TButton", command=borrow_book).pack(pady=20)

    def show_return_window(self):
        # Tạo cửa sổ trả sách
        return_window = tk.Toplevel(self.main_window.root)
        return_window.title("Trả sách")
        return_window.geometry("800x600")
        return_window.transient(self.main_window.root)
        return_window.grab_set()

        # Khung tìm kiếm/lọc sách đang mượn
        filter_frame = ttk.LabelFrame(return_window, text="Tìm kiếm/Lọc sách đang mượn")
        filter_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(filter_frame, text="Tìm theo:", font=FONT).pack(side='left', padx=5)
        filter_criteria = ["Tất cả", "Mã bạn đọc", "Mã sách", "Tên sách"]
        filter_criteria_combo = ttk.Combobox(filter_frame, values=filter_criteria, state="readonly", font=FONT)
        filter_criteria_combo.current(0)
        filter_criteria_combo.pack(side='left', padx=5, expand=True, fill='x')

        filter_keyword_entry = ttk.Entry(filter_frame, font=FONT)
        filter_keyword_entry.pack(side='left', padx=5, expand=True, fill='x')

        # Frame chứa Treeview
        tree_frame = ttk.Frame(return_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'trang_thai')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        tree.heading('ma_ban_doc', text='Mã bạn đọc')
        tree.heading('ma_sach_muon', text='Mã sách')
        tree.heading('ten_sach_muon', text='Tên sách')
        tree.heading('ngay_muon', text='Ngày mượn')
        tree.heading('trang_thai', text='Trạng thái')

        # Đặt độ rộng cột
        tree.column('ma_ban_doc', width=100)
        tree.column('ma_sach_muon', width=100)
        tree.column('ten_sach_muon', width=200)
        tree.column('ngay_muon', width=100)
        tree.column('trang_thai', width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

        def update_return_treeview(filtered_tracks=None):
            # Xóa dữ liệu cũ
            for item in tree.get_children():
                tree.delete(item)
            
            tracks_to_display = filtered_tracks if filtered_tracks is not None else [track for track in data_handler.tracking_db.values() if track.trang_thai == "Đang mượn"]

            # Thêm các sách đang mượn
            idx = 0
            for track in tracks_to_display:
                if track.trang_thai == "Đang mượn":
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                    tree.insert('', 'end', values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        track.trang_thai
                    ), tags=(tag,))
                    idx += 1
            tree.tag_configure('evenrow', background='#ffffff')
            tree.tag_configure('oddrow', background='#E3F6FF')

        def filter_borrowed_books():
            field = filter_criteria_combo.get()
            keyword = filter_keyword_entry.get().strip().lower()
            filtered_tracks = []
            for track in data_handler.tracking_db.values():
                 # Chỉ lọc các bản ghi đang mượn hoặc quá hạn
                if track.trang_thai in ("Đang mượn", "Quá hạn"):
                    if field == "Tất cả":
                         if (keyword in track.ma_ban_doc.lower() or
                             keyword in track.ma_sach_muon.lower() or
                             keyword in track.ten_sach_muon.lower()):
                              filtered_tracks.append(track)
                    elif field == "Mã bạn đọc" and keyword in track.ma_ban_doc.lower():
                         filtered_tracks.append(track)
                    elif field == "Mã sách" and keyword in track.ma_sach_muon.lower():
                         filtered_tracks.append(track)
                    elif field == "Tên sách" and keyword in track.ten_sach_muon.lower():
                         filtered_tracks.append(track)
            update_return_treeview(filtered_tracks)

        ttk.Button(filter_frame, text="Tìm", command=filter_borrowed_books).pack(side='left', padx=5)

        # Cập nhật danh sách ban đầu
        update_return_treeview()

        def return_books():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần trả")
                return

            try:
                for item in selected_items:
                    values = tree.item(item)['values']
                    ma_ban_doc = values[0]
                    ma_sach = values[1]
                    ngay_muon = values[3]

                    # Tìm bản ghi mượn sách
                    track_key = f"{ma_ban_doc}_{ma_sach}_{ngay_muon}"
                    track = data_handler.tracking_db.get(track_key)
                    if track:
                        # Cập nhật trạng thái
                        track.trang_thai = "Đã trả"
                        track.ngay_tra = datetime.now().strftime("%d/%m/%Y")

                        # Cập nhật số lượng sách
                        book = data_handler.books_db.get(ma_sach)
                        if book:
                            book.so_luong += 1

                data_handler.save_data()
                self.update_tracking_list()
                messagebox.showinfo("Thành công", "Đã trả sách thành công")
                return_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi trả sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể trả sách: {e}")

        # Nút trả sách
        ttk.Button(return_window, text="Trả sách đã chọn", command=return_books).pack(pady=20)

    def update_tracking_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu mới vào Treeview
        for idx, track in enumerate(data_handler.tracking_db.values()):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                track.ma_ban_doc,
                track.ma_sach_muon,
                track.ten_sach_muon,
                track.ngay_muon,
                track.ngay_tra or "",
                track.trang_thai
            ), tags=(tag,))
        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('oddrow', background='#E3F6FF')

    def show_history_window(self):
        # Tạo cửa sổ lịch sử
        history_window = tk.Toplevel(self.main_window.root)
        history_window.title("Lịch sử Mượn/Trả Sách")
        history_window.geometry("900x600")
        history_window.transient(self.main_window.root)
        history_window.grab_set()

        # Khung tìm kiếm
        search_frame = ttk.Frame(history_window)
        search_frame.pack(padx=10, pady=10, fill='x', anchor='center')

        # Tiêu chí tìm kiếm
        ttk.Label(search_frame, text="Tìm theo:").pack(side='left', padx=5)
        history_criteria = ["Mã bạn đọc", "Mã sách"]
        self.history_criteria_combo = ttk.Combobox(search_frame, values=history_criteria, state="readonly")
        self.history_criteria_combo.current(0) # Default to Reader ID
        self.history_criteria_combo.pack(side='left', padx=5)

        # Ô nhập từ khóa
        self.history_keyword_entry = ttk.Entry(search_frame)
        self.history_keyword_entry.pack(side='left', padx=5, expand=True, fill='x')
        self.history_keyword_entry.bind('<Return>', lambda event=None: self.perform_history_search())

        # Nút Tìm kiếm và Xem tất cả
        ttk.Button(search_frame, text="Tìm", command=self.perform_history_search).pack(side='left', padx=5)
        ttk.Button(search_frame, text="Xem tất cả", command=self.show_all_history).pack(side='left', padx=5)

        # Frame chứa Treeview
        tree_frame = ttk.Frame(history_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview cho lịch sử
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'ngay_tra', 'trang_thai', 'so_ngay_muon')
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        self.history_tree.heading('ma_ban_doc', text='Mã bạn đọc')
        self.history_tree.heading('ma_sach_muon', text='Mã sách')
        self.history_tree.heading('ten_sach_muon', text='Tên sách')
        self.history_tree.heading('ngay_muon', text='Ngày mượn')
        self.history_tree.heading('ngay_tra', text='Ngày trả')
        self.history_tree.heading('trang_thai', text='Trạng thái')
        self.history_tree.heading('so_ngay_muon', text='Số ngày mượn')

        # Đặt độ rộng cột
        self.history_tree.column('ma_ban_doc', width=100, anchor='center')
        self.history_tree.column('ma_sach_muon', width=100, anchor='center')
        self.history_tree.column('ten_sach_muon', width=200)
        self.history_tree.column('ngay_muon', width=100, anchor='center')
        self.history_tree.column('ngay_tra', width=100, anchor='center')
        self.history_tree.column('trang_thai', width=100, anchor='center')
        self.history_tree.column('so_ngay_muon', width=100, anchor='center')

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.history_tree.pack(side='left', fill='both', expand=True)

        # Hiển thị tất cả lịch sử khi mở cửa sổ
        self.show_all_history()

    def show_overdue_books_window(self):
        # Tạo cửa sổ sách quá hạn
        overdue_window = tk.Toplevel(self.main_window.root)
        overdue_window.title("Sách quá hạn")
        overdue_window.geometry("800x500")
        overdue_window.transient(self.main_window.root)
        overdue_window.grab_set()

        # Frame chứa Treeview
        tree_frame = ttk.Frame(overdue_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview cho sách quá hạn
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'so_ngay_muon')
        self.overdue_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        self.overdue_tree.heading('ma_ban_doc', text='Mã bạn đọc')
        self.overdue_tree.heading('ma_sach_muon', text='Mã sách')
        self.overdue_tree.heading('ten_sach_muon', text='Tên sách')
        self.overdue_tree.heading('ngay_muon', text='Ngày mượn')
        self.overdue_tree.heading('so_ngay_muon', text='Số ngày mượn quá hạn')

        # Đặt độ rộng cột
        self.overdue_tree.column('ma_ban_doc', width=100, anchor='center')
        self.overdue_tree.column('ma_sach_muon', width=100, anchor='center')
        self.overdue_tree.column('ten_sach_muon', width=250)
        self.overdue_tree.column('ngay_muon', width=100, anchor='center')
        self.overdue_tree.column('so_ngay_muon', width=150, anchor='center')

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.overdue_tree.yview)
        self.overdue_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.overdue_tree.pack(side='left', fill='both', expand=True)

        # Hiển thị danh sách sách quá hạn khi mở cửa sổ
        self.update_overdue_list()

    def show_all_history(self):
        # Clear the search entry
        self.history_keyword_entry.delete(0, tk.END)
        # Display all tracking records in the history treeview
        all_records = list(data_handler.tracking_db.values())
        self.update_history_list(all_records)

    def update_history_list(self, tracking_records):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Thêm dữ liệu mới
        for track in tracking_records:
            try:
                # Calculate days borrowed
                borrow_date = datetime.strptime(track.ngay_muon, "%d/%m/%Y")
                if track.ngay_tra and track.ngay_tra != "N/A":
                    return_date = datetime.strptime(track.ngay_tra, "%d/%m/%Y")
                    days_borrowed = (return_date - borrow_date).days
                else:
                    # For borrowed/overdue books, calculate days until now
                    current_date = datetime.now()
                    days_borrowed = (current_date - borrow_date).days

                self.history_tree.insert('', tk.END,
                    values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        track.ngay_tra,
                        track.trang_thai,
                        days_borrowed # Add days borrowed column
                    )
                )
            except Exception as e:
                logger.error(f"Error inserting history record into treeview: {track} - {e}")
                # Optionally insert with error indicator or skip
                self.history_tree.insert('', tk.END,
                    values=(track.ma_ban_doc, track.ma_sach_muon, "Error loading data", "", "", "", ""))

        # Apply alternating row colors
        for i, item in enumerate(self.history_tree.get_children()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.history_tree.item(item, tags=(tag,))

        # Scroll to the top after update
        if self.history_tree.get_children():
            self.history_tree.yview_moveto(0)

    def perform_history_search(self):
        criteria = self.history_criteria_combo.get()
        keyword = self.history_keyword_entry.get().strip().lower()

        filtered_records = []
        for track in data_handler.tracking_db.values():
            if criteria == "Mã bạn đọc":
                if keyword in track.ma_ban_doc.lower():
                    filtered_records.append(track)
            elif criteria == "Mã sách":
                if keyword in track.ma_sach_muon.lower():
                    filtered_records.append(track)

        self.update_history_list(filtered_records)

    def update_overdue_list(self):
        # Implementation of update_overdue_list method
        pass