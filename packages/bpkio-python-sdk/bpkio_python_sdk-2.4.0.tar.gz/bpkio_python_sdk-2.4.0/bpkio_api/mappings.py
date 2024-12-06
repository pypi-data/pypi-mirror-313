from __future__ import annotations

from typing import TYPE_CHECKING

import bpkio_api.models as m

if TYPE_CHECKING:
    from bpkio_api.api import BroadpeakIoApi
    from bpkio_api.models.common import BaseResource


def model_to_endpoint(api: BroadpeakIoApi, model: type):
    match model:
        case m.SourceSparse:
            return api.sources
        case m.AssetSource | m.AssetSourceIn:
            return api.sources.asset
        case m.LiveSource | m.LiveSourceIn:
            return api.sources.live
        case m.AssetCatalogSource | m.AssetCatalogSourceIn:
            return api.sources.asset_catalog
        case m.AdServerSource | m.AdServerSourceIn:
            return api.sources.ad_server
        case m.SlateSource | m.SlateSourceIn:
            return api.sources.slate
        case m.AdInsertionService | m.AdInsertionServiceIn:
            return api.services.ad_insertion
        case m.ContentReplacementService | m.ContentReplacementServiceIn:
            return api.services.content_replacement
        case m.VirtualChannelService | m.VirtualChannelServiceIn:
            return api.services.virtual_channel
        case m.Category | m.CategoryIn:
            return api.categories
        case m.ContentReplacementSlot:
            return api.services.content_replacement.slots
        case m.VirtualChannelSlot:
            return api.services.virtual_channel.slots
        case m.Tenant:
            return api.tenants
        case m.TranscodingProfile | m.TranscodingProfileIn | m.TranscodingProfileId:
            return api.transcoding_profiles
        case m.ConsumptionData:
            return api.consumption
        case m.User:
            return api.users
        case _:
            raise Exception(f"No endpoint found for model {model.__name__}")


MODELS_OUT_IN = [
    (m.AssetSource, m.AssetSourceIn),
    (m.LiveSource, m.LiveSourceIn),
    (m.AdServerSource, m.AdServerSourceIn),
    (m.AssetCatalogSource, m.AssetCatalogSourceIn),
    (m.SlateSource, m.SlateSourceIn),
    (m.ContentReplacementService, m.ContentReplacementServiceIn),
    (m.VirtualChannelService, m.VirtualChannelServiceIn),
    (m.AdInsertionService, m.AdInsertionServiceIn),
    (m.Category, m.CategoryIn),
    (m.TranscodingProfile, m.TranscodingProfileIn),
    (m.ServiceSparse, m.ServiceIn),
    (m.SourceSparse, m.SourceIn),
]


def _model_to_input_model(model: type):
    return next(i for (o, i) in MODELS_OUT_IN if o == model)


def to_input_model(resource: BaseResource):
    in_model = _model_to_input_model(type(resource))
    in_obj = in_model.parse_obj(resource.dict())
    return in_obj


def type_to_model(type_: str):
    match type_:
        case "virtual-channel":
            return m.VirtualChannelService
        case "content-replacement":
            return m.ContentReplacementService
        case "ad-insertion":
            return m.AdInsertionService

        case _:
            raise Exception(f"No model found for type {type_}")
