from typing import Any, Dict, List, Optional
# unifi_access/managers/identity.py


class IdentityManager:
    """High-level manager for UniFi Access Identity-related operations.

    Wraps endpoints for invitations and resource assignments for users and
    user groups. All HTTP I/O is delegated to `client` which must expose a
    `_make_request(method, path, ...)` method.

    Notes for LLMs/MCP:
    - IDs are strings provided by the UniFi backend.
    - Return values mirror the API responses where possible.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def send_invitations(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send UniFi Identity invitations to users.

        Args:
            users: List of user dictionaries (e.g., with email and user_id).

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/identity/invitations
            - Permission Key: edit:identity
            - Method: POST
        """
        path = "/developer/users/identity/invitations"
        data = users

        return self.client._make_request("POST", path, json=data)

    def fetch_available_resources(self, resource_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch available resources that can be assigned.

        Args:
            resource_type: Optional resource type filter (e.g., "door").

        Returns:
            A list of available resource dictionaries.

        Notes:
            - Request URL: /developer/users/identity/assignments
            - Permission Key: view:identity
            - Method: GET
        """
        path = "/developer/users/identity/assignments"
        params: Dict[str, Any] = {}
        if resource_type:
            params["resource_type"] = resource_type
        return self.client._make_request("GET", path, params=params)

    def assign_resources_to_users(self, user_id: str, resource_type: str, resource_ids: List[str]) -> Dict[str, Any]:
        """Assign resources of a given type to a specific user.

        Args:
            user_id: Target user's ID.
            resource_type: Type of resource (e.g., 'door', 'door_group').
            resource_ids: List of resource IDs to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/identity/assignments
            - Permission Key: edit:identity
            - Method: POST
        """
        path = f"/developer/users/{user_id}/identity/assignments"
        data = {
            "resource_type": resource_type,
            "resource_ids": resource_ids
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_user_resources(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch resources assigned to a user.

        Args:
            user_id: The user's ID.

        Returns:
            A list of resource dictionaries assigned to the user.

        Notes:
            - Request URL: /developer/users/:id/identity/assignments
            - Permission Key: view:identity
            - Method: GET
        """
        path = f"/developer/users/{user_id}/identity/assignments"

        return self.client._make_request("GET", path)

    def assign_resources_to_user_groups(self, group_id: str, resource_type: str, resource_ids: List[str]) -> Dict[str, Any]:
        """Assign resources to a user group.

        Args:
            group_id: User group ID to assign resources to.
            resource_type: Type of resource (e.g., 'door', 'door_group').
            resource_ids: List of resource IDs to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id/identity/assignments
            - Permission Key: edit:identity
            - Method: POST
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/identity/assignments"
        data = {
            "resource_type": resource_type,
            "resource_ids": resource_ids
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_user_group_resources(self, group_id: str) -> List[Dict[str, Any]]:
        """Fetch resources assigned to a user group.

        Args:
            group_id: The user group's ID.

        Returns:
            A list of resource dictionaries assigned to the user group.

        Notes:
            - Request URL: /developer/user_groups/:id/identity/assignments
            - Permission Key: view:identity
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/identity/assignments"
        return self.client._make_request("GET", path)