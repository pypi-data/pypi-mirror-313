from datetime import datetime
from typing import Optional

from bpkio_api.models.common import BaseResource


class User(BaseResource):
    firstName: str
    lastName: str
    email: str
    tenantId: Optional[int]

    creationDate: datetime
    updateDate: datetime

    @property
    def name(self):
        return "{} {}".format(self.firstName, self.lastName)
