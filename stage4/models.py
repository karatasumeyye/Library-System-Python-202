from sqlalchemy import Boolean
from sqlalchemy import Column, ForeignKey, String, Integer, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from stage4.database import Base

# Kitap tablosu
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  # otomatik id
    isbn = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    # Yeni alanlar
    publisher = Column(String, nullable=True)       # Yayıncı
    page_count = Column(Integer, nullable=True)     # Sayfa sayısı
    cover_url = Column(String, nullable=True)       # Kapak resmi


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)  # otomatik id
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hash olarak tutulacak
    role = Column(String, default="member")  # "member" veya "admin"
    created_at = Column(DateTime, default=datetime.utcnow)



class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)

    member = relationship("Member", backref="borrows")
    book = relationship("Book")


class MemberBook(Base):
    __tablename__ = "member_books"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    is_favorite = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    

    member = relationship("Member", backref="member_books")
    book = relationship("Book", backref="member_books")    