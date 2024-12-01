from fastapi import FastAPI, Body
from typing import Annotated
from enum import Enum
from data import books

app = FastAPI()

class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"


@app.get("/books/")
async def get_books():
    return books


@app.post("/books/")
async def create_book(
    title: Annotated[str, Body()],
    language: Annotated[Language, Body()],
    year: Annotated[int, Body()],
    sell_price: Annotated[float, Body()],
    buy_price: Annotated[float, Body()],
):
    new_book = {
        "id": max(book["id"] for book in books) + 1,
        "title": title,
        "language": language,
        "year": year,
        "sell_price": sell_price,
        "buy_price": buy_price,
        "path": None,
    }

    books.append(new_book)
    return books[-1]
