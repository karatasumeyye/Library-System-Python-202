# Library System - Python 202

Bu proje; kütüphane envanterini (kitap ekleme/listeleme/güncelleme/silme) ve ödünç alma–iade süreçlerini yönetmek için **çok-aşamalı** bir yapı sunar.

- **Aşama 1–2 (Terminal):** JSON dosyası üzerinde çalışan konsol uygulaması (temel CRUD).
- **Aşama 3 (API – JSON):** FastAPI ile REST uç noktaları; veri kaynağı JSON dosyalarıdır.
- **Aşama 4 (API – Veritabanı):** FastAPI + SQLAlchemy (kalıcı DB, varsayılan: SQLite). Üretime daha yakın bir katmanlı mimari kullanır.

## **📁 Dizin Yapısı**

Library System-Python 202/
├─ common/
│ ├─ data/
│ │ └─ library.json # JSON veri kaynağı (Stage 1–3 tarafından kullanılır)
│ ├─ models/
│ │ └─ [book.py](http://book.py/) # Ortak domain modeli (örn. Book)
│ └─ services/
│ └─ [library.py](http://library.py/) # Ortak servisler/işlevler
├─ stage1/
│ ├─ [main.py](http://main.py/) # Aşama 1 – Terminal uygulaması
│ └─ test_library.py # Aşama 1 testleri
├─ stage2/
│ ├─ [main.py](http://main.py/) # Aşama 2 – Terminal uygulaması (gelişmiş)
│ ├─ api_services.py # Servis katmanı
│ └─ test_api_services.py # Aşama 2 testleri
├─ stage3/
│ ├─ [api.py](http://api.py/) # FastAPI uygulaması (JSON veri kaynağı)
│ ├─ [models.py](http://models.py/) # Pydantic/yardımcı modeller
│ └─ test_api.py # Aşama 3 testleri
├─ stage4/

│ ├─ [api.py](http://main.py/) 
│ ├─ auth[.py](http://database.py/)  # 

│ ├─ [crud.py](http://crud.py/) # Veri erişim/iş mantığı

│ ├─ [database.py](http://database.py/) # SQLAlchemy engine/session
│ ├─ [main.py](http://main.py/) # FastAPI uygulaması (SQLAlchemy DB)
│ ├─ [models.py](http://models.py/) # Veritabanı modelleri (Book, Borrow, ...)

│ ├─ openlibrary[.py](http://schemas.py/) 
│ ├─ [schemas.py](http://schemas.py/) # Pydantic şemaları

│ └─ routers/ # (Varsa) modüler endpointler
├─ requirements.txt
├─ .env.example # Örnek ortam değişkenleri
├─ .env # Gerçek ortam değişkenleri (git'e eklenmez)
└─ [README.md](http://readme.md/)

- Stage 1–3 klasörlerinde test dosyaları (`test_*.py`) bulunur, böylece her aşamadaki fonksiyonellik bağımsız test edilebilir.
- `common/` klasörü; **veri**, **model** ve **servis** kodlarının aşamalar arasında paylaşılmasını sağlar.

## 🔧 Kurulum

## **1) Depoyu klonla**

```jsx
# HTTPS
git clone https://github.com/<kullanici>/<repo-adi>.git
cd "Library System-Python 202" # ya da repo klasör adın
```

## 2) Sanal ortam ve bağımlılıklar (standart `venv` + `pip`)

```jsx
# Windows (PowerShell)
py -m venv .venv
. .venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Ortak: bağımlılıkları kurun
pip install -r requirements.txt
```

### 2-b) Sanal ortam ve bağımlılıklar **(uv ile – hızlı kurulum)**

`uv` (Astral) kullanıyorsanız sanal ortamı ve paketleri tek araçla yönetebilirsiniz.

### Kurulum

```jsx
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

### Sanal ortam oluşturma ve paket kurulumu

```jsx
# Proje kökünde
uv venv # .venv oluşturur
# Windows etkinleştirme
. .venv\Scripts\Activate.ps1
# Linux/macOS etkinleştirme
# source .venv/bin/activate

# requirements.txt'i uv ile kur
uv pip install -r requirements.txt
```

## 3) Ortam değişkenleri (.env)

• `.env.example` dosyasını kopyalayın ve kendi değerlerinizi girin:

```jsx
# proje kökünde
copy .env.example .env # Windows
# veya
cp .env.example .env # Linux/macOS
```

## ▶️ Kullanım

### A) Aşama 1 & 2 – Terminal Uygulaması

```python
python stage1/main.py
python stage2/main.py
```

- Temel işlemler: kitap listeleme, ekleme, silme, güncelleme
- Veriler JSON dosyasında tutulur (örn. library.json)

### B) Aşama 3 – API (JSON Veri Kaynağı)

```python
cd stage3
uvicorn api:app --reload
```

Projeyi çalıştırdıktan sonra API uç noktalarını incelemek için:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## GET - List Books

Endpoint: `/books`

Kütüphanedeki tüm kitapları JSON olarak döndürür.

### Request

cURL

```bash
curl --location '/books' \
--header 'Accept: application/json'
```

200 OK

### Response

- Body
- Headers (1)

```json
[
  {
    "title": "string",
    "author": "string",
    "isbn": "string"
  },
  {
    "title": "string",
    "author": "string",
    "isbn": "string"
  }
]
```

## POST - Add Book

Endpoint: `/books`

Body: `{"isbn": "..."}`

- Open Library API (Stage 2) ile başlık & yazar çek
- Zaten varsa 409 döndür
- Başarılıysa eklenen kitabı döndür

### Body

```json
{
  "isbn": "stringstring"
}
```

### Request

```bash
curl --location '/books' \
--header 'Accept: application/json' \
--data '{
  "isbn": "stringstring"
}'
```

201 Created

### Response

```json
{
  "title": "string",
  "author": "string",
  "isbn": "string"
}
```

## DELETE - Delete Book

Endpoint: `/books/:isbn`

Param: /books/{isbn}

- Varsa sil, yoksa 404 döndür

## C) Aşama 4 – API (Veritabanı – SQLAlchemy)

```python
uv run uvicorn stage4.main:app --reload
```

Diğer aşamalarda öğrenilen bilgiler ışığında aşama 4’te sisteme kullanıcı yönetimi ve daha gelişmiş kütüphane fonksiyonları eklendi:

- **Üye (Member) modeli** oluşturuldu, rol bazlı yetkilendirme desteği sağlandı.
- **Ödünç alma (Borrow)** modeli ile kitap ödünç verme ve iade süreçleri yönetildi.
- **Üye–Kitap (MemberBook) ilişkisi** eklenerek favori kitaplar ve okuma durumu takip edilebildi.
- **Kayıt ve giriş (auth)** endpoint’leri entegre edildi, rol tabanlı erişim kontrolü uygulandı.
- Kitap CRUD işlemleri **harici ISBN sorgulama** desteğiyle zenginleştirildi.
- Veritabanı şeması daha tutarlı ve doğrulamalı olacak şekilde iyileştirildi.

## 📚 API Dokümantasyonu (Aşama 4 – Veritabanı + Auth)

### 🔑 Auth

- **POST `/api/auth/register`** → Yeni üye kaydı.
    
    ```json
    {
      "username": "sumeyye",
      "email": "sumeyye@example.com",
      "password": "123456"
    }
    
    ```
    
- **POST `/api/auth/login`** → Kullanıcı girişi (OAuth2 Password Flow).
- **GET `/api/auth/me`** → Oturum açan kullanıcının bilgilerini döner.

---

### 📚 Books

- **GET `/api/books/?skip=0&limit=10`** → Kitap listesini döner (sayfalama destekli).
- **GET `/api/books/{book_id}`** → ID’ye göre tek kitap getirir.
- **POST `/api/books/`** → Yeni kitap ekler.
    
    ```json
    {
      "isbn": "9780141182803",
      "title": "1984",
      "author": "George Orwell",
      "publisher": "Secker & Warburg",
      "page_count": 328,
      "cover_url": "http://.../1984.jpg"
    }
    
    ```
    
- **PUT `/api/books/{book_id}`** → Kitap günceller.
- **DELETE `/api/books/{book_id}`** → Kitap siler.

---

### 📖 Borrows

- **GET `/api/borrows/`** → Tüm ödünç kayıtlarını listeler (sadece yetkili roller görebilir).
- **GET `/api/borrows/me`** → Giriş yapan üyenin ödünç aldığı kitapları listeler.
- **POST `/api/borrows/`** → Kitap ödünç alma.
    
    ```json
    {
      "member_id": 1,
      "book_id": 5
    }
    
    ```
    
- **PUT `/api/borrows/{borrow_id}/return`** → Ödünç alınan kitabı iade et.

---

### 📌 MemberBooks

- **POST `/api/memberbooks/`** → Üyeye kitap ekle (favori/okundu).
    
    ```json
    {
      "book_id": 5,
      "is_favorite": true,
      "is_read": false}
    
    ```
- **DELETE `/api/memberbooks/{book_id}?is_favorite=false&is_read=false`** → Üye–kitap ilişkisini kaldır.
- **GET `/api/memberbooks/favorites`** → Üyenin favori kitaplarını listeler.
- **GET `/api/memberbooks/read`** → Üyenin okuduğu kitapları listeler.

Projeyi çalıştırdıktan sonra API uç noktalarını incelemek için:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Test Senaryoları

Proje boyunca her aşama için ayrı testler yazılmıştır:

- **Aşama 1 (OOP Tabanlı Kütüphane Yönetimi):**
    - Kitap ekleme, silme, listeleme ve arama fonksiyonları test edildi.
- **Aşama 2 (ISBN Servis Entegrasyonu):**
    - Geçerli ISBN ile doğru kitap ve yazar bilgisi döndürme
    - Geçersiz ISBN için hata senaryosu
    - HTTP cevaplarının sahte (mock) versiyonları ile test
- **Aşama 3 (FastAPI ile REST API):**
    - `/books` endpointlerinin CRUD işlemleri
    - Hatalı ISBN ile kitap ekleme (404 Not Found)
    - Aynı ISBN ile tekrar ekleme (409 Conflict)
    - Kitap silme ve sonrası doğrulama

### 🔧 Testlerin Çalıştırılması

Projeyi test etmek için pytest kullanılmaktadır.

1. Sanal ortamı aktif edin:
    
    ```bash
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # Linux/Mac
    
    ```
    
2. Testleri çalıştırın:
    
    ```bash
    pytest
    
    ```
    
3. Belirli bir aşamadaki testleri çalıştırmak için:
    
    ```bash
    pytest stage1/
    pytest stage2/
    pytest stage3/
    
    ```
    
Pytest çalıştırıldığında her test dosyası otomatik olarak algılanır ve sonuçlar özetlenir.

NOT:  Bu projede **Aşama 1, 2 ve 3** için kapsamlı test senaryoları hazırlanmıştır. **Aşama 4** ise genişletme aşaması olup, zaman kısıtları nedeniyle testler henüz eklenmemiştir.