import requests
import uplink
from bpkio_api.constants import api_client


class BpkioSdkConsumer(uplink.Consumer):
    def __init__(self, base_url="", verify_ssl=True, **kwargs):
        self.verify_ssl = verify_ssl
        s = requests.Session()
        s.verify = verify_ssl

        # Hide warnings about InsecureRequestWarning (from not validating SSL self-signed certificates)
        if verify_ssl is False:
            requests.packages.urllib3.disable_warnings()

        super().__init__(base_url, client=s, **kwargs)

        # Set headers for all requests of the instance.
        client_string = api_client
        if "api_client" in kwargs:
            self.api_client = kwargs.get("api_client")
            client_string = kwargs.get("api_client") + " " + api_client
            self.session.headers["x-api-client"] = client_string
        else:
            self.api_client = ""

        if "user_agent" in kwargs:
            self.user_agent = kwargs.get("user_agent")
            self.session.headers["User-Agent"] = kwargs.get("user_agent")
        else:
            self.user_agent = ""
