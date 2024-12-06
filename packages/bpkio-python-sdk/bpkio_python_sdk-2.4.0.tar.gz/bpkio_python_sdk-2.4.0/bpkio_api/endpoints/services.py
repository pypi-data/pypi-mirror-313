from datetime import datetime
from typing import Any, List, Tuple

from bpkio_api.caching import cache_api_results
from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.exceptions import BroadpeakIoHelperError, ResourceExistsError
from bpkio_api.helpers.list import collect_from_ids, get_all_with_pagination
from bpkio_api.helpers.objects import find_duplicates_of
from bpkio_api.helpers.search import SearchMethod, search_array_with_filters
from bpkio_api.models import ContentReplacementSlot
from bpkio_api.models import Services as Svc
from bpkio_api.models import VirtualChannelSlot, VirtualChannelSlotIn
from bpkio_api.response_handler import postprocess_response, return_count
from uplink import (Body, Query, delete, get, json, params, post, put,
                    response_handler, returns)

from .enums import UpsertOperationType


@response_handler(postprocess_response)
class ServicesApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

        self.virtual_channel = VirtualChannelServiceApi(
            parent_api=self, base_url=base_url, **kwargs
        )
        self.content_replacement = ContentReplacementServiceApi(
            parent_api=self, base_url=base_url, **kwargs
        )
        self.ad_insertion = AdInsertionServiceApi(
            parent_api=self, base_url=base_url, **kwargs
        )
        self.adaptive_streaming_cdn = AdaptiveStreamingCdnServiceApi(
            parent_api=self, base_url=base_url, **kwargs
        )

    def _mappings(self, model):
        match model:
            case Svc.VirtualChannelServiceIn():
                return self.virtual_channel
            case Svc.VirtualChannelService():
                return self.virtual_channel
            case Svc.AdInsertionServiceIn():
                return self.ad_insertion
            case Svc.AdInsertionService():
                return self.ad_insertion
            case Svc.ContentReplacementServiceIn():
                return self.content_replacement
            case Svc.ContentReplacementService():
                return self.content_replacement
            case Svc.AdaptiveStreamingCdnService():
                return self.adaptive_streaming_cdn
            case _:
                raise Exception(
                    f"Model {model.__class__.__name__} "
                    "not recognised as a valid service type"
                )

    @returns.json(List[Svc.ServiceSparse])
    @get("services")
    def get_page(self, offset: Query = 0, limit: Query = 5) -> List[Svc.ServiceSparse]:  # type: ignore
        """List all services"""

    # === Helpers ===

    @cache_api_results("list_services")
    def list(self):
        return get_all_with_pagination(self.get_page)

    def search_by_type(self, type: Svc.ServiceType) -> List[Svc.ServiceSparse]:
        all_items = self.list()
        return [i for i in all_items if i.type == type]

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Svc.ServiceSparse]:
        """Searches the list of services for those matching a particular filter query

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
            List[Svc.ServiceSparse]: List of matching services
        """
        if not filters:
            filters = [(value, field, method)]

        services = self.list()
        return search_array_with_filters(services, filters=filters)

    def retrieve(
        self, service_id: int
    ) -> (
        Svc.AdInsertionService
        | Svc.ContentReplacementService
        | Svc.VirtualChannelService
        | Svc.AdaptiveStreamingCdnService
        | None
    ):
        """Gets a service by its ID

        This is a helper method that allows you to get the full Service sub-type (eg. virtual-channel,
        content-replacement etc) without having to know its type in advance and calling the specific
        endpoint.

        Args:
            service_id (int): The service identifier

        Raises:
            e: _description_

        Returns:
            VirtualChannelService, AdInsertionService, ContentReplacementService :
              A specific sub-type of service
        """

        candidates = self.search(
            int(service_id), field="id", method=SearchMethod.STRICT
        )
        try:
            service = candidates[0]
            if service.type == Svc.ServiceType.AD_INSERTION:
                return self.ad_insertion.retrieve(service_id)
            if service.type == Svc.ServiceType.VIRTUAL_CHANNEL:
                return self.virtual_channel.retrieve(service_id)
            if service.type == Svc.ServiceType.CONTENT_REPLACEMENT:
                return self.content_replacement.retrieve(service_id)
            if service.type == Svc.ServiceType.ADAPTIVE_STREAMING_CDN:
                return self.adaptive_streaming_cdn.retrieve(service_id)
        except IndexError as e:
            raise BroadpeakIoHelperError(
                message=f"There is no service with ID {service_id}",
                original_message=e.args[0],
            )

    def create(
        self, service: Svc.ServiceIn
    ) -> (
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
    ):
        """Create a service"""
        endpoint = self._mappings(service)
        return endpoint.create(service)

    def delete(self, service_id: int):
        """Delete a service"""
        service = self.retrieve(service_id)
        if not service:
            raise BroadpeakIoHelperError(
                message=f"There is no service with ID {service_id}",
            )
        endpoint = self._mappings(service)
        return endpoint.delete(service_id)

    def _update(
        self, service_id: int, service: Svc.ServiceIn
    ) -> (
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
    ):
        """Update a service"""
        endpoint = self._mappings(service)
        return endpoint.update(service_id, service)

    def update(
        self, service_id: int, service: Svc.ServiceIn
    ) -> (
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
    ):
        """Create a service"""
        endpoint = self._mappings(service)
        return endpoint.update(service_id, service)

    def upsert(
        self,
        service: Svc.ServiceIn,
        if_exists: str = "retrieve",
        unique_fields: List[str | Tuple] = [],
    ) -> Tuple[
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
        | Svc.ServiceIn,
        UpsertOperationType,
    ]:
        """Creates a service with adaptable behaviour if it already exist.

        Args:
            service (ServiceIn): The payload for the service to create
            if_exists (str): What action to take if it exists:
              `error` (default) returns an error;
              `retrieve` returns the existing object;
              `update` updates the existing object.
            unique_fields (List[str | Tuple], optional): List of the fields
            or combination of fields to check for unicity. Defaults to [].

        Returns:
            Tuple[VirtualChannelService | ContentReplacementService |
            AdInsertionService | ServiceIn, int]:
            The resource created or retrieved, with an indicator:
            1 = created, 0 = retrieved, 2 = updated, -1 = failed

        """

        try:
            return (self.create(service), UpsertOperationType.CREATED)
        except ResourceExistsError as e:
            if if_exists == "error":
                return (service, UpsertOperationType.ERROR)

            unique_fields = list(set(unique_fields + ["name"]))
            for fld in unique_fields:
                # single field
                if isinstance(fld, str):
                    fld = (fld,)

                # find duplicates
                dupes = find_duplicates_of(
                    obj=service, in_list=self.list(), by_fields=fld
                )
                if dupes:
                    existing_resource = self.retrieve(dupes[0][1].id)

                    if if_exists == "retrieve":
                        return (existing_resource, UpsertOperationType.RETRIEVED)
                    elif if_exists == "update":
                        updated_resource = self._update(existing_resource.id, service)
                        return (updated_resource, UpsertOperationType.UPDATED)

    def pause(
        self, service_id: int
    ) -> (
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
    ):
        """Disable (pause) a service"""
        service = self.retrieve(service_id)
        service.state = "paused"
        endpoint = self._mappings(service)
        return endpoint.update(service_id, service)

    def unpause(
        self, service_id: int
    ) -> (
        Svc.VirtualChannelService
        | Svc.ContentReplacementService
        | Svc.AdInsertionService
    ):
        """Enable (unpause) a service"""
        service = self.retrieve(service_id)
        service.state = "enabled"
        endpoint = self._mappings(service)
        return endpoint.update(service_id, service)


# === CONTENT-REPLACEMENT SERVICES ===


@response_handler(postprocess_response)
class ContentReplacementServiceApi(BpkioSdkConsumer):
    def __init__(self, parent_api: ServicesApi, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)
        self.parent_api = parent_api

        self.slots = ContentReplacementServiceSlotsApi(base_url, **kwargs)

    @returns.json(Svc.ContentReplacementService)
    @get("services/content-replacement/{service_id}")
    def retrieve(self, service_id):
        """Get a single Content Replacement service, by ID"""

    @json
    @returns.json(Svc.ContentReplacementService)
    @post("services/content-replacement")
    def create(
        self, service: Body(type=Svc.ContentReplacementServiceIn)  # type: ignore
    ) -> Svc.ContentReplacementService:  # type: ignore
        """Create a new Content Replacement service"""

    @json
    @returns.json(Svc.ContentReplacementService)
    @put("services/content-replacement/{service_id}")
    def update(self, service_id: int, service: Body(type=Svc.ContentReplacementServiceIn)) -> Svc.ContentReplacementService:  # type: ignore
        """Update a Content Replacement service"""

    def upsert(
        self, service: Svc.ContentReplacementServiceIn, if_exists: str = "retrieve"
    ) -> Tuple[Svc.ContentReplacementService, UpsertOperationType]:
        """Conditionally create, retrieve or update a Content Replacement service"""
        return self.parent_api.upsert(
            service, unique_fields=["url"], if_exists=if_exists
        )

    @delete("services/content-replacement/{service_id}")
    def delete(self, service_id: int):
        """Delete a Content Replacement service, by ID"""

    def pause(self, service_id: int) -> Svc.ContentReplacementService:
        """Disable (pause) a Content Replacement service, by ID"""
        return self.parent_api.pause(service_id)

    def unpause(self, service_id: int) -> Svc.ContentReplacementService:
        """Enable (unpause) a Content Replacement service, by ID"""
        return self.parent_api.unpause(service_id)

    @cache_api_results("list_cr")
    def list(self) -> List[Svc.ContentReplacementService]:
        """List all Content Replacement services"""
        sparse_vcs = self.parent_api.search(
            Svc.ServiceType.CONTENT_REPLACEMENT,
            field="type",
            method=SearchMethod.STRICT,
        )
        return collect_from_ids(ids=[vc.id for vc in sparse_vcs], get_fn=self.retrieve)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Svc.ContentReplacementService]:
        """Searches the list of Content Replacement services for those matching a particular filter query"""
        if not filters:
            filters = [(value, field, method)]

        services = self.list()
        return search_array_with_filters(services, filters=filters)

    def clear(self, service_id):
        """Delete all Content Replacement slots, for a given service

        Args:
            service_id (int): ID of the Content Replacement service

        Returns:
            Tuple: Number of slots successfully and unsuccessfully deleted
        """
        deleted = 0
        failed = 0
        for slot in self.slots.list(service_id):
            try:
                self.slots.delete(service_id, slot.id)
                deleted += 1
            except Exception:
                failed += 1
        return (deleted, failed)


@response_handler(postprocess_response)
class ContentReplacementServiceSlotsApi(BpkioSdkConsumer):
    @returns.json()
    @get("services/content-replacement/{service_id}/slots")
    def get_page(
        self,
        service_id,
        offset: Query = 0,
        limit: Query = 50,
        from_time: Query("from", type=datetime) = None,
        to_time: Query("to", type=datetime) = None,
        categories: Query(type=List[int]) = [],
    ) -> List[ContentReplacementSlot]:  # type: ignore
        """Get a (partial) list of Content Replacement slots"""

    @returns.json()
    @get("services/content-replacement/{service_id}/slots/{slot_id}")
    def retrieve(self, service_id, slot_id) -> ContentReplacementSlot:
        """Get a single Content Replacement slot, by ID"""

    @delete("services/content-replacement/{service_id}/slots/{slot_id}")
    def delete(self, service_id, slot_id):
        """Delete a Content Replacement slot, by ID"""

    @response_handler(return_count)
    @params({"offset": 0, "limit": 1})
    @get("services/content-replacement/{service_id}/slots")
    def count(
        self,
        service_id,
        from_time: Query("from", type=datetime) = None,
        to_time: Query("to", type=datetime) = None,
        categories: Query(type=List[int]) = [],
    ) -> int:  # type: ignore
        """Get a count of all Content Replacement slots"""

    def list(
        self,
        service_id: int,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
        categories: List[int] | None = [],
    ) -> List[ContentReplacementSlot]:
        """Get the full list of Content Replacement slots"""
        slots = get_all_with_pagination(
            self.get_page,
            service_id=service_id,
            from_time=from_time,
            to_time=to_time,
            categories=categories,
        )
        if categories is None:
            return [s for s in slots if s.category is None]
        else:
            return slots


# === VIRTUAL-CHANNEL SERVICES ===


@response_handler(postprocess_response)
class VirtualChannelServiceApi(BpkioSdkConsumer):
    def __init__(self, parent_api: ServicesApi, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)
        self.parent_api = parent_api

        self.slots = VirtualChannelServiceSlotsApi(base_url, **kwargs)

    @returns.json(Svc.VirtualChannelService)
    @get("services/virtual-channel/{service_id}")
    def retrieve(self, service_id):
        """Get a single Virtual Channel service, by ID"""

    @json
    @returns.json(Svc.VirtualChannelService)
    @post("services/virtual-channel")
    def create(
        self, service: Body(type=Svc.VirtualChannelServiceIn)  # type: ignore
    ) -> Svc.VirtualChannelService:  # type: ignore
        """Create a new Virtual Channel service"""

    @json
    @returns.json(Svc.VirtualChannelService)
    @put("services/virtual-channel/{service_id}")
    def update(self, service_id: int, service: Body(type=Svc.VirtualChannelServiceIn)) -> Svc.VirtualChannelService:  # type: ignore
        """Update a Virtual Channel service"""

    def upsert(
        self, service: Svc.VirtualChannelServiceIn, if_exists: str = "retrieve"
    ) -> Tuple[Svc.VirtualChannelService, UpsertOperationType]:
        """Conditionally create, retrieve or update a Virtual Channel service"""
        return self.parent_api.upsert(
            service, unique_fields=["url"], if_exists=if_exists
        )

    @delete("services/virtual-channel/{service_id}")
    def delete(self, service_id: int):
        """Delete a Virtual Channel service, by ID"""

    def pause(self, service_id: int):
        """Pause a Virtual Channel service, by ID"""
        return self.parent_api.pause(service_id)

    def unpause(self, service_id: int):
        """Unpause a Virtual Channel service, by ID"""
        return self.parent_api.unpause(service_id)

    @cache_api_results("list_vcs")
    def list(self) -> List[Svc.VirtualChannelService]:
        """List all Virtual Channel services"""
        sparse_vcs = self.parent_api.search(
            Svc.ServiceType.VIRTUAL_CHANNEL, field="type", method=SearchMethod.STRICT
        )
        return collect_from_ids(ids=[vc.id for vc in sparse_vcs], get_fn=self.retrieve)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Svc.VirtualChannelService]:
        """Searches the list of Virtual Channel services for those matching a particular filter query"""
        if not filters:
            filters = [(value, field, method)]

        services = self.list()
        return search_array_with_filters(services, filters=filters)

    def clear(self, service_id):
        """Delete all Virtual Channel slots, for a given service

        Args:
            service_id (int): ID of the Content Replacement service

        Returns:
            Tuple: Number of slots successfully and unsuccessfully deleted
        """
        deleted = 0
        failed = 0
        for slot in self.slots.list(service_id):
            try:
                self.slots.delete(service_id, slot.id)
                deleted += 1
            except Exception:
                failed += 1
        return (deleted, failed)


@response_handler(postprocess_response)
class VirtualChannelServiceSlotsApi(BpkioSdkConsumer):
    @returns.json()
    @get("services/virtual-channel/{service_id}/slots")
    def get_page(
        self,
        service_id,
        offset: Query = 0,
        limit: Query = 50,
        from_time: Query("from", type=datetime) = None,
        to_time: Query("to", type=datetime) = None,
        categories: Query(type=List[int]) = [],
    ) -> List[VirtualChannelSlot]:  # type: ignore
        """Get a (partial) list of Virtual Channel slots"""

    @returns.json()
    @get("services/virtual-channel/{service_id}/slots/{slot_id}")
    def retrieve(self, service_id, slot_id) -> VirtualChannelSlot:
        """Get a single Virtual Channel slot, by ID"""

    @json
    @returns.json(VirtualChannelSlot)
    @post("services/virtual-channel/{service_id}/slots")
    def create(
        self, service_id, service: Body(type=VirtualChannelSlotIn)  # type: ignore
    ) -> VirtualChannelSlot:  # type: ignore
        """Create a new Virtual Channel slot"""

    @delete("services/virtual-channel/{service_id}/slots/{slot_id}")
    def delete(self, service_id, slot_id):
        """Delete a Virtual Channel slot, by ID"""

    @response_handler(return_count)
    @params({"offset": 0, "limit": 1})
    @get("services/virtual-channel/{service_id}/slots")
    def count(
        self,
        service_id,
        from_time: Query("from", type=datetime) = None,
        to_time: Query("to", type=datetime) = None,
        categories: Query(type=List[int]) = [],
    ) -> int:  # type: ignore
        """Get a count of all Virtual Channel slots"""

    def list(
        self,
        service_id: int,
        from_time: datetime = None,
        to_time: datetime = None,
        categories: List[int] | None = [],
    ) -> List[VirtualChannelSlot]:
        """Get the full list of Virtual Channel slots"""
        slots = get_all_with_pagination(
            self.get_page,
            service_id=service_id,
            from_time=from_time,
            to_time=to_time,
            categories=categories,
        )
        if categories is None:
            return [s for s in slots if s.category is None]
        else:
            return slots


# === AD-INSERTION SERVICES ===


@response_handler(postprocess_response)
class AdInsertionServiceApi(BpkioSdkConsumer):
    def __init__(self, parent_api: ServicesApi, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)
        self.parent_api = parent_api

    @returns.json(Svc.AdInsertionService)
    @get("services/ad-insertion/{service_id}")
    def retrieve(self, service_id):
        """Get a single Ad Insertion service, by ID"""

    @json
    @returns.json(Svc.AdInsertionService)
    @post("services/ad-insertion")
    def create(
        self, service: Body(type=Svc.AdInsertionServiceIn)  # type: ignore
    ) -> Svc.AdInsertionService:  # type: ignore
        """Create a new Ad Insertion service"""

    @json
    @returns.json(Svc.AdInsertionService)
    @put("services/ad-insertion/{service_id}")
    def update(self, service_id: int, service: Body(type=Svc.AdInsertionServiceIn)) -> Svc.AdInsertionService:  # type: ignore
        """Update an Ad Insertion service"""

    def upsert(
        self, service: Svc.AdInsertionServiceIn, if_exists: str = "retrieve"
    ) -> Tuple[Svc.AdInsertionService, UpsertOperationType]:
        """Conditionally create, retrieve or update an Ad Insertion service"""
        return self.parent_api.upsert(
            service, unique_fields=["url"], if_exists=if_exists
        )

    @delete("services/ad-insertion/{service_id}")
    def delete(self, service_id: int):
        """Delete an Ad Insertion service, by ID"""

    def pause(self, service_id: int):
        """Pause an Ad Insertion service, by ID"""
        return self.parent_api.pause(service_id)

    def unpause(self, service_id: int):
        """Unpause an Ad Insertion service, by ID"""
        return self.parent_api.unpause(service_id)

    @cache_api_results("list_dai")
    def list(self) -> List[Svc.AdInsertionService]:
        """List all Ad Insertion services"""
        sparse_vcs = self.parent_api.search(
            Svc.ServiceType.AD_INSERTION, field="type", method=SearchMethod.STRICT
        )
        return collect_from_ids(ids=[vc.id for vc in sparse_vcs], get_fn=self.retrieve)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Svc.AdInsertionService]:
        """Searches the list of Ad Insertion services for those matching a particular filter query"""
        if not filters:
            filters = [(value, field, method)]

        services = self.list()
        return search_array_with_filters(services, filters=filters)


# === ADADTIVE-STREAMING-CDN SERVICES ===


@response_handler(postprocess_response)
class AdaptiveStreamingCdnServiceApi(BpkioSdkConsumer):
    def __init__(self, parent_api: ServicesApi, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)
        self.parent_api = parent_api

    @returns.json(Svc.AdaptiveStreamingCdnService)
    @get("services/adaptive-streaming-cdn/{service_id}")
    def retrieve(self, service_id):
        """Get a single Adaptive Streaming CDN service, by ID"""

    @json
    @returns.json(Svc.AdaptiveStreamingCdnService)
    @post("services/adaptive-streaming-cdn")
    def create(
        self, service: Body(type=Svc.AdaptiveStreamingCdnServiceIn)  # type: ignore
    ) -> Svc.AdaptiveStreamingCdnService:  # type: ignore
        """Create a new Adaptive Streaming CDN service"""

    @json
    @returns.json(Svc.AdaptiveStreamingCdnService)
    @put("services/adaptive-streaming-cdn/{service_id}")
    def update(self, service_id: int, service: Body(type=Svc.AdaptiveStreamingCdnServiceIn)) -> Svc.AdaptiveStreamingCdnService:  # type: ignore
        """Update an Adaptive Streaming CDN service"""

    def upsert(
        self, service: Svc.AdaptiveStreamingCdnServiceIn, if_exists: str = "retrieve"
    ) -> Tuple[Svc.AdaptiveStreamingCdnService, UpsertOperationType]:
        """Conditionally create, retrieve or update an Adaptive Streaming CDN service"""
        return self.parent_api.upsert(
            service, unique_fields=["url"], if_exists=if_exists
        )

    @delete("services/adaptive-streaming-cdn/{service_id}")
    def delete(self, service_id: int):
        """Delete an Adaptive Streaming CDN service, by ID"""

    def pause(self, service_id: int):
        """Pause an Adaptive Streaming CDN service, by ID"""
        return self.parent_api.pause(service_id)

    def unpause(self, service_id: int):
        """Unpause an Adaptive Streaming CDN service, by ID"""
        return self.parent_api.unpause(service_id)

    @cache_api_results("list_ascdn")
    def list(self) -> List[Svc.AdaptiveStreamingCdnService]:
        """List all Adaptive Streaming CDN services"""
        sparse_vcs = self.parent_api.search(
            Svc.ServiceType.ADAPTIVE_STREAMING_CDN,
            field="type",
            method=SearchMethod.STRICT,
        )
        return collect_from_ids(ids=[vc.id for vc in sparse_vcs], get_fn=self.retrieve)

    def search(
        self,
        value: Any | None = None,
        field: str | None = None,
        method: SearchMethod = SearchMethod.STRING_SUB,
        filters: List[Tuple[Any, str | None, SearchMethod | None]] | None = None,
    ) -> List[Svc.AdaptiveStreamingCdnService]:
        """Searches the list of Adaptive Streaming CDN services for those matching a particular filter query"""
        if not filters:
            filters = [(value, field, method)]

        services = self.list()
        return search_array_with_filters(services, filters=filters)
