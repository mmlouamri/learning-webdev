import uuid
import aiofiles
from fastapi import Body, FastAPI, Query, Path, HTTPException, UploadFile, status
from typing import Annotated
from enum import Enum
from data import books
from pydantic import BaseModel, Field

app = FastAPI()

def generate_unique_filename() -> str:
    return f"{uuid.uuid4().hex}"

class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"

class BookBase(BaseModel):
    title: str
    language: Language
    year: int = Field(lt=2025)
    sell_price: float = Field(ge=0)

class BookIn(BookBase):
    buy_price: float = Field(ge=0)

class BookOut(BookBase):
    id: int
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
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found!"
    )


@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book: Annotated[
        BookIn,
        Body(
            openapi_examples={
                "1984": {
                    "summary": "George's Orwell 1984",
                    "description": "",
                    "value": {
                        "title": "1984",
                        "language": "English",
                        "year": 1949,
                        "sell_price": 15.99,
                        "buy_price": 10.12,
                    },
                },
                "bovary": {
                    "summary": "Gustave Flaubert's Madame Bovary",
                    "description": "",
                    "value": {
                        "title": "Madame Bovary",
                        "language": "French",
                        "year": 1857,
                        "sell_price": 19.99,
                        "buy_price": 12.65,
                    },
                },
            }
        ),
    ]
):
    new_book = {"id": max(book["id"] for book in books) + 1, **book.model_dump(), "path": ""}

    books.append(new_book)
    return books[-1]

@app.patch('/books/{book_id}/file')
async def patch_file(
    book_id: Annotated[int, Path(ge=0)],
    file: UploadFile):
    books_with_id = [(book_index, book) for book_index, book in enumerate(books) if book['id'] == book_id]
    if len(books_with_id) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found!")
    
    book_index, book = books_with_id[0]
    filename = generate_unique_filename()
    filepath = f'storage/{filename}.pdf'


    async with aiofiles.open(filepath, "wb") as out_file:
        while content := await file.read(1024): 
            await out_file.write(content)
    
    books[book_index] = {
        **book, 'path': filepath
    }
    return books[book_index]