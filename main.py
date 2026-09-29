from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    id: str
    title: str

class BookAdd(BaseModel):
    title: str

book: list[BookCreate] = []
@app.get("/")
def get_book():
    return {"message": f"Моя любимая книга: {book[0].title}"}

@app.post("/add_book")
def add_book(payload: BookAdd) -> BookCreate:
    new_book = BookCreate(id=str(uuid4()), title=payload.title)
    book.append(new_book)
    return new_book
