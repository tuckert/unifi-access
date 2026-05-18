from typing import Any, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class DeviceManager:
    """High-level manager for UniFi Access device operations.

    Wraps endpoints related to devices. All HTTP I/O is delegated to `client`
    which must expose `_make_request(method, path, ...)`.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def list_devices(self) -> List[Dict[str, Any]]:
        """Fetch all devices.

        Returns:
            A list of device data dictionaries.

        Notes:
            - Request URL: /developer/devices
            - Permission Key: view:device
            - Method: GET
        """
        path = "/developer/devices"

        return self.client._make_request("GET", path)

