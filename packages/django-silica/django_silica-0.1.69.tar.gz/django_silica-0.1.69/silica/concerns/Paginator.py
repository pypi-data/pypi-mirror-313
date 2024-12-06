from typing import TypeVar


class Paginator:
    """A simple paginator class that returns page details for a given 1-based page number."""

    def __init__(self, total_count, per_page=10, page_fn=None):
        self.total_count = total_count
        self.per_page = per_page
        self.num_pages = self._get_num_pages()
        self.page_fn = page_fn

    def _get_num_pages(self):
        """Returns the total number of pages."""
        if self.total_count % self.per_page == 0:
            return self.total_count // self.per_page
        return self.total_count // self.per_page + 1

    def validate_number(self, number):
        """Validates the given 1-based page number."""
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid page number: {number}")
        if number < 1 or number > self.num_pages:
            raise ValueError(f"Page number out of range: {number}")
        return number

    def page(self, number):
        """Returns page details for the given 1-based page number."""
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page
        limit = self.per_page

        # # If a page function is provided, use it to fetch data.
        # if self.page_fn:
        #     object_list = self.page_fn(offset, limit)
        # else:
        #     object_list = range(offset, limit)  # Default behavior for demonstration

        return {
            'number': number,
            'offset': offset,
            'limit': limit,
            'has_previous': number > 1,
            'has_next': number < self.num_pages,
            'num_pages': self.num_pages,
            'next_page_number': number + 1 if number < self.num_pages else None,
            'previous_page_number': number - 1 if number > 1 else None,
        }

    __repr__ = __str__ = lambda self: f"<Paginator with {self.num_pages} pages>"


# create a type from Paginator class page() method:
PaginatorPage = TypeVar("PaginatorPage", bound=Paginator.page)
