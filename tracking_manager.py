import datetime
from models import TrackBook
import data_handler # To access all dbs and tracking_records
import ui # For get_input

def borrow_book():
    ui.clear_screen()
    print("\n--- Muon Sach ---")
    ma_ban_doc = ui.get_input("Nhap ma ban doc: ")
    if ma_ban_doc not in data_handler.readers_db:
        print("Loi: Ban doc khong ton tai.")
        return

    ma_sach = ui.get_input("Nhap ma sach muon muon: ")
    if ma_sach not in data_handler.books_db:
        print("Loi: Sach khong ton tai.")
        return

    book_to_borrow = data_handler.books_db[ma_sach]
    if book_to_borrow.so_luong <= 0:
        print("Loi: Sach da het hoac khong con du trong kho.")
        return

    # Check if already borrowed and not returned
    for record in data_handler.tracking_records:
        if record.ma_ban_doc == ma_ban_doc and record.ma_sach_muon == ma_sach and record.trang_thai == "Borrowed":
            print(f"Loi: Ban doc '{data_handler.readers_db[ma_ban_doc].ten}' da muon sach '{book_to_borrow.ten_sach}' va chua tra.")
            return
            
    book_to_borrow.so_luong -= 1
    # Consider updating book_to_borrow.tinh_trang if necessary
    
    ngay_muon_dt = datetime.date.today()
    ngay_muon_str = ngay_muon_dt.strftime("%d/%m/%Y")
    
    new_tracking_record = TrackBook(
        ma_ban_doc, 
        ma_sach, 
        book_to_borrow.ten_sach, 
        ngay_muon_str
    )
    data_handler.tracking_records.append(new_tracking_record)
    print(f"Ban doc '{data_handler.readers_db[ma_ban_doc].ten}' da muon sach '{book_to_borrow.ten_sach}' vao ngay {ngay_muon_str}.")

def return_book():
    ui.clear_screen()
    print("\n--- Tra Sach ---")
    ma_ban_doc = ui.get_input("Nhap ma ban doc tra sach: ")
    if ma_ban_doc not in data_handler.readers_db:
        print(f"Loi: Khong tim thay ban doc voi ma '{ma_ban_doc}'.")
        return
        
    ma_sach = ui.get_input("Nhap ma sach duoc tra: ")
    if ma_sach not in data_handler.books_db:
        print(f"Loi: Khong tim thay sach voi ma '{ma_sach}' trong he thong.")
        # Even if book was deleted, we might still want to process return from tracking
        # but for now, let's assume book must exist.

    found_record_idx = -1
    for idx, record in enumerate(data_handler.tracking_records):
        if record.ma_ban_doc == ma_ban_doc and \
           record.ma_sach_muon == ma_sach and \
           record.trang_thai == "Borrowed":
            found_record_idx = idx
            break
    
    if found_record_idx == -1:
        print("Loi: Khong tim thay lich su muon sach phu hop (dang muon) cho ban doc va sach nay.")
        return

    # Update book quantity
    if ma_sach in data_handler.books_db:
        data_handler.books_db[ma_sach].so_luong += 1
    
    # Update tracking record
    ngay_tra_dt = datetime.date.today()
    ngay_tra_str = ngay_tra_dt.strftime("%d/%m/%Y")
    data_handler.tracking_records[found_record_idx].ngay_tra = ngay_tra_str
    data_handler.tracking_records[found_record_idx].trang_thai = "Returned"
    
    print(f"Sach '{data_handler.tracking_records[found_record_idx].ten_sach_muon}' da duoc tra boi ban doc '{data_handler.readers_db[ma_ban_doc].ten}' vao ngay {ngay_tra_str}.")


def view_borrow_return_history():
    ui.clear_screen()
    print("\n--- Lich Su Muon/Tra Sach cua Ban Doc ---")
    ma_ban_doc = ui.get_input("Nhap ma ban doc de xem lich su: ")
    if ma_ban_doc not in data_handler.readers_db:
        print("Loi: Ban doc khong ton tai.")
        return
    
    print(f"Lich su cho ban doc: {data_handler.readers_db[ma_ban_doc].ten} (Ma: {ma_ban_doc})")
    found = False
    for record in data_handler.tracking_records:
        if record.ma_ban_doc == ma_ban_doc:
            print(f"- Sach: {record.ten_sach_muon} (Ma: {record.ma_sach_muon}), Ngay muon: {record.ngay_muon}, "
                  f"Ngay tra: {record.ngay_tra if record.ngay_tra else 'Chua tra'}, Trang thai: {record.trang_thai}")
            found = True
    if not found:
        print("Khong co lich su muon/tra nao.")

def list_overdue_books():
    ui.clear_screen()
    print("\n--- Danh Sach Muon Sach Qua Han ---")
    try:
        due_days_limit_str = ui.get_input("Nhap so ngay toi da duoc muon (vi du: 14): ")
        due_days_limit_int = int(due_days_limit_str)
        if due_days_limit_int <=0:
            print("So ngay phai la so duong.")
            return
    except ValueError:
        print("So ngay khong hop le.")
        return

    today = datetime.date.today()
    due_delta = datetime.timedelta(days=due_days_limit_int)
    found_overdue = False

    print(f"Cac sach muon qua {due_days_limit_int} ngay (tinh den {today.strftime('%d/%m/%Y')}):")
    for record in data_handler.tracking_records:
        if record.trang_thai == "Borrowed":
            try:
                ngay_muon_dt = datetime.datetime.strptime(record.ngay_muon, "%d/%m/%Y").date()
                if today - ngay_muon_dt > due_delta:
                    reader_name = data_handler.readers_db.get(record.ma_ban_doc, None)
                    reader_info = f"{reader_name.ten} (Ma: {record.ma_ban_doc})" if reader_name else f"Ma ban doc: {record.ma_ban_doc}"
                    print(f"- QUA HAN: Sach '{record.ten_sach_muon}' (Ma: {record.ma_sach_muon}), "
                          f"Muon boi: {reader_info}, Ngay muon: {record.ngay_muon}")
                    found_overdue = True
            except ValueError:
                print(f"Loi dinh dang ngay muon cho record: {record.ma_sach_muon} cua ban doc {record.ma_ban_doc}")
    
    if not found_overdue:
        print("Khong co sach nao bi muon qua han.")