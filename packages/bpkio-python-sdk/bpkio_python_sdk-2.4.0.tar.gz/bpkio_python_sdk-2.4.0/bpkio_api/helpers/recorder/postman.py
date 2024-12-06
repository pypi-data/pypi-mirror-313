import json
import re
import uuid
from typing import List
from urllib.parse import urlparse

from requests import PreparedRequest, Response

from .exporter import SessionExporter
from .session_items import (SessionComment, SessionItem,
                            SessionRequestResponse, SessionSection)


class PostmanExporter(SessionExporter):
    def __init__(
        self,
        session_id: str,
        **kwargs,
    ) -> None:
        super().__init__(
            session_id=session_id,
            **kwargs,
        )

        self.vars = dict()

    def export(self, session: List[SessionItem], collection_name=None):
        """
        Converts a list of requests.Response to a Postman collection.

        :param requests: list[requests.PreparedRequest]
        :param collection_name: str The name of the Postman collection.
        :return: dict Postman collection
        """
        items = self.filter_session_items(session)

        if not collection_name:
            collection_name = "bpkio Session: " + self.session_id

        outputs = []
        curr_section = outputs
        output_contains_sections = False
        for item in items:
            match item:
                case SessionRequestResponse():
                    output = self._request_to_postman_item(item.request, item.response)
                    curr_section.append(output)
                case SessionSection():
                    # If this is the first section, and the outputs already contain items,
                    # we need to create an unnamed section to put the items in.
                    if not output_contains_sections and len(outputs) > 0:
                        section_item = dict(name="(Unnamed section)", item=outputs)
                        outputs = [section_item]
                        output_contains_sections = True

                    section_item = dict(
                        name=item.title, description=item.description, item=list()
                    )
                    outputs.append(section_item)
                    # switch pointer to section's list
                    curr_section = section_item["item"]
                    pass
                case SessionComment():
                    pass
                case _:
                    raise ValueError(f"Unknown item type: {item}")

        # Remove empty sections
        if output_contains_sections:
            outputs = [output for output in outputs if len(output["item"]) > 0]

        collection = {
            "info": {
                "_postman_id": str(uuid.uuid4()),
                "name": collection_name,
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
            },
            "item": outputs,
            "variable": self._define_variables(),
        }

        return json.dumps(collection, indent=2)

    def _request_to_postman_item(
        self, req: PreparedRequest, res: Response | None = None
    ):
        """
        Converts a PreparedRequest to a Postman collection item.

        :param req: requests.PreparedRequest
        :return: dict Postman collection item
        """
        body = {}
        auth = {}

        # Extract Bearer token from Authorization header
        authorization = req.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            # extract token as variable
            token = authorization[7:]
            var_name = self._turn_to_variable("API_KEY", token)

            auth = {
                "type": "bearer",
                "bearer": [
                    {"key": "token", "value": "{{%s}}" % var_name, "type": "string"}
                ],
            }

        for h in ["User-Agent", "Authorization"]:
            del req.headers[h]

        headers = [
            {"key": k, "value": v, "description": ""} for k, v in req.headers.items()
        ]

        # Extract FQDN from URL
        parsed_url = urlparse(req.url)
        fqdn = parsed_url.netloc
        var_name = self._turn_to_variable("HOST", fqdn)

        url = req.url.replace(str(fqdn), "{{%s}}" % var_name)

        name = re.sub(r"^.*{}".format(fqdn), "", req.url)  # type: ignore

        # Convert body to json if it exists
        if req.body:
            body = {
                "mode": "raw",
                "raw": json.dumps(json.loads(req.body.decode()), indent=2),
                "options": {"raw": {"language": "json"}},
            }

        request = {
            "method": req.method,
            "header": headers,
            "body": body,
            "url": url,
            "description": "",
            "auth": auth if auth else None,
        }

        # Prepare response if it exists
        response = []
        if res and self.has_flag("include_response"):
            response = [
                {
                    "name": "Response",
                    "originalRequest": request,
                    "status": res.reason,
                    "code": res.status_code,
                    "header": [
                        {"key": k, "value": v, "description": ""}
                        for k, v in res.headers.items()
                    ],
                    "body": json.dumps(res.json(), indent=2) if res.text else "",
                    "_postman_previewlanguage": "json",
                }
            ]

        item = {
            "name": name,
            "request": request,
            "response": response,
        }

        return item

    def _turn_to_variable(self, name: str, value) -> str:
        var_name = self.vars.get(value)
        if not var_name:
            count = len([k for k in self.vars.values() if k.startswith(name)])
            var_name = f"{name}{count}" if count > 0 else name
            self.vars[value] = var_name
        return var_name

    def _define_variables(self) -> List:
        variables = []
        for v, k in self.vars.items():
            if self.has_flag("remove_secrets"):
                if k.startswith("API_KEY"):
                    v = "YOUR_" + k
            variables.append({"key": k, "value": v})

        return variables
