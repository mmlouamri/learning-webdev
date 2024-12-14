from enum import Enum
from sqlmodel import SQLModel, Field, create_engine, Session, select, col
from data import books as books_dict
from pprint import pprint

class Language(str, Enum):
    ENGLISH = "English"
    FRENCH = "French"
    SPANISH = "Spanish"
    RUSSIAN = "Russian"

class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    year: int
    language: Language
    buy_price: float = Field(ge=0)
    sell_price: float = Field(ge=0)

engine = create_engine("sqlite://", echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_book(book: Book) -> Book:
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
    return book

def get_books() -> list[Book]:
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
    return books

def get_book_by_id(id: int) -> Book | None:
    with Session(engine) as session:
        book = session.get(Book, id)
    return book

def get_books_by_language(language: Language) -> list[Book]:
    with Session(engine) as session:
        books = session.exec(select(Book).where(col(Book.language) == language)).all()
    return books

def update_book_sell_price(id: int, new_sell_price: float) -> Book:
    with Session(engine) as session:
        book = session.exec(select(Book).where(col(Book.id) == id)).one()
        book.sell_price = new_sell_price
        session.add(book)
        session.commit()
        session.refresh(book)
    return book

def delete_book(id: int) -> dict[str, int]:
    with Session(engine) as session:
        book = session.get(Book, id)
        session.delete(book)
        session.commit()
    return {"ok": 1}


if __name__ == "__main__":
    create_db_and_tables()

    print("\n\nCreating Books")
    for book in books_dict:
        new_book = Book(**book)
        create_book(new_book)
        pprint(new_book)

    print("\n\nGetting Books")
    books = get_books()
    pprint(books)

    print("\n\nGetting Book by ID")
    book = get_book_by_id(2)
    pprint(book)

    print("\n\nGetting Books by language")
    books = get_books_by_language(Language.RUSSIAN)
    pprint(books)

    print("\n\nUpdating Book")
    update_book_sell_price(2, 13.37)
    book = get_book_by_id(2)
    pprint(book)

    print("\n\nDeleting Book")
    delete_book(2)
    book = get_book_by_id(2)
    pprint(book)