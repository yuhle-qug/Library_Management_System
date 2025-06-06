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

        ttk.Button(center_frame, text="Mượn sách", command=self.show_borrow_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Trả sách", command=self.show_return_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Xem lịch sử", command=self.show_history_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Sách quá hạn", command=self.show_overdue_books_window).pack(side='left', padx=10)

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
        borrow_window.geometry("600x500")
        borrow_window.transient(self.main_window.root)
        borrow_window.grab_set()

        # Tạo các trường nhập liệu
        ttk.Label(borrow_window, text="Mã bạn đọc:").pack(pady=5)
        ma_ban_doc_combo = ttk.Combobox(borrow_window)
        ma_ban_doc_combo['values'] = [reader.ma_ban_doc for reader in data_handler.readers_db.values()]
        ma_ban_doc_combo.pack(pady=5)

        ttk.Label(borrow_window, text="Mã sách:").pack(pady=5)
        ma_sach_combo = ttk.Combobox(borrow_window)
        ma_sach_combo['values'] = [book.ma_sach for book in data_handler.books_db.values() if book.so_luong > 0]
        ma_sach_combo.pack(pady=5)

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

                # Kiểm tra sách có sẵn không
                book = data_handler.books_db.get(ma_sach)
                if not book or book.so_luong <= 0:
                    messagebox.showerror("Lỗi", "Sách không có sẵn để mượn")
                    return

                # Kiểm tra bạn đọc đã mượn sách này chưa
                for track in data_handler.tracking_db.values():
                    if (track.ma_ban_doc == ma_ban_doc and 
                        track.ma_sach_muon == ma_sach and 
                        track.trang_thai == "Borrowed"):
                        messagebox.showerror("Lỗi", "Bạn đọc đã mượn sách này")
                        return

                # Tạo bản ghi mượn sách mới
                ngay_muon = datetime.now().strftime("%Y-%m-%d")
                new_track = TrackBook(
                    ma_ban_doc=ma_ban_doc,
                    ma_sach_muon=ma_sach,
                    ten_sach_muon=book.ten_sach,
                    ngay_muon=ngay_muon
                )
                data_handler.tracking_db[f"{ma_ban_doc}_{ma_sach}_{ngay_muon}"] = new_track

                # Cập nhật số lượng sách
                book.so_luong -= 1
                data_handler.save_data()

                self.update_tracking_list()
                messagebox.showinfo("Thành công", "Đã mượn sách thành công")
                borrow_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi mượn sách: {e}")
                messagebox.showerror("Lỗi", f"Không thể mượn sách: {e}")

        # Nút mượn sách
        ttk.Button(borrow_window, text="Mượn sách", command=borrow_book).pack(pady=20)

    def show_return_window(self):
        # Tạo cửa sổ trả sách
        return_window = tk.Toplevel(self.main_window.root)
        return_window.title("Trả sách")
        return_window.geometry("800x600")
        return_window.transient(self.main_window.root)
        return_window.grab_set()

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

        def update_treeview():
            # Xóa dữ liệu cũ
            for item in tree.get_children():
                tree.delete(item)
            
            # Thêm các sách đang mượn
            for track in data_handler.tracking_db.values():
                if track.trang_thai == "Borrowed":
                    tree.insert('', 'end', values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        track.trang_thai
                    ))

        # Cập nhật danh sách ban đầu
        update_treeview()

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
                        track.trang_thai = "Returned"
                        track.ngay_tra = datetime.now().strftime("%Y-%m-%d")

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
        for track in data_handler.tracking_db.values():
            self.tree.insert('', 'end', values=(
                track.ma_ban_doc,
                track.ma_sach_muon,
                track.ten_sach_muon,
                track.ngay_muon,
                track.ngay_tra or "",
                track.trang_thai
            ))
    def show_history_window(self):
        # Tạo cửa sổ lịch sử
        history_window = tk.Toplevel(self.main_window.root)
        history_window.title("Lịch sử mượn/trả sách")
        history_window.geometry("800x600")
        history_window.transient(self.main_window.root)
        history_window.grab_set()

        # Frame chứa tìm kiếm
        search_frame = ttk.Frame(history_window)
        search_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(search_frame, text="Mã bạn đọc:").pack(side='left', padx=5)
        ma_ban_doc_combo = ttk.Combobox(search_frame)
        ma_ban_doc_combo['values'] = [reader.ma_ban_doc for reader in data_handler.readers_db.values()]
        ma_ban_doc_combo.pack(side='left', padx=5)

        # Frame chứa Treeview
        tree_frame = ttk.Frame(history_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'ngay_tra', 'trang_thai')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        tree.heading('ma_ban_doc', text='Mã bạn đọc')
        tree.heading('ma_sach_muon', text='Mã sách')
        tree.heading('ten_sach_muon', text='Tên sách')
        tree.heading('ngay_muon', text='Ngày mượn')
        tree.heading('ngay_tra', text='Ngày trả')
        tree.heading('trang_thai', text='Trạng thái')

        # Đặt độ rộng cột
        tree.column('ma_ban_doc', width=100)
        tree.column('ma_sach_muon', width=100)
        tree.column('ten_sach_muon', width=200)
        tree.column('ngay_muon', width=100)
        tree.column('ngay_tra', width=100)
        tree.column('trang_thai', width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

        def search_history(*args):
            ma_ban_doc = ma_ban_doc_combo.get()
            
            # Xóa dữ liệu cũ
            for item in tree.get_children():
                tree.delete(item)
            
            # Thêm dữ liệu mới
            for track in data_handler.tracking_db.values():
                if not ma_ban_doc or track.ma_ban_doc == ma_ban_doc:
                    tree.insert('', 'end', values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        track.ngay_tra or "",
                        track.trang_thai
                    ))

        # Bind sự kiện thay đổi combobox
        ma_ban_doc_combo.bind('<<ComboboxSelected>>', search_history)
        
        # Hiển thị tất cả lịch sử ban đầu
        search_history()

    def show_overdue_books_window(self):
        # Tạo cửa sổ sách quá hạn
        overdue_window = tk.Toplevel(self.main_window.root)
        overdue_window.title("Sách quá hạn")
        overdue_window.geometry("800x600")
        overdue_window.transient(self.main_window.root)
        overdue_window.grab_set()

        # Frame chứa Treeview
        tree_frame = ttk.Frame(overdue_window)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_ban_doc', 'ma_sach_muon', 'ten_sach_muon', 'ngay_muon', 'so_ngay_qua_han')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        tree.heading('ma_ban_doc', text='Mã bạn đọc')
        tree.heading('ma_sach_muon', text='Mã sách')
        tree.heading('ten_sach_muon', text='Tên sách')
        tree.heading('ngay_muon', text='Ngày mượn')
        tree.heading('so_ngay_qua_han', text='Số ngày quá hạn')

        # Đặt độ rộng cột
        tree.column('ma_ban_doc', width=100)
        tree.column('ma_sach_muon', width=100)
        tree.column('ten_sach_muon', width=200)
        tree.column('ngay_muon', width=100)
        tree.column('so_ngay_qua_han', width=100)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

        # Thêm dữ liệu sách quá hạn
        current_date = datetime.now()
        for track in data_handler.tracking_db.values():
            if track.trang_thai == "Borrowed":
                borrow_date = datetime.strptime(track.ngay_muon, "%Y-%m-%d")
                days_overdue = (current_date - borrow_date).days - 14  # Trừ đi 14 ngày cho phép
                if days_overdue > 0:
                    tree.insert('', 'end', values=(
                        track.ma_ban_doc,
                        track.ma_sach_muon,
                        track.ten_sach_muon,
                        track.ngay_muon,
                        days_overdue
                    ))

        if not tree.get_children():
            messagebox.showinfo("Thông báo", "Không có sách nào quá hạn")
            overdue_window.destroy()