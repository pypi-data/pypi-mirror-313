from .module_imports import key
from uplink import (
    Consumer,
    get as http_get,
    returns,
    headers,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class _Warranty_Assessments(Consumer):
    """Inteface to warranty assessments resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("warranties/assessments")
    def list(
        self,
        machine_uid: Query = None,
        brand: Query = None,
    ):
        """This call will return warranty assessments information for the specified criteria."""
