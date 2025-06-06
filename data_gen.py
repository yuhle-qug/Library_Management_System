import json
import random
from faker import Faker

fake = Faker('vi_VN')

def generate_books(n):
    books = {}
    for i in range(1, n + 1):
        books[str(i)] = {
            "ma_sach": str(i),
            "ten_sach": fake.sentence(nb_words=4),
            "tac_gia": fake.name(),
            "the_loai": random.choice([
                "Khoa học", "Văn học", "Lịch sử", "Thiếu nhi", "Kinh tế", "Tâm lý", "Công nghệ", "Y học"
            ]),
            "so_luong": random.randint(1, 20),
            "tinh_trang": random.choice(["Mới", "Đã sử dụng"]),
            "nha_xuat_ban": fake.company()
        }
    return books

def generate_readers(n):
    readers = {}
    for i in range(1, n + 1):
        readers[str(i)] = {
            "ma_ban_doc": str(i),
            "ten": fake.name(),
            "ngay_sinh": fake.date_of_birth(minimum_age=10, maximum_age=70).strftime("%d/%m/%Y"),
            "gioi_tinh": random.choice(["Nam", "Nữ", "Khác"]),
            "dia_chi": fake.address().replace('\n', ', '),
            "so_dien_thoai": fake.phone_number()
        }
    return readers

def generate_tracking_records(n, books, readers):
    tracking_records = []
    for i in range(1, n + 1):
        book_id = random.choice(list(books.keys()))
        reader_id = random.choice(list(readers.keys()))
        tracking_records.append({
            "ma_ban_doc": reader_id,
            "ma_sach_muon": book_id,
            "ten_sach_muon": books[book_id]["ten_sach"],
            "ngay_muon": fake.date_between(start_date="-30d", end_date="today").strftime("%d/%m/%Y"),
            "ngay_tra": None,
            "trang_thai": random.choice(["Đang mượn", "Quá hạn"])
        })
    return tracking_records

if __name__ == "__main__":
    books = generate_books(10000)
    readers = generate_readers(5000)
    tracking_records = generate_tracking_records(30, books, readers)

    with open("Data/books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    with open("Data/readers.json", "w", encoding="utf-8") as f:
        json.dump(readers, f, ensure_ascii=False, indent=2)

    with open("Data/tracking.json", "w", encoding="utf-8") as f:
        json.dump(tracking_records, f, ensure_ascii=False, indent=2)