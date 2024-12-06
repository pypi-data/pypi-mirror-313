from .module_imports import key
from uplink import (
    Consumer,
    get as http_get,
    returns,
    headers,
    Query,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class _Oracle_Installed_Base_Assets(Consumer):
    """Inteface to Oracle knowledge management resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("oracle/installed-base-assets")
    def list(
        self,
        expand: Query = None,
        fields: Query = None,
        finder: Query = None,
        limit: Query = None,
        links: Query = None,
        offset: Query = None,
        only_data: Query = None,
        order_by: Query = None,
        q: Query = None,
        total_results: Query = None,
    ):
        """This call will return installed base assets from Oracle."""

    @returns.json
    @http_get("oracle/installed-base-assets/{asset_id}")
    def http_get(
        self,
        asset_id: int,
        expand: Query = None,
        fields: Query = None,
        links: Query = None,
        only_data: Query = None,
    ):
        """This call will return the installed base asset from Oracle."""
