from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, UploadFile, status
from data import books
import uuid
import os
import aiofiles

app = FastAPI()

def generate_unique_filename() -> str:
    return f"{uuid.uuid4().hex}"

@app.get("/books/")
async def get_books():
    return books

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
