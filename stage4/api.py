from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from stage4.database import get_db
from stage4 import crud, schemas
from stage4.auth import verify_password, create_access_token, get_current_member,get_current_admin
from datetime import timedelta
from stage4 import models



router = APIRouter()


# ---------- BOOK ENDPOINTLERİ ----------
@router.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/books/", response_model=list[schemas.BookOut])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)

@router.get("/books/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id, book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


# ---------- AUTH ENDPOINTLERİ ----------
@router.post("/auth/register", response_model=schemas.MemberOut, tags=["auth"])
def register(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.get_member_by_email(db, member.email)
    if db_member:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_member(db, member)

@router.post("/auth/login", tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_member_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email, "role": user.role}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=schemas.MemberOut, tags=["auth"])
def read_users_me(current_member: models.Member = Depends(get_current_member)):
    return current_member


# ---------- BORROW ENDPOINTLERİ ----------

@router.post("/borrows/", response_model=schemas.BorrowOut, tags=["borrows"])
def give_book(
    borrow: schemas.BorrowCreate,
    db: Session = Depends(get_db),
    current_admin: models.Member = Depends(get_current_admin)  # ✅ sadece admin verebilir
):
    return crud.create_borrow(db, borrow)


@router.put("/borrows/{borrow_id}/return", response_model=schemas.BorrowOut, tags=["borrows"])
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Member = Depends(get_current_admin)  #  sadece admin alabilir
):
    db_borrow = crud.return_borrow(db, borrow_id)
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    return db_borrow


@router.get("/borrows/me", response_model=list[schemas.BorrowOut], tags=["borrows"])
def my_borrows(
    current_member: models.Member = Depends(get_current_member),  #  üye kendi borrows’unu görebilir
    db: Session = Depends(get_db)
):
    return crud.get_member_borrows(db, current_member.id)


@router.get("/borrows/", response_model=list[schemas.BorrowOut], tags=["borrows"])
def list_all_borrows(
    db: Session = Depends(get_db),
    current_admin: models.Member = Depends(get_current_admin)  # sadece admin tüm listeyi görebilir
):
    return crud.get_all_borrows(db)






# ---------- MEMBERBOOK ENDPOINTLERİ ----------

#  Favori veya Okunan ekle
@router.post("/memberbooks/", response_model=schemas.MemberBookOut, tags=["memberbooks"])
def add_member_book(
    item: schemas.MemberBookCreate,
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_member)
):
    return crud.add_member_book(
        db,
        member_id=current_member.id,
        book_id=item.book_id,
        is_favorite=item.is_favorite,
        is_read=item.is_read,
    )


#  Favori veya Okunan listeden çıkar
@router.delete("/memberbooks/{book_id}", response_model=schemas.MemberBookOut, tags=["memberbooks"])
def remove_member_book(
    book_id: int,
    is_favorite: bool = False,
    is_read: bool = False,
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_member)
):
    db_item = crud.remove_member_book(
        db,
        member_id=current_member.id,
        book_id=book_id,
        is_favorite=is_favorite,
        is_read=is_read,
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

#  Favorileri listele
@router.get("/memberbooks/favorites", response_model=list[schemas.MemberBookOut], tags=["memberbooks"])
def list_favorites(
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_member)
):
    return crud.get_favorites(db, current_member.id)


#  Okunanları listele
@router.get("/memberbooks/read", response_model=list[schemas.MemberBookOut], tags=["memberbooks"])
def list_read_books(
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_member)
):
    return crud.get_read_books(db, current_member.id)