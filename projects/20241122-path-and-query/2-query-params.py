from data import books
from fastapi import FastAPI

app = FastAPI()


@app.get("/books/")
async def get_books(id=None, title=None, language=None, year=None):
    where = {}
    if id:
        where["id"] = int(id)
    if title:
        where["title"] = title
    if language:
        where["language"] = language
    if year:
        where["year"] = int(year)
    return [book for book in books if all(book[k] == v for k, v in where.items())]
