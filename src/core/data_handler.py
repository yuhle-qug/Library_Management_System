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
        self.BOOKS_FILE = "Data/books.json"
        self.READERS_FILE = "Data/readers.json"
        self.TRACKING_FILE = "Data/tracking.json"

        # Load dữ liệu khi khởi tạo
        self.load_data()

    def save_data(self):
        """Lưu dữ liệu vào các file JSON"""
        try:
            # Chuyển HashTable thành dict để serialize JSON
            books_to_save = {key: book.to_dict() for key, book in self.books_db.items()}
            with open(self.BOOKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(books_to_save, f, indent=4, ensure_ascii=False)

            readers_to_save = {key: reader.to_dict() for key, reader in self.readers_db.items()}
            with open(self.READERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(readers_to_save, f, indent=4, ensure_ascii=False)
            
            # Chuyển tracking_db thành dictionary để serialize JSON
            tracking_to_save = {key: record.to_dict() for key, record in self.tracking_db.items()}
            with open(self.TRACKING_FILE, 'w', encoding='utf-8') as f:
                json.dump(tracking_to_save, f, indent=4, ensure_ascii=False)

            logger.info("Đã lưu dữ liệu thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            raise

    def load_data(self):
        """Tải dữ liệu từ các file JSON"""
        # Load books
        self.books_db.clear()
        try:
            with open(self.BOOKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ma_sach, book_data in data.items():
                    self.books_db[ma_sach] = Book.from_dict(book_data)
        except FileNotFoundError:
            logger.warning(f"File {self.BOOKS_FILE} không tìm thấy")
        except Exception as e:
            logger.error(f"Lỗi khi tải {self.BOOKS_FILE}: {e}")
            raise

        # Load readers
        self.readers_db.clear()
        try:
            with open(self.READERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for ma_bd, reader_data in data.items():
                    self.readers_db[ma_bd] = Reader.from_dict(reader_data)
        except FileNotFoundError:
            logger.warning(f"File {self.READERS_FILE} không tìm thấy")
        except Exception as e:
            logger.error(f"Lỗi khi tải {self.READERS_FILE}: {e}")
            raise

        # Load tracking data
        self.tracking_db.clear()
        try:
            with open(self.TRACKING_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, record_data in data.items():
                    self.tracking_db[key] = TrackBook.from_dict(record_data)
        except FileNotFoundError:
            logger.warning(f"File {self.TRACKING_FILE} không tìm thấy")
        except Exception as e:
            logger.error(f"Lỗi khi tải {self.TRACKING_FILE}: {e}")
            raise

    def is_book_borrowed(self, ma_sach):
        """Kiểm tra xem sách có đang được mượn không"""
        for record in self.tracking_db.values():
            if record.ma_sach_muon == ma_sach and record.trang_thai in ("Đang mượn", "Quá hạn"):
                return True
        return False

    def is_reader_borrowing(self, ma_ban_doc):
        """Kiểm tra xem bạn đọc có đang mượn sách nào không"""
        for record in self.tracking_db.values():
            if record.ma_ban_doc == ma_ban_doc and record.trang_thai in ("Đang mượn", "Quá hạn"):
                return True
        return False

    def delete_book(self, ma_sach):
        """Xóa sách khỏi CSDL"""
        del self.books_db[ma_sach]
        self.save_data()

    def delete_reader(self, ma_ban_doc):
        """Xóa bạn đọc khỏi CSDL"""
        del self.readers_db[ma_ban_doc]
        self.save_data()

# Tạo một instance của DataHandler
data_handler = DataHandler()
