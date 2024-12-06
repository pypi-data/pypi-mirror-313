import json
from typing import List

from requests import PreparedRequest, Response

from .curl import request_to_curl
from .exporter import SessionExporter
from .session_items import (SessionComment, SessionItem,
                            SessionRequestResponse, SessionSection)
from .text import request_to_text


class MarkdownExporter(SessionExporter):
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
        """
        Converts a list of requests.Response to a readable list of commands.

        :param requests: list[requests.PreparedRequest]
        :return: str
        """

        items = self.filter_session_items(session)

        outputs = []
        outputs.append("# Session: " + self.session_id)

        for item in items:
            match item:
                case SessionRequestResponse():
                    outputs.append(self._summarize_request(item.request, item.response))
                case SessionSection():
                    outputs.append(f"## {item.title}")
                    outputs.append(item.description) if item.description else None
                case SessionComment():
                    outputs.append(item.comment)
                case _:
                    continue

        return "\n".join(outputs)

    def _summarize_request(self, req: PreparedRequest, res: Response | None = None):
        """
        Converts a PreparedRequest to a cURL command.

        :param req: requests.PreparedRequest
        :return: dict Postman collection item
        """

        output = []

        output.append("\n### " + request_to_text(req, compact=True))

        for h in ["User-Agent", "Content-Length"]:
            try:
                del req.headers[h]
            except KeyError:
                pass

        if self.has_flag("remove_secrets"):
            if "Authorization" in req.headers:
                req.headers["Authorization"] = "Bearer YOUR_API_KEY"

        curl_string = request_to_curl(req, compact=False)
        output.append(f"```bash\n{curl_string}\n```")

        if self.has_flag("include_response") and res:
            output.append(f"--> response (HTTP {res.status_code})")
            if res.text:
                response_json = json.dumps(res.json(), indent=4)
                output.append(f"```json\n{response_json}\n```")

        return "\n".join(output)
