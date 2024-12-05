from google_books_api.models import GoogleBook, GoogleBookBuilder


class GoogleBooksApiResult:
    def __init__(self, result: dict):
        self._parse_result(result)

    def _parse_result(self, result: dict):
        """
        Parse the result of a Google Books API request.

        Args:
            result (dict): The result of the Google Books API request.

        Returns:
            None

        """
        self.total_items: int = result.get("totalItems", 0)
        self.items: list = result.get("items", [])
        self.books: list[GoogleBook] = GoogleBookBuilder(self.items).build()
