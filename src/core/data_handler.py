# data_handler.py
import json
from src.core.models import Book, Reader, TrackBook
from src.utils.custom_hash_table import HashTable
from src.utils.logger import logger

class DataHandler:
    def __init__(self):
        # Khởi tạo bằng HashTable thay vì dict
        self.HASH_TABLE_DEFAULT_SIZE = 100
        self.books_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)
        self.readers_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)
        self.tracking_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)

        # File names for data persistence
        self.BOOKS_FILE = "data/books.json"
        self.READERS_FILE = "data/readers.json"
        self.TRACKING_FILE = "data/tracking.json"

        # Load dữ liệu khi khởi tạo
        self.load_data()

    def save_data(self):
        try:
            # Chuyển HashTable thành dict để serialize JSON
            books_to_save = {key: book.to_dict() for key, book in self.books_db.items()}
            logger.debug(f"Dữ liệu sách được lưu: {books_to_save}")
            with open(self.BOOKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(books_to_save, f, indent=4, ensure_ascii=False)

            readers_to_save = {key: reader.to_dict() for key, reader in self.readers_db.items()}
            logger.debug(f"Dữ liệu bạn đọc được lưu: {readers_to_save}")
            with open(self.READERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(readers_to_save, f, indent=4, ensure_ascii=False)
            
            # Chuyển tracking_db thành list để serialize JSON
            tracking_to_save = [record.to_dict() for record in self.tracking_db.values()]
            logger.debug(f"Dữ liệu mượn/trả được lưu: {tracking_to_save}")
            with open(self.TRACKING_FILE, 'w', encoding='utf-8') as f:
                json.dump(tracking_to_save, f, indent=4, ensure_ascii=False)
            print("Du lieu da duoc luu.")
        except IOError as e:
            print(f"Loi khi luu du lieu: {e}")

    def load_data(self):
        self.books_db.clear() # Xóa dữ liệu cũ trước khi tải
        try:
            with open(self.BOOKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ma_sach, book_data in data.items():
                    logger.debug(f"Tải sách: {ma_sach} -> {book_data}")
                    self.books_db[ma_sach] = Book.from_dict(book_data)
                    logger.debug(f"Đã thêm sách vào books_db: {ma_sach}")
        except FileNotFoundError:
            print(f"File {self.BOOKS_FILE} khong tim thay, bat dau voi du lieu trong.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Loi khi tai {self.BOOKS_FILE}: {e}")

        self.readers_db.clear()
        try:
            with open(self.READERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ma_bd, reader_data in data.items():
                    self.readers_db[ma_bd] = Reader.from_dict(reader_data)
        except FileNotFoundError:
            print(f"File {self.READERS_FILE} khong tim thay, bat dau voi du lieu trong.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Loi khi tai {self.READERS_FILE}: {e}")

        self.tracking_db.clear()
        try:
            with open(self.TRACKING_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Xử lý dữ liệu dạng list
                for record_data in data:
                    # Tạo key từ thông tin của record
                    key = f"{record_data['ma_ban_doc']}_{record_data['ma_sach_muon']}_{record_data['ngay_muon']}"
                    self.tracking_db[key] = TrackBook.from_dict(record_data)
        except FileNotFoundError:
            print(f"File {self.TRACKING_FILE} khong tim thay, bat dau voi du lieu trong.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Loi khi tai {self.TRACKING_FILE}: {e}")

# Tạo một instance của DataHandler và export nó
data_handler = DataHandler()