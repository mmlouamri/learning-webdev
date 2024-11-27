from typing import Annotated

from data import books
from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()


@app.get("/books/{book_id}")
async def get_book(book_id: Annotated[int, Path(ge=0)]):
    for book in books:
        if book["id"] == book_id:
            return book
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
    )
