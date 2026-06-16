from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Create the FastAPI application instance
app = FastAPI(title="Bookshelf API")

# --- Models ---

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    rating: int = Field(ge=1, le=5)

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    rating: int = Field(ge=1, le=5)

# --- In-memory data store ---

books: list[dict] = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "rating": 5},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "rating": 4},
    {"id": 3, "title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "rating": 5},
]
next_id: int = 4

# Root endpoint to verify the server is running
@app.get("/")
def root():
    return {"message": "Welcome to the Bookshelf API"}

@app.get("/books", response_model=list[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    # Search for the book by ID
    for book in books:
        if book["id"] == book_id:
            return book
    # No match found - return a 404 error
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookCreate):
    global next_id
    # Build a full book dict by combining the auto-assigned ID with the request data
    new_book = {"id": next_id, **book_data.model_dump()}
    books.append(new_book)
    next_id += 1
    return new_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookCreate):
    # Loop through books to find the matching ID
    for i, book in enumerate(books):
        if book["id"] == book_id:
            # Replace the old book data with the new data
            updated_book = {"id": book_id, **book_data.model_dump()}
            books[i] = updated_book
            return updated_book
    # If no book matched, return a 404 error
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    # Loop through books to find the matching ID
    for i, book in enumerate(books):
        if book["id"] == book_id:
            # Remove the book from the list
            books.pop(i)
            return {"message": f"Book {book_id} deleted successfully"}
    # If no book matched, return a 404 error
    raise HTTPException(status_code=404, detail="Book not found")