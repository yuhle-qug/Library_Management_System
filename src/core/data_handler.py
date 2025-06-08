# data_handler.py
import json
from src.core.models import Book, Reader, TrackBook
from src.utils.custom_hash_table import HashTable
from src.utils.logger import logger

class DataHandler:
    def __init__(self):
        """Khởi tạo DataHandler với các HashTable để lưu trữ dữ liệu"""
        self.HASH_TABLE_DEFAULT_SIZE = 100  # Kích thước mặc định của HashTable
        self.books_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)  # CSDL sách
        self.readers_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)  # CSDL bạn đọc
        self.tracking_db = HashTable(size=self.HASH_TABLE_DEFAULT_SIZE)  # CSDL theo dõi mượn sách

        # Đường dẫn file để lưu trữ dữ liệu
        self.BOOKS_FILE = "Data/books.json"
        self.READERS_FILE = "Data/readers.json"
        self.TRACKING_FILE = "Data/tracking.json"

        # Tải dữ liệu từ file khi khởi tạo
        self.load_data()

    def save_data(self):
        """Lưu dữ liệu vào các file JSON"""
        try:
            # Lưu dữ liệu sách
            books_to_save = {key: book.to_dict() for key, book in self.books_db.items()}
            with open(self.BOOKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(books_to_save, f, indent=4, ensure_ascii=False)

            # Lưu dữ liệu bạn đọc
            readers_to_save = {key: reader.to_dict() for key, reader in self.readers_db.items()}
            with open(self.READERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(readers_to_save, f, indent=4, ensure_ascii=False)

            # Lưu dữ liệu theo dõi mượn sách
            tracking_to_save = {key: record.to_dict() for key, record in self.tracking_db.items()}
            with open(self.TRACKING_FILE, 'w', encoding='utf-8') as f:
                json.dump(tracking_to_save, f, indent=4, ensure_ascii=False)

            logger.info("Đã lưu dữ liệu thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu dữ liệu: {e}")
            raise

    def load_data(self):
        """Tải dữ liệu từ các file JSON"""
        # Tải dữ liệu sách
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

        # Tải dữ liệu bạn đọc
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

        # Tải dữ liệu theo dõi mượn sách
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

    def count_borrowed_books(self, ma_sach):
        """Đếm số lượng sách đang được mượn với mã sách cụ thể"""
        count = 0
        for record in self.tracking_db.values():
            if record.ma_sach_muon == ma_sach and record.trang_thai in ("Đang mượn", "Quá hạn"):
                count += 1
        return count

# Tạo một instance của DataHandler
data_handler = DataHandler()
