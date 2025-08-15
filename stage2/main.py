import sys
from pathlib import Path

# Proje kök dizinini sys.path'e ekle
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from stage2.api_services import get_book_data_from_isbn
from common.services.library import Library

lib = Library()
isbn = input("ISBN girin: ")
book_data = get_book_data_from_isbn(isbn)
lib.add_book_from_api(book_data)
