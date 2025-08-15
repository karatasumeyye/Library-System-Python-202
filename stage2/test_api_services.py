import sys
import os
import pytest

# Üst dizindeki dosyalara erişebilmek için Python'un arama yoluna ekliyoruz
# Böylece stage2/api_services.py içindeki fonksiyona import ile ulaşabiliriz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from stage2.api_services import get_book_data_from_isbn


# ==============================================
#  MockResponse: httpx.Response nesnesini taklit eder
# ==============================================
class MockResponse:
    def __init__(self, json_data, status_code=200):
        # Döndürülecek JSON verisi
        self._json_data = json_data
        # HTTP durum kodu (200 OK, 404 Not Found vb.)
        self.status_code = status_code
    
    def json(self):
        """Gerçek response.json() gibi çalışır"""
        return self._json_data

    def raise_for_status(self):
        """
        Gerçek httpx.Response.raise_for_status() davranışını taklit eder.
        Eğer status_code >= 400 ise hata fırlatır.
        """
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code} Hatası")


# ==============================================
#  Mock Fonksiyonlar
# ==============================================

def mock_httpx_get_success(url, **kwargs):
    """
    Geçerli ISBN verilirse hem kitap hem de yazar bilgisi döner.
    Fonksiyon URL'ye göre farklı sahte cevap döndürür.
    """
    if "isbn" in url:
        # Kitap bilgisi
        return MockResponse({
            "title": "The Lord of the Rings",
            "authors": [{"key": "/authors/OL26320A"}]  # Yazar bilgisi URL'si
        })
    elif "/authors/" in url:
        # Yazar bilgisi
        return MockResponse({"name": "J.R.R. Tolkien"})
    
    # Başka bir URL gelirse 404 döndür
    return MockResponse({}, status_code=404)


def mock_httpx_get_not_found(url, **kwargs):
    """
    Geçersiz ISBN durumunu simüle eder.
    Direkt boş veri ve 404 döner.
    """
    return MockResponse({}, status_code=404)


# ==============================================
#  Test Senaryoları
# ==============================================

def test_get_book_data_from_isbn_success(monkeypatch):
    """
     Geçerli ISBN verildiğinde:
    - Doğru başlık dönmeli
    - Doğru yazar dönmeli
    - ISBN bilgisi korunmalı
    """
    # httpx.get fonksiyonunu sahte versiyon ile değiştiriyoruz
    monkeypatch.setattr("httpx.get", mock_httpx_get_success)
    
    # Fonksiyonu çağır
    result = get_book_data_from_isbn("9780261103573")
    
    # Beklenen değerleri doğrula
    assert result["title"] == "The Lord of the Rings"
    assert result["authors"] == "J.R.R. Tolkien"
    assert result["isbn"] == "9780261103573"


def test_get_book_data_from_isbn_not_found(monkeypatch):
    """
      Geçersiz ISBN verildiğinde:
    - Fonksiyon None dönmeli
    """
    monkeypatch.setattr("httpx.get", mock_httpx_get_not_found)
    
    result = get_book_data_from_isbn("invalid_isbn")
    
    assert result is None
