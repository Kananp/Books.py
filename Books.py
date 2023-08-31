from typing import Optional

from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self. description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt= 1980, lt=2030)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'CodingwithRoby',
                'description': 'A new description of a book',
                'rating': 5,
                'published date': 2012
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5, 2021),
    Book(2, 'Be fast with FastAPI', 'codingwithroby', 'A great book', 5, 1982),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book', 5, 2021),
    Book(4, 'HP1', 'Auhtor One', 'Book Description', 2, 2021),
    Book(5, 'HP2', 'Author Two', 'Book Description', 3, 1998),
    Book(6, 'HP3', 'Author Three', 'Book Description', 1, 1998)

]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book-id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book



@app.put("/books/update-book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book-id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

@app.get("/books/{published_date}")
async def get_book_PB(published_date: int = Path(gt=1980, lt=2030)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return
