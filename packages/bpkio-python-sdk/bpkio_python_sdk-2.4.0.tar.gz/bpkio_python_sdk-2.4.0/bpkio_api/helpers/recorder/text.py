import re
from typing import List

from requests import PreparedRequest

from .exporter import SessionExporter
from .session_items import (SessionComment, SessionItem,
                            SessionRequestResponse, SessionSection)


class TextExporter(SessionExporter):
    def __init__(
        self,
        session_id: str,
        **kwargs,
    ) -> None:
        super().__init__(
            session_id=session_id,
            **kwargs,
        )

    def export(self, session: List[SessionItem]):
        items = self.filter_session_items(session)
        outputs = []
        for item in items:
            match item:
                case SessionSection():
                    outputs.append("# " + item.title)
                    outputs.append("## " + item.description)

                case SessionComment():
                    outputs.append(item.comment)

                case SessionRequestResponse():
                    out = request_to_text(item.request)

                    if self.has_flag("include_response"):
                        out += " --> {s}".format(s=item.response.status_code)

                    outputs.append(out)

        return "\n".join(outputs)


def request_to_text(req: PreparedRequest, compact=False):
    if compact:
        #  strip out the protocol and domain
        url = re.sub(r"http.*?://[^/]+", "", req.url)
    else:
        url = req.url

    string = "{m} {u}".format(m=req.method, u=url)

    return string
