class GoogleBook:
    def __init__(
        self,
        google_id,
        title,
        description,
        published_date,
        authors,
        isbn_13,
        isbn_10,
        categories,
        images,
    ):
        self.google_id = google_id
        self.title = title
        self.description = description
        self.published_date = published_date
        self.authors = authors
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.categories = categories
        self.images = images


class GoogleBookBuilder:

    def __init__(self, items: list):
        self.items = items

    def build(self):
        return [self._build_book(item) for item in self.items]

    def _build_book(self, item: dict):
        google_id = item.get("id", "")
        title = self._get_volume_info(item).get("title", "")
        description = self._get_volume_info(item).get("description", "")
        published_date = self._get_volume_info(item).get("publishedDate", "")
        authors = self._parse_authors(item)
        [isbn_13, isbn_10] = self._get_isbn(item)
        categories = self._parse_categories(item)
        images = self._parse_images(item)
        return GoogleBook(
            google_id,
            title,
            description,
            published_date,
            authors,
            isbn_13,
            isbn_10,
            categories,
            images,
        )

    def _get_volume_info(self, item: dict):
        return item.get("volumeInfo", {})

    def _parse_authors(self, item: dict):
        authors = self._get_volume_info(item).get("authors", [])
        return [Author(author) for author in authors]

    def _get_isbn(self, item: dict):
        identifiers = self._get_volume_info(item).get("industryIdentifiers", [])
        isbn_13 = ""
        isbn_10 = ""
        for identifier in identifiers:
            if identifier.get("type") == "ISBN_13":
                isbn_13 = identifier.get("identifier", "")
            if identifier.get("type") == "ISBN_10":
                isbn_10 = identifier.get("identifier", "")
        return [isbn_13, isbn_10]

    def _parse_categories(self, item: dict):
        categories = self._get_volume_info(item).get("categories", [])
        return [Category(category) for category in categories]

    def _parse_images(self, item: dict):
        images = self._get_volume_info(item).get("imageLinks", {})
        return {
            "small_thumbnail": images.get("smallThumbnail", ""),
            "thumbnail": images.get("thumbnail", ""),
            "small": images.get("small", ""),
            "medium": images.get("medium", ""),
            "large": images.get("large", ""),
            "extra_large": images.get("extraLarge", ""),
        }


class Author:
    def __init__(self, name):
        self.name = name


class Category:
    def __init__(self, name):
        self.name = name
