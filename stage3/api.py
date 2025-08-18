from fastapi import FastAPI, Depends, HTTPException, status
from typing import List

# Proje kökünü import yoluna ekleyelim (kökten çalıştırmıyorsan önemli)
import sys, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# Ortak kodlar
from common.services.library import Library
from stage2.api_services import get_book_data_from_isbn
from stage3.models import ISBNIn, BookOut

app = FastAPI(title="Library API", version="1.0")

library = Library("common/data/library.json")

def get_library()->Library:
    """
    Dependency function:
    Endpoint'ler buradan aynı Library örneğini alır.
    """
    return library

@app.get("/books", response_model=List[BookOut], status_code=status.HTTP_200_OK)
def list_books(lib: Library = Depends(get_library)):
    """
    Kütüphanedeki tüm kitapları JSON olarak döndürür.
    """
    return [BookOut(title=b.title, author=b.author, isbn=b.isbn) for b in lib.list_books()]


@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(isbn_in: ISBNIn, lib: Library = Depends(get_library)):
    """
    Body: {"isbn": "..."} 
    - Open Library API (Stage 2) ile başlık & yazar çek
    - Zaten varsa 409 döndür
    - Başarılıysa eklenen kitabı döndür
    """
    # Duplicate kontrolü (Library.add_book_from_api doğrudan append yapıyorsa burada yakalıyoruz)
    if any(b.isbn == isbn_in.isbn for b in lib.list_books()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book already exists.")

    data = get_book_data_from_isbn(isbn_in.isbn)
    if not data:
        # Stage 2 fonksiyonu None döndüyse (404 ya da bağlantı sorunu),
        # kullanıcıya bulunamadı mesajı veriyoruz.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found by ISBN.")

    # Stage 2'de yazdığın yardımcı metotla ekle
    lib.add_book_from_api(data)
    # Response modeli BookOut ile eşleşsin diye alanları adlandır
    return BookOut(title=data["title"], author=data["authors"], isbn=data["isbn"])

@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(isbn: str, lib: Library = Depends(get_library)):
    """
    Param: /books/{isbn}
    - Varsa sil, yoksa 404 döndür
    """
    try:
        lib.remove_book(isbn)  # Library.remove_book yoksa ValueError atar
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    # 204 No Content: gövdede veri yok; return gerekmez