from datetime import datetime
from typing import Optional

from bpkio_api.models.common import NamedModel
from pydantic import PrivateAttr


class Tenant(NamedModel):
    id: Optional[int] = None

    email: Optional[str]
    # TODO - Turn to enum
    commercialPlan: str
    # TODO - Turn to enum
    state: str
    sendAnalytics: Optional[bool] = False
    creationDate: datetime
    updateDate: datetime
    subscriptionDate: Optional[datetime]
    expirationDate: Optional[datetime]

    _fqdn: str = PrivateAttr()
