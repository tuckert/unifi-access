from typing import Any, List, Dict, TYPE_CHECKING, Optional

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

    def fetch_devices(self, refresh: Optional[bool]) -> List[Dict[str, Any]]:
        """Fetch all devices.

        Returns:
            A list of device data dictionaries.

        Notes:
            - Request URL: /developer/devices
            - Permission Key: view:device
            - Method: GET
        """
        path = "/developer/devices"
        params = {}
        if refresh:
            params["refresh"] = 'true'
        return self.client._make_request("GET", path, params=params)

    def fetch_access_devices_access_method_settings(self, device_id: str) -> Dict[str, Any]:
        """
        This API allows you to fetch the current access method settings of an Access device.

        Args:
            device_id (str): The unique identifier of the device for which access method
                settings are being retrieved.  Get it from the API api/v1/developer/devices

        Returns:
            Dict[str, Any]: A dictionary containing key-value pairs representing the access
                method settings of the specified device.

        Raises:
            ValueError: If the provided device_id is invalid or empty.
            KeyError: If no access settings are found for the specified device.
            ConnectionError: If there is an error retrieving the access settings due to
                connectivity issues.
        """

        path = f"/developer/devices/{device_id}/settings"
        return self.client._make_request("GET", path)

    def update_access_devices_access_method_settings(self, device_id: str, access_methods: Dict[str, Any]):
        """ See section 8.3 of the Unifi Access API Docs"""

        path = f"/developer/devices/{device_id}/settings"
        return self.client._make_request("PUT", path, json=access_methods)

    def trigger_doorbells(self, device_id: str, room_name: Optional[str], cancel: Optional[bool]):
        """ Trigger the doorbell on an Intercom or Reader Pro"""
        path = f"/developer/devices/{device_id}/doorbell"
        body = {}
        if room_name:
            body["room_name"] = room_name
        if cancel:
            body["cancel"] = cancel
        return self.client._make_request("POST", path, json=body)
