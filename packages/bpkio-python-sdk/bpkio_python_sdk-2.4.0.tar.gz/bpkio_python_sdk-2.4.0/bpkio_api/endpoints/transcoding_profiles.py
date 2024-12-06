from typing import Any, List, Tuple

from bpkio_api.caching import cache_api_results
from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.helpers.list import get_all_with_pagination
from bpkio_api.helpers.search import SearchMethod, search_array_with_filters
from bpkio_api.models.TranscodingProfiles import TranscodingProfile
from bpkio_api.response_handler import postprocess_response
from uplink import Query, get, response_handler, returns


@response_handler(postprocess_response)
class TranscodingProfilesApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json()
    @get("transcoding-profiles")
    def get_page(
        self, offset: Query = 0, limit: Query = 50, tenant_id: Query("tenantId") = None
    ) -> List[TranscodingProfile]:  # type: ignore
        """List all transcoding profiles"""

    @returns.json()
    @get("transcoding-profiles/{transcoding_profile_id}")
    def retrieve(
        self, transcoding_profile_id, tenant_id: Query("tenantId") = None
    ) -> TranscodingProfile:
        """Get a single transcoding profile, by ID"""

    # === Helpers ===

    @cache_api_results("list_profiles")
    def list(self, tenant_id: int = None):
        return get_all_with_pagination(self.get_page, tenant_id=tenant_id)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
        tenant_id: int = None,
    ) -> List[TranscodingProfile]:
        """Searches the list of transcoding profiles for those matching a particular filter query

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
            List[Svc.SourceSpare]: List of matching sources
        """
        if not filters:
            filters = [(value, field, method)]

        profiles = self.list(tenant_id=tenant_id)
        return search_array_with_filters(profiles, filters=filters)
