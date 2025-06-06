import tkinter as tk
from tkinter import ttk, messagebox
from src.core.models import Reader
from src.core.data_handler import data_handler
from src.utils.logger import logger
from src.gui.date_picker import MyDatePicker

class ReaderTab:
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
        ttk.Button(center_frame, text="Thêm bạn đọc mới", command=self.show_add_reader_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Cập nhật bạn đọc", command=self.show_update_reader_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Tìm kiếm bạn đọc", command=self.show_search_reader_window).pack(side='left', padx=10)

        # Frame chứa Treeview
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Tạo Treeview
        columns = ('ma_ban_doc', 'ten', 'ngay_sinh', 'gioi_tinh', 'dia_chi', 'so_dien_thoai')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # Định nghĩa các cột
        self.tree.heading('ma_ban_doc', text='Mã bạn đọc')
        self.tree.heading('ten', text='Họ tên')
        self.tree.heading('ngay_sinh', text='Ngày sinh')
        self.tree.heading('gioi_tinh', text='Giới tính')
        self.tree.heading('dia_chi', text='Địa chỉ')
        self.tree.heading('so_dien_thoai', text='Số điện thoại')

        # Đặt độ rộng cột
        self.tree.column('ma_ban_doc', width=100)
        self.tree.column('ten', width=200)
        self.tree.column('ngay_sinh', width=100)
        self.tree.column('gioi_tinh', width=80)
        self.tree.column('dia_chi', width=200)
        self.tree.column('so_dien_thoai', width=120)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        # Cập nhật danh sách bạn đọc
        self.update_reader_list()

    def show_add_reader_window(self):
        # Tạo cửa sổ mới
        add_window = tk.Toplevel(self.main_window.root)
        add_window.title("Thêm bạn đọc mới")
        add_window.geometry("600x700")
        add_window.transient(self.main_window.root)
        add_window.grab_set()

        # Tạo các trường nhập liệu
        ttk.Label(add_window, text="Mã bạn đọc:").pack(pady=5)
        ma_ban_doc_entry = ttk.Entry(add_window)
        ma_ban_doc_entry.pack(pady=5)

        ttk.Label(add_window, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(add_window)
        ten_entry.pack(pady=5)

        ttk.Label(add_window, text="Ngày sinh:").pack(pady=5)
        ngay_sinh_frame = ttk.Frame(add_window)
        ngay_sinh_frame.pack(pady=5)
        ngay_sinh_entry = ttk.Entry(ngay_sinh_frame)
        ngay_sinh_entry.pack(side='left', padx=5)
        
        def open_date_picker():
            date_picker = MyDatePicker(add_window)
            selected_date = date_picker.get_date()
            if selected_date:
                ngay_sinh_entry.delete(0, tk.END)
                ngay_sinh_entry.insert(0, selected_date.strftime("%Y-%m-%d"))

        ttk.Button(ngay_sinh_frame, text="Chọn ngày", command=open_date_picker).pack(side='left')

        ttk.Label(add_window, text="Giới tính:").pack(pady=5)
        gioi_tinh_combo = ttk.Combobox(add_window, values=["Nam", "Nữ", "Khác"])
        gioi_tinh_combo.pack(pady=5)

        ttk.Label(add_window, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(add_window)
        dia_chi_entry.pack(pady=5)

        ttk.Label(add_window, text="Số điện thoại:").pack(pady=5)
        so_dien_thoai_entry = ttk.Entry(add_window)
        so_dien_thoai_entry.pack(pady=5)

        def save_reader():
            try:
                ma_ban_doc = ma_ban_doc_entry.get().strip()
                if not ma_ban_doc:
                    messagebox.showerror("Lỗi", "Mã bạn đọc không được để trống")
                    return

                if ma_ban_doc in data_handler.readers_db:
                    messagebox.showerror("Lỗi", "Mã bạn đọc đã tồn tại")
                    return

                ten = ten_entry.get().strip()
                if not ten:
                    messagebox.showerror("Lỗi", "Họ tên không được để trống")
                    return

                ngay_sinh = ngay_sinh_entry.get().strip()
                if not ngay_sinh:
                    messagebox.showerror("Lỗi", "Ngày sinh không được để trống")
                    return

                gioi_tinh = gioi_tinh_combo.get()
                if not gioi_tinh:
                    messagebox.showerror("Lỗi", "Vui lòng chọn giới tính")
                    return

                dia_chi = dia_chi_entry.get().strip()
                if not dia_chi:
                    messagebox.showerror("Lỗi", "Địa chỉ không được để trống")
                    return

                so_dien_thoai = so_dien_thoai_entry.get().strip()
                if not so_dien_thoai:
                    messagebox.showerror("Lỗi", "Số điện thoại không được để trống")
                    return

                new_reader = Reader(ma_ban_doc, ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai)
                data_handler.readers_db[ma_ban_doc] = new_reader
                data_handler.save_data()
                self.update_reader_list()
                messagebox.showinfo("Thành công", f"Đã thêm bạn đọc '{ten}' thành công")
                add_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi thêm bạn đọc: {e}")
                messagebox.showerror("Lỗi", f"Không thể thêm bạn đọc: {e}")

        # Nút lưu
        ttk.Button(add_window, text="Lưu", command=save_reader).pack(pady=20)

    def show_update_reader_window(self):
        # Lấy item được chọn
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn đọc cần cập nhật")
            return

        # Lấy thông tin bạn đọc được chọn
        reader_id = self.tree.item(selected_item[0])['values'][0]
        reader = data_handler.readers_db.get(reader_id)
        if not reader:
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin bạn đọc")
            return

        # Tạo cửa sổ cập nhật
        update_window = tk.Toplevel(self.main_window.root)
        update_window.title("Cập nhật thông tin bạn đọc")
        update_window.geometry("600x700")
        update_window.transient(self.main_window.root)
        update_window.grab_set()

        # Tạo các trường nhập liệu với giá trị hiện tại
        ttk.Label(update_window, text="Mã bạn đọc:").pack(pady=5)
        ma_ban_doc_entry = ttk.Entry(update_window)
        ma_ban_doc_entry.insert(0, reader.ma_ban_doc)
        ma_ban_doc_entry.configure(state='readonly')
        ma_ban_doc_entry.pack(pady=5)

        ttk.Label(update_window, text="Họ tên:").pack(pady=5)
        ten_entry = ttk.Entry(update_window)
        ten_entry.insert(0, reader.ten)
        ten_entry.pack(pady=5)

        ttk.Label(update_window, text="Ngày sinh:").pack(pady=5)
        ngay_sinh_frame = ttk.Frame(update_window)
        ngay_sinh_frame.pack(pady=5)
        ngay_sinh_entry = ttk.Entry(ngay_sinh_frame)
        ngay_sinh_entry.insert(0, reader.ngay_sinh)
        ngay_sinh_entry.pack(side='left', padx=5)
        
        def open_date_picker():
            date_picker = MyDatePicker(update_window)
            selected_date = date_picker.get_date()
            if selected_date:
                ngay_sinh_entry.delete(0, tk.END)
                ngay_sinh_entry.insert(0, selected_date.strftime("%Y-%m-%d"))

        ttk.Button(ngay_sinh_frame, text="Chọn ngày", command=open_date_picker).pack(side='left')

        ttk.Label(update_window, text="Giới tính:").pack(pady=5)
        gioi_tinh_combo = ttk.Combobox(update_window, values=["Nam", "Nữ", "Khác"])
        gioi_tinh_combo.set(reader.gioi_tinh)
        gioi_tinh_combo.pack(pady=5)

        ttk.Label(update_window, text="Địa chỉ:").pack(pady=5)
        dia_chi_entry = ttk.Entry(update_window)
        dia_chi_entry.insert(0, reader.dia_chi)
        dia_chi_entry.pack(pady=5)

        ttk.Label(update_window, text="Số điện thoại:").pack(pady=5)
        so_dien_thoai_entry = ttk.Entry(update_window)
        so_dien_thoai_entry.insert(0, reader.so_dien_thoai)
        so_dien_thoai_entry.pack(pady=5)

        def update_reader():
            try:
                ten = ten_entry.get().strip()
                if not ten:
                    messagebox.showerror("Lỗi", "Họ tên không được để trống")
                    return

                ngay_sinh = ngay_sinh_entry.get().strip()
                if not ngay_sinh:
                    messagebox.showerror("Lỗi", "Ngày sinh không được để trống")
                    return

                gioi_tinh = gioi_tinh_combo.get()
                if not gioi_tinh:
                    messagebox.showerror("Lỗi", "Vui lòng chọn giới tính")
                    return

                dia_chi = dia_chi_entry.get().strip()
                if not dia_chi:
                    messagebox.showerror("Lỗi", "Địa chỉ không được để trống")
                    return

                so_dien_thoai = so_dien_thoai_entry.get().strip()
                if not so_dien_thoai:
                    messagebox.showerror("Lỗi", "Số điện thoại không được để trống")
                    return

                # Cập nhật thông tin bạn đọc
                reader.ten = ten
                reader.ngay_sinh = ngay_sinh
                reader.gioi_tinh = gioi_tinh
                reader.dia_chi = dia_chi
                reader.so_dien_thoai = so_dien_thoai

                data_handler.save_data()
                self.update_reader_list()
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin bạn đọc")
                update_window.destroy()

            except Exception as e:
                logger.error(f"Lỗi khi cập nhật bạn đọc: {e}")
                messagebox.showerror("Lỗi", f"Không thể cập nhật bạn đọc: {e}")

        # Nút cập nhật
        ttk.Button(update_window, text="Cập nhật", command=update_reader).pack(pady=20)
    def update_reader_list(self):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu mới vào Treeview
        for reader in data_handler.readers_db.values():
            self.tree.insert('', 'end', values=(
                reader.ma_ban_doc,
                reader.ten,
                reader.ngay_sinh,
                reader.gioi_tinh,
                reader.dia_chi,
                reader.so_dien_thoai
            ))

    def show_search_reader_window(self):
        # Tạo cửa sổ tìm kiếm
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("Tìm kiếm bạn đọc")
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

            # Tìm kiếm bạn đọc
            found_readers = []
            for reader in data_handler.readers_db.values():
                if (search_term in reader.ma_ban_doc.lower() or
                    search_term in reader.ten.lower() or
                    search_term in reader.dia_chi.lower() or
                    search_term in reader.so_dien_thoai.lower()):
                    found_readers.append(reader)

            if found_readers:
                # Cập nhật Treeview với kết quả tìm kiếm
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for reader in found_readers:
                    self.tree.insert('', 'end', values=(
                        reader.ma_ban_doc,
                        reader.ten,
                        reader.ngay_sinh,
                        reader.gioi_tinh,
                        reader.dia_chi,
                        reader.so_dien_thoai
                    ))
                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_readers)} bạn đọc")
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy bạn đọc nào")
                self.update_reader_list()  # Hiển thị lại tất cả bạn đọc

            search_window.destroy()

        # Nút tìm kiếm
        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)