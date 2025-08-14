from dataclasses import dataclass, field
import re
from datetime import datetime

@dataclass(frozen=True)
class Book:
    """
    Bir kitabı temsil eden veri modeli.
    
    @dataclass: __init__, __repr__, __eq__ gibi metotları otomatik oluşturur.
    frozen=True: Nesne immutable olur (sonradan değiştirilemez).
    """

    title: str
    author: str
    isbn: str
    added_at: datetime= field(default_factory=datetime.now)

    # def __post_init__(self):
         
    #     """
    #     __post_init__: __init__ tamamlandıktan sonra ek kontroller yapar.
    #     Burada ISBN formatını kontrol edeceğiz.
    #     """
         
    #     if not re.match(r"^[0-9\-]{10,17}$", self.isbn):
    #         raise ValueError(f"Geçersiz ISBN formatı : {self.isbn}")
        
    def __str__(self) -> str:

        """
        print(book) çağrıldığında çalışır.
        Daha okunabilir bir temsil döndürür.
        """
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    @property
    def short_title(self) -> str :

        """
        property: Metod gibi çağrılır ama değişken gibi kullanılır.
        Kitap adını kısaltarak verir (ör: uzun başlıklar için).
        """
        return (self.title[:27] + "..." if len(self.title)>30 else self.title)
    
    @classmethod
    def from_dict(cls,data:dict) -> "Book":
        """
        classmethod: Sınıfın kendisini (cls) kullanarak nesne oluşturur.
        JSON/dict verisinden Book nesnesi üretmek için kullanılır.
        """

        return cls(
            title = data["title"],
            author = data["author"],
            isbn=data["isbn"],
            added_at=datetime.fromisoformat(data["added_at"]) if "added_at" in data else datetime.now()
        )
    
    def to_dict(self) -> dict:
        """
        Nesneyi JSON'a yazmak için dict formatına çevirir.
        datetime nesneleri string'e dönüştürülür.
        """

        return {
             "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "added_at": self.added_at.isoformat()
        }