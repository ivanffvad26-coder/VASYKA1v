from fastapi import FastAPI
from db import engine, Base
import models  # ⚠️ ОБЯЗАТЕЛЬНО ДО create_all
from auth import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth)


@app.get("/")
def root():
    return {"status": "alive"}