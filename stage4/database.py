from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Veritabanı bağlantı URL'si
# SQLite kullanıyoruz, dosya aynı dizinde olacak
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# Engine (bağlantı noktası)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM tabloları için Base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()