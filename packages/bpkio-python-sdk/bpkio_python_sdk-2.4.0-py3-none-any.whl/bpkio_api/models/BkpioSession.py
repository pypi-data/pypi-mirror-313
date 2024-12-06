from datetime import datetime
from typing import Any, Dict, Optional
from bpkio_api.models.common import PropertyMixin
from pydantic import BaseModel


class BpkioSession(BaseModel, PropertyMixin):
    id: str
    service_id: Optional[str]
    first_seen: datetime
    last_seen: Optional[datetime] = None
    context: str

    def get_all_fields_and_properties(self) -> Dict[str, Any]:
        d = super().get_all_fields_and_properties()
        d["hash"] = self.service_id
        d["sessionId"] = self.id
        return d
