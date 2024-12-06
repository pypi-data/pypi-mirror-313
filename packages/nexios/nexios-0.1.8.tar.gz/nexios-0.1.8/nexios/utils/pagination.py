from tortoise.queryset import QuerySet
from typing import List, Dict, Callable, Any, Optional, Iterable, Union


class Paginator:
    def __init__(
        self,
        data_source: Union[QuerySet, Iterable[Any]],
        page: int = 1,
        page_size: int = 10,
        transformer: Optional[Callable[[Any], Dict]] = None,
        include_metadata: Optional[List[str]] = None,
    ):
        
        """
        A flexible and reusable paginator.

        Args:
            data_source: A Tortoise ORM QuerySet or any iterable data source to paginate.
            page: Current page number (1-based).
            page_size: Number of items per page (default 10).
            transformer: Optional function to transform objects into dictionaries.
                         Defaults to `None`, which means raw objects are returned.
            include_metadata: Optional list of metadata fields to include in the response.
                              Defaults to including all fields.
        """
        self.data_source = data_source
        self.page = max(1, page)
        self.page_size = max(1, min(page_size, 100))
        self.transformer = transformer

        # Default metadata fields to include
        self.default_metadata = [
            "page",
            "page_size",
            "total_items",
            "total_pages",
            "current_page",
            "next_page",
            "previous_page",
            "has_next_page",
            "has_previous_page",
        ]
        self.include_metadata = include_metadata or self.default_metadata

    async def get_total_items(self) -> int:
        """Get the total number of items."""
        if isinstance(self.data_source, QuerySet):
            return await self.data_source.count()
        return len(self.data_source)

    async def get_items(self, offset: int, limit: int) -> List[Any]:
        """Fetch items from the data source."""
        if isinstance(self.data_source, QuerySet):
            return await self.data_source.offset(offset).limit(limit).all()
        return list(self.data_source)[offset : offset + limit]

    async def get_paginated_response(self) -> Dict[str, Any]:
        """
        Paginates the data source and returns the response.

        Returns:
            A dictionary containing paginated data and metadata.
        """
        total_items = await self.get_total_items()
        total_pages = (total_items + self.page_size - 1) // self.page_size  # Ceiling division
        offset = (self.page - 1) * self.page_size

        # Fetch items
        items = await self.get_items(offset, self.page_size)
        
        # Transform the items if a transformer is provided
        if self.transformer:
            data = [self.transformer(item) for item in items]
        else:
            # Modified part to handle empty items list
            if items:
                data = [item.__dict__ for item in items] if hasattr(items[0], "__dict__") else list(items)
            else:
                data = []


        # Construct metadata
        metadata = {
            "page": self.page,
            "page_size": self.page_size,
            "current_page": self.page,
            "next_page": self.page + 1 if self.page < total_pages else None,
            "previous_page": self.page - 1 if self.page > 1 else None,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next_page": self.page < total_pages,
            "has_previous_page": self.page > 1 and len(data) > 0,
        }

        # Include only specified metadata fields
        metadata = {key: value for key, value in metadata.items() if key in self.include_metadata}

        return {
            "metadata": metadata,
            "items": data,
        }
