from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# Ortak alanlar
class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    cover_url: Optional[str] = None

# CREATE için (id yok)
class BookCreate(BookBase):
    isbn: str
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    cover_url: Optional[str] = None

# UPDATE için (alanlar opsiyonel)
class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    cover_url: Optional[str] = None

# RESPONSE için
class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True



##### Member #####


class MemberBase(BaseModel):
    username: str
    email: EmailStr

class MemberCreate(MemberBase):
    password: str   

class MemberOut(MemberBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True    




# Borrow işlemleri için
class BorrowBase(BaseModel):
    member_id: int
    book_id: int

class BorrowCreate(BorrowBase):
    pass

class BorrowOut(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime]
    is_returned: bool

    class Config:
        from_attributes = True


# MemberBook işlemleri için
class MemberBookBase(BaseModel):
    book_id: int
    is_favorite: Optional[bool] = False
    is_read: Optional[bool] = False

class MemberBookCreate(MemberBookBase):
    pass

class MemberBookOut(BaseModel):
    id: int
    is_favorite: bool
    is_read: bool
    book: BookOut   #  ilişkili kitap bilgisi burada

    class Config:
        from_attributes = True