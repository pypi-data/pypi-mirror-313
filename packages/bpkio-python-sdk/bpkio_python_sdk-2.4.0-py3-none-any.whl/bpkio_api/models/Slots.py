from datetime import datetime
from enum import Enum
from typing import Optional

from bpkio_api.helpers.times import relative_time
from bpkio_api.models.common import BaseResource
from bpkio_api.models.Sources import SourceSparse
from pydantic import BaseModel


class VirtualChannelSlotType(Enum):
    CONTENT = "content"
    AD_BREAK = "ad-break"

    def __str__(self):
        return str(self.value)


class SlotBaseModel(BaseModel):
    name: Optional[str] = None
    startTime: datetime
    endTime: Optional[datetime] = None
    duration: Optional[float] = None

    @property
    def relativeStartTime(self):
        return relative_time(self.startTime)

    @property
    def relativeEndTime(self):
        return relative_time(self.endTime) if self.endTime else None


class VirtualChannelSlotBase(SlotBaseModel):
    pass


class VirtualChannelSlotIn(VirtualChannelSlotBase):
    # TODO - ensure that if type is AD_BREAK, replacement is not None
    replacement: Optional[BaseResource] = None
    category: Optional[BaseResource] = None
    type: VirtualChannelSlotType = VirtualChannelSlotType.CONTENT


class VirtualChannelSlot(BaseResource, VirtualChannelSlotBase):
    replacement: Optional[SourceSparse] = None
    category: BaseResource | None
    type: VirtualChannelSlotType = VirtualChannelSlotType.CONTENT


class ContentReplacementSlotBase(SlotBaseModel):
    pass


class ContentReplacementSlotIn(ContentReplacementSlotBase):
    replacement: BaseResource
    category: BaseResource | None


class ContentReplacementSlot(BaseResource, ContentReplacementSlotBase):
    replacement: SourceSparse
    category: BaseResource | None



