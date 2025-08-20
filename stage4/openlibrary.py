import httpx
from datetime import datetime, date

def get_book_data_from_isbn(isbn: str) -> dict | None:
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

        for author in authors_data:
            author_url = f"https://openlibrary.org{author['key']}.json"
            author_res = httpx.get(author_url, follow_redirects=True, timeout=5.0)
            if author_res.status_code == 200:
                author_name = author_res.json().get("name")
                if author_name:
                    authors.append(author_name)

        return {
            "title": title,
            "author": ", ".join(authors) if authors else "Bilinmiyor",
            "publisher": data.get("publishers", [None])[0] if "publishers" in data else None,
            "page_count": data.get("number_of_pages"),
            "cover_url": f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg",
        }

    except Exception as e:
        print(f"Hata: {e}")
        return None