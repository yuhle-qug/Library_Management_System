import datetime

# Lớp Book (Sách)
class Book:
    def __init__(self, ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban):
        # Khởi tạo thông tin sách
        self.ma_sach = str(ma_sach)  # Mã sách (string)
        self.ten_sach = ten_sach  # Tên sách
        self.tac_gia = tac_gia  # Tác giả
        self.the_loai = the_loai  # Thể loại
        self.so_luong = int(so_luong)  # Số lượng sách
        self.tinh_trang = tinh_trang  # Tình trạng sách
        self.nha_xuat_ban = nha_xuat_ban  # Nhà xuất bản

    def __str__(self):
        # Chuỗi mô tả sách
        return (f"Book[ID: {self.ma_sach}, Title: {self.ten_sach}, Author: {self.tac_gia}, "
                f"Qty: {self.so_luong}, Status: {self.tinh_trang}]")

    def to_dict(self):
        # Chuyển đổi đối tượng sách thành dictionary
        data = self.__dict__.copy()
        data['ma_sach'] = str(self.ma_sach)  # Đảm bảo mã sách là string
        return data

    @classmethod
    def from_dict(cls, data_dict):
        # Tạo đối tượng sách từ dictionary
        data_copy = data_dict.copy()
        if 'ma_sach' in data_copy:
            data_copy['ma_sach'] = str(data_copy['ma_sach'])  # Đảm bảo mã sách là string
        return cls(**data_copy)

# Lớp Reader (Bạn đọc)
class Reader:
    def __init__(self, ma_ban_doc, ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai):
        # Khởi tạo thông tin bạn đọc
        self.ma_ban_doc = ma_ban_doc  # Mã bạn đọc
        self.ten = ten  # Tên bạn đọc
        self.ngay_sinh = ngay_sinh  # Ngày sinh
        self.gioi_tinh = gioi_tinh  # Giới tính
        self.dia_chi = dia_chi  # Địa chỉ
        self.so_dien_thoai = so_dien_thoai  # Số điện thoại

    def __str__(self):
        # Chuỗi mô tả bạn đọc
        return f"Reader[ID: {self.ma_ban_doc}, Name: {self.ten}, Phone: {self.so_dien_thoai}]"

    def to_dict(self):
        # Chuyển đổi đối tượng bạn đọc thành dictionary
        return self.__dict__

    @classmethod
    def from_dict(cls, data_dict):
        # Tạo đối tượng bạn đọc từ dictionary
        return cls(**data_dict)

# Lớp TrackBook (Theo dõi mượn sách)
class TrackBook:
    def __init__(self, ma_ban_doc, ma_sach_muon, ten_sach_muon, ngay_muon, ngay_tra=None, trang_thai="Đang mượn"):
        # Khởi tạo thông tin theo dõi mượn sách
        self.ma_ban_doc = ma_ban_doc  # Mã bạn đọc
        self.ma_sach_muon = ma_sach_muon  # Mã sách mượn
        self.ten_sach_muon = ten_sach_muon  # Tên sách mượn
        self.ngay_muon = ngay_muon  # Ngày mượn
        self.ngay_tra = ngay_tra  # Ngày trả (có thể None)
        self.trang_thai = trang_thai  # Trạng thái ("Đang mượn", "Quá hạn", "Đã trả")

    def __str__(self):
        # Chuỗi mô tả thông tin mượn sách
        return (f"Track[Mã bạn đọc: {self.ma_ban_doc}, Mã sách: {self.ma_sach_muon}, "
                f"Ngày mượn: {self.ngay_muon}, Ngày trả: {self.ngay_tra}, Trạng thái: {self.trang_thai}]")

    def to_dict(self):
        # Chuyển đổi đối tượng theo dõi mượn sách thành dictionary
        return self.__dict__

    @classmethod
    def from_dict(cls, data_dict):
        # Tạo đối tượng theo dõi mượn sách từ dictionary
        return cls(**data_dict)