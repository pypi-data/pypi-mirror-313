# coding: utf-8
import json
import sys

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote

from typing import List

from requests import PreparedRequest, Response

from .exporter import SessionExporter
from .session_items import (SessionComment, SessionItem,
                            SessionRequestResponse, SessionSection)


class CurlExporter(SessionExporter):
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
                case SessionRequestResponse():
                    output = self._request_to_curl_string(item.request, item.response)
                    outputs.append(output)
                case SessionSection():
                    outputs.append(f"### {item.title}")
                    outputs.append(f"# {item.description}")
                case SessionComment():
                    outputs.append(f"# {item.comment}")
                case _:
                    pass

        return "\n\n".join(outputs)

    def _request_to_curl_string(
        self, req: PreparedRequest, res: Response | None = None
    ):
        """
        Converts a PreparedRequest to a cURL command.

        :param req: requests.PreparedRequest
        :return: dict Postman collection item
        """

        for h in ["User-Agent", "Content-Length"]:
            try:
                del req.headers[h]
            except KeyError:
                pass

        if self.has_flag("remove_secrets"):
            if "Authorization" in req.headers:
                req.headers["Authorization"] = "Bearer YOUR_API_KEY"

        curl_string = request_to_curl(req, compact=self.has_flag("compact"))

        if self.has_flag("include_response") and res:
            res_output = []

            res_output.append(f"\n-> [{res.status_code}]")

            if res.text:
                response_json = res.json()
                if not self.has_flag("compact"):
                    response_json = json.dumps(response_json, indent=4)
                res_output.append(f" {response_json}")

            if self.has_flag("compact"):
                curl_string += " ".join(res_output)
            else:
                curl_string += "\n".join(res_output)

        return curl_string


def request_to_curl(request, compressed=False, verify=True, compact=False):
    """
    Returns string with curl command by provided request object

    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    """

    parts = [
        ("curl", None),
        ("-X", request.method),
    ]

    for k, v in sorted(request.headers.items()):
        parts += [("-H", "{0}: {1}".format(k, v))]

    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        parts += [("-d", body)]

    if compressed:
        parts += [("--compressed", None)]

    if not verify:
        parts += [("--insecure", None)]

    parts += [(None, request.url)]

    flat_parts = []
    for i, (k, v) in enumerate(parts):
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))
        if not compact:
            flat_parts.append("\\\n") if i < len(parts) - 1 else None

    return " ".join(flat_parts)
