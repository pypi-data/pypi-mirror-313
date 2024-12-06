from enum import Enum
from typing import List, Literal, Optional
from urllib.parse import urljoin

from media_muncher.format import MediaFormat
from pydantic import AnyHttpUrl, BaseModel, IPvAnyAddress

from .common import BaseResource, NamedModel, PropertyMixin, WithDescription

# Tuple(BkYou var name, description, bpkio var name)
ADSERVER_SYSTEM_VALUES = [
    ("$MMVAR_CACHE_BUSTER", "Cachebuster value", "$CACHE_BUSTER"),
    (
        "$MAP_REMOTE_ADDR",
        "Client IP address (from header 'X-Forwarded-For')",
        "$REMOTE_ADDRESS",
    ),
    (
        "$_MMVAR_LIVEAR_SIGNALID",
        "Signal ID (from the SCTE35 marker)",
        "$LIVE_AR_SIGNALID",
    ),
    ("$_MMVAR_LIVEAR_UPID", "UPID (from the SCTE35 marker)", "$LIVE_AR_UPID"),
    ("$_MMVAR_LIVEAR_SLOTDURATION", "Slot duration (in seconds)", "$AD_BREAK_DURATION"),
    (
        "${_MMVAR_LIVEAR_SLOTDURATION}000",
        "Slot duration (in microseconds)",
        "$AD_BREAK_DURATION_MS",
    ),
]


class SourceType(Enum):
    AD_SERVER = "ad-server"
    ASSET = "asset"
    ASSET_CATALOG = "asset-catalog"
    LIVE = "live"
    SLATE = "slate"
    ORIGIN = "origin"

    def __str__(self):
        return str(self.value)


# === SOURCES Models ===


class SourceIn(NamedModel, PropertyMixin):
    url: Optional[AnyHttpUrl | str] = None

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, *args, **kwargs):
        return self.url


class SourceSparse(SourceIn, BaseResource):
    type: SourceType
    format: Optional[MediaFormat] = None


class OriginCustomHeaders(BaseModel):
    name: str
    value: str


class OriginConfig(BaseModel):
    customHeaders: List[OriginCustomHeaders] = []


# === ASSET SOURCE Models ===


class AssetSourceIn(SourceIn, WithDescription):
    backupIp: Optional[IPvAnyAddress] = None
    origin: Optional[OriginConfig] = None

    def is_live(self):
        return False


class AssetSource(AssetSourceIn, BaseResource):
    format: Optional[MediaFormat]
    type: Literal["asset"]

    # @property
    # def type(self):
    #     return SourceType.ASSET


# === LIVE SOURCE Models ===


class LiveSourceIn(SourceIn, WithDescription):
    backupIp: Optional[IPvAnyAddress] = None
    origin: Optional[OriginConfig] = None
    multiPeriod: bool = False

    def is_live(self):
        return True


class LiveSource(LiveSourceIn, BaseResource):
    format: Optional[MediaFormat]

    @property
    def type(self):
        return SourceType.LIVE


# === ASSET CATALOG SOURCE Models ===


class AssetCatalogSourceIn(SourceIn, WithDescription):
    backupIp: Optional[IPvAnyAddress] = None
    # TODO - add type and/or validator for path
    assetSample: str
    origin: Optional[OriginConfig] = None

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, extra=None, *args, **kwargs):
        u = self.url
        if extra:
            u = urljoin(u, extra)
        else:
            u = urljoin(u, self.assetSample)
        return u

    def is_live(self):
        return False


class AssetCatalogSource(AssetCatalogSourceIn, BaseResource):
    @property
    def type(self):
        return SourceType.ASSET_CATALOG


# === AD SERVER SOURCE Models ===


class AdServerQueryParameterType(str, Enum):
    from_query_parameter = "from-query-parameter"
    from_header = "from-header"
    from_variable = "from-variable"
    forward = "forward"
    custom = "custom"


class AdServerQueryParameter(BaseModel):
    name: str
    type: AdServerQueryParameterType
    value: Optional[str] = None

    def as_string(self):
        if self.type == AdServerQueryParameterType.from_query_parameter:
            return f"{self.name}=$arg_{self.value}"
        elif self.type == AdServerQueryParameterType.from_header:
            return f"{self.name}=$http_{self.value.lower().replace('-','_')}"
        elif self.type == AdServerQueryParameterType.from_variable:
            return f"{self.name}={self.value}"
        elif self.type == AdServerQueryParameterType.forward:
            return f"{self.name}=$FORWARD"
        elif self.type == AdServerQueryParameterType.custom:
            return f"{self.name}={self.value}"
        else:
            raise ValueError(f"Unknown AdServerQueryParameterType: {self.type}")

    def is_from_variable(self):
        return self.type == AdServerQueryParameterType.from_variable or (
            self.type == AdServerQueryParameterType.custom
            and self.value.startswith("$")
            and not self.value.startswith("$arg_")
            and not self.value.startswith("$http_")
        )

    def is_from_query_parameter(self):
        return self.type == AdServerQueryParameterType.from_query_parameter or (
            self.type == AdServerQueryParameterType.custom
            and self.value.startswith("$arg_")
        )

    def is_from_header(self):
        return self.type == AdServerQueryParameterType.from_header or (
            self.type == AdServerQueryParameterType.custom
            and self.value.startswith("$http_")
        )

    def is_forwarded(self):
        return self.type == AdServerQueryParameterType.forward

    def is_custom(self):
        return (
            not self.is_forwarded()
            and not self.is_from_header()
            and not self.is_from_variable()
            and not self.is_from_query_parameter()
        )


class AdServerSourceIn(SourceIn, WithDescription):
    # TODO - add type and/or validator for queries
    queries: Optional[str]
    template: Optional[str]
    queryParameters: Optional[List[AdServerQueryParameter]] = []
    adOrigin: Optional[OriginConfig] = None

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, *args, **kwargs):
        u = self.url
        if self.queryParameters:
            qpStrings = [qp.as_string() for qp in self.queryParameters]
            u = u + "?" + "&".join(qpStrings)
        return u

    def is_live(self):
        return False


class AdServerSource(AdServerSourceIn, BaseResource):
    @property
    def type(self):
        return SourceType.AD_SERVER


# === SLATE SOURCE Models ===


class SlateSourceIn(SourceIn, WithDescription):
    def is_live(self):
        return False


class SlateSource(SlateSourceIn, BaseResource):
    format: Optional[MediaFormat]
    type: Literal["slate"]

    # @property
    # def type(self):
    #     return SourceType.SLATE


# === ORIGIN SOURCE Models ===


class OriginSourceIn(SourceIn, WithDescription):
    pass


class OriginSource(OriginSourceIn, BaseResource):
    type: Literal["origin"]


# === CHECK RESULTS Model ===


class SourceStatusCheck(BaseModel):
    url: AnyHttpUrl
    origin: Optional[OriginConfig] = None


class SourceStatusCheckResult(BaseModel):
    sourceStatus: str
    sourceInfo: object
    errors: list
    warnings: list
    format: Optional[MediaFormat] = None

    class Config:
        use_enum_values = True
