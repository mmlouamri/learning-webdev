from enum import Enum
from typing import Annotated

from data import books
from fastapi import FastAPI, Query

app = FastAPI()


class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"


@app.get("/books/")
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
