from datetime import datetime
from sqlalchemy.orm import Session
from stage4.models import Book
from stage4.schemas import BookCreate, BookUpdate
from stage4.auth import hash_password
from stage4 import models, schemas
from stage4.openlibrary import get_book_data_from_isbn

def create_book(db: Session, book: BookCreate):
    api_data = get_book_data_from_isbn(book.isbn)

    db_book = models.Book(
        isbn=book.isbn,
        title=book.title or (api_data.get("title") if api_data else "Bilinmeyen Başlık"),
        author=book.author or (api_data.get("author") if api_data else "Bilinmeyen Yazar"),
        publisher=book.publisher or (api_data.get("publisher") if api_data else None),
        page_count=book.page_count or (api_data.get("page_count") if api_data else None),
        cover_url=book.cover_url or (api_data.get("cover_url") if api_data else None),
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book




# Member CRUD operations
def get_member_by_email(db: Session, email: str):
    return db.query(models.Member).filter(models.Member.email == email).first()

def create_member(db: Session, member: schemas.MemberCreate):
    hashed_pw = hash_password(member.password)
    db_member = models.Member(username=member.username, email=member.email, password=hashed_pw)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member



# Borrow CRUD operations

def create_borrow(db: Session, borrow: schemas.BorrowCreate):
    db_borrow = models.Borrow(**borrow.dict())
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

def return_borrow(db: Session, borrow_id: int):
    db_borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if db_borrow:
        db_borrow.is_returned = True
        db_borrow.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_borrow)
    return db_borrow

def get_member_borrows(db: Session, member_id: int):
    return db.query(models.Borrow).filter(models.Borrow.member_id == member_id).all()

def get_all_borrows(db: Session):
    return db.query(models.Borrow).all()





# ---------- FAVORİ / OKUNAN EKLE ----------
def add_member_book(db: Session, member_id: int, book_id: int, is_favorite=False, is_read=False):
    db_item = models.MemberBook(
        member_id=member_id,
        book_id=book_id,
        is_favorite=is_favorite,
        is_read=is_read,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ---------- FAVORİ / OKUNAN KALDIR ----------
def remove_member_book(db: Session, member_id: int, book_id: int, is_favorite=False, is_read=False):
    db_item = (
        db.query(models.MemberBook)
        .filter(
            models.MemberBook.member_id == member_id,
            models.MemberBook.book_id == book_id,
            models.MemberBook.is_favorite == is_favorite,
            models.MemberBook.is_read == is_read,
        )
        .first()
    )
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None


# ---------- FAVORİLERİ GETİR ----------
def get_favorites(db: Session, member_id: int):
    return (
        db.query(models.MemberBook)
        .filter(
            models.MemberBook.member_id == member_id,
            models.MemberBook.is_favorite == True,
        )
        .all()
    )


# ---------- OKUNANLARI GETİR ----------
def get_read_books(db: Session, member_id: int):
    return (
        db.query(models.MemberBook)
        .filter(
            models.MemberBook.member_id == member_id,
            models.MemberBook.is_read == True,
        )
        .all()
    )
