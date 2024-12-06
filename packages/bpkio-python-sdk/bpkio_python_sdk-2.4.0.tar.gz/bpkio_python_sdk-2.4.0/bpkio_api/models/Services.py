import os
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

from bpkio_api.models.common import BaseResource, NamedModel, PropertyMixin
from media_muncher.format import MediaFormat
from bpkio_api.models.Sources import (
    AdServerSource,
    AssetSource,
    SlateSource,
    SourceSparse,
)
from bpkio_api.models.TranscodingProfiles import (
    TranscodingProfile,
    TranscodingProfileId,
)
from pydantic import BaseModel, HttpUrl


class ServiceType(Enum):
    AD_INSERTION = "ad-insertion"
    VIRTUAL_CHANNEL = "virtual-channel"
    CONTENT_REPLACEMENT = "content-replacement"
    ADAPTIVE_STREAMING_CDN = "adaptive-streaming-cdn"

    def __str__(self):
        return str(self.value)


def handle_service_id(url: str, move: bool):
    if not move:
        return url

    u_parts = urlparse(url)
    path_parts = u_parts.path.split("/")
    service_id = path_parts[1]
    new_path = "/".join(path_parts[2:])

    query_params = parse_qs(u_parts.query)
    query_params["bpkio_serviceid"] = service_id

    u_parts = u_parts._replace(path=new_path, query=urlencode(query_params, doseq=True))
    return urlunparse(u_parts)


# === SERVICES Models ===


class QueryManagement(BaseModel):
    addToMediaSegmentURI: Optional[List[str]] = []
    addToHLSMediaPlaylistURI: Optional[List[str]] = []
    forwardInOriginRequest: Optional[List[str]] = []


class UrlManagement(BaseModel):
    convertSourceSegmentToAbsoluteURI: Optional[bool] = False
    convertAdSegmentToAbsoluteURI: Optional[bool] = False
    sourceSegmentPrefix: Optional[str] = ""
    adSegmentPrefix: Optional[str] = ""


class AuthorizationHeader(BaseModel):
    name: str
    value: str


class AdvancedOptions(BaseModel):
    queryManagement: Optional[QueryManagement] = None
    urlManagement: Optional[UrlManagement] = None
    authorizationHeader: Optional[AuthorizationHeader] = None


class ServiceIn(NamedModel, PropertyMixin):
    tags: Optional[List[str]] = []
    state: str = "enabled"
    advancedOptions: Optional[AdvancedOptions]


class WithCommonServiceFields(BaseResource):
    url: HttpUrl
    creationDate: datetime
    updateDate: datetime

    advancedOptions: Optional[AdvancedOptions]

    @property
    def hash(self):
        return self.url.path.split("/")[1]

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, *args, **kwargs):
        return handle_service_id(self.url, move=kwargs.get("service_as_param"))

    @property
    def format(self):
        # Check the extension first
        ext = os.path.splitext(urlparse(self.url).path)[1]
        match ext:
            case ".m3u8":
                return MediaFormat.HLS
            case ".mpd":
                return MediaFormat.DASH

        # otherwise search for match in the URL
        if any(s in self.url for s in [".mpd", "dash"]):
            return MediaFormat.DASH
        if any(s in self.url for s in [".m3u8", "hls"]):
            return MediaFormat.HLS


class ServiceSparse(ServiceIn, WithCommonServiceFields):
    type: ServiceType


# === AD-INSERTION SERVICE Models ===


class VodAdInsertionModel(BaseModel):
    adServer: AdServerSource


class VodAdInsertionModelIn(BaseModel):
    adServer: BaseResource


class LiveAdReplacementModel(BaseModel):
    adServer: AdServerSource
    gapFiller: Optional[Union[SlateSource, AssetSource]] = None
    frenchAddressableTV: Optional[bool] = False
    maxAdDurationExcess: float = 1
    pastAdBreakReplacement: float = 0


class LiveAdReplacementModelIn(BaseModel):
    adServer: BaseResource
    gapFiller: Optional[BaseResource] = None
    frenchAddressableTV: Optional[bool] = False
    maxAdDurationExcess: float = 1
    pastAdBreakReplacement: float = 0


class AdBreakInsertionModel(BaseModel):
    adServer: AdServerSource
    gapFiller: Optional[Union[SlateSource, AssetSource]] = None


class AdBreakInsertionModelIn(BaseModel):
    adServer: BaseResource
    gapFiller: Optional[BaseResource] = None


class LiveAdPreRollModel(BaseModel):
    adServer: AdServerSource
    maxDuration: float = 360
    offset: float = 0


class LiveAdPreRollModelIn(BaseModel):
    adServer: BaseResource
    maxDuration: float = 360
    offset: float = 0


class ServerSideAdTracking(BaseModel):
    enable: Optional[bool] = False
    checkAdMediaSegmentAvailability: Optional[bool] = False


class WithCommonAdInsertionServiceFields(BaseModel):
    enableAdTranscoding: Optional[bool] = False
    serverSideAdTracking: ServerSideAdTracking
    transcodingProfile: Optional[TranscodingProfileId] = None

    @property
    def sub_type(self):
        enabled = []
        for prop in ["vodAdInsertion", "liveAdPreRoll", "liveAdReplacement"]:
            if getattr(self, prop):
                enabled.append(prop)
        return " + ".join(enabled)

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, extra=None, *args, **kwargs):
        u = handle_service_id(self.url, move=kwargs.get("service_as_param"))

        if extra:
            return urljoin(u, extra)

        return u

    def is_live(self):
        if getattr(self, "vodAdInsertion", None):
            return False
        else:
            return True


class AdInsertionServiceIn(ServiceIn, WithCommonAdInsertionServiceFields):
    # TODO: parse the specific sub-type of source
    source: BaseResource

    vodAdInsertion: Optional[VodAdInsertionModelIn] = None
    liveAdPreRoll: Optional[LiveAdPreRollModelIn] = None
    liveAdReplacement: Optional[LiveAdReplacementModelIn] = None


class AdInsertionService(
    WithCommonAdInsertionServiceFields, WithCommonServiceFields, ServiceIn
):
    # TODO: parse the specific sub-type of source
    source: SourceSparse

    vodAdInsertion: Optional[VodAdInsertionModel] = None
    liveAdPreRoll: Optional[LiveAdPreRollModel] = None
    liveAdReplacement: Optional[LiveAdReplacementModel] = None

    @property
    def type(self):
        return ServiceType.AD_INSERTION

    def main_source(self):
        return self.source


# === CONTENT-REPLACEMENT SERVICE Models ===


class ContentReplacementServiceIn(ServiceIn):
    # TODO: parse the specific sub-type of source
    source: BaseResource
    replacement: BaseResource

    def is_live(self):
        return True


class ContentReplacementService(WithCommonServiceFields, ServiceIn):
    source: SourceSparse
    replacement: SourceSparse

    @property
    def type(self):
        return ServiceType.CONTENT_REPLACEMENT

    def main_source(self):
        return self.source


# === VIRTUAL-CHANNEL SERVICE Models ===


class WithCommonVirtualChannelServiceFields(BaseModel):
    enableAdTranscoding: Optional[bool] = False
    serverSideAdTracking: Optional[ServerSideAdTracking] = None

    transcodingProfile: Optional[TranscodingProfileId] = None

    def is_live(self):
        return True


class VirtualChannelServiceIn(ServiceIn, WithCommonVirtualChannelServiceFields):
    # TODO: parse the specific sub-type of source
    baseLive: BaseResource

    adBreakInsertion: Optional[AdBreakInsertionModelIn] = None


class VirtualChannelService(
    WithCommonVirtualChannelServiceFields, WithCommonServiceFields, ServiceIn
):
    baseLive: SourceSparse

    adBreakInsertion: Optional[AdBreakInsertionModel] = None

    @property
    def type(self):
        return ServiceType.VIRTUAL_CHANNEL

    def main_source(self):
        return self.baseLive


# === ADAPTIVE-STREAMING-CDN SERVICE Models ===


class WithCommonAdaptiveStreamingCdnServiceFields(BaseResource):
    url: HttpUrl
    creationDate: datetime
    updateDate: datetime
    disableManifestCaching: bool


class AdaptiveStreamingCdnServiceIn(
    WithCommonAdaptiveStreamingCdnServiceFields, ServiceIn
):
    pass


class AdaptiveStreamingCdnService(
    WithCommonAdaptiveStreamingCdnServiceFields, ServiceIn
):

    @property
    def type(self):
        return ServiceType.ADAPTIVE_STREAMING_CDN
