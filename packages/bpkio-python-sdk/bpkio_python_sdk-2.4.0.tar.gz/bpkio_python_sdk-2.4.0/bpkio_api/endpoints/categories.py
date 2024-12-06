from typing import Any, List, Tuple

from bpkio_api.caching import cache_api_results
from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.exceptions import ResourceExistsError
from bpkio_api.helpers.list import get_all_with_pagination
from bpkio_api.helpers.search import SearchMethod, search_array_with_filters
from bpkio_api.models.Categories import Category, CategoryIn
from bpkio_api.response_handler import postprocess_response
from uplink import (Body, Query, delete, get, json, post, put,
                    response_handler, returns)

from .enums import UpsertOperationType


@response_handler(postprocess_response)
class CategoriesApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json(List[Category])
    @get("categories")
    def get_page(self, offset: Query = 0, limit: Query = 5) -> List[Category]:  # type: ignore
        """Get a (partial) list of categories"""

    @returns.json(Category)
    @get("categories/{category_id}")
    def retrieve(self, category_id) -> Category | None:
        """Get a single category, by ID"""

    @json
    @returns.json(Category)
    @post("categories")
    def create(self, category: Body(type=CategoryIn)) -> Category:  # type: ignore
        """Create a new category"""

    @json
    @returns.json(Category)
    @put("categories/{category_id}")
    def update(self, category_id: int, category: Body(type=CategoryIn)) -> Category:  # type: ignore
        """Update a category"""

    @delete("categories/{category_id}")
    def delete(self, category_id: int):
        """Delete a category, by ID"""

    # === Helpers ===

    @cache_api_results("list_categories")
    def list(self):
        """Get the full list of categories"""
        return get_all_with_pagination(self.get_page)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Category]:
        """Searches the list of categories for those matching a particular filter query

        You can search for full or partial matches in all or specific fields.
        All searches are done as string matches (regarding of the actual type of each field)

        Args:
            value (Any, optional): The string value to search. Defaults to None.
            field (str, optional): The field name in which to search for the value.
                Defaults to None.
            method (SearchMethod, optional): How to perform the search.
                SearchMethod.STRING_SUB searches for partial string match. This is the default.
                SearchMethod.STRING_MATCH searches for a complete match (after casting to string).
                SearchMethod.STRICT searches for a strict match (including type)
            filters (List[Tuple[Any, Optional[str], Optional[SearchMethod]]], optional):
                Can be used as an alternatitve to using `value`, `field` and `method`,
                in particular if multiple search patterns need to be specified
                (which are then treated as logical `AND`). Defaults to None.

        Returns:
            List[Category]: List of matching sources
        """
        if not filters:
            filters = [(value, field, method)]

        sources = self.list()
        return search_array_with_filters(sources, filters=filters)

    def upsert(
        self, category: CategoryIn, if_exists: str | None = None
    ) -> Tuple[Category, UpsertOperationType]:
        """Create, retrieve or update a category

        Args:
            category (CategoryIn): The category payload
            if_exists (str): What to do if the category already exists (error, retrieve, update)

        Returns:
            Category: the category retrieved or created
        """

        try:
            return (self.create(category), UpsertOperationType.CREATED)
        except ResourceExistsError as e:
            if if_exists == "error":
                return (category, UpsertOperationType.ERROR)

            existing_category = self.search(value=category.name, field="name")[0]

            if if_exists == "retrieve":
                return (existing_category, UpsertOperationType.RETRIEVED)
            elif if_exists == "update":
                updated_category = self.update(existing_category.id, category)
                return (updated_category, UpsertOperationType.UPDATED)
