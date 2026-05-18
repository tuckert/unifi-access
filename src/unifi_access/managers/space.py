from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class SpaceManager:
    """High-level manager for space-related operations (doors, door groups).

    Wraps endpoints for door groups and doors including control operations like
    unlock, temporary lock rules, and emergency status. All HTTP I/O is
    delegated to `client` which must expose `_make_request(method, path, ...)`.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def fetch_door_group_topology(self) -> Dict[str, Any]:
        """Fetch the topology of door groups.

        Returns:
            Door group topology details as a dictionary.

        Notes:
            - Request URL: /developer/door-groups/topology
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/door_groups/topology"
        return self.client._make_request("GET", path)

    def create_door_group(
            self,
            name: str,
            door_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Create a new door group.

        Args:
            name (str): Name of the door group.
            door_ids (list[str]): List of door IDs to include in the group.

        Returns:
            Door group data as a dictionary.

        Notes:
            - Request URL: /developer/door-groups
            - Permission Key: edit:space
            - Method: POST
        """
        path = "/developer/door_groups"
        data = {
            "group_name": name,
            "resources": door_ids  # list of door ids
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_door_group(self, group_id: str) -> Dict[str, Any]:
        """
        Fetch a door group's details.

        Args:
            group_id (str): The door group's ID.

        Returns:
            Door group data as a dictionary.

        Notes:
            - Request URL: /developer/door-groups/:id
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/door_groups/{group_id}"
        return self.client._make_request("GET", path)

    def update_door_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        door_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing door group.

        Args:
            group_id (str): The door group's ID.
            name (str, optional): New name for the group.
            door_ids (list[str], optional): New list of door IDs.

        Returns:
            Updated door group data as a dictionary.

        Notes:
            - Request URL: /developer/door-groups/:id
            - Permission Key: edit:space
            - Method: PUT
        """
        path = f"/developer/door_groups/{group_id}"
        data = {}
        if name:
            data["group_name"] = name
        if door_ids is not None:
            data["resources"] = door_ids
        return self.client._make_request("PUT", path, json=data)

    def fetch_all_door_groups(self) -> List[Dict[str, Any]]:
        """
        Fetch all door groups with pagination.
        Returns:
            A list of door group data dictionaries.

        Notes:
            - Request URL: /developer/door-groups
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/door_groups"
        return self.client._make_request("GET", path)

    def delete_door_group(self, group_id: str) -> Dict[str, Any]:
        """
        Delete a door group.

        Args:
            group_id (str): The door group's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/door-groups/:id
            - Permission Key: edit:space
            - Method: DELETE
        """
        path = f"/developer/door_groups/{group_id}"
        return self.client._make_request("DELETE", path)

    def fetch_door(self, door_id: str) -> Dict[str, Any]:
        """
        Fetch a door's details.

        Args:
            door_id (str): The door's ID.

        Returns:
            Door data as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/{door_id}"
        return self.client._make_request("GET", path)

    def fetch_all_doors(self) -> List[Dict[str, Any]]:
        """
        Fetch all doors with pagination.

        Returns:
            A list of door data dictionaries.

        Notes:
            - Request URL: /developer/doors
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/doors"
        return self.client._make_request("GET", path)

    def unlock_door(
        self,
        door_id: str,
        actor_id: Optional[str] = None,
        actor_name: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Remotely unlock a door.

        Args:
            door_id (str): The door's ID.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/unlock
            - Permission Key: edit:space
            - Method: POST
            - UniFi Access Requirement: Version 2.2.6 or later for UA-Ultra
        """

        payload = {
            "actor_id": actor_id,
            "actor_name": actor_name,
            "extra": extra
        }
        path = f"/developer/doors/{door_id}/unlock"
        return self.client._make_request("PUT", path, json=payload)

    def set_temporary_door_lock_rule(self, door_id: str, unlock_type: str, duration: int = None) -> Dict[str, Any]:
        """
        Set a temporary door locking rule.

        Args:
            door_id (str): The door's ID.
            type (str): enum type {keep_lock,keep_unlock,custom,reset,lock_early} keep_lock is used to
set the door to the "keep locked" state, while keep_unlock is used to set it to the "keep unlocked"
state. custom allows customization of the unlock time duration, and reset is used to restore the
door to its initial state (not applicable to the "lock_early" state). NOTE: If the door is currently on an
unlock schedule ( schedule ), you can use lock_early to lock the door early.
            lock_state (str): State to set ("locked" or "unlocked", default: "locked").

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/locking-rule
            - Permission Key: edit:space
            - Method: POST
            - UniFi Access Requirement: Version 3.1.30 or later for EAH8, UA-Hub-Door-Mini, UA-Ultra
        """
        path = f"/developer/doors/{door_id}/lock_rule"
        data = {
            "type": unlock_type,
        }
        if duration is not None:
            data["interval"] = duration,
        return self.client._make_request("PUT", path, json=data)

    def get_door_lock_rule(self, door_id: str) -> Dict[str, Any]:
        """
        Fetch the current door locking rule.

        Args:
            door_id (str): The door's ID.

        Returns:
            Door locking rule details as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/locking-rule
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/{door_id}/lock_rule"
        return self.client._make_request("GET", path)

    def set_door_emergency_status(self, lockdown: bool, evacuation: bool) -> Dict[str, Any]:
        """
        Set the emergency status for a door.

        Args:
            lockdown (bool): True will keep the door locked
            evacuation (bool): True will keep the door unlocked

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/emergency-status
            - Permission Key: edit:space
            - Method: POST
        """
        path = f"/developer/doors/settings/emergency"
        data = {
            "lockdown": lockdown,
            "evacuation": evacuation
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_door_emergency_status(self) -> Dict[str, Any]:
        """
        Fetch the emergency status of a door.

        Args:
            door_id (str): The door's ID.

        Returns:
            Door emergency status details as a dictionary.

        Notes:
            - Request URL: /developer/doors/settings/emergency
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/settings/emergency"
        return self.client._make_request("GET", path)
