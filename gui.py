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

    def setup_book_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.book_tab)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Thêm sách mới", 
                  command=self.show_add_book_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cập nhật sách", 
                  command=self.show_update_book_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Tìm kiếm sách", 
                  command=self.show_search_book_window).pack(side=tk.LEFT, padx=5)

        # Treeview để hiển thị danh sách sách
        self.book_tree = ttk.Treeview(self.book_tab, columns=('ID', 'Tên', 'Tác giả', 'Số lượng'))
        self.book_tree.heading('ID', text='Mã sách')
        self.book_tree.heading('Tên', text='Tên sách')
        self.book_tree.heading('Tác giả', text='Tác giả')
        self.book_tree.heading('Số lượng', text='Số lượng')
        self.book_tree.pack(pady=10, padx=10, fill='both', expand=True)

    def setup_reader_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.reader_tab)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Thêm bạn đọc", 
                  command=self.show_add_reader_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cập nhật thông tin", 
                  command=self.show_update_reader_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Tìm kiếm bạn đọc", 
                  command=self.show_search_reader_window).pack(side=tk.LEFT, padx=5)

        # Treeview để hiển thị danh sách bạn đọc
        self.reader_tree = ttk.Treeview(self.reader_tab, 
                                      columns=('ID', 'Tên', 'SĐT', 'Địa chỉ'))
        self.reader_tree.heading('ID', text='Mã bạn đọc')
        self.reader_tree.heading('Tên', text='Tên')
        self.reader_tree.heading('SĐT', text='Số điện thoại')
        self.reader_tree.heading('Địa chỉ', text='Địa chỉ')
        self.reader_tree.pack(pady=10, padx=10, fill='both', expand=True)

    def setup_tracking_tab(self):
        # Frame chứa các nút chức năng
        btn_frame = ttk.Frame(self.tracking_tab)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Mượn sách", 
                  command=self.show_borrow_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Trả sách", 
                  command=self.show_return_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Xem lịch sử", 
                  command=self.show_history_window).pack(side=tk.LEFT, padx=5)

        # Treeview để hiển thị danh sách mượn/trả
        self.tracking_tree = ttk.Treeview(self.tracking_tab, 
                                        columns=('Bạn đọc', 'Sách', 'Ngày mượn', 'Ngày trả', 'Trạng thái'))
        self.tracking_tree.heading('Bạn đọc', text='Bạn đọc')
        self.tracking_tree.heading('Sách', text='Sách')
        self.tracking_tree.heading('Ngày mượn', text='Ngày mượn')
        self.tracking_tree.heading('Ngày trả', text='Ngày trả')
        self.tracking_tree.heading('Trạng thái', text='Trạng thái')
        self.tracking_tree.pack(pady=10, padx=10, fill='both', expand=True)

    # Các phương thức hiển thị cửa sổ chức năng
    def show_add_book_window(self):
        logger.info("Mở cửa sổ thêm sách mới")
        add_window = ttk.Toplevel(self.root)
        add_window.title("Thêm Sách Mới")
        add_window.geometry("400x300")

        ttk.Label(add_window, text="Mã sách:").pack(pady=5)
        ma_sach_entry = ttk.Entry(add_window)
        ma_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(add_window)
        ten_sach_entry.pack(pady=5)

        ttk.Label(add_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(add_window)
        tac_gia_entry.pack(pady=5)

        ttk.Label(add_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(add_window)
        so_luong_entry.pack(pady=5)

        def save_book():
            logger.info("Đã lưu sách mới")
            # Logic to save book goes here
            add_window.destroy()

        ttk.Button(add_window, text="Lưu", command=save_book).pack(pady=20)

    def show_update_book_window(self):
        logger.info("Mở cửa sổ cập nhật sách")
        if not self.book_tree.selection():
            logger.warning("Không có sách nào được chọn để cập nhật")
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách cần cập nhật!")
            return
            
        selected_item = self.book_tree.selection()[0]
        book_id = self.book_tree.item(selected_item)['values'][0]
        book = data_handler.books_db[book_id]
        logger.info(f"Mở cửa sổ cập nhật cho sách: {book_id}")
        
        update_window = tk.Toplevel(self.root)
        update_window.title("Cập Nhật Thông Tin Sách")
        update_window.geometry("400x500")
        
        ttk.Label(update_window, text="Tên sách:").pack(pady=5)
        ten_sach_entry = ttk.Entry(update_window)
        ten_sach_entry.insert(0, book.ten_sach)
        ten_sach_entry.pack(pady=5)
        
        ttk.Label(update_window, text="Tác giả:").pack(pady=5)
        tac_gia_entry = ttk.Entry(update_window)
        tac_gia_entry.insert(0, book.tac_gia)
        tac_gia_entry.pack(pady=5)
        
        ttk.Label(update_window, text="Số lượng:").pack(pady=5)
        so_luong_entry = ttk.Entry(update_window)
        so_luong_entry.insert(0, str(book.so_luong))
        so_luong_entry.pack(pady=5)

        def update_book():
            try:
                book.ten_sach = ten_sach_entry.get().strip()
                book.tac_gia = tac_gia_entry.get().strip()
                book.so_luong = int(so_luong_entry.get().strip())
                
                self.update_book_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin sách!")
                update_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")

        ttk.Button(update_window, text="Cập nhật", command=update_book).pack(pady=20)

    def update_book_list(self):
        logger.debug("Cập nhật danh sách sách hiển thị")
        # Xóa dữ liệu cũ
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
            
        # Cập nhật dữ liệu mới
        for book in data_handler.books_db.values():
            self.book_tree.insert('', 'end', values=(
                book.ma_sach,
                book.ten_sach,
                book.tac_gia,
                book.so_luong
            ))
        logger.debug("Đã cập nhật xong danh sách sách")

    def show_search_book_window(self):
        logger.info("Mở cửa sổ tìm kiếm sách")
        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm Kiếm Sách")
        search_window.geometry("400x200")

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
                                     columns=('ID', 'Tên', 'Tác giả', 'Số lượng'))
            result_tree.heading('ID', text='Mã sách')
            result_tree.heading('Tên', text='Tên sách')
            result_tree.heading('Tác giả', text='Tác giả')
            result_tree.heading('Số lượng', text='Số lượng')
            result_tree.pack(pady=10, padx=10, fill='both', expand=True)
            
            for book in found_books:
                result_tree.insert('', 'end', values=(
                    book.ma_sach,
                    book.ten_sach,
                    book.tac_gia,
                    book.so_luong
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
        logger.debug("Cập nhật danh sách bạn đọc hiển thị")
        # Xóa dữ liệu cũ
        for item in self.reader_tree.get_children():
            self.reader_tree.delete(item)
            
        # Cập nhật dữ liệu mới
        for reader in data_handler.readers_db.values():
            self.reader_tree.insert('', 'end', values=(
                reader.ma_ban_doc,
                reader.ten,
                reader.so_dien_thoai,
                reader.dia_chi
            ))
        logger.debug("Đã cập nhật xong danh sách bạn đọc")

    def show_update_reader_window(self):
        logger.info("Mở cửa sổ cập nhật bạn đọc")
        if not self.reader_tree.selection():
            logger.warning("Không có bạn đọc nào được chọn để cập nhật")
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn đọc cần cập nhật!")
            return
            
        selected_item = self.reader_tree.selection()[0]
        reader_id = self.reader_tree.item(selected_item)['values'][0]
        reader = data_handler.readers_db[reader_id]
        logger.info(f"Mở cửa sổ cập nhật cho bạn đọc: {reader_id}")
        
        update_window = ttk.Toplevel(self.root)
        update_window.title("Cập Nhật Thông Tin Bạn Đọc")
        update_window.geometry("400x600")
        
        form = ScrolledFrame(update_window)
        form.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        ttk.Label(form, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(form)
        ten_entry.insert(0, reader.ten)
        ten_entry.pack(pady=5)
        
        ttk.Label(form, text="Ngày sinh:").pack(pady=5)
        ngay_sinh_entry = ttk.Entry(form)
        ngay_sinh_entry.insert(0, reader.ngay_sinh)
        ngay_sinh_entry.pack(pady=5)
        
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
                reader.dia_chi = dia_chi_entry.get().strip()
                reader.so_dien_thoai = sdt_entry.get().strip()
                
                self.update_reader_list()
                logger.info(f"Cập nhật thông tin bạn đọc thành công: {reader_id}")
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin bạn đọc!")
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
        logger.debug("Cập nhật danh sách mượn/trả sách")
        # Xóa dữ liệu cũ
        for item in self.tracking_tree.get_children():
            self.tracking_tree.delete(item)
            
        # Cập nhật dữ liệu mới
        for record in data_handler.tracking_records:
            reader = data_handler.readers_db.get(record.ma_ban_doc, None)
            reader_name = reader.ten if reader else "Unknown"
            
            self.tracking_tree.insert('', 'end', values=(
                reader_name,
                record.ten_sach_muon,
                record.ngay_muon,
                record.ngay_tra or "Chưa trả",
                record.trang_thai
            ))
        logger.debug("Đã cập nhật xong danh sách mượn/trả sách")

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