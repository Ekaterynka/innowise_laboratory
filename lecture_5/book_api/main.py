"""
Simple Book Collection API
Built with FastAPI and SQLAlchemy ORM
"""

# Import necessary libraries and modules
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List


# Pydantic schemas

class BookCreate(BaseModel):
    """
    Pydantic model for creating a new book.
    This validates the data sent by the user in POST request.
    """
    title: str  # Book title (required)
    author: str  # Book author (required)
    year: Optional[int] = None  # Publication year (optional)


class BookUpdate(BaseModel):
    """
    Pydantic model for updating an existing book.
    All fields are optional - only provided fields will be updated.
    """
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BaseModel):
    """
    Pydantic model for API response.
    This is what we return to the user.
    """
    id: int
    title: str
    author: str
    year: Optional[int]

    class Config:
        """Pydantic configuration for ORM compatibility"""
        from_attributes = True


# Database setup

# SQLite database URL it creates a file called 'books.db' in current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# Database model (orm)

class BookDB(Base):
    """
    SQLAlchemy ORM model for the 'books' table.
    This represents the actual database table structure.
    """
    __tablename__ = "books"  # Table name in database

    # Columns/fields in the table
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)  # Optional field


# Create all tables in the database
# This will create the 'books' table if it doesn't exist
Base.metadata.create_all(bind=engine)

# FastAPI application

# Initialize FastAPI application
app = FastAPI(
    title="Simple Book Collection API",
    description="A REST API for managing personal book collection",
    version="1.0.0"
)


# Database dependency

def get_db():
    """Creates database session for each request, auto-closes after"""
    db = SessionLocal()
    try:
        yield db  # Provide session to endpoint function
    finally:
        db.close()  # Always close session


# API endpoints

@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book in the collection.
    Example JSON request:
        {
            "title": "Some book",
            "author": "Ekaterina",
            "year": 2025
        }
    """
    # Create new BookDB instance from request data
    db_book = BookDB(
        title=book.title,
        author=book.author,
        year=book.year
    )

    # Add to database session
    db.add(db_book)
    db.commit()  # Save changes to database
    db.refresh(db_book)  # Refresh to get auto-generated ID

    return db_book


@app.get("/books/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    """
    Get all books from the collection.
    Returns: All books in the collection

    Example response:
        [
            {
                "id": 1,
                "title": "Easy Python",
                "author": "Lubanovich",
                "year": 2019
            }
        ]
    """
    # Query all books from database
    books = db.query(BookDB).all()
    return books


@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
        title: Optional[str] = Query(None, description="Search by book title (partial match)"),
        author: Optional[str] = Query(None, description="Search by author name (partial match)"),
        year: Optional[int] = Query(None, description="Search by publication year (exact match)"),
        db: Session = Depends(get_db)
):
    """
    Search books by title, author, or year.
    Returns: Books matching the search criteria
    """
    # Start with base query
    query = db.query(BookDB)

    # Add filters based on provided parameters
    if title:
        query = query.filter(BookDB.title.contains(title))
    if author:
        query = query.filter(BookDB.author.contains(author))
    if year:
        query = query.filter(BookDB.year == year)

    # Execute query and return results
    return query.all()


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
        book_id: int,
        book_update: BookUpdate,
        db: Session = Depends(get_db)
):
    """
    Update an existing book by ID.
    Only provided fields will be updated.
    HTTPException: 404 if book with given ID is not found

    Example JSON request:
        {
            "title": "New Title",
            "year": 2025
        }
    """
    # Find book in database
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()

    # Check if book exists
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only the fields that were provided
    if book_update.title is not None:
        db_book.title = book_update.title
    if book_update.author is not None:
        db_book.author = book_update.author
    if book_update.year is not None:
        db_book.year = book_update.year

    # Save changes
    db.commit()
    db.refresh(db_book)

    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by ID.

    Returns: Success message

        HTTPException: 404 if book with given ID is not found

    Example response:
        {"message": "Book deleted successfully"}
    """
    # Find book in database
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()

    # Check if book exists
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Delete book from database
    db.delete(db_book)
    db.commit()

    return {"message": "Book deleted successfully"}

# Root endpoint (health check)

@app.get("/")
def read_root():
    """
    Root endpoint: health check and API information.

    Returns: Welcome message and API status
    """
    return {
        "message": "Welcome to Book Collection API",
        "docs": "Visit /docs for Swagger UI documentation",
        "endpoints": [
            "POST /books/ - Add new book",
            "GET /books/ - Get all books",
            "GET /books/search/ - Search books",
            "PUT /books/{id} - Update book",
            "DELETE /books/{id} - Delete book"
        ]
    }


# Application entry point

if __name__ == "__main__":
    """
    This allows running the application directly with: python main.py
    But we'll use uvicorn for development: uvicorn main:app --reload
    """
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)