from bpkio_api.consumer import BpkioSdkConsumer
from bpkio_api.models.Consumption import ConsumptionData
from bpkio_api.response_handler import postprocess_response
from uplink import Query, get, response_handler, returns


@response_handler(postprocess_response)
class ConsumptionApi(BpkioSdkConsumer):
    def __init__(self, base_url="", **kwargs):
        super().__init__(base_url, **kwargs)

    @returns.json()
    @get("consumption")
    def retrieve(
        self,
        start_time: Query("start-time"),  # type: ignore
        end_time: Query("end-time"),  # type: ignore
        tenant: Query("tenantId"),
    ) -> ConsumptionData:  # type: ignore
        """Get the consumption data between 2 dates"""
