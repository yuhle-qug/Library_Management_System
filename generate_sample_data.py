import json
from datetime import datetime, timedelta
import random

# Danh sách tên và họ Việt Nam để sinh ngẫu nhiên
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
dem = ["Văn", "Thị", "Đức", "Minh", "Hoàng", "Thành", "Đình", "Xuân", "Thu", "Hồng", "Phương", "Thanh", "Quang", "Hải", "Anh"]
ten = ["An", "Bình", "Châu", "Dung", "Em", "Phúc", "Giang", "Hà", "Hải", "Hùng", "Hương", "Lan", "Linh", "Mai", "Nam", 
       "Ngọc", "Phương", "Quân", "Thành", "Uyên", "Việt", "Xuân", "Yến", "Phú", "Tài", "Tâm", "Thảo", "Trí", "Tuấn", "Tùng"]

# Danh sách thể loại sách
the_loai_sach = ["Văn học", "Khoa học", "Lịch sử", "Thiếu nhi", "Kinh tế", "Tâm lý", "Công nghệ", "Y học", "Triết học", 
                 "Nghệ thuật", "Du lịch", "Âm nhạc", "Thể thao", "Ngoại ngữ", "Giáo dục"]

# Danh sách nhà xuất bản
nha_xuat_ban = ["NXB Giáo dục", "NXB Kim Đồng", "NXB Trẻ", "NXB Tổng hợp", "NXB Văn học", "NXB Khoa học Kỹ thuật", 
                "NXB Hội Nhà văn", "NXB Thanh niên", "NXB Đại học Quốc gia", "NXB Chính trị Quốc gia"]

# Sinh dữ liệu sách
books = {}
for i in range(1, 101):
    ma_sach = f"B{str(i).zfill(3)}"
    ten_sach = f"Sách {i}: {random.choice(['Nghiên cứu về', 'Hướng dẫn', 'Cẩm nang', 'Những điều cần biết về', 'Khám phá'])} {random.choice(the_loai_sach)}"
    books[ma_sach] = {
        "ma_sach": ma_sach,
        "ten_sach": ten_sach,
        "tac_gia": f"{random.choice(ho)} {random.choice(dem)} {random.choice(ten)}",
        "the_loai": random.choice(the_loai_sach),
        "so_luong": random.randint(1, 5),
        "tinh_trang": random.choice(["Mới", "Đã sử dụng", "Có sẵn"]),
        "nha_xuat_ban": random.choice(nha_xuat_ban)
    }

# Sinh dữ liệu bạn đọc
readers = {}
for i in range(1, 101):
    ma_ban_doc = f"R{str(i).zfill(3)}"
    ho_ban_doc = random.choice(ho)
    dem_ban_doc = random.choice(dem)
    ten_ban_doc = random.choice(ten)
    
    # Sinh ngày sinh ngẫu nhiên từ 1990 đến 2005
    ngay_sinh = datetime(random.randint(1990, 2005), random.randint(1, 12), random.randint(1, 28)).strftime("%d/%m/%Y")
    
    readers[ma_ban_doc] = {
        "ma_ban_doc": ma_ban_doc,
        "ten": f"{ho_ban_doc} {dem_ban_doc} {ten_ban_doc}",
        "ngay_sinh": ngay_sinh,
        "gioi_tinh": random.choice(["Nam", "Nữ"]),
        "dia_chi": f"Số {random.randint(1, 200)}, {random.choice(['Phố', 'Đường'])} {random.choice(ten)}, Hà Nội",
        "so_dien_thoai": f"0{random.randint(300000000, 999999999)}"
    }

# Sinh dữ liệu mượn/trả sách
tracking = {}
current_date = datetime.now()

for i in range(1, 101):
    ma_ban_doc = f"R{str(random.randint(1, 100)).zfill(3)}"
    ma_sach = f"B{str(random.randint(1, 100)).zfill(3)}"
    
    # Ngày mượn là một ngày ngẫu nhiên trong 60 ngày trước
    days_ago = random.randint(0, 60)
    ngay_muon = (current_date - timedelta(days=days_ago)).strftime("%d/%m/%Y")
    
    # 70% sách đã trả, 20% đang mượn, 10% quá hạn
    status_random = random.random()
    if status_random < 0.7:  # Đã trả
        ngay_tra = (current_date - timedelta(days=random.randint(0, days_ago))).strftime("%d/%m/%Y")
        trang_thai = "Đã trả"
    elif status_random < 0.9:  # Đang mượn
        ngay_tra = "N/A"
        trang_thai = "Đang mượn"
    else:  # Quá hạn
        ngay_tra = "N/A"
        trang_thai = "Quá hạn"
    
    track_key = f"{ma_ban_doc}_{ma_sach}_{ngay_muon}"
    tracking[track_key] = {
        "ma_ban_doc": ma_ban_doc,
        "ma_sach_muon": ma_sach,
        "ten_sach_muon": books[ma_sach]["ten_sach"] if ma_sach in books else "Unknown",
        "ngay_muon": ngay_muon,
        "ngay_tra": ngay_tra,
        "trang_thai": trang_thai
    }

# Lưu dữ liệu vào file JSON
with open("data/books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)

with open("data/readers.json", "w", encoding="utf-8") as f:
    json.dump(readers, f, ensure_ascii=False, indent=4)

with open("data/tracking.json", "w", encoding="utf-8") as f:
    json.dump(tracking, f, ensure_ascii=False, indent=4)

print("Đã tạo thành công 100 dữ liệu mẫu cho mỗi loại!")
