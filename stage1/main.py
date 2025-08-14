import sys
from pathlib import Path

# Proje kök dizinini sys.path'e ekle
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))


from common.models.book import Book
from common.services.library import Library


def main():
    library = Library("common/data/library.json")

    while True:
        print("\n Kütüphane Yönetim Sistemi")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        secim = input("Seçiminiz: ").strip()

        try:
            if secim == "1":
                title = input("Kitap adı: ")
                author = input("Yazar: ")
                isbn = input("ISBN: ")
                book = Book(title=title, author=author, isbn=isbn)
                library.add_book(book)
                print(" Kitap eklendi.")

            elif secim == "2":
                isbn = input("Silinecek ISBN: ")
                library.remove_book(isbn)
                print(" Kitap silindi.")

            elif secim == "3":
                books = library.list_books()
                if books:
                    for book in books:
                        print(book)
                else:
                    print(" Kütüphane boş.")

            elif secim == "4":
                isbn = input("Aranan ISBN: ")
                book = library.find_book(isbn)
                print(book)

            elif secim == "5":
                print(" Çıkış yapılıyor...")
                break

            else:
                print("⚠️ Geçersiz seçim.")

        except ValueError as e:
            print(f" Hata: {e}")

if __name__ == "__main__":
    main()