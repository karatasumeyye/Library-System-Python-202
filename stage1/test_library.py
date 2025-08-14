import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.models.book import Book
from common.services.library import Library


@pytest.fixture
def library(tmp_path):
    test_file = tmp_path / "test_library.json"
    test_file.write_text("[]")
    return Library(str(test_file))


def test_add_book(library):
    book = Book(title="Test Book", author="Test Author", isbn="12345")
    library.add_book(book)
    assert len(library.books) == 1
    assert library.books[0].title == "Test Book"


def test_remove_book(library):
    book = Book(title="Delete Me", author="Author", isbn="999")
    library.add_book(book)
    library.remove_book("999")  # hata atmamalı
    assert all(b.isbn != "999" for b in library.books)


def test_remove_book_not_found(library):
    with pytest.raises(ValueError) as excinfo:
        library.remove_book("not-found")
    assert "bulunamadı" in str(excinfo.value)


def test_list_books(library):
    book1 = Book(title="Book 1", author="Author 1", isbn="111")
    book2 = Book(title="Book 2", author="Author 2", isbn="222")
    library.add_book(book1)
    library.add_book(book2)
    books = library.list_books()
    assert len(books) == 2
    assert books[0].title == "Book 1"
    assert books[1].isbn == "222"


def test_find_book(library):
    book = Book(title="Search Me", author="Author", isbn="333")
    library.add_book(book)
    found = library.find_book("333")  # ISBN ile arıyoruz
    assert found is not None
    assert found.title == "Search Me"
