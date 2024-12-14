from enum import Enum
from typing import Annotated

from data import books
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel

app = FastAPI()


class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"


class BookOut(BaseModel):
    id: int
    title: str
    language: Language
    year: int
    sell_price: float
    path: str


@app.get("/books/", response_model=list[BookOut])
async def get_books(
    id: Annotated[int | None, Query(ge=0)] = None,
    title: str | None = None,
    language: Annotated[list[Language] | None, Query()] = None,
    year: Annotated[int | None, Query(lt=2025)] = None,
):

    where = {}
    if id is not None:
        where["id"] = id
    if title is not None:
        where["title"] = title
    if language is not None:
        where["language"] = language
    if year is not None:
        where["year"] = year
    return [
        book
        for book in books
        if all(
            book[k] == v if k != "language" else book[k] in v for k, v in where.items()
        )
    ]


@app.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: Annotated[int, Path(ge=0)]):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
    )
