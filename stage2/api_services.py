import httpx
from common.models.book import Book
from common.services.library import Library

def get_book_data_from_isbn(isbn: str) -> dict:
    """Open Library API'den ISBN ile kitap bilgisi alır."""
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        response = httpx.get(url, follow_redirects=True, timeout=5.0)
        if response.status_code == 404:
            return None
        response.raise_for_status()

        data = response.json()
        title = data.get("title")
        authors_data = data.get("authors", [])
        authors = []

        # Yazar bilgilerini çek
        for author in authors_data:
            author_url = f"https://openlibrary.org{author['key']}.json"
            author_res = httpx.get(author_url, follow_redirects=True, timeout=5.0)
            if author_res.status_code == 200:
                author_name = author_res.json().get("name")
                if author_name:
                    authors.append(author_name)

        return {
            "title": title,
            "authors": ", ".join(authors) if authors else "Bilinmiyor",
            "isbn": isbn
        }

    except httpx.RequestError:
        print("Bağlantı hatası.")
        return None
    except Exception as e:
        print(f"Hata: {e}")
        return None
    

