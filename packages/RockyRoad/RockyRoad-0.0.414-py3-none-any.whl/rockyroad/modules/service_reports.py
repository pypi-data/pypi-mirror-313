from .module_imports import key
from uplink import (
    Consumer,
    get as http_get,
    post,
    patch,
    delete,
    returns,
    headers,
    Body,
    json,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class Service_Reports(Consumer):
    """Inteface to service reports resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("services/reports")
    def list(
        self,
        service_report_uid: Query = None,
        machine_uid: Query = None,
        model: Query = None,
        serial: Query = None,
        account: Query = None,
        account_uid: Query = None,
    ):
        """This call will return service report information for the specified criteria."""

    @returns.json
    @delete("services/reports")
    def delete(self, uid: Query):
        """This call will delete the service report information for the specified uid."""

    @returns.json
    @json
    @post("services/reports")
    def insert(self, service_report: Body):
        """This call will create service report information with the specified parameters."""

    @returns.json
    @json
    @patch("services/reports")
    def update(self, service_report: Body):
        """This call will update the service report information with the specified parameters."""
