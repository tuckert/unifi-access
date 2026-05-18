from typing import Any, Dict, List, Optional
# unifi_access/managers/notification.py


class NotificationManager:
    """High-level manager for notification (webhook) operations.

    Wraps endpoints for creating, updating, listing, and deleting webhook
    endpoints. All HTTP I/O is delegated to `client` which must expose
    `_make_request(method, path, ...)`.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def list_webhook_endpoints(self, page_num: Optional[int] = None, page_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch the list of webhook endpoints with optional pagination.

        Args:
            page_num: Page number (server default if omitted).
            page_size: Page size (server default if omitted).

        Returns:
            A list of webhook endpoint dictionaries.

        Notes:
            - Request URL: /developer/webhooks/endpoints
            - Permission Key: view:webhook
            - Method: GET
            - UniFi Access Requirement: Version 2.2.10 or later
        """
        path = "/developer/webhooks/endpoints"
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        return self.client._make_request("GET", path, params=params)

    def add_webhook_endpoint(
        self,
        name: str,
        endpoint: str,
        events: List[str],
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add a new webhook endpoint.

        Args:
            name: Name of the webhook subscription.
            endpoint: HTTPS URL where webhook events are sent.
            events: List of events to subscribe to (e.g., ["access.door.unlock"]).
            headers: Optional custom headers for requests (e.g., {"key": "value"}).

        Returns:
            Created webhook endpoint details as a dictionary (may include ID and secret).

        Notes:
            - Request URL: /developer/webhooks/endpoints
            - Permission Key: edit:webhook
            - Method: POST
            - UniFi Access Requirement: Version 2.2.10 or later
        """
        path = "/developer/webhooks/endpoints"
        data = {
            "name": name,
            "endpoint": endpoint,
            "events": events
        }
        if headers:
            data["headers"] = headers
        return self.client._make_request("POST", path, json=data)

    def update_webhook_endpoint(
        self,
        endpoint_id: str,
        name: Optional[str] = None,
        endpoint: Optional[str] = None,
        events: Optional[List[str]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update an existing webhook endpoint.

        Args:
            endpoint_id: The webhook endpoint's ID.
            name: New name for the webhook subscription.
            endpoint: New HTTPS URL for the webhook.
            events: New list of events to subscribe to.
            headers: New custom headers (or None to unset).

        Returns:
            Updated webhook endpoint details as a dictionary.

        Notes:
            - Request URL: /developer/webhooks/endpoints/:id
            - Permission Key: edit:webhook
            - Method: PUT
            - UniFi Access Requirement: Version 2.2.10 or later
        """
        path = f"/developer/webhooks/endpoints/{endpoint_id}"
        data: Dict[str, Any] = {}
        if name:
            data["name"] = name
        if endpoint:
            data["endpoint"] = endpoint
        if events:
            data["events"] = events
        if headers is not None:
            data["headers"] = headers
        return self.client._make_request("PUT", path, json=data)

    def delete_webhook_endpoint(self, endpoint_id: str) -> Dict[str, Any]:
        """Delete a webhook endpoint.

        Args:
            endpoint_id: The webhook endpoint's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/webhooks/endpoints/:id
            - Permission Key: edit:webhook
            - Method: DELETE
            - UniFi Access Requirement: Version 2.2.10 or later
        """
        path = f"/developer/webhooks/endpoints/{endpoint_id}"
        return self.client._make_request("DELETE", path)