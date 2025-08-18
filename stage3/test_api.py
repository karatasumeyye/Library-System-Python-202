import sys
import os
import pytest

# Üst dizindeki dosyalara erişebilmek için Python'un arama yoluna ekliyoruz
# Böylece stage2/api_services.py içindeki fonksiyona import ile ulaşabiliriz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from fastapi.testclient import TestClient

# api modülünü import et (içindeki 'app' ve 'library'yi kullanacağız)
from stage3 import api
from common.services.library import Library

client = TestClient(api.app)

def test_get_books_initially_empty(monkeypatch, tmp_path):
    # Test sırasında kalıcı dosyayı etkilememek için yeni Library örneği ver
    monkeypatch.setattr(api, "library", Library(str(tmp_path / "lib.json")))

    r = client.get("/books")
    assert r.status_code == 200
    assert r.json() == []

def test_add_book_invalid_isbn(monkeypatch, tmp_path):
    # Geçici Library
    monkeypatch.setattr(api, "library", Library(str(tmp_path / "lib.json")))

    # Stage2 fonksiyonunu "bulunamadı" dönecek şekilde sahtele
    def fake_get_book_data(isbn: str):
        return None
    monkeypatch.setattr(api, "get_book_data_from_isbn", fake_get_book_data)

    r = client.post("/books", json={"isbn": "0000000000"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Book not found by ISBN."

def test_add_and_delete_book_success(monkeypatch, tmp_path):
    # Geçici Library
    monkeypatch.setattr(api, "library", Library(str(tmp_path / "lib.json")))

    # Başarılı kitap verisi döndür
    def fake_get_book_data(isbn: str):
        return {"title": "Test Title", "authors": "Test Author", "isbn": isbn}
    monkeypatch.setattr(api, "get_book_data_from_isbn", fake_get_book_data)

    # EKLE
    r = client.post("/books", json={"isbn": "1234567890"})
    assert r.status_code == 201
    assert r.json()["title"] == "Test Title"

    # LİSTE
    r = client.get("/books")
    assert r.status_code == 200
    assert any(b["isbn"] == "1234567890" for b in r.json())

    # TEKRAR EKLE (duplicate → 409)
    r = client.post("/books", json={"isbn": "1234567890"})
    assert r.status_code == 409

    # SİL
    r = client.delete("/books/1234567890")
    assert r.status_code == 204

    # SİLDİKTEN SONRA LİSTE
    r = client.get("/books")
    assert all(b["isbn"] != "1234567890" for b in r.json())
