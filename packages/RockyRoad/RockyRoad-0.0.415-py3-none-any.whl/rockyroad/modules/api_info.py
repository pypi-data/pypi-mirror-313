from .module_imports import key
from uplink import (
    get as http_get,
    Consumer,
    returns,
    headers,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class _API_Info(Consumer):
    """Inteface to API Info resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("health")
    def health(self):
        """This call will delete the account for the specified brand and alert request id."""

    @returns.json
    @http_get("version")
    def version(self):
        """This call will delete the account for the specified brand and alert request id."""
