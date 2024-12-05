from typing import Optional
from easy_http_requests.easy_http_request import EasyHttpRequest
from easy_http_requests.easy_http_response import EasyHttpResponse
from google_books_api.models import GoogleBookBuilder, GoogleBook
from google_books_api.google_books_api_params import GoogleBooksApiParams
from google_books_api.google_books_api_result import GoogleBooksApiResult
from google_books_api.exceptions.google_books_api_exception import (
    GoogleBooksApiException,
)


class GoogleBookApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.http_request: EasyHttpRequest = EasyHttpRequest(self.base_url)

    def search_book(self, search_params: dict) -> GoogleBooksApiResult:
        """
        Search for books using the Google Books API.

        Args:
            search_params (dict): A dictionary containing search parameters for the book query.

        Returns:
            GoogleBooksApiResult: A GoogleBooksApiResult object containing the search results.

        Raises:
            GoogleBooksApiException: If an error occurs while making the request.
        """
        response = self._make_get_request("volumes", search_params)
        return GoogleBooksApiResult(response.body)

    def search_by_title(self, title: str, max_results: int = 5) -> GoogleBooksApiResult:
        """
        Search for books by title using the Google Books API.

        Args:
            title (str): The title of the book to search for.
            max_results (int): The maximum number of results to return. Default is 5.

        Returns:
            GoogleBooksApiResult: A GoogleBooksApiResult object containing the search results.

        Raises:
            GoogleBooksApiException: If an error occurs while making the request.
        """
        params = {
            "q": GoogleBooksApiParams.IN_TITLE + title,
            GoogleBooksApiParams.MAX_RESULTS: max_results,
        }
        return self.search_book(search_params=params)

    def get_by_id(self, book_id: str) -> GoogleBook:
        """
        Get book details by book ID using the Google Books API.

        Args:
            book_id (str): The ID of the book to retrieve.

        Returns:
            GoogleBook: A GoogleBook object containing the book details.

        Raises:

            GoogleBooksApiException: If an error occurs while making the request.
        """
        response = self._make_get_request(f"volumes/{book_id}")
        return GoogleBookBuilder([response.body]).build()[0]

    def _make_get_request(
        self, endpoint: str, params: Optional[dict] = None
    ) -> EasyHttpResponse:
        """
        Make a GET request to the Google Books API.

        Args:
            endpoint (str): The API endpoint to make the request to.
            params (dict): Optional query parameters for the request.

        Returns:
            EasyHttpResponse: An EasyHttpResponse object containing the response data.

        Raises:
            GoogleBooksApiException: If an error occurs while making the request.
        """
        try:
            easy_http_response = self.http_request.get(endpoint, params)
            easy_http_response.response.raise_for_status()
            return easy_http_response
        except Exception as e:
            raise GoogleBooksApiException(
                f"An unexpected error occurred while making request to {endpoint}", e
            )
