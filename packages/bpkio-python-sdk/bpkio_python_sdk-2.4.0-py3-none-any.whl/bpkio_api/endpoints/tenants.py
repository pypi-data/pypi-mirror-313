from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.models.Tenants import Tenant
from bpkio_api.response_handler import postprocess_response
from uplink import get, response_handler, returns


@response_handler(postprocess_response)
class TenantsApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json(Tenant)
    @get("tenants/me")
    def retrieve_self(self) -> Tenant:
        """Get the tenant information for the current user"""
