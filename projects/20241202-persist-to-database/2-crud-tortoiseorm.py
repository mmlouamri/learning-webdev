from enum import Enum
from pydantic import BaseModel, Field
from tortoise import Model, fields, Tortoise
from data import books as books_dict
from pprint import pprint
import asyncio

class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"

class BookDB(Model):
    id = fields.BigIntField(primary_key=True)
    title = fields.CharField(max_length=255)
    year = fields.IntField()
    language = fields.CharEnumField(Language)
    buy_price = fields.DecimalField(max_digits=10, decimal_places=2)
    sell_price = fields.DecimalField(max_digits=10, decimal_places=2)

class BookCreateSchema(BaseModel):
    title: str
    year: int
    language: Language
    buy_price: float = Field(ge=0)
    sell_price: float = Field(ge=0)

def print_tortoise_model(model: Model):
    print(f"{model}(id={model.id}, title={model.title}, year={model.year}, language={model.language}, buy_price={model.buy_price}, sell_price={model.sell_price})")

async def create_db_and_tables():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['__main__']},
    )
    await Tortoise.generate_schemas()

async def create_book(book: BookCreateSchema) -> BookDB:
    created_book = await BookDB.create(**book.model_dump())
    return created_book

async def get_books() -> list[BookDB]:
    books = await BookDB.all() 
    return books

async def get_book_by_id(id: int) -> BookDB | None:
    book = await BookDB.get_or_none(id=id)
    return book

async def get_books_by_language(language: Language) -> list[BookDB]:
    books = await BookDB.filter(language=language)
    return books

async def update_book_sell_price(id: int, new_sell_price: float) -> BookDB:
    book = await BookDB.get_or_none(id=id)
    if not book:
        raise ValueError(f"Book with id {id} not found")
    book.sell_price = new_sell_price
    await book.save()
    return book 

async def delete_book(id: int) -> dict[str, int]:
    book = await BookDB.get_or_none(id=id)
    if not book:
        raise ValueError(f"Book with id {id} not found")
    await book.delete()
    return {"ok": 1}

async def main():
    await create_db_and_tables()

    print("\n\nCreating Books")
    for book in books_dict:
        new_book = BookCreateSchema(**book)
        created_book = await create_book(new_book)
        print_tortoise_model(created_book)

    print("\n\nGetting Books")
    books = await get_books()
    [print_tortoise_model(book) for book in books]

    print("\n\nGetting Book by ID")
    book = await get_book_by_id(2)
    print_tortoise_model(book)

    print("\n\nGetting Books by language")
    books = await get_books_by_language(Language.RUSSIAN)
    [print_tortoise_model(book) for book in books]


    print("\n\nUpdating Book")
    updated_book = await update_book_sell_price(2, 13.37)
    print_tortoise_model(updated_book)

    print("\n\nDeleting Book")
    deleted_book = await delete_book(2)
    print(deleted_book)


if __name__ == "__main__":
    asyncio.run(main())