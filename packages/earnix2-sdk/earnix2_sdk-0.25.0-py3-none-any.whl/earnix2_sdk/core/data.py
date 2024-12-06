from typing import Any

from ..clients.data import ApiClient, Configuration, DataTableServiceApi


class DataClient(ApiClient):
    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        base_url = f"https://{server}.e2.earnix.com/api/data"
        kwargs["configuration"] = Configuration(host=base_url)
        super().__init__(*args, **kwargs)


class DataTableService(DataTableServiceApi):
    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        kwargs["api_client"] = DataClient(server=server)
        super().__init__(*args, **kwargs)
