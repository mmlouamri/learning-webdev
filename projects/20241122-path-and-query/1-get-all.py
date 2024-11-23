from data import books
from fastapi import FastAPI

app = FastAPI()


@app.get("/books/")
async def get_books():
    return books
