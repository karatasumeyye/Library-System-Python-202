from fastapi import FastAPI
from stage4 import api
from stage4.database import Base, engine
from stage4 import models
# from stage4.api import router as book_router

# DB tabloları oluştur
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API")

# Router ekle
app.include_router(api.router, prefix="/api")


