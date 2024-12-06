from .module_imports import key
from uplink import (
    Consumer,
    headers,
)


@headers({"Ocp-Apim-Subscription-Key": key})
class _Calculators(Consumer):
    """Inteface to Calculators resource for the RockyRoad API."""
    from .tco_calculator import _TCO

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def tco(self):
        return self._TCO(self)
