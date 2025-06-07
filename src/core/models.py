import datetime

class Book:
    def __init__(self, ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban):
        self.ma_sach = str(ma_sach)
        self.ten_sach = ten_sach
        self.tac_gia = tac_gia
        self.the_loai = the_loai
        self.so_luong = int(so_luong)
        self.tinh_trang = tinh_trang
        self.nha_xuat_ban = nha_xuat_ban

    def __str__(self):
        return (f"Book[ID: {self.ma_sach}, Title: {self.ten_sach}, Author: {self.tac_gia}, "
                f"Qty: {self.so_luong}, Status: {self.tinh_trang}]")

    def to_dict(self):
        data = self.__dict__.copy()
        data['ma_sach'] = str(self.ma_sach)
        return data

    @classmethod
    def from_dict(cls, data_dict):
        data_copy = data_dict.copy()
        if 'ma_sach' in data_copy:
            data_copy['ma_sach'] = str(data_copy['ma_sach'])
        return cls(**data_copy)

class Reader:
    def __init__(self, ma_ban_doc, ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai):
        self.ma_ban_doc = ma_ban_doc
        self.ten = ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh
        self.dia_chi = dia_chi
        self.so_dien_thoai = so_dien_thoai

    def __str__(self):
        return f"Reader[ID: {self.ma_ban_doc}, Name: {self.ten}, Phone: {self.so_dien_thoai}]"

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

class TrackBook:    
    def __init__(self, ma_ban_doc, ma_sach_muon, ten_sach_muon, ngay_muon, ngay_tra=None, trang_thai="Đang mượn"):
        self.ma_ban_doc = ma_ban_doc
        self.ma_sach_muon = ma_sach_muon
        self.ten_sach_muon = ten_sach_muon
        self.ngay_muon = ngay_muon
        self.ngay_tra = ngay_tra
        self.trang_thai = trang_thai

    def __str__(self):        return (f"Track[Mã bạn đọc: {self.ma_ban_doc}, Mã sách: {self.ma_sach_muon}, "
                f"Ngày mượn: {self.ngay_muon}, Ngày trả: {self.ngay_tra}, Trạng thái: {self.trang_thai}]")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)