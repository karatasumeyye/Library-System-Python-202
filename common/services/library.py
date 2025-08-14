from pathlib import Path
import json
from typing import List, Optional
from common.models.book import Book

class Library:

    def __init__(self, file_path: str = "coomon/data/library.json"):
        self.file_path = Path(file_path)
        self.books : List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """
        JSON dosyasını okuyup Book nesnelerine dönüştürür.
        Eğer dosya yoksa boş listeyle başlar.
        """

        if not self.file_path.exists():
            self.books = []
            return

        with self.file_path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.books = [Book.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.books = []


    def save_books(self) -> None :
        """
        Kitap listesini JSON dosyasına yazar.
        Pathlib ile klasörü otomatik oluşturur.
        """

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4, ensure_ascii=False)          


    def add_book(self, book: Book) -> None:
        """Yeni kitap ekler, ISBN zaten varsa hata verir."""
        if any(existing.isbn == book.isbn for existing in self.books):
            raise ValueError(f"ISBN {book.isbn} numaralı kitap zaten mevcut.")
        self.books.append(book)
        self.save_books()

    def remove_book(self, isbn: str) -> None:
        """ISBN'e göre kitabı siler, yoksa hata verir."""
        for existing in self.books:
            if existing.isbn == isbn:
                self.books.remove(existing)
                self.save_books()
                return
        raise ValueError(f"ISBN {isbn} numaralı kitap bulunamadı.")
    
    def list_books(self) -> List[Book]:
        return self.books
    
    def find_book(self, isbn: str) -> Optional[Book]:
        for book in self.books:
            if book.isbn == isbn :
                return book
            
        raise ValueError (f"ISBN {isbn} numaralı kitap bulunamadı.")



