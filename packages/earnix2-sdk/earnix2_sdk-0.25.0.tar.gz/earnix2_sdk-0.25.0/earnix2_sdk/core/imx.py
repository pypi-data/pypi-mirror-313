from typing import Any

from ..clients.imx import (
    ApiClient,
    Configuration,
    ConnectionServiceApi,
    DataSourceServiceApi,
)


class ImxClient(ApiClient):
    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        base_url = f"https://{server}.e2.earnix.com/api/imx"
        kwargs["configuration"] = Configuration(host=base_url)
        super().__init__(*args, **kwargs)


class ConnectionService(ConnectionServiceApi):
    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        kwargs["api_client"] = ImxClient(server=server)
        super().__init__(*args, **kwargs)


class DataSourceService(DataSourceServiceApi):
    def __init__(self, server: str, *args: Any, **kwargs: Any) -> None:
        kwargs["api_client"] = ImxClient(server=server)
        super().__init__(*args, **kwargs)
