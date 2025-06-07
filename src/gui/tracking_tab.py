import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.core.models import TrackBook
from src.core.data_handler import data_handler
from src.utils.logger import logger

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

        # Standard ttk buttons without custom styles
        ttk.Button(center_frame, text="Mượn sách", command=self.show_borrow_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_frame, text="Trả sách", command=self.show_return_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_frame, text="Xem lịch sử", command=self.show_history_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_frame, text="Sách quá hạn", command=self.show_overdue_books_window).pack(side=tk.LEFT, padx=5)


        # Tạo Treeview
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'ngay_tra', 'trang_thai')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')

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
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        # Cập nhật danh sách mượn/trả
        self.update_tracking_list()

    def show_borrow_window(self):
        # Tạo cửa sổ mượn sách
        borrow_window = tk.Toplevel(self.main_window.root)
        borrow_window.title("Mượn sách")
        borrow_window.geometry("600x700")
        borrow_window.transient(self.main_window.root)
        borrow_window.grab_set()

        # Frame chứa form nhập liệu
        input_frame = ttk.LabelFrame(borrow_window, text="Nhập thông tin mượn sách")
        input_frame.pack(padx=10, pady=5, fill="x")

        # Nhập mã bạn đọc
        ttk.Label(input_frame, text="Mã bạn đọc:").pack(pady=5)
        ma_ban_doc_entry = ttk.Entry(input_frame)
        ma_ban_doc_entry.pack(pady=5, fill="x", padx=10)

        # Frame hiển thị thông tin bạn đọc
        reader_info_frame = ttk.LabelFrame(borrow_window, text="Thông tin bạn đọc")
        reader_info_frame.pack(padx=10, pady=5, fill="x")
        reader_info_label = ttk.Label(reader_info_frame, text="", justify=tk.LEFT)
        reader_info_label.pack(pady=5, padx=5)

        # Nhập mã sách
        ttk.Label(input_frame, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(input_frame)
        ma_sach_entry.pack(pady=5, fill="x", padx=10)

        # Frame hiển thị thông tin sách
        book_info_frame = ttk.LabelFrame(borrow_window, text="Thông tin sách")
        book_info_frame.pack(padx=10, pady=5, fill="x")
        book_info_label = ttk.Label(book_info_frame, text="", justify=tk.LEFT)
        book_info_label.pack(pady=5, padx=5)

        def check_info():
            try:
                ma_ban_doc = ma_ban_doc_entry.get().strip()
                ma_sach = ma_sach_entry.get().strip()

                if not ma_ban_doc or not ma_sach:
                    messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ mã bạn đọc và mã sách")
                    return

                # Kiểm tra và hiển thị thông tin bạn đọc
                reader = data_handler.readers_db.get(ma_ban_doc)
                if not reader:
                    reader_info_label.config(text="⚠️ Không tìm thấy bạn đọc với mã này")
                    return

                # Đếm số sách quá hạn của bạn đọc
                overdue_count = 0
                for track in data_handler.tracking_db.values():
                    if track.ma_ban_doc == ma_ban_doc and track.trang_thai == "Quá hạn":
                        overdue_count += 1

                if overdue_count >= 10:
                    reader_info_label.config(text="⚠️ Bạn đọc hiện có 10 sách quá hạn chưa trả!\nVui lòng trả sách quá hạn trước khi mượn thêm.")
                    borrow_button.pack_forget()
                    return

                # Hiển thị thông tin bạn đọc
                reader_info = f"Họ tên: {reader.ten}\n" \
                            f"Ngày sinh: {reader.ngay_sinh}\n" \
                            f"Giới tính: {reader.gioi_tinh}\n" \
                            f"Email: {reader.email}\n" \
                            f"Số điện thoại: {reader.so_dien_thoai}"
                if overdue_count > 0:
                    reader_info += f"\n⚠️ Bạn đọc hiện có {overdue_count} sách quá hạn"
                reader_info_label.config(text=reader_info)

                # Kiểm tra và hiển thị thông tin sách
                book = data_handler.books_db.get(ma_sach)
                if not book:
                    book_info_label.config(text="⚠️ Không tìm thấy sách với mã này")
                    borrow_button.pack_forget()
                    return
                if book.so_luong <= 0 or book.tinh_trang != "Có sẵn":
                    book_info_label.config(text="⚠️ Sách này hiện không khả dụng để mượn")
                    borrow_button.pack_forget()
                    return

                # Kiểm tra xem bạn đọc có đang mượn sách này không
                for record in data_handler.tracking_db.values():
                    if (record.ma_ban_doc == ma_ban_doc and 
                        record.ma_sach_muon == ma_sach and 
                        record.trang_thai in ("Đang mượn", "Quá hạn")):
                        book_info_label.config(text="⚠️ Bạn đọc đã mượn cuốn sách này và chưa trả!")
                        borrow_button.pack_forget()
                        return

                book_info = (f"Tên sách: {book.ten_sach}\n"
                           f"Tác giả: {book.tac_gia}\n"
                           f"Thể loại: {book.the_loai}\n"
                           f"Số lượng có sẵn: {book.so_luong}\n"
                           f"Nhà xuất bản: {book.nha_xuat_ban}")
                book_info_label.config(text=book_info)

                # Hiển thị nút mượn sách khi tìm thấy cả bạn đọc và sách hợp lệ
                borrow_button.pack(pady=20)

            except Exception as e:
                logger.error(f"Lỗi khi kiểm tra thông tin: {e}")
                messagebox.showerror("Lỗi", str(e))

        def borrow_book():
            try:
                ma_ban_doc = ma_ban_doc_entry.get().strip()
                ma_sach = ma_sach_entry.get().strip()

                reader = data_handler.readers_db.get(ma_ban_doc)
                book = data_handler.books_db.get(ma_sach)

                if not reader or not book:
                    messagebox.showerror("Lỗi", "Vui lòng kiểm tra lại mã bạn đọc và mã sách")
                    return

                # Kiểm tra số lượng sách và tình trạng
                if book.so_luong <= 0 or book.tinh_trang != "Có sẵn":
                    messagebox.showerror("Lỗi", "Sách này hiện không khả dụng để mượn")
                    return

                # Hiển thị xác nhận với đầy đủ thông tin
                confirmation_message = (
                    f"Xác nhận cho mượn sách:\n\n"
                    f"Thông tin bạn đọc:\n"
                    f"- Mã bạn đọc: {ma_ban_doc}\n"
                    f"- Họ tên: {reader.ten}\n\n"
                    f"Thông tin sách:\n"
                    f"- Mã sách: {ma_sach}\n"
                    f"- Tên sách: {book.ten_sach}\n"
                    f"- Tác giả: {book.tac_gia}\n"
                    f"- Thể loại: {book.the_loai}"
                )

                if not messagebox.askyesno("Xác nhận mượn sách", confirmation_message):
                    return

                # Tạo bản ghi mượn sách mới
                ngay_muon = datetime.now().strftime("%d/%m/%Y")
                new_track = TrackBook(ma_ban_doc, ma_sach, book.ten_sach, ngay_muon)
                
                # Cập nhật số lượng sách
                book.so_luong -= 1
                if book.so_luong == 0:
                    book.tinh_trang = "Đã mượn"

                # Lưu vào CSDL
                track_key = f"{ma_ban_doc}_{ma_sach}_{ngay_muon}"
                data_handler.tracking_db[track_key] = new_track
                data_handler.save_data()

                # Cập nhật giao diện
                self.update_tracking_list()
                messagebox.showinfo("Thành công", f"Đã cho mượn sách '{book.ten_sach}' thành công!")
                borrow_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi cho mượn sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể cho mượn sách: {e}")

        # Nút kiểm tra thông tin
        ttk.Button(input_frame, text="Kiểm tra thông tin", command=check_info).pack(pady=10)

        # Nút mượn sách (ẩn ban đầu)
        borrow_button = ttk.Button(borrow_window, text="Xác nhận mượn sách", command=borrow_book)
        # Nút mượn sách chỉ hiện khi đã kiểm tra thông tin hợp lệ
        borrow_button.pack_forget()

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

        ttk.Label(filter_frame, text="Tìm theo:", style="Bold.TLabel").pack(side='left', padx=5)
        filter_criteria = ["Tất cả", "Mã bạn đọc", "Mã sách", "Tên sách"]
        filter_criteria_combo = ttk.Combobox(filter_frame, values=filter_criteria, state="readonly")
        filter_criteria_combo.current(0)
        filter_criteria_combo.pack(side='left', padx=5, expand=True, fill='x')

        filter_keyword_entry = ttk.Entry(filter_frame)
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
            
            tracks_to_display = filtered_tracks if filtered_tracks is not None else [
                track for track in data_handler.tracking_db.values() 
                if track.trang_thai in ("Đang mượn", "Quá hạn")
            ]

            # Thêm các sách đang mượn và quá hạn
            idx = 0
            for track in tracks_to_display:
                tag = 'overdue' if track.trang_thai == "Quá hạn" else ('evenrow' if idx % 2 == 0 else 'oddrow')
                tree.insert('', 'end', values=(
                    track.ma_ban_doc,
                    track.ma_sach_muon,
                    track.ten_sach_muon,
                    track.ngay_muon,
                    track.trang_thai
                ), tags=(tag,))
                idx += 1
            
            # Configure tags            tree.tag_configure('evenrow', background='#ffffff')
            tree.tag_configure('oddrow', background='#E3F6FF')
            tree.tag_configure('overdue', background='#FFE3E3')  # Light red background for overdue items

        def filter_borrowed_books():
            field = filter_criteria_combo.get()
            keyword = filter_keyword_entry.get().strip().lower()
            filtered_tracks = []
            
            # First update all book statuses
            current_date = datetime.now()
            max_borrow_days = 30

            for track in data_handler.tracking_db.values():
                if track.trang_thai == "Đang mượn":
                    try:
                        borrow_date = datetime.strptime(track.ngay_muon, "%d/%m/%Y")
                        days_borrowed = (current_date - borrow_date).days
                        
                        if days_borrowed > max_borrow_days:
                            track.trang_thai = "Quá hạn"
                            data_handler.save_data()
                    except ValueError as e:
                        logger.error(f"Lỗi xử lý ngày mượn: {e}")

            # Then apply filters
            for track in data_handler.tracking_db.values():
                if track.trang_thai in ("Đang mượn", "Quá hạn"):
                    if field == "Tất cả":
                        if not keyword or (
                            keyword in track.ma_ban_doc.lower() or
                            keyword in track.ma_sach_muon.lower() or
                            keyword in track.ten_sach_muon.lower()
                        ):
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
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần trả", style="Bold.TLabel")
                return

            try:
                track_key = tree.item(selected_item[0])['values'][0] # Using track_key as identifier
                track = data_handler.tracking_db.get(track_key)
                if track:
                    # Cập nhật trạng thái
                    track.trang_thai = "Đã trả"
                    track.ngay_tra = datetime.now().strftime("%d/%m/%Y")

                    # Cập nhật số lượng sách
                    book = data_handler.books_db.get(track.ma_sach_muon)
                    if book:
                        book.so_luong += 1

                data_handler.save_data()
                self.main_window.update_tracking_list()
                update_return_treeview() # Update return window list
                messagebox.showinfo("Thành công", "Trả sách thành công!")
            except Exception as e:
                logger.error(f"Lỗi khi trả sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể trả sách: {e}", style="Bold.TLabel")

        # Nút trả sách
        ttk.Button(return_window, text="Trả sách được chọn", command=return_books).pack(pady=10)

        # Cập nhật danh sách sách đang mượn khi mở cửa sổ
        update_return_treeview()

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
        ttk.Label(search_frame, text="Tìm theo:", style="Bold.TLabel").pack(side='left', padx=5)
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

                # Determine tag based on status
                if track.trang_thai == "Quá hạn":
                    tag = 'overdue'
                else:
                    # Keep alternating colors for non-overdue items
                    count = len(self.history_tree.get_children())
                    tag = 'evenrow' if count % 2 == 0 else 'oddrow'

                self.history_tree.insert('', tk.END,
                    values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        track.ngay_tra,
                        track.trang_thai,
                        days_borrowed # Add days borrowed column
                    ),
                    tags=(tag,)
                )
            except Exception as e:
                logger.error(f"Error inserting history record into treeview: {track} - {e}")
                # Optionally insert with error indicator or skip
                self.history_tree.insert('', tk.END,
                    values=(track.ma_ban_doc, track.ma_sach_muon, "Error loading data", "", "", "", ""))

        # Configure the tags
        self.history_tree.tag_configure('evenrow', background='#ffffff')
        self.history_tree.tag_configure('oddrow', background='#E3F6FF')
        self.history_tree.tag_configure('overdue', background='#FFE3E3')  # Light red background

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
        # Xóa dữ liệu cũ trong Treeview
        for item in self.overdue_tree.get_children():
            self.overdue_tree.delete(item)

        try:
            current_date = datetime.now()
            max_borrow_days = 30  # Số ngày mượn tối đa
            overdue_records = []

            # Lọc và hiển thị sách quá hạn
            for track in data_handler.tracking_db.values():
                if track.trang_thai != "Đã trả":  # Chỉ xét sách chưa trả
                    try:
                        # Chuyển ngày mượn sang datetime object
                        borrow_date = datetime.strptime(track.ngay_muon, "%d/%m/%Y")
                        days_borrowed = (current_date - borrow_date).days

                        # Nếu số ngày mượn vượt quá giới hạn
                        if days_borrowed > max_borrow_days:
                            # Cập nhật trạng thái quá hạn
                            track.trang_thai = "Quá hạn"
                            data_handler.save_data()
                            overdue_records.append(track)

                    except ValueError as e:
                        logger.error(f"Lỗi xử lý định dạng ngày tháng: {e}")
                        continue

            # Thêm các sách quá hạn vào treeview
            for track in overdue_records:
                try:
                    borrow_date = datetime.strptime(track.ngay_muon, "%d/%m/%Y")
                    days_overdue = (current_date - borrow_date).days - max_borrow_days

                    self.overdue_tree.insert('', tk.END,
                        values=(
                            track.ma_ban_doc,
                            track.ma_sach_muon,
                            track.ten_sach_muon,
                            track.ngay_muon,
                            days_overdue  # Số ngày quá hạn
                        ),
                        tags=('overdue',)
                    )
                except Exception as e:
                    logger.error(f"Error inserting overdue record into treeview: {track} - {e}")
                    self.overdue_tree.insert('', tk.END,
                        values=(track.ma_ban_doc, track.ma_sach_muon, "Error loading data", "", ""))

            # Configure tags
            self.overdue_tree.tag_configure('overdue', background='#FFE3E3')  # Light red background

            # Hiển thị thông báo số lượng sách quá hạn
            if overdue_records:
                messagebox.showinfo("Thông báo", f"Có {len(overdue_records)} sách đang quá hạn!")

            # Scroll to the top after update
            if self.overdue_tree.get_children():
                self.overdue_tree.yview_moveto(0)

        except Exception as e:
            logger.error(f"Lỗi khi cập nhật danh sách sách quá hạn: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật danh sách sách quá hạn: {e}")