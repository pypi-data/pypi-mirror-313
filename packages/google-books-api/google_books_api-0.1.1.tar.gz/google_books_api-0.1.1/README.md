## Google Books API

Usage:
```python

from google_books_api.google_books_api import GoogleBookApi

api = GoogleBookApi("Google Books API URL")

# Search for books
books = api.search_by_title("Python")
print(books)

# Get book by id
book = api.get_by_id("id")
print(book.title)
```