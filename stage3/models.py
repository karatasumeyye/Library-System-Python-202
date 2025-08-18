from pydantic import BaseModel,Field

class ISBNIn(BaseModel):
    # İstemcinin POST /books ile yollayacağı gövde
    isbn: str = Field(..., min_length=10, max_length=17, description="ISBN-10/13; tire (-) içerebilir" )

class BookOut(BaseModel):
    # İstemciye döneceğimiz kitap modeli
    title: str
    author: str 
    isbn : str
