import tkinter as tk
from tkinter import ttk, messagebox
from src.core.models import Reader
from src.core.data_handler import data_handler
from src.utils.logger import logger
from src.gui.date_picker import MyDatePicker
import datetime

FONT = ("Arial Unicode MS", 11)

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

        ttk.Button(center_frame, text="Thêm bạn đọc mới", style="Pastel.TButton", command=self.show_add_reader_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Cập nhật bạn đọc", style="Pastel.TButton", command=self.show_update_reader_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Tìm kiếm bạn đọc", style="Pastel.TButton", command=self.show_search_reader_window).pack(side='left', padx=10)
        ttk.Button(center_frame, text="Xóa bạn đọc", style="Pastel.TButton", command=self.delete_reader_window).pack(side='left', padx=10)

        # Frame chứa các điều khiển sắp xếp và lọc
        controls_frame = ttk.Frame(self.frame)
        controls_frame.pack(fill='x', padx=10, pady=5)

        # Phần sắp xếp
        sort_frame = ttk.LabelFrame(controls_frame, text="Sắp xếp")
        sort_frame.pack(side='left', padx=5, fill='x', expand=True)

        ttk.Label(sort_frame, text="Sắp xếp theo:").pack(side='left', padx=5)
        self.sort_by_combo = ttk.Combobox(sort_frame, values=["Mã bạn đọc", "Họ tên", "Ngày sinh", "Số điện thoại"], state="readonly")
        self.sort_by_combo.current(0)  # Mặc định sắp xếp theo Mã bạn đọc
        self.sort_by_combo.pack(side='left', padx=5)

        ttk.Label(sort_frame, text="Thứ tự:").pack(side='left', padx=5)
        self.sort_order_combo = ttk.Combobox(sort_frame, values=["Tăng dần", "Giảm dần"], state="readonly")
        self.sort_order_combo.current(0)  # Mặc định tăng dần
        self.sort_order_combo.pack(side='left', padx=5)

        # Phần lọc
        filter_frame = ttk.LabelFrame(controls_frame, text="Lọc")
        filter_frame.pack(side='left', padx=5, fill='x', expand=True)

        ttk.Label(filter_frame, text="Lọc theo:").pack(side='left', padx=5)
        self.filter_by_combo = ttk.Combobox(filter_frame, values=["Giới tính", "Địa chỉ"], state="readonly")
        self.filter_by_combo.pack(side='left', padx=5)

        ttk.Label(filter_frame, text="Giá trị:").pack(side='left', padx=5)
        self.filter_value_entry = ttk.Entry(filter_frame)
        self.filter_value_entry.pack(side='left', padx=5)

        # Nút điều khiển
        control_buttons_frame = ttk.Frame(controls_frame)
        control_buttons_frame.pack(side='left', padx=5)

        ttk.Button(control_buttons_frame, text="Áp dụng", style="Pastel.TButton", command=self.apply_filters).pack(side='left', padx=5)
        ttk.Button(control_buttons_frame, text="Reset", style="Pastel.TButton", command=self.reset_filters).pack(side='left', padx=5)

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
        ttk.Label(add_window, text="Mã bạn đọc:", font=FONT).pack(pady=5)
        ma_ban_doc_entry = ttk.Entry(add_window)
        ma_ban_doc_entry.pack(pady=5)

        ttk.Label(add_window, text="Họ tên:", font=FONT).pack(pady=5)
        ten_entry = ttk.Entry(add_window)
        ten_entry.pack(pady=5)

        ttk.Label(add_window, text="Ngày sinh:", font=FONT).pack(pady=5)
        ngay_sinh_frame = ttk.Frame(add_window)
        ngay_sinh_frame.pack(pady=5)
        ngay_sinh_entry = ttk.Entry(ngay_sinh_frame)
        ngay_sinh_entry.pack(side='left', padx=5)
        
        def open_date_picker():
            date_picker = MyDatePicker(add_window)
            selected_date = date_picker.get_date()
            if selected_date:
                ngay_sinh_entry.delete(0, tk.END)
                ngay_sinh_entry.insert(0, selected_date.strftime("%d/%m/%Y"))

        ttk.Button(ngay_sinh_frame, text="Chọn ngày", command=open_date_picker).pack(side='left')

        ttk.Label(add_window, text="Giới tính:", font=FONT).pack(pady=5)
        gioi_tinh_combo = ttk.Combobox(add_window, values=["Nam", "Nữ", "Khác"], font=FONT)
        gioi_tinh_combo.pack(pady=5)

        ttk.Label(add_window, text="Địa chỉ:", font=FONT).pack(pady=5)
        dia_chi_entry = ttk.Entry(add_window)
        dia_chi_entry.pack(pady=5)

        ttk.Label(add_window, text="Số điện thoại:", font=FONT).pack(pady=5)
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
        ttk.Label(update_window, text="Mã bạn đọc:", font=FONT).pack(pady=5)
        ma_ban_doc_entry = ttk.Entry(update_window)
        ma_ban_doc_entry.insert(0, reader.ma_ban_doc)
        ma_ban_doc_entry.configure(state='readonly')
        ma_ban_doc_entry.pack(pady=5)

        ttk.Label(update_window, text="Họ tên:", font=FONT).pack(pady=5)
        ten_entry = ttk.Entry(update_window)
        ten_entry.insert(0, reader.ten)
        ten_entry.pack(pady=5)

        ttk.Label(update_window, text="Ngày sinh:", font=FONT).pack(pady=5)
        ngay_sinh_frame = ttk.Frame(update_window)
        ngay_sinh_frame.pack(pady=5)
        ngay_sinh_entry = ttk.Entry(ngay_sinh_frame)
        try:
            dt = datetime.strptime(reader.ngay_sinh, "%Y-%m-%d")
            ngay_sinh_entry.insert(0, dt.strftime("%d/%m/%Y"))
        except Exception:
            ngay_sinh_entry.insert(0, reader.ngay_sinh)
        ngay_sinh_entry.pack(side='left', padx=5)
        
        def open_date_picker():
            date_picker = MyDatePicker(update_window)
            selected_date = date_picker.get_date()
            if selected_date:
                ngay_sinh_entry.delete(0, tk.END)
                ngay_sinh_entry.insert(0, selected_date.strftime("%d/%m/%Y"))

        ttk.Button(ngay_sinh_frame, text="Chọn ngày", command=open_date_picker).pack(side='left')

        ttk.Label(update_window, text="Giới tính:", font=FONT).pack(pady=5)
        gioi_tinh_combo = ttk.Combobox(update_window, values=["Nam", "Nữ", "Khác"], font=FONT)
        gioi_tinh_combo.set(reader.gioi_tinh)
        gioi_tinh_combo.pack(pady=5)

        ttk.Label(update_window, text="Địa chỉ:", font=FONT).pack(pady=5)
        dia_chi_entry = ttk.Entry(update_window)
        dia_chi_entry.insert(0, reader.dia_chi)
        dia_chi_entry.pack(pady=5)

        ttk.Label(update_window, text="Số điện thoại:", font=FONT).pack(pady=5)
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

    def update_reader_list(self, readers=None):
        logger.info(f"update_reader_list called with {len(readers) if readers is not None else 'default'} readers.")
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Temporarily hide headings to force redraw
        self.tree.config(show='')

        # Lấy danh sách bạn đọc cần hiển thị
        if readers is None:
            readers = sorted(data_handler.readers_db.values(), key=lambda x: x.ma_ban_doc)

        # Thêm dữ liệu mới vào Treeview
        try:
            for idx, reader in enumerate(readers):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                values = (
                    reader.ma_ban_doc,
                    reader.ten,
                    reader.ngay_sinh,
                    reader.gioi_tinh,
                    reader.dia_chi,
                    reader.so_dien_thoai
                )
                logger.info(f"update_reader_list: Inserting values for reader {reader.ma_ban_doc}: {values}")
                self.tree.insert('', 'end', values=values, tags=(tag,))

            self.tree.tag_configure('evenrow', background='#ffffff')
            self.tree.tag_configure('oddrow', background='#E3F6FF')

            # Show headings again
            self.tree.config(show='headings')

            self.tree.update_idletasks() # Explicitly update the Treeview display

        except Exception as e:
            logger.error(f"Lỗi khi cập nhật Treeview bạn đọc: {e}")
            # Optionally show an error message to the user
            # messagebox.showerror("Lỗi", f"Không thể cập nhật hiển thị bạn đọc: {e}")

    def apply_filters(self):
        # Lấy các giá trị từ controls
        sort_field = self.sort_by_combo.get()
        sort_order = self.sort_order_combo.get()
        filter_field = self.filter_by_combo.get()
        filter_value = self.filter_value_entry.get().strip().lower()

        # Chuyển đổi tên trường sang tên thuộc tính
        field_map = {
            "Mã bạn đọc": "ma_ban_doc",
            "Họ tên": "ten",
            "Ngày sinh": "ngay_sinh",
            "Số điện thoại": "so_dien_thoai",
            "Giới tính": "gioi_tinh",
            "Địa chỉ": "dia_chi"
        }

        # Lọc dữ liệu
        filtered_readers = list(data_handler.readers_db.values())
        if filter_field and filter_value:
            field = field_map[filter_field]
            filtered_readers = [
                reader for reader in filtered_readers
                if str(getattr(reader, field)).lower() == filter_value
            ]

        logger.info(f"apply_filters (reader_tab): Filtered {len(filtered_readers)} readers.")

        # Sắp xếp dữ liệu
        if sort_field:
            field = field_map[sort_field]
            reverse = sort_order == "Giảm dần"
            try:
                 filtered_readers.sort(key=lambda x: getattr(x, field), reverse=reverse)
            except Exception as e:
                logger.error(f"Lỗi khi sắp xếp bạn đọc: {e}")
                messagebox.showerror("Lỗi", f"Không thể sắp xếp danh sách: {e}")
                return # Stop if sorting fails

        logger.info(f"apply_filters (reader_tab): Filtered and sorted {len(filtered_readers)} readers.")

        # Cập nhật Treeview
        self.update_reader_list(filtered_readers)

    def reset_filters(self):
        # Reset các controls về giá trị mặc định
        self.sort_by_combo.current(0)
        self.sort_order_combo.current(0)
        self.filter_by_combo.set("")
        self.filter_value_entry.delete(0, tk.END)

        # Hiển thị lại danh sách gốc (sắp xếp theo mã bạn đọc tăng dần)
        readers = sorted(data_handler.readers_db.values(), key=lambda x: x.ma_ban_doc)
        self.update_reader_list(readers)

    def show_search_reader_window(self):
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("Tìm kiếm bạn đọc")
        search_window.geometry("900x600")
        search_window.transient(self.main_window.root)
        search_window.grab_set()
        ttk.Label(search_window, text="Tìm kiếm theo:").pack(pady=5)
        criteria = ["Tất cả", "Mã bạn đọc", "Họ tên", "Số điện thoại"]
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
        columns = ('ma_ban_doc', 'ten', 'ngay_sinh', 'gioi_tinh', 'dia_chi', 'so_dien_thoai')
        results_tree = ttk.Treeview(results_frame, columns=columns, show='headings')

        # Define columns for the results Treeview
        results_tree.heading('ma_ban_doc', text='Mã bạn đọc')
        results_tree.heading('ten', text='Họ tên')
        results_tree.heading('ngay_sinh', text='Ngày sinh')
        results_tree.heading('gioi_tinh', text='Giới tính')
        results_tree.heading('dia_chi', text='Địa chỉ')
        results_tree.heading('so_dien_thoai', text='Số điện thoại')

        # Set column widths (optional, can adjust as needed)
        results_tree.column('ma_ban_doc', width=80)
        results_tree.column('ten', width=150)
        results_tree.column('ngay_sinh', width=100)
        results_tree.column('gioi_tinh', width=80)
        results_tree.column('dia_chi', width=150)
        results_tree.column('so_dien_thoai', width=100)

        # Add scrollbar to results Treeview
        results_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=results_tree.yview)
        results_tree.configure(yscrollcommand=results_scrollbar.set)
        results_scrollbar.pack(side='right', fill='y')
        results_tree.pack(side='left', fill='both', expand=True)

        def search():
            field = criteria_combo.get()
            keyword = search_entry.get().strip().lower()
            found_readers = []
            for reader in data_handler.readers_db.values():
                if field == "Tất cả":
                    if (keyword in reader.ma_ban_doc.lower() or
                        keyword in reader.ten.lower() or
                        keyword in reader.so_dien_thoai.lower()):
                        found_readers.append(reader)
                elif field == "Mã bạn đọc" and keyword in reader.ma_ban_doc.lower():
                    found_readers.append(reader)
                elif field == "Họ tên" and keyword in reader.ten.lower():
                    found_readers.append(reader)
                elif field == "Số điện thoại" and keyword in reader.so_dien_thoai.lower():
                    found_readers.append(reader)
            if found_readers:
                logger.info(f"search (reader_tab): Found {len(found_readers)} readers.")
                # Clear previous results in the search window Treeview
                for item in results_tree.get_children():
                    results_tree.delete(item)
                # Insert new results
                for idx, reader in enumerate(found_readers):
                    tag = 'evenrow' if idx % 2 == 0 else 'oddrow' # Reuse row tags
                    values = (
                        reader.ma_ban_doc,
                        reader.ten,
                        reader.ngay_sinh,
                        reader.gioi_tinh,
                        reader.dia_chi,
                        reader.so_dien_thoai
                    )
                    results_tree.insert('', 'end', values=values, tags=(tag,))
                results_tree.tag_configure('evenrow', background='#ffffff') # Reuse row tags config
                results_tree.tag_configure('oddrow', background='#E3F6FF') # Reuse row tags config

                results_tree.update_idletasks() # Update the search results Treeview

                messagebox.showinfo("Kết quả", f"Tìm thấy {len(found_readers)} bạn đọc")
            else:
                logger.info("search (reader_tab): No readers found.")
                # Xóa toàn bộ các hàng trong Treeview khi không tìm thấy kết quả
                for item in results_tree.get_children():
                    results_tree.delete(item)
                results_tree.update_idletasks() # Update the search results Treeview
                messagebox.showinfo("Kết quả", "Không tìm thấy bạn đọc nào")
            # Don't destroy window immediately, let user view results

        ttk.Button(search_window, text="Tìm kiếm", command=search).pack(pady=20)

    def delete_reader_window(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bạn đọc cần xóa")
            return
        reader_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bạn đọc '{reader_id}' không?"):
            if data_handler.is_reader_borrowing(reader_id):
                messagebox.showerror("Lỗi", "Không thể xóa bạn đọc đang mượn hoặc quá hạn!")
                return
            data_handler.delete_reader(reader_id)
            self.update_reader_list()
            messagebox.showinfo("Thành công", "Đã xóa bạn đọc thành công!")