from typing import Any, List, Tuple

from bpkio_api.caching import cache_api_results
from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.helpers.list import get_all_with_pagination
from bpkio_api.helpers.search import SearchMethod, search_array_with_filters
from bpkio_api.models.Users import User
from bpkio_api.response_handler import postprocess_response
from uplink import Query, get, response_handler, returns


@response_handler(postprocess_response)
class UsersApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json()
    @get("users")
    def get_page(self, offset: Query = 0, limit: Query = 5) -> List[User]:  # type: ignore
        """List all users"""

    @returns.json()
    @get("users/{user_id}")
    def retrieve(self, user_id) -> User:
        """Get a single user, by ID"""

    # === Helpers ===

    @cache_api_results("list_users")
    def list(self):
        return get_all_with_pagination(self.get_page)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[User]:
        """Searches the list of users for those matching a particular filter query

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
            List[User]: List of matching sources
        """
        if not filters:
            filters = [(value, field, method)]

        sources = self.list()
        return search_array_with_filters(sources, filters=filters)
