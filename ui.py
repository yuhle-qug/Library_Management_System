def clear_screen():
    # A simple way to "clear" for console.
    # For Windows: import os; os.system('cls')
    # For Linux/Mac: import os; os.system('clear')
    print("\n" * 30) # Print many newlines

def display_main_menu():
    print("\n=====================================")
    print("   HE THONG QUAN LY THU VIEN (PYTHON)")
    print("=====================================")
    print("1. Quan ly Sach")
    print("2. Quan ly Ban Doc")
    print("3. Theo doi Muon/Tra Sach")
    print("0. Thoat va Luu")
    print("-------------------------------------")

def display_book_menu():
    print("\n--- Quan Ly Sach ---")
    print("1. Them sach moi")
    print("2. Cap nhat thong tin sach")
    print("3. Tim kiem sach")
    print("4. Kiem tra so luong sach")
    print("0. Quay lai Menu chinh")

def display_reader_menu():
    print("\n--- Quan Ly Ban Doc ---")
    print("1. Them ban doc moi")
    print("2. Cap nhat thong tin ban doc")
    print("3. Tim kiem ban doc")
    print("0. Quay lai Menu chinh")

def display_tracking_menu():
    print("\n--- Theo doi Muon/Tra Sach ---")
    print("1. Muon sach")
    print("2. Tra sach")
    print("3. Xem lich su muon/tra cua ban doc")
    print("4. Liet ke sach muon qua han")
    print("0. Quay lai Menu chinh")

def get_input(prompt_message="Nhap lua chon cua ban: "):
    return input(prompt_message).strip()

def pause():
    input("Nhan Enter de tiep tuc...")