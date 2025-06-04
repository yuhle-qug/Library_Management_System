from models import Book
import data_handler # To access books_db
import ui # For get_input

def add_book():
    ui.clear_screen()
    print("\n--- Them Sach Moi ---")
    ma_sach = ui.get_input("Ma sach: ")
    if ma_sach in data_handler.books_db:
        print("Loi: Ma sach da ton tai.")
        return
    ten_sach = ui.get_input("Ten sach: ")
    tac_gia = ui.get_input("Tac gia: ")
    the_loai = ui.get_input("The loai: ")
    while True:
        try:
            so_luong_str = ui.get_input("So luong: ")
            so_luong = int(so_luong_str)
            if so_luong < 0: raise ValueError("So luong phai la so khong am.")
            break
        except ValueError as e:
            print(f"So luong khong hop le: {e}. Vui long nhap so nguyen.")
    tinh_trang = ui.get_input("Tinh trang (mac dinh 'Available'): ") or "Available"
    nha_xuat_ban = ui.get_input("Nha xuat ban: ")

    new_book = Book(ma_sach, ten_sach, tac_gia, the_loai, so_luong, tinh_trang, nha_xuat_ban)
    data_handler.books_db[ma_sach] = new_book
    print(f"Da them sach '{ten_sach}' thanh cong.")
    data_handler.save_data()  # Save changes to file

def update_book_info():
    ui.clear_screen()
    print("\n--- Cap Nhat Thong Tin Sach ---")
    ma_sach = ui.get_input("Nhap ma sach can cap nhat: ")
    if ma_sach not in data_handler.books_db:
        print(f"Loi: Khong tim thay sach voi ma '{ma_sach}'.")
        return

    book = data_handler.books_db[ma_sach]
    print(f"Thong tin hien tai: {book}")
    
    book.ten_sach = ui.get_input(f"Ten sach moi ({book.ten_sach}): ") or book.ten_sach
    book.tac_gia = ui.get_input(f"Tac gia moi ({book.tac_gia}): ") or book.tac_gia
    book.the_loai = ui.get_input(f"The loai moi ({book.the_loai}): ") or book.the_loai
    
    new_so_luong_str = ui.get_input(f"So luong moi ({book.so_luong}): ")
    if new_so_luong_str:
        try:
            new_so_luong = int(new_so_luong_str)
            if new_so_luong < 0: raise ValueError("So luong phai la so khong am.")
            book.so_luong = new_so_luong
        except ValueError as e:
            print(f"So luong khong hop le ({e}), khong thay doi so luong.")
            
    book.tinh_trang = ui.get_input(f"Tinh trang moi ({book.tinh_trang}): ") or book.tinh_trang
    book.nha_xuat_ban = ui.get_input(f"Nha xuat ban moi ({book.nha_xuat_ban}): ") or book.nha_xuat_ban
    
    print("Da cap nhat thong tin sach.")  # Save changes to file
    data_handler.save_data()  # Save changes to file

def search_book():
    ui.clear_screen()
    print("\n--- Tim Kiem Sach ---")
    search_term = ui.get_input("Nhap ten sach, tac gia, hoac ma sach de tim: ").lower()
    found_books = []
    for book in data_handler.books_db.values():
        if (search_term in book.ma_sach.lower() or
            search_term in book.ten_sach.lower() or
            search_term in book.tac_gia.lower()):
            found_books.append(book)

    if found_books:
        print("Sach tim thay:")
        for b in found_books:
            print(b)
    else:
        print("Khong tim thay sach nao phu hop.")

def check_book_quantity():
    ui.clear_screen()
    print("\n--- Kiem Tra So Luong Sach ---")
    if not data_handler.books_db:
        print("Trong kho chua co sach.")
        return
    print("So luong sach hien co:")
    for ma_sach, book in data_handler.books_db.items():
        print(f"- Ma: {book.ma_sach}, Ten: {book.ten_sach}, So luong: {book.so_luong}")