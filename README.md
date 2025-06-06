# Library Management System

Hệ thống quản lý thư viện với giao diện đồ họa hiện đại, được xây dựng bằng Python và Tkinter.

## Tính năng
- Quản lý sách (thêm, cập nhật, tìm kiếm, kiểm tra số lượng)
- Quản lý bạn đọc (thêm, cập nhật, tìm kiếm)
- Theo dõi mượn/trả sách
- Giám sát sách quá hạn
- Giao diện đồ họa hiện đại

## Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (trình quản lý gói Python)

## Cài đặt
1. Clone repository:
```bash
git clone <repository_url>
cd Library_Management_System
```

2. Tạo môi trường ảo:
```bash
python -m venv .venv
```

3. Kích hoạt môi trường ảo:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng
```bash
python main.py
```

## Cấu trúc dự án
Library_Management_System/
├── src/
│ ├── core/ # Chứa các class và xử lý dữ liệu cốt lõi
│ ├── gui/ # Chứa các thành phần giao diện
│ └── utils/ # Chứa các tiện ích
├── data/ # Thư mục chứa dữ liệu
├── assets/ # Thư mục chứa tài nguyên
├── logs/ # Thư mục chứa log
├── main.py # Điểm khởi đầu của ứng dụng
├── requirements.txt # Danh sách dependencies
└── README.md # Tài liệu hướng dẫn


## Hướng dẫn sử dụng
1. Quản lý sách:
   - Thêm sách mới
   - Cập nhật thông tin sách
   - Tìm kiếm sách
   - Kiểm tra số lượng sách

2. Quản lý bạn đọc:
   - Thêm bạn đọc mới
   - Cập nhật thông tin bạn đọc
   - Tìm kiếm bạn đọc

3. Mượn/Trả sách:
   - Mượn sách
   - Trả sách
   - Xem lịch sử mượn/trả
   - Kiểm tra sách quá hạn