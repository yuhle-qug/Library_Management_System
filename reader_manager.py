from models import Reader
import data_handler # To access readers_db
import ui # For get_input

def add_reader():
    ui.clear_screen()
    print("\n--- Them Ban Doc Moi ---")
    ma_ban_doc = ui.get_input("Ma ban doc: ")
    if ma_ban_doc in data_handler.readers_db:
        print("Loi: Ma ban doc da ton tai.")
        return
    ten = ui.get_input("Ten ban doc: ")
    ngay_sinh = ui.get_input("Ngay sinh (DD/MM/YYYY): ")
    gioi_tinh = ui.get_input("Gioi tinh: ")
    dia_chi = ui.get_input("Dia chi: ")
    so_dien_thoai = ui.get_input("So dien thoai: ")

    new_reader = Reader(ma_ban_doc, ten, ngay_sinh, gioi_tinh, dia_chi, so_dien_thoai)
    data_handler.readers_db[ma_ban_doc] = new_reader
    print(f"Da them ban doc '{ten}' thanh cong.")

def update_reader_info():
    ui.clear_screen()
    print("\n--- Cap Nhat Thong Tin Ban Doc ---")
    ma_ban_doc = ui.get_input("Nhap ma ban doc can cap nhat: ")
    if ma_ban_doc not in data_handler.readers_db:
        print(f"Loi: Khong tim thay ban doc voi ma '{ma_ban_doc}'.")
        return

    reader = data_handler.readers_db[ma_ban_doc]
    print(f"Thong tin hien tai: {reader}")

    reader.ten = ui.get_input(f"Ten moi ({reader.ten}): ") or reader.ten
    reader.ngay_sinh = ui.get_input(f"Ngay sinh moi ({reader.ngay_sinh}): ") or reader.ngay_sinh
    reader.gioi_tinh = ui.get_input(f"Gioi tinh moi ({reader.gioi_tinh}): ") or reader.gioi_tinh
    reader.dia_chi = ui.get_input(f"Dia chi moi ({reader.dia_chi}): ") or reader.dia_chi
    reader.so_dien_thoai = ui.get_input(f"So dien thoai moi ({reader.so_dien_thoai}): ") or reader.so_dien_thoai
    
    print("Da cap nhat thong tin ban doc.")

def search_reader():
    ui.clear_screen()
    print("\n--- Tim Kiem Ban Doc ---")
    search_term = ui.get_input("Nhap ten ban doc, ma ban doc de tim: ").lower()
    found_readers = []
    for reader in data_handler.readers_db.values():
        if (search_term in reader.ma_ban_doc.lower() or
            search_term in reader.ten.lower()):
            found_readers.append(reader)

    if found_readers:
        print("Ban doc tim thay:")
        for r in found_readers:
            print(r)
    else:
        print("Khong tim thay ban doc nao phu hop.")