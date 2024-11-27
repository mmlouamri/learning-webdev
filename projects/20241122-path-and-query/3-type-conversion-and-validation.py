from data import books
from fastapi import FastAPI

app = FastAPI()


@app.get("/books/")
async def get_books(
    id: int | None = None,
    title: str | None = None,
    language: str | None = None,
    year: int | None = None,
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
    return [book for book in books if all(book[k] == v for k, v in where.items())]
