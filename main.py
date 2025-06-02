import ui # For UI functions
import data_handler # For load/save and accessing dbs
import book_manager
import reader_manager
import tracking_manager

def handle_book_management():
    while True:
        ui.clear_screen()
        ui.display_book_menu()
        choice = ui.get_input()
        if choice == '1': book_manager.add_book()
        elif choice == '2': book_manager.update_book_info()
        elif choice == '3': book_manager.search_book()
        elif choice == '4': book_manager.check_book_quantity()
        elif choice == '0': break
        else: print("Lua chon khong hop le.")
        if choice != '0': ui.pause()

def handle_reader_management():
    while True:
        ui.clear_screen()
        ui.display_reader_menu()
        choice = ui.get_input()
        if choice == '1': reader_manager.add_reader()
        elif choice == '2': reader_manager.update_reader_info()
        elif choice == '3': reader_manager.search_reader()
        elif choice == '0': break
        else: print("Lua chon khong hop le.")
        if choice != '0': ui.pause()

def handle_tracking_management():
    while True:
        ui.clear_screen()
        ui.display_tracking_menu()
        choice = ui.get_input()
        if choice == '1': tracking_manager.borrow_book()
        elif choice == '2': tracking_manager.return_book()
        elif choice == '3': tracking_manager.view_borrow_return_history()
        elif choice == '4': tracking_manager.list_overdue_books()
        elif choice == '0': break
        else: print("Lua chon khong hop le.")
        if choice != '0': ui.pause()

if __name__ == "__main__":
    data_handler.load_data()
    
    while True:
        ui.clear_screen()
        ui.display_main_menu()
        main_choice = ui.get_input()

        if main_choice == '1':
            handle_book_management()
        elif main_choice == '2':
            handle_reader_management()
        elif main_choice == '3':
            handle_tracking_management()
        elif main_choice == '0':
            data_handler.save_data()
            print("Ket thuc chuong trinh. Da luu du lieu.")
            break
        else:
            print("Lua chon khong hop le. Vui long thu lai.")
            ui.pause()