import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from stage4 import models
from stage4.database import get_db

# .env dosyasını yükle
load_dotenv()

# Güvenlik için ortam değişkenlerinden alınan değerler
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Şifreleme (hashing) ayarları
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -----------------------------------------------------
# Şifreleme Fonksiyonları
# -----------------------------------------------------


def hash_password(password: str) -> str:
    """
    Kullanıcının parolasını bcrypt algoritmasıyla hashler.
    Hashlenmiş değer veritabanında saklanır.
    """

    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    """
    Kullanıcının girdiği parolayı, veritabanında saklanan hash ile karşılaştırır.
    Doğruysa True, yanlışsa False döner.
    """

    return pwd_context.verify(plain_password, hashed_password)



# -----------------------------------------------------
# JWT Token Oluşturma
# -----------------------------------------------------


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Kullanıcıya JWT access token oluşturur.
    - data: Token içerisine gömülecek payload (ör. {"sub": email, "role": "member"})
    - expires_delta: Token geçerlilik süresi (belirtilmezse default kullanılır)
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




# -----------------------------------------------------
# Token Çözümleme ve Kullanıcı Doğrulama
# -----------------------------------------------------
# FastAPI'nin OAuth2PasswordBearer mekanizması ile login endpointini tanımlıyoruz
# Kullanıcı giriş yaptıktan sonra Authorization header'dan token gönderir.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_member(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    JWT token'ı çözümleyerek oturum açmış kullanıcıyı (member) döner.
    - Token doğrulanamazsa 401 hatası döner.
    - Kullanıcı veritabanında yoksa 401 hatası döner.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # Token içinden email alınır
        role: str = payload.get("role") # Token içinden rol alınır
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Veritabanında kullanıcı aranır
    member = db.query(models.Member).filter(models.Member.email == email).first()
    if member is None:
        raise credentials_exception
    return member


def get_current_admin(current_member: models.Member = Depends(get_current_member)):
    """
    Sadece admin rolüne sahip kullanıcıların erişebilmesi için kontrol yapar.
    - Eğer kullanıcı admin değilse 403 Forbidden döner.
    """
    
    if current_member.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_member