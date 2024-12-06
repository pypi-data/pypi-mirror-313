from abc import ABC, abstractmethod
from typing import List

from .session_items import (SessionComment, SessionRequestResponse,
                            SessionSection)


class SessionExporter(ABC):
    @abstractmethod
    def __init__(self, session_id: str, **kwargs) -> None:
        super().__init__()
        self.session_id = session_id
        self.flags = kwargs

    @abstractmethod
    def export(self, session: list) -> None:
        pass

    def filter_session_items(self, session) -> List:
        # Cleanup and remove unnecessary ones
        items = []
        for item in session:
            filtered_out = False
            
            if isinstance(item, SessionRequestResponse):
                if item.request.method == "GET":
                    if not self.flags.get("include_get", True):
                        filtered_out = True
                    if isinstance(item.response.json(), list):
                        if not self.flags.get("include_list", False):
                            filtered_out = True
                            
            if filtered_out:
                # Remove any preceding comments that may already have been added
                while items and isinstance(items[-1], (SessionComment, SessionSection)):
                    items.pop()
                
                continue
            items.append(item)
        return items

    def has_flag(self, flag):
        return self.flags.get(flag, False)
