from datetime import datetime

from pydantic import BaseModel


class ConsumptionData(BaseModel):
    tenantId: int
    startTime: datetime
    endTime: datetime
    egress: int
    virtualChannel: int
    contentReplacement: int
    insertedAds: int

    @property
    def days(self):
        return (self.endTime - self.startTime).days
