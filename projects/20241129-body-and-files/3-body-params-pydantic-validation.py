from fastapi import FastAPI
from enum import Enum
from data import books
from pydantic import BaseModel, Field

app = FastAPI()


class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"


class BookIn(BaseModel):
    title: str
    language: Language
    year: int = Field(lt=2025)
    sell_price: float = Field(ge=0)
    buy_price: float = Field(ge=0)


@app.get("/books/")
async def get_books():
    return books


@app.post("/books/")
async def create_book(book: BookIn):
    new_book = {"id": max(book["id"] for book in books) + 1, **book.model_dump(), 'path': None}

    books.append(new_book)
    return books[-1]
